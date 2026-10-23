#!/usr/bin/env python3
"""Render exact, pedagogical music animation from the clAIvier event scores.

No pitches, subject labels or timings are inferred from generated imagery.
The written score is the animation's clock and sole note source.

Examples:
  python tools/animate_cycle.py --score work/fugue_iv.json \
    --audio output/04-fugue-csharp-minor.mp3 --mode performance
  python tools/animate_cycle.py --score work/fugue_iv.json --mode lesson \
    --lesson-config work/animation/iv-lesson.json
  python tools/animate_cycle.py --batch work/animation/render-manifest.json

Lesson JSON is {"segments": [...]}. A segment is either:
  {"kind":"card", "duration":4, "title":"...", "text":"...",
   "narration_audio":"optional/path.wav"}
or:
  {"kind":"score", "start":0, "end":16, "solo":[2],
   "title":"Hear the subject", "text":"...", "music_gain":0.85,
   "narration_audio":"optional/path.wav", "narration_delay":0}
Times start/end are quarter-note beats. Card durations and narration delays
are seconds. Omitting solo plays all parts. Music excerpt timings remain
exact; narration can extend a segment with a held end frame if necessary.

Batch manifest is a JSON list of ordinary argument dictionaries, with keys
score, audio, output, mode, lesson_config, fps, short_seconds and preview_only.
System requirements: Pillow, NumPy, FFmpeg; FluidSynth and render_music.py
dependencies only when synthesizing an isolated excerpt or missing audio.
"""
from __future__ import annotations

import argparse
import bisect
import colorsys
import copy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'work'/'animation'
if (ROOT/'vendor').is_dir():sys.path.insert(0,str(ROOT/'vendor'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H=1280,720
BG='#f4f0e6';INK='#25333a';MUTED='#697478';GRID='#dddcd3'
PANEL='#fffcf5';LIGHT='#e8e8dd';ACCENT='#ae583d'
FAMILIES=['#2e6584','#b85c42','#9e7c2e','#397e70','#7b6293']
FONTDIR=Path('/usr/share/fonts/truetype/dejavu')
FONT_CACHE={}
TEXT_CACHE={}
LENGTH_CACHE={}

class FastDraw:
    """Cache rasterized labels shared by thousands of video frames."""
    def __init__(self,im):
        self.im=im;self.draw=ImageDraw.Draw(im)
    def __getattr__(self,name):return getattr(self.draw,name)
    def textlength(self,text,font=None,**kwargs):
        if kwargs:return self.draw.textlength(text,font=font,**kwargs)
        key=(str(text),id(font))
        if key not in LENGTH_CACHE:LENGTH_CACHE[key]=self.draw.textlength(text,font=font)
        return LENGTH_CACHE[key]
    def text(self,xy,text,font=None,fill=None,**kwargs):
        if kwargs:return self.draw.text(xy,text,font=font,fill=fill,**kwargs)
        if not text:return
        key=(str(text),id(font),str(fill))
        if key not in TEXT_CACHE:
            a,b,c,d=font.getbbox(str(text))
            stamp=Image.new('RGBA',(max(1,c-a),max(1,d-b)))
            ImageDraw.Draw(stamp).text((-a,-b),str(text),font=font,fill=fill)
            TEXT_CACHE[key]=(stamp,a,b)
        stamp,a,b=TEXT_CACHE[key]
        self.im.paste(stamp,(round(xy[0]+a),round(xy[1]+b)),stamp)

def font(size,bold=False,serif=False):
    key=(size,bold,serif)
    if key not in FONT_CACHE:
        name='DejaVuSerif' if serif else 'DejaVuSans'
        if bold:name+='-Bold'
        FONT_CACHE[key]=ImageFont.truetype(str(FONTDIR/(name+'.ttf')),size)
    return FONT_CACHE[key]

def rgb(h):return tuple(int(h.lstrip('#')[k:k+2],16) for k in (0,2,4))
def mix(a,b,t):return tuple(round(x*(1-t)+y*t) for x,y in zip(rgb(a) if isinstance(a,str) else a,rgb(b) if isinstance(b,str) else b))
def clamp(x,a,b):return max(a,min(b,x))

def wrap(draw,text,ft,width,max_lines=8):
    lines=[]
    for para in str(text).split('\n'):
        line=''
        for word in para.split():
            test=(line+' '+word).strip()
            if line and draw.textlength(test,font=ft)>width:
                lines.append(line);line=word
            else:line=test
        lines.append(line)
    if len(lines)>max_lines:
        lines=lines[:max_lines]
        while draw.textlength(lines[-1]+'…',font=ft)>width:lines[-1]=lines[-1][:-1]
        lines[-1]+='…'
    return lines

def textblock(draw,xy,text,size=22,fill=INK,width=600,bold=False,serif=False,max_lines=8,leading=None):
    x,y=xy;ft=font(size,bold,serif);leading=leading or round(size*1.35)
    for line in wrap(draw,text,ft,width,max_lines):
        draw.text((x,y),line,font=ft,fill=fill);y+=leading
    return y

def duration(path):
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(path)],capture_output=True,text=True,check=True)
    return float(r.stdout.strip())

def note_name(p):
    return ['C','C♯','D','D♯','E','F','F♯','G','G♯','A','A♯','B'][int(p)%12]+str(int(p)//12-1)

def validate_score(d):
    v=d.get('voices',[])
    if not v:raise ValueError('Score contains no voices.')
    for voice in v:
        previous=-1
        for e in sorted(voice['events'],key=lambda e:e['t']):
            if e['d']<=0 or e['t']<previous-1e-7:raise ValueError('Invalid or overlapping monophonic events.')
            previous=e['t']+e['d']
        voice['events'].sort(key=lambda e:e['t'])
    return d

def load_score(path):return validate_score(json.loads(Path(path).read_text()))

def publish_file(temporary,target):
    """Commit completed bytes before publishing the filename to other workers."""
    temporary=Path(temporary);target=Path(target)
    with temporary.open('rb') as handle:os.fsync(handle.fileno())
    temporary.replace(target)
    fd=os.open(str(target.parent),os.O_RDONLY|os.O_DIRECTORY)
    try:os.fsync(fd)
    finally:os.close(fd)

def atomic_json(target,value):
    target=Path(target);temporary=target.with_name(target.name+'.tmp')
    with temporary.open('w') as handle:
        json.dump(value,handle,indent=2);handle.flush();os.fsync(handle.fileno())
    publish_file(temporary,target)

def export_cues(score,path,target,audio=None):
    """Export score-clock control data for stage lights and video overlays.

    Voice IDs and colors agree with the teaching renderer. Subject states come
    from the score's authored annotations; they are not audio detections. A
    separate note_on/note_off stream controls whether a player is sounding.
    """
    def seconds(beat):return round(float(beat)*score.spb,6)
    stream=[];voices=[];entries=[]
    for i,e in enumerate(score.entries):
        q={'id':f'entry-{i+1:03d}','voice_id':f"voice-{e['voice']+1:02d}",
           'voice_index':e['voice'],'start_beat':e['t'],'end_beat':e['end'],
           'start_seconds':seconds(e['t']),'end_seconds':seconds(e['end']),
           'label':e.get('label','Subject entry'),'subject_id':e.get('subject_id','minor'),
           'thematic_role':e.get('role','subject'),
           'duration_scale':e.get('scale',1),'transpose_semitones':e.get('transpose',0)}
        entries.append(q)
        for kind,b in [('subject_on',e['t']),('subject_off',e['end'])]:
            stream.append({'kind':kind,'beat':b,'seconds':seconds(b),'voice_id':q['voice_id'],'entry_id':q['id'],'thematic_role':q['thematic_role']})
    for vi,v in enumerate(score.voices):
        ident=f'voice-{vi+1:02d}';ve=[e for e in entries if e['voice_index']==vi];notes=[]
        for ni,n in enumerate(v['events']):
            if n.get('p') is None:continue
            note_id=f'{ident}-note-{ni+1:05d}'
            entry_ids=[e['id'] for e in ve if e['start_beat']-1e-8<=n['t']<e['end_beat']-1e-8]
            notes.append({'id':note_id,'start_beat':n['t'],'duration_beats':n['d'],
                          'start_seconds':seconds(n['t']),'duration_seconds':seconds(n['d']),
                          'end_seconds':seconds(n['t']+n['d']),'midi_pitch':n['p'],
                          'velocity':n.get('v',80),'subject_entry_ids':entry_ids})
            for kind,b in [('note_on',n['t']),('note_off',n['t']+n['d'])]:
                stream.append({'kind':kind,'beat':b,'seconds':seconds(b),'voice_id':ident,'note_id':note_id,'midi_pitch':n['p']})
        first=min((n['start_beat'] for n in notes),default=None)
        if first is not None:stream.append({'kind':'voice_first_entrance','beat':first,'seconds':seconds(first),'voice_id':ident})
        boundaries=sorted(set([0,score.end]+[e[k] for e in ve for k in ['start_beat','end_beat']]))
        states=[]
        for a,b in zip(boundaries,boundaries[1:]):
            if b<=a:continue
            active=[e for e in ve if e['start_beat']<=a<e['end_beat']]
            on=[e['id'] for e in active];roles=sorted(set(e['thematic_role'] for e in active))
            states.append({'start_beat':a,'end_beat':b,'start_seconds':seconds(a),'end_seconds':seconds(b),
                           'state':roles[0] if len(roles)==1 else ('mixed_themes' if roles else 'free'),'entry_ids':on})
        color='#'+''.join(f'{c:02x}' for c in score.colors[vi])
        voices.append({'id':ident,'index':vi,'position_slot':vi+1,'name':v.get('name',ident),
                       'abbreviation':v.get('abbr',str(vi+1)),'color':color,
                       'first_entrance_beat':first,'first_entrance_seconds':seconds(first) if first is not None else None,
                       'pitch_range':[min(n['midi_pitch'] for n in notes),max(n['midi_pitch'] for n in notes)] if notes else None,
                       'notes':notes,'subject_states':states})
    markers=[]
    for i,m in enumerate(score.markers):
        q={'id':f'marker-{i+1:03d}','beat':m['t'],'seconds':seconds(m['t']),'label':m['label']}
        markers.append(q);stream.append({'kind':'form_marker',**q})
    order={'note_off':0,'subject_off':1,'form_marker':2,'voice_first_entrance':3,'subject_on':4,'note_on':5}
    stream.sort(key=lambda e:(e['beat'],order[e['kind']],e.get('voice_id','')))
    report={'schema':'clAIvier-score-cues/v1','title':score.meta.get('title',''),
            'subtitle':score.meta.get('subtitle',''),'score_file':str(path),
            'score_sha256':getattr(score,'source_sha256',None) or hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'audio_file':str(audio) if audio else None,
            'clock':{'origin_seconds':0,'bpm':score.bpm,'seconds_per_quarter_beat':score.spb,
                     'score_duration_beats':score.end,'score_duration_seconds':seconds(score.end),
                     'meter':score.meta.get('meter',[4,4]),
                     'simultaneous_event_order':'note_off, subject_off, form_marker, voice_first_entrance, subject_on, note_on'},
            'semantics':{'subject_states':'Authored thematic annotations; thematic_role distinguishes complete subject, countersubject and short fragment. States remain active through any written rests within a statement.',
                         'note_stream':'Use note_on/note_off to control sounding intensity; subject_on/subject_off identify thematic roles.',
                         'positions':'position_slot is a stable one-based slot only; instrument assignment and architectural location belong to the film manifest.'},
            'voice_count':score.n,'voices':voices,'subject_entries':entries,'form_markers':markers,'event_stream':stream}
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    atomic_json(target,report)
    return target

class Score:
    def __init__(self,data):
        self.data=data;self.meta=data.get('metadata',{});self.voices=data['voices'];self.n=len(self.voices)
        self.bpm=float(self.meta.get('bpm',80));self.spb=60/self.bpm
        self.end=max(e['t']+e['d'] for v in self.voices for e in v['events'])
        meter=self.meta.get('meter',[4,4]);self.bar=float(meter[0])*4/float(meter[1])
        self.starts=[[e['t'] for e in v['events']] for v in self.voices]
        self.markers=sorted(self.meta.get('markers',[]),key=lambda m:m['t'])
        self.entries=[]
        for source in data.get('subject_entries',[]):
            e=dict(source);pattern=data.get('subjects',{}).get(e.get('subject_id','minor'),{}).get('events',[])
            if not pattern:continue
            e['end']=e['t']+max(n['t']+n['d'] for n in pattern)*e.get('scale',1)
            thematic_name=(e.get('subject_id','')+' '+e.get('label','')).lower().replace('_','').replace('-','').replace(' ','')
            e['role']=('fragment' if 'fragment' in thematic_name else 'countersubject' if 'countersubject' in thematic_name or e.get('subject_id','').lower()=='cs' else 'subject')
            if not 0<=e['voice']<self.n:raise ValueError('Subject entry refers to missing voice.')
            self.entries.append(e)
        # Short tonal sequences are explicit fragments, never complete entries.
        for f in data.get('motivic_fragments',[]):
            self.entries.append({**f,'end':f['t']+f['d'],'role':'fragment',
                'subject_id':'fragment:'+f.get('source_subject','subject'),
                'label':f.get('label',f.get('technique','Subject-head fragment'))})
        self.entries.sort(key=lambda e:e['t'])
        self.primary_entries=[e for e in self.entries if e['role']=='subject']
        pitches=[e['p'] for v in self.voices for e in v['events'] if e.get('p') is not None]
        self.low=min(pitches)-2;self.high=max(pitches)+2
        self.colors=[]
        for i in range(self.n):
            base=FAMILIES[i%5] if self.n<=5 else FAMILIES[min(4,i//5)]
            explicit=self.voices[i].get('color')
            self.colors.append(rgb(explicit) if explicit else (rgb(base) if self.n<=5 else mix(base,'#ffffff',.055*(i%5))))

    def note(self,vi,beat):
        ix=bisect.bisect_right(self.starts[vi],beat+1e-8)-1
        if ix<0:return None
        e=self.voices[vi]['events'][ix]
        return e if beat<e['t']+e['d']-1e-8 else None

    def active_entries(self,beat):return [e for e in self.entries if e['t']<=beat<e['end']]
    def note_role(self,vi,n):
        found=[e['role'] for e in self.entries if e['voice']==vi and e['t']-1e-8<=n['t']<e['end']-1e-8]
        return next((r for r in ['subject','countersubject','fragment'] if r in found),None)
    def subject_note(self,vi,n):return self.note_role(vi,n) is not None
    def densest(self):
        changes={}
        for v in self.voices:
            for n in v['events']:
                if n.get('p') is None:continue
                changes[n['t']]=changes.get(n['t'],0)+1
                end=n['t']+n['d'];changes[end]=changes.get(end,0)-1
        active=peak=0;start=0
        for t,delta in sorted(changes.items()):
            active+=delta
            if active>peak:peak=active;start=t
        return start,peak
    def marker(self,beat):
        a=[m for m in self.markers if m['t']<=beat+1e-8]
        return a[-1]['label'] if a else ('Prelude' if not self.entries else 'Exposition')

    def section(self,beat):
        sections=self.data.get('sections',self.meta.get('sections',[]))
        return next((s for s in sections if s.get('t',0)<=beat<s.get('end',s.get('t',0)+s.get('d',self.end))),None)

    def explanation(self,beat):
        if beat>=self.end:return 'Final resonance','The written notes have ended. Let the remaining sound settle.'
        for a in self.data.get('pedagogy',{}).get('annotations',[]):
            if a.get('t',0)<=beat<a.get('end',a.get('t',0)+4):return a.get('title','Listen'),a.get('text','')
        entries=self.active_entries(beat)
        primary=[e for e in entries if e['role']=='subject'];counter=[e for e in entries if e['role']=='countersubject']
        if any(e.get('scale',1)>1 for e in primary):
            e=next(e for e in primary if e.get('scale',1)>1)
            return 'Augmentation',f"{self.voices[e['voice']]['name']} carries the subject with note lengths multiplied by {e.get('scale',1):g}."
        if len(primary)>1:
            latest=max(primary,key=lambda e:e['t'])
            earlier=[e for e in primary if e['t']<latest['t']]
            tails=[{n['p'] for n in self.voices[e['voice']]['events'] if n.get('p') is not None and n['t']<e['end'] and n['t']+n['d']>latest['t']} for e in earlier]
            if tails and all(len(p)==1 for p in tails):
                return 'Brief overlap of the held tail','The new subject begins under the earlier subject’s sustained final note. This is a mild form of stretto.'
            return f'{len(primary)} overlapping subject entries','Follow the outlined notes: a new statement begins before an earlier subject has ended.'
        if primary and counter:
            main=self.voices[primary[0]['voice']]['name'];companion=self.voices[counter[0]['voice']]['name']
            return 'Subject and countersubject',f'{main} carries the subject; {companion} carries the recurring companion theme.'
        if primary:
            e=primary[0];name=self.voices[e['voice']]['name']
            return e.get('label','Subject entry'),f'{name} carries the theme. The other sounding parts continue their own lines.'
        fragments=[e for e in entries if e['role']=='fragment']
        if fragments:
            e=fragments[0]
            return 'Developing the subject head',f"{self.voices[e['voice']]['name']} develops a short fragment of the subject. The fragment is not counted as a complete subject entry."
        if counter:
            return 'Countersubject',f"{self.voices[counter[0]['voice']]['name']} carries the recurring companion theme."
        if not self.entries:
            section=self.section(beat)
            if section:return section.get('label',self.marker(beat)),section.get('explanation',section.get('detail','Trace the shapes of the moving lines.'))
            return self.marker(beat),'Trace the shapes of the lines and notice which register carries the motion.'
        section=self.section(beat)
        if section:return section.get('label',self.marker(beat)),section.get('detail',section.get('explanation','Listen for the motion of the individual lines.'))
        return self.marker(beat),'The full subject is between entries. Listen to how the free lines carry the music onward.'

class Painter:
    def __init__(self,score):
        self.s=score
        self.base=Image.new('RGB',(W,H),BG)
        d=FastDraw(self.base)
        d.line((34,135,1246,135),fill=GRID,width=2)
        d.text((36,23),'THE WELL-TEMPERED clAIvier',font=font(14,True),fill=ACCENT)
        subtitle=self.s.meta.get('subtitle','Prelude and Fugue')
        textblock(d,(34,49),subtitle,size=31,serif=True,width=1180,max_lines=1)
        label=self.s.meta.get('animation_part_label',f'{self.s.n} SCORED PARTS   ·   QUARTER = {self.s.bpm:g}')
        d.text((36,101),label,font=font(14),fill=MUTED)
        if self.s.entries:
            role_legend=('S: outline  ·  CS: underline  ·  fragment: dots'
                         if any(e['role']=='countersubject' for e in self.s.entries)
                         else 'Complete theme: outline  ·  fragment: dots')
            d.text((413,102),role_legend,font=font(12),fill=MUTED)

    def legend(self,d,beat,solo=None,ended=False):
        n=self.s.n;selected=set(range(n)) if solo is None else set(solo)
        notes=[None if ended else self.s.note(i,beat) for i in range(n)];active=sum(x is not None for x in notes)
        heard=sum(notes[i] is not None for i in selected)
        textblock(d,(36,157),'THE VOICES',size=14,bold=True,fill=MUTED,width=220)
        if n<=9:
            height=min(53,315/max(1,n))
            for i,v in enumerate(self.s.voices):
                y=190+i*height;is_on=notes[i] is not None;color=self.s.colors[i]
                if i not in selected:color=mix(color,BG,.78)
                d.rounded_rectangle((34,y,244,y+height-8),radius=7,fill=mix(color,BG,.84 if is_on else .96))
                d.ellipse((45,y+11,57,y+23),fill=color if is_on else mix(color,BG,.6))
                name=v.get('name',f'Voice {i+1}')
                textblock(d,(68,y+7),name,size=17 if n<=5 else 14,bold=is_on,width=160,max_lines=1)
                if is_on and n<=5:d.text((69,y+28),note_name(notes[i]['p']),font=font(11),fill=MUTED)
        else:
            for i in range(n):
                group=i//5;col=i%5;x=35+col*42;y=197+group*56
                color=self.s.colors[i];is_on=notes[i] is not None
                if i not in selected:color=mix(color,BG,.75)
                d.rounded_rectangle((x,y,x+35,y+35),radius=6,fill=color if is_on else mix(color,BG,.84))
                label=str(i+1);w=d.textlength(label,font=font(14,True))
                d.text((x+17.5-w/2,y+8),label,font=font(14,True),fill='#ffffff' if is_on else MUTED)
            d.text((36,492),'Each row is a family of five.',font=font(12),fill=MUTED)
        d.text((36,526),f'{heard} / {n}',font=font(29,True),fill=INK)
        d.text((36,564),'written parts active',font=font(13),fill=MUTED)
        if solo is not None:d.text((36,587),'ISOLATED LISTENING',font=font(12,True),fill=ACCENT)
        else:d.text((36,587),'FULL ENSEMBLE',font=font(12,True),fill=MUTED)
        if n>=10:
            distinct=len(set(notes[i]['p'] for i in selected if notes[i] is not None))
            d.text((36,611),f'{distinct} distinct pitches now',font=font(12),fill=MUTED)

    def performance(self,beat,segment=None,index=None,count=None):
        im=self.base.copy();d=FastDraw(im);segment=segment or {};solo=segment.get('solo')
        selected=set(range(self.s.n)) if solo is None else set(solo)
        ended=segment.get('_excerpt_ended',False)
        self.legend(d,beat,solo,ended)
        mode=f'GUIDED LISTENING {index+1}/{count}' if index is not None else 'ANIMATED PERFORMANCE'
        w=d.textlength(mode,font=font(13,True));d.text((1244-w,104),mode,font=font(13,True),fill=ACCENT)
        x0,y0,x1,y1=284,161,1246,509
        d.rounded_rectangle((x0,y0,x1,y1),radius=10,fill=PANEL,outline=GRID,width=1)
        window=segment.get('window_beats',16 if self.s.n<10 else 12)
        begin=max(0,beat-window*.34)
        begin=min(begin,max(0,self.s.end-window))
        end=begin+window;scale=(x1-x0-30)/window;left=x0+18
        top=y0+25;bottom=y1-28;yscale=(bottom-top)/(self.s.high-self.s.low)
        for p in range(self.s.low,self.s.high+1):
            if p%12==0:
                y=bottom-(p-self.s.low)*yscale
                d.line((x0+1,y,x1-1,y),fill='#ebe9df',width=1)
                d.text((x0+5,y-12),note_name(p),font=font(10),fill='#a4aaa5')
        for bar in range(math.floor(begin/self.s.bar),math.ceil(end/self.s.bar)+1):
            q=bar*self.s.bar;x=left+(q-begin)*scale
            if x0+1<=x<=x1-1:
                d.line((x,y0+21,x,y1-20),fill=GRID,width=1)
                d.text((x+5,y0+5),str(bar+1),font=font(11),fill=MUTED)
        active_entries=self.s.active_entries(beat);focused={e['voice'] for e in active_entries}
        for i,v in enumerate(self.s.voices):
            es=v['events'];starts=self.s.starts[i]
            lo=max(0,bisect.bisect_left(starts,begin)-2);hi=bisect.bisect_right(starts,end)
            for e in es[lo:hi]:
                if e.get('p') is None or e['t']+e['d']<=begin:continue
                xa=max(left,left+(e['t']-begin)*scale);xb=min(x1-8,left+(e['t']+e['d']-begin)*scale)
                if xb<=xa:continue
                y=bottom-(e['p']-self.s.low)*yscale;h=clamp(yscale*.74,3,8)
                role=self.s.note_role(i,e);is_subject=role is not None;is_on=not ended and e['t']<=beat<e['t']+e['d'];color=self.s.colors[i]
                if i not in selected:color=mix(color,PANEL,.86)
                elif not is_on:color=mix(color,PANEL,.17 if is_subject else .43)
                # A note clipped at the window edge can be much narrower than
                # its height. Pillow's rounded-corner construction is unstable
                # for those fractional slivers, so use a plain rectangle there.
                box=(round(xa),round(y-h/2),round(xb),round(y+h/2))
                outline=INK if role=='subject' and i in selected else None
                if box[2]-box[0]<4:
                    d.rectangle(box,fill=color,outline=outline,width=1)
                else:
                    d.rounded_rectangle(box,radius=min(3,(box[3]-box[1])/2,(box[2]-box[0])/2),
                                        fill=color,outline=outline,width=1)
                if i in selected and role=='countersubject':
                    d.line((box[0],box[3]+2,box[2],box[3]+2),fill=INK,width=1)
                elif i in selected and role=='fragment':
                    for dot in range(box[0],box[2]+1,5):d.point((dot,box[1]-2),fill=INK)
        # Thematic entry spans provide an exact temporal comparison without
        # replacing notes or suggesting that an unannotated fragment is a subject.
        for rank,e in enumerate(active_entries[:5]):
            if e['voice'] not in selected:continue
            a=max(left,left+(e['t']-begin)*scale);b=min(x1-8,left+(e['end']-begin)*scale)
            if b>a:
                y=y1-10-rank*4
                d.line((a,y,b,y),fill=self.s.colors[e['voice']],width=2)
        play=left+(beat-begin)*scale
        if left<=play<x1:
            d.line((play,y0+21,play,y1-20),fill=INK,width=2)
            d.polygon([(play-5,y0+17),(play+5,y0+17),(play,y0+24)],fill=INK)
        title,body=self.s.explanation(beat)
        title=segment.get('title') or title;body=segment.get('text') or body
        if ended:title='The excerpt has ended'
        textblock(d,(284,530),title,size=24,bold=True,width=948,max_lines=1)
        textblock(d,(284,568),body,size=19,width=942,max_lines=2,leading=26)
        self.footer(d,beat,segment)
        return im

    def footer(self,d,beat,segment=None):
        d.line((35,643,1245,643),fill=GRID,width=1)
        d.text((36,658),f'BAR {min(math.floor(beat/self.s.bar)+1,math.ceil(self.s.end/self.s.bar))} / {math.ceil(self.s.end/self.s.bar)}',font=font(12,True),fill=MUTED)
        label=self.s.marker(beat)
        entries=self.s.active_entries(beat)
        solo=(segment or {}).get('solo')
        if solo is not None:
            entries=[e for e in entries if e['voice'] in solo]
        if entries and not (segment or {}).get('_excerpt_ended'):
            e=entries[0]
            label+=f" · {e.get('label','Subject')} — {self.s.voices[e['voice']]['name']}"
        if not self.s.entries:
            harmony=next((h for h in self.s.data.get('pedagogy',{}).get('harmony',[]) if h['t']<=beat<h['t']+h['d']),None)
            if harmony:label+=f" · Harmony: {harmony.get('roman',harmony.get('label',''))}"
        textblock(d,(185,656),label,size=14,width=920,max_lines=1)
        sec=beat*self.s.spb;clock=f'{int(sec)//60}:{int(sec)%60:02d}'
        d.text((1170,656),clock,font=font(15,True),fill=INK)
        d.rounded_rectangle((36,692,1244,696),radius=2,fill=GRID)
        d.rounded_rectangle((36,692,36+max(1,1208*clamp(beat/self.s.end,0,1)),696),radius=2,fill=ACCENT)

    def card(self,segment,elapsed,index,count):
        im=Image.new('RGB',(W,H),BG);d=FastDraw(im)
        d.text((54,38),'THE WELL-TEMPERED clAIvier',font=font(14,True),fill=ACCENT)
        d.text((54,83),f'GUIDED LISTENING  ·  {index+1} / {count}',font=font(13),fill=MUTED)
        y=textblock(d,(50,156),segment.get('title','Listen closely'),size=46,serif=True,width=720,max_lines=3,leading=58)
        textblock(d,(54,y+35),segment.get('text',''),size=24,width=710,max_lines=5,leading=35)
        # The subject's actual contour is drawn at right; the cursor follows its
        # written durations. It is a visual quotation, not an invented waveform.
        themes=self.s.data.get('subjects',{})
        first=self.s.primary_entries[0] if self.s.primary_entries else None
        subject_id=segment.get('subject_id',first.get('subject_id','minor') if first else None)
        focus=segment.get('focus_voice',first['voice'] if first else 0)
        theme_color=self.s.colors[focus]
        pattern=themes.get(subject_id,{}).get('events',[])
        if not pattern:pattern=next(iter(themes.values()),{}).get('events',[])
        if not pattern:pattern=self.s.voices[0]['events'][:16]
        if pattern:
            p0=min(e['p'] for e in pattern);p1=max(e['p'] for e in pattern);t0=pattern[0]['t'];t1=max(e['t']+e['d'] for e in pattern)
            x0,x1=850,1215;y0,y1=225,456
            d.rounded_rectangle((815,171,1240,520),radius=18,fill=PANEL,outline=GRID,width=1)
            d.text((842,190),'THE SHAPE OF THE THEME',font=font(12,True),fill=MUTED)
            points=[]
            cursor=(elapsed/(self.s.spb*segment.get('subject_scale',1)))%(t1-t0)
            for e in pattern:
                x=x0+(e['t']-t0)/(t1-t0)*(x1-x0);xx=x0+(e['t']+e['d']-t0)/(t1-t0)*(x1-x0)
                y=y1-(e['p']-p0)/max(1,p1-p0)*(y1-y0)
                color=theme_color if e['t']-t0<=cursor<e['t']+e['d']-t0 else mix(theme_color,PANEL,.35)
                d.line((x,y,xx-2,y),fill=color,width=7);points.append((x,y))
            if len(points)>1:d.line(points,fill=mix(theme_color,PANEL,.7),width=1)
        d.line((54,625,1225,625),fill=GRID,width=1)
        d.text((54,648),'Listen • isolate • compare • recombine',font=font(17),fill=MUTED)
        return im

def default_lesson(score):
    entries=score.primary_entries
    if not entries:
        length=min(score.end,16)
        characteristic=score.data.get('pedagogy',{}).get('characteristic_figure','Listen for a melody, its support, and the way the texture changes.')
        return {'segments':[
            {'kind':'card','duration':4,'title':score.meta.get('character','Follow the moving line'),'text':characteristic},
            {'kind':'score','start':0,'end':length,'solo':[0],'title':'One line at a time','text':'Hear the upper part on its own. Its written notes and timing are unchanged.'},
            {'kind':'score','start':0,'end':length,'title':'Restore the complete texture','text':'The same passage returns with every written part.'}]}
    first=entries[0];second=entries[1] if len(entries)>1 else None
    segments=[{'kind':'card','duration':4,'focus_voice':first['voice'],'title':'One subject. Independent voices.','text':'First learn the shape of the theme. Then hear how another part enters while the first continues.'},
              {'kind':'score','start':first['t'],'end':first['end'],'solo':[first['voice']],'title':'Hear the subject alone','text':f"Follow {score.voices[first['voice']]['name']}. Horizontal length shows duration; height shows pitch."}]
    if second:
        answer='answer' in second.get('label','').lower()
        segments += [
            {'kind':'card','duration':3.5,'focus_voice':second['voice'],'title':'Hear the answer' if answer else 'A second voice enters','text':'The theme returns in a new voice. Hear the new statement alone, then restore the part that continues around it.'},
            {'kind':'score','start':second['t'],'end':second['end'],'solo':[second['voice']],'title':second.get('label','The second entry'),'text':f"Follow {score.voices[second['voice']]['name']}. The new color identifies a new voice, while the outline identifies the theme."},
            {'kind':'score','start':second['t'],'end':second['end'],'title':'Hear the lines together','text':'Follow the entering theme, then shift your attention to the part that continues around it.'}]
    first_by_voice={}
    for e in entries:first_by_voice.setdefault(e['voice'],e)
    if len(first_by_voice)>2:
        last=max(first_by_voice.values(),key=lambda e:e['t'])
        dense_start,peak=score.densest()
        if sum(score.note(i,last['t']) is not None for i in range(score.n))==peak:dense_start=last['t']
        dense_end=min(score.end,dense_start+last['end']-last['t'])
        segments += [{'kind':'card','duration':3.5,'focus_voice':last['voice'],'title':f'Now hear {peak} parts together','text':'Each part keeps its own identity. The color stays with the voice when its musical role changes.'},
                     {'kind':'score','start':dense_start,'end':dense_end,'title':'The dense texture','text':'The sounding count is measured from the written notes. Follow one part, then listen again for the whole.'}]
    stretto=next((e for e in entries if sum(x['t']<=e['t']<x['end'] for x in entries)>=2),None)
    if stretto:
        start=max(0,stretto['t']-min(8,stretto['end']-stretto['t']))
        segments += [{'kind':'card','duration':3.5,'focus_voice':stretto['voice'],'title':'The entries overlap','text':'A new statement begins before an earlier statement has finished. Watch their outlined notes share the same time axis.'},
                     {'kind':'score','start':start,'end':min(score.end,stretto['end']+4),'title':'Overlapping thematic statements','text':'The colored spans beneath the notes show how long each complete entry lasts.'}]
    augmented=next((e for e in entries if e.get('scale',1)>1),None)
    if augmented:
        segments += [{'kind':'card','duration':3.5,'focus_voice':augmented['voice'],'subject_scale':augmented.get('scale',1),'title':'Change the scale of time','text':f"This statement multiplies the subject’s note lengths by {augmented.get('scale',1):g}. Other voices can continue at their own pace."},
                     {'kind':'score','start':augmented['t'],'end':augmented['end'],'title':'Subject in augmentation','text':f"Trace {score.voices[augmented['voice']]['name']} while hearing the surrounding motion."}]
    return {'segments':segments}

def decode_audio(path,start=0,seconds=None,rate=44100):
    args=['ffmpeg','-hide_banner','-loglevel','error','-ss',str(start),'-i',str(path)]
    if seconds is not None:args+=['-t',str(seconds)]
    args+=['-f','f32le','-ac','2','-ar',str(rate),'-']
    r=subprocess.run(args,capture_output=True,check=True)
    return np.frombuffer(r.stdout,dtype='<f4').reshape(-1,2).copy()

def synth_excerpt(score,start,end,solo,cache_dir):
    cache_dir.mkdir(parents=True,exist_ok=True)
    chamber=score.meta.get('lesson_rendering')=='chamber'
    payload={'score':score.data,'start':start,'end':end,'solo':solo,
             'chamber':chamber,'excerpt_renderer_version':2}
    key=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()[:18]
    target=cache_dir/(key+'.wav')
    if target.exists():return target
    data=copy.deepcopy(score.data);selected=set(range(score.n)) if solo is None else set(solo)
    for vi,v in enumerate(data['voices']):
        out=[]
        if vi in selected:
            for e in v['events']:
                a=max(start,e['t']);b=min(end,e['t']+e['d'])
                if b>a:out.append({**e,'t':a-start,'d':b-a})
        v['events']=out
    spec=importlib.util.spec_from_file_location('clavier_music_renderer',ROOT/'tools/render_music.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.render_audio(data,target,cache_dir/(key+'.mp3'),Path('/usr/share/sounds/sf2/FluidR3_GM.sf2'),
                        chamber=chamber)
    return target

def prepare_timeline(score,mode,audio,config,cache,short_seconds=None):
    if mode=='performance':
        length=duration(audio) if audio else score.end*score.spb+3
        return [dict(kind='score',start=0,end=score.end,duration=length,timeline_start=0)],min(length,short_seconds) if short_seconds else length
    segments=copy.deepcopy(config['segments']);cursor=0
    for s in segments:
        if s.get('kind','score')=='score':
            s['kind']='score';s.setdefault('start',0);s.setdefault('end',min(score.end,s['start']+16))
            if s['start']<0 or s['end']<=s['start'] or s['end']>score.end+1e-7:raise ValueError('Lesson excerpt outside score.')
            if 'solo' in s and any(not 0<=i<score.n for i in s['solo']):raise ValueError('Missing solo voice.')
            s['duration']=max(s.get('duration',0),(s['end']-s['start'])*score.spb)
        else:s.setdefault('duration',4)
        if s.get('narration_audio'):
            s['duration']=max(s['duration'],duration(s['narration_audio'])+s.get('narration_delay',0)+.3)
        s['timeline_start']=cursor;cursor+=s['duration']
    return segments,min(cursor,short_seconds) if short_seconds else cursor

def timeline_frame(painter,segments,t,mode):
    ix=next((i for i,s in enumerate(segments) if s['timeline_start']<=t<s['timeline_start']+s['duration']),len(segments)-1)
    s=segments[ix];elapsed=t-s['timeline_start']
    if s['kind']=='card':return painter.card(s,elapsed,ix,len(segments))
    beat=min(s['end'],s['start']+elapsed/painter.s.spb)
    if mode=='lesson' and elapsed>=(s['end']-s['start'])*painter.s.spb:
        s={**s,'_excerpt_ended':True}
        beat=max(s['start'],s['end']-1e-6)
    return painter.performance(beat,s,ix if mode=='lesson' else None,len(segments))

def make_soundtrack(score,segments,length,mode,audio,cache,target):
    rate=44100
    if mode=='performance' and audio:
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(audio),'-t',str(length),'-ac','2','-ar',str(rate),str(target)],check=True)
        return
    result=np.zeros((math.ceil(length*rate),2),dtype=np.float32)
    for s in segments:
        offset=round(s['timeline_start']*rate)
        if offset>=len(result):break
        seglen=min(round(s['duration']*rate),len(result)-offset)
        if s['kind']=='score':
            musical_seconds=(s['end']-s['start'])*score.spb
            # A final-cadence excerpt may include the release already present
            # in the recording. Never read past an intermediate cut into the
            # next passage merely to fill a longer caption segment.
            final_release=(max(0,s['duration']-musical_seconds)
                           if abs(s['end']-score.end)<1e-7 else 0)
            if s.get('solo') is None and audio:
                music=decode_audio(audio,s['start']*score.spb,musical_seconds+final_release)
            else:
                wav=synth_excerpt(score,s['start'],s['end'],s.get('solo'),cache)
                music=decode_audio(wav,0,musical_seconds+final_release)
            take=min(seglen,len(music));gain=s.get('music_gain',.32 if s.get('narration_audio') else .88)
            # Short edge fades avoid clicks when a lesson isolates a sounding note.
            fade=min(round(.015*rate),take//2)
            if fade:music[:fade]*=np.linspace(0,1,fade)[:,None];music[take-fade:take]*=np.linspace(1,0,fade)[:,None]
            result[offset:offset+take]+=music[:take]*gain
        if s.get('narration_audio'):
            speech=decode_audio(s['narration_audio']);delay=round(s.get('narration_delay',0)*rate)
            take=min(len(speech),seglen-delay)
            if take>0:result[offset+delay:offset+delay+take]+=speech[:take]*s.get('narration_gain',1)
    peak=float(np.abs(result).max(initial=0))
    if peak>.96:result*=.96/peak
    from scipy.io import wavfile
    wavfile.write(str(target),rate,np.int16(np.clip(result,-1,1)*32767))

def render(args):
    WORK.mkdir(parents=True,exist_ok=True)
    path=Path(args['score']);source_bytes=path.read_bytes();source_hash=hashlib.sha256(source_bytes).hexdigest()
    if args.get('expected_sha256') and args['expected_sha256']!=source_hash:raise RuntimeError(f'Frozen source hash mismatch: {path}')
    score=Score(validate_score(json.loads(source_bytes)));score.source_sha256=source_hash
    mode=args.get('mode','performance')
    audio=Path(args['audio']) if args.get('audio') else None
    out=Path(args.get('output') or WORK/(path.stem+'-'+mode+'.mp4'));out.parent.mkdir(parents=True,exist_ok=True)
    cues=export_cues(score,path,args.get('cue_output') or out.with_suffix('.cues.json'),audio)
    if args.get('cues_only'):
        print(json.dumps({'cues':str(cues),'voices':score.n,'score_seconds':score.end*score.spb}),flush=True);return
    fps=int(args.get('fps',12))
    if not 1<=fps<=15:raise ValueError('Use 1–15 fps for this efficient pedagogical renderer.')
    config_path=args.get('lesson_config')
    config=json.loads(Path(config_path).read_text()) if config_path else default_lesson(score)
    if mode=='lesson' and not config_path:
        out.with_suffix('.lesson.json').write_text(json.dumps(config,indent=2))
    timeline,length=prepare_timeline(score,mode,audio,config,WORK/'audio_cache',args.get('short_seconds'))
    painter=Painter(score)
    preview_dir=WORK/'previews'/out.stem;preview_dir.mkdir(parents=True,exist_ok=True)
    preview_times=args.get('preview_times') or [0,min(8,length/3),min(28,length*.66),max(0,length-2)]
    for t in preview_times:
        if 0<=t<length:timeline_frame(painter,timeline,t,mode).save(preview_dir/f'{t:07.2f}.png')
    if args.get('preview_only'):
        print(json.dumps({'previews':str(preview_dir),'seconds':length,'mode':mode}),flush=True);return
    # Performance audio can be muxed directly from its frozen source. Avoid an
    # unnecessary PCM round trip; guided lessons still need an assembled track.
    track=audio if mode=='performance' and audio else WORK/(out.stem+'-soundtrack.wav')
    if not (mode=='performance' and audio):make_soundtrack(score,timeline,length,mode,audio,WORK/'audio_cache',track)
    video=WORK/(out.stem+'-silent.mp4')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-',
         '-an','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    frames=math.ceil(length*fps);started=time.monotonic()
    try:
        for k in range(frames):
            frame=timeline_frame(painter,timeline,k/fps,mode);proc.stdin.write(frame.tobytes())
            if k and k%(fps*30)==0:print(json.dumps({'file':out.name,'rendered_seconds':k/fps,'total_seconds':length}),flush=True)
    finally:proc.stdin.close()
    if proc.wait():raise RuntimeError('FFmpeg frame encoder failed.')
    muxing=out.with_name(out.stem+'-muxing.mp4')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video),'-i',str(track),'-map','0:v:0','-map','1:a:0',
                    '-c:v','copy','-c:a','aac','-b:a','160k','-t',str(length),'-movflags','+faststart',str(muxing)],check=True)
    checked=json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,duration,width,height:format=duration',
                                      '-of','json',str(muxing)],capture_output=True,text=True,check=True).stdout)
    types={s['codec_type'] for s in checked['streams']}
    if types!={'video','audio'} or abs(float(checked['format']['duration'])-length)>1/fps+.02:
        raise RuntimeError(f'Encoded movie failed duration/stream check: {out}')
    if hashlib.sha256(path.read_bytes()).hexdigest()!=source_hash:
        raise RuntimeError(f'Score changed while rendering; refusing to publish {out}')
    publish_file(muxing,out)
    video.unlink()
    report={'score':str(path),'output':str(out),'mode':mode,'width':W,'height':H,'fps':fps,'duration_seconds':length,
            'score_voices':score.n,'score_beats':score.end,'subject_entries':len(score.entries),'render_seconds':round(time.monotonic()-started,2),
            'audio':str(audio) if audio else 'synthesized from exact score','previews':str(preview_dir),'timeline':timeline,'cues':str(cues),
            'score_sha256':source_hash}
    atomic_json(out.with_suffix('.animation.json'),report)
    print(json.dumps(report,indent=2),flush=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--score');ap.add_argument('--audio');ap.add_argument('--output')
    ap.add_argument('--mode',choices=['performance','lesson'],default='performance')
    ap.add_argument('--lesson-config');ap.add_argument('--fps',type=int,default=12)
    ap.add_argument('--short-seconds',type=float);ap.add_argument('--preview-only',action='store_true')
    ap.add_argument('--preview-times',type=float,nargs='+');ap.add_argument('--batch')
    ap.add_argument('--cues-only',action='store_true');ap.add_argument('--cue-output')
    ap.add_argument('--expected-sha256')
    a=vars(ap.parse_args())
    if a['batch']:
        records=json.loads(Path(a['batch']).read_text())
        if isinstance(records,dict):records=records['renders']
        for row in records:render({**a,**row,'batch':None})
    elif not a['score']:ap.error('--score or --batch is required')
    else:render(a)

if __name__=='__main__':main()
