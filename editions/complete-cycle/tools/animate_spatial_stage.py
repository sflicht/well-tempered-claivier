#!/usr/bin/env python3
"""Exact-score spatial rehearsal for the clAIvier XXIV architectural film.

This is a schematic animatic, not a finished cinematic reconstruction. It draws
one persistent instrumentalist glyph for every canonical voice, at the stable
positions in production-design.json. Note gates control bow/breath gestures;
no instrumental fingering or physical room acoustics are claimed.

python tools/animate_spatial_stage.py --score work/cycle_fugues/24-fugue.json \
  --design work/film_xxiv/production-design.json --seconds 30 --draft \
  --output work/animation/spatial/24-stage-pilot.mp4
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import time

from animate_cycle import Score,load_score,validate_score,font,FastDraw,textblock,mix,clamp,note_name,export_cues,duration,publish_file,atomic_json,ROOT
from PIL import Image,ImageDraw

W,H=1280,720
SW,SH=950,510
PAPER='#f1eee5';INK='#26353c';MUTED='#657276';LINE='#d8d7cd';STONE='#b9b5a5'
WORK=ROOT/'work/animation/spatial'

def point(x,y,z=0):
    return (450+(x-.5)*630+(y-.5)*210,485-235*y+55*(x-.5)-365*z)

def poly(draw,xyz,fill,outline=None,width=1):
    pts=[point(*p) for p in xyz];draw.polygon(pts,fill=fill)
    if outline:draw.line(pts+[pts[0]],fill=outline,width=width,joint='curve')

def architecture():
    im=Image.new('RGB',(SW,SH),'#e9e7dd');d=FastDraw(im)
    # Designed geometry: its proportions are not a survey of the real basilica.
    poly(d,[(0,0,0),(0,1,0),(0,1,1),(0,0,1)],'#e1e1d8')
    poly(d,[(1,0,0),(1,1,0),(1,1,1),(1,0,1)],'#e1d8c8')
    poly(d,[(0,1,0),(1,1,0),(1,1,1),(0,1,1)],'#ece9dc')
    poly(d,[(0,0,0),(1,0,0),(1,1,0),(0,1,0)],'#d9d5c6',LINE)
    for k in range(1,10):
        d.line([point(k/10,0),point(k/10,1)],fill='#c8c6b9',width=1)
        d.line([point(0,k/10),point(1,k/10)],fill='#c8c6b9',width=1)
    # Abstract colored side windows and intersecting pools of light.
    for side,colors in [(0,['#638c9a','#6f9c9e','#8db6ab','#7d9e9c','#64839e']),
                         (1,['#b66d50','#c38c55','#c9a565','#bc764c','#a65c47'])]:
        for j,col in enumerate(colors):
            y=.12+j*.17
            for band in range(3):
                z=.48+band*.145
                poly(d,[(side,y,z),(side,y+.09,z),(side,y+.09,z+.125),(side,y,z+.125)],col,'#ece8dc',1)
                poly(d,[(side,y,0),(.52,y+.08,0),(.48,y+.18,0),(side,y+.09,0)],mix(col,'#d9d5c6',.77))
    # Two imagined raised galleries. Their stable player positions come from
    # the production manifest; these are not real access or placement plans.
    for a,b in [(.055,.185),(.815,.945)]:
        poly(d,[(a,.07,.25),(b,.07,.25),(b,.94,.25),(a,.94,.25)],'#aba997')
        poly(d,[(a,.07,.32),(b,.07,.32),(b,.94,.32),(a,.94,.32)],'#d0cbbb',STONE)
        edge=b if a<.5 else a
        d.line([point(edge,.07,.37),point(edge,.94,.37)],fill='#9b9c91',width=2)
        for y in [.08,.25,.42,.59,.76,.93]:d.line([point(edge,y,.32),point(edge,y,.37)],fill='#9b9c91',width=2)
    # Branching support columns supply a readable architectural scale.
    for y in [.90,.64,.38,.10]:
        for x in [.22,.78]:
            base=point(x,y,0);fork=point(x,y,.72);top=point(x,y,.95)
            d.line([base,fork],fill='#9e9f94',width=16)
            d.line([(base[0]-3,base[1]),(fork[0]-3,fork[1])],fill='#d2d1c1',width=6)
            for dx,dy in [(-.13,-.06),(.13,-.06),(-.06,.14),(.06,.14)]:
                branch=point(x+dx,y+dy,1.02)
                d.line([fork,branch],fill='#aaa99b',width=8)
                d.line([(fork[0]-2,fork[1]),(branch[0]-2,branch[1])],fill='#d4d1c0',width=3)
            d.ellipse((base[0]-12,base[1]-5,base[0]+12,base[1]+5),fill='#a7a89c')
    # A small apse suggestion, not religious iconography or a documentary claim.
    for j in range(7):
        x=.38+j*.04
        d.line([point(x,.98,.03),point(x,.98,.55+(.12-abs(x-.5)))],fill='#beb59c',width=5)
    return im

def player_glyph(draw,xy,size,player,color,sounding,phase=0,theme=False,show_id=True):
    x,y=xy;h=size;stroke=max(1,round(h*.065));head=h*.105
    coat=color if sounding else mix(color,'#a9aaa1',.6)
    limb=INK if sounding else '#7d817a';wood='#8b6247';metal='#aa8753'
    if theme:draw.ellipse((x-h*.50,y-h*.14,x+h*.50,y+h*.13),outline=color,width=max(2,stroke))
    elif sounding:draw.ellipse((x-h*.34,y-h*.09,x+h*.34,y+h*.09),outline=color,width=max(1,stroke))
    draw.ellipse((x-head,y-h*.86-head,x+head,y-h*.86+head),fill='#c8b29a',outline=limb,width=1)
    draw.line((x-head,y-h*.94,x+head*.55,y-h*.97),fill=limb,width=stroke)
    draw.polygon([(x-h*.17,y-h*.69),(x+h*.17,y-h*.69),(x+h*.21,y-h*.28),(x-h*.17,y-h*.28)],fill=coat)
    seated=not player.get('standing',True)
    if seated:
        draw.line([(x-h*.2,y-h*.29),(x+h*.2,y-h*.29),(x+h*.22,y)],fill='#7e8179',width=stroke)
        draw.line([(x,y-h*.30),(x+h*.12,y-h*.16),(x+h*.16,y)],fill=limb,width=stroke)
        draw.line([(x-h*.1,y-h*.30),(x-h*.15,y-h*.10),(x-h*.20,y)],fill=limb,width=stroke)
    else:
        draw.line([(x-h*.07,y-h*.30),(x-h*.12,y)],fill=limb,width=stroke)
        draw.line([(x+h*.08,y-h*.30),(x+h*.15,y)],fill=limb,width=stroke)
    rig=player.get('rig','clarinet');motion=math.sin(phase*math.pi*2) if sounding else 0
    if rig in ['violin','viola']:
        draw.ellipse((x-h*.34,y-h*.70,x+h*.02,y-h*.48),fill=wood,outline=limb,width=1)
        draw.line((x-h*.23,y-h*.59,x-h*.46,y-h*.81),fill=wood,width=stroke+1)
        bx=x+h*.07+motion*h*.10
        draw.line((bx-h*.18,y-h*.82,bx+h*.15,y-h*.40),fill='#e0d4b4',width=max(1,stroke))
        draw.line([(x+h*.14,y-h*.66),(bx+h*.07,y-h*.48)],fill=limb,width=stroke)
    elif rig in ['cello','double_bass','contrabass','doublebass'] or 'bass' in rig and player.get('family')=='string':
        tall=1.13 if 'double' in rig or 'contra' in rig else .86
        draw.ellipse((x-h*.17,y-h*.54*tall,x+h*.18,y-h*.08),fill=wood,outline=limb,width=1)
        draw.line((x,y-h*.22,x,y-h*.9*tall),fill=wood,width=stroke+1)
        draw.line((x,y-h*.1,x,y+h*.04),fill=limb,width=1)
        by=y-h*.35;offset=motion*h*.12
        draw.line((x-h*.40+offset,by,x+h*.39+offset,by+h*.03),fill='#e0d4b4',width=stroke)
    elif rig in ['flute','piccolo']:
        draw.line((x-h*.05,y-h*.8,x+h*.48,y-h*.72),fill='#e5ddd0',width=stroke+1)
        draw.line([(x-h*.13,y-h*.63),(x+h*.13,y-h*.76),(x+h*.32,y-h*.74)],fill=limb,width=stroke)
    elif rig in ['horn','euphonium','tuba']:
        draw.ellipse((x-h*.08,y-h*.61,x+h*.29,y-h*.23),outline=metal,width=stroke+1)
        draw.line((x,y-h*.78,x+h*.10,y-h*.56),fill=metal,width=stroke)
        draw.polygon([(x+h*.17,y-h*.42),(x+h*.37,y-h*.60),(x+h*.41,y-h*.42)],fill=metal)
        draw.line((x-h*.12,y-h*.62,x+h*.16,y-h*.42),fill=limb,width=stroke)
    elif 'trombone' in rig:
        extent=h*(.50+.10*motion)
        draw.line([(x,y-h*.8),(x+extent,y-h*.58),(x+extent,y-h*.50),(x+h*.12,y-h*.67)],fill=metal,width=stroke)
        draw.line((x-h*.12,y-h*.62,x+h*.25,y-h*.66),fill=limb,width=stroke)
    else:
        long='bassoon' in rig or 'bass_clarinet' in rig
        end=(x+h*(.24 if long else .18),y-h*(.08 if long else .32))
        draw.line((x,y-h*.79,*end),fill=wood if 'bassoon' in rig else '#363e3c',width=stroke+1)
        draw.line((x-h*.13,y-h*.63,x+h*.10,y-h*.52),fill=limb,width=stroke)
        draw.line((x+h*.12,y-h*.65,x+h*.16,y-h*.39),fill=limb,width=stroke)
    if sounding and player.get('family')!='string':
        pulse=.5+.5*math.sin(phase*math.pi*2)
        r=h*(.12+.035*pulse)
        draw.arc((x-r,y-h*.86-r,x+r,y-h*.86+r),300,55,fill=color,width=max(1,stroke))
    if show_id:
        label=f"{player['score_voice_index']+1:02d}";ft=font(10,True);width=draw.textlength(label,font=ft)
        draw.rounded_rectangle((x-width/2-3,y+3,x+width/2+3,y+17),radius=3,fill=color if sounding else '#e5e3d8')
        draw.text((x-width/2,y+3),label,font=ft,fill='#ffffff' if sounding else MUTED)

class Stage:
    def __init__(self,score,design,draft=False,audio_label='General MIDI orchestration sketch'):
        self.score=score;self.design=design;self.draft=draft;self.audio_label=audio_label
        self.players=sorted(design['players'],key=lambda p:p['score_voice_index'])
        if len(self.players)!=score.n or {p['score_voice_index'] for p in self.players}!=set(range(score.n)):
            raise ValueError('There must be exactly one player for each canonical voice.')
        self.backdrop=architecture()
        self.positions={p['score_voice_index']:point(**p['position_normalized']) for p in self.players}

    def floorplan(self,d,beat,focus):
        x0,y0,x1,y1=1001,151,1246,333
        d.rounded_rectangle((x0,y0,x1,y1),radius=8,fill='#e8e6dc',outline=LINE,width=1)
        for x in [.12,.31,.5,.69,.88]:
            xx=x0+20+x*(x1-x0-40);d.line((xx,y0+20,xx,y1-18),fill='#cccec3',width=1)
        for p in self.players:
            i=p['score_voice_index'];pos=p['position_normalized'];xx=x0+20+pos['x']*(x1-x0-40);yy=y1-18-pos['y']*(y1-y0-36)
            on=self.score.note(i,beat) is not None;color=self.score.colors[i]
            d.ellipse((xx-6,yy-6,xx+6,yy+6),fill=color if on else '#d4d5ca',outline=INK if i==focus else None,width=1)
            if i==focus:d.ellipse((xx-9,yy-9,xx+9,yy+9),outline=color,width=2)
        d.text((1002,126),'FLOORPLAN · 25 FIXED POSITIONS',font=font(11,True),fill=MUTED)
        d.text((1002,343),'All players stay present during rests.',font=font(11),fill=MUTED)

    def frame(self,seconds):
        beat=min(self.score.end,seconds/self.score.spb)
        active=self.score.active_entries(beat);primary=[e for e in active if e['role']=='subject']
        focus_entry=primary[-1] if primary else None
        focus=focus_entry['voice'] if focus_entry else None
        notes=[self.score.note(i,beat) for i in range(self.score.n)];count=sum(n is not None for n in notes)
        scene=self.backdrop.copy();sd=FastDraw(scene)
        themes={e['voice'] for e in primary}
        for p in sorted(self.players,key=lambda p:self.positions[p['score_voice_index']][1]):
            i=p['score_voice_index'];note=notes[i];on=note is not None
            phase=((beat-note['t'])/max(.2,note['d']))*2 if on else 0
            player_glyph(sd,self.positions[i],31,p,self.score.colors[i],on,phase,i in themes)
        # A restrained focus move preserves the fixed geometry. The inset
        # continues to show every location even when the camera crops the view.
        zoom=1.;target=(SW/2,SH/2)
        if focus_entry and seconds>5 and count<25:
            elapsed=(beat-focus_entry['t'])*self.score.spb
            remaining=(focus_entry['end']-beat)*self.score.spb
            amount=min(clamp(elapsed/1.2,0,1),clamp(remaining/1.2,0,1))
            amount=amount*amount*(3-2*amount)
            zoom=1+.14*amount
            fx,fy=self.positions[focus];target=(SW/2+(fx-SW/2)*.55*amount,SH/2+(fy-SH/2)*.45*amount)
        if zoom>1:
            large=scene.resize((round(SW*zoom),round(SH*zoom)),Image.Resampling.BICUBIC)
            cx=clamp(target[0]*zoom-SW/2,0,large.width-SW);cy=clamp(target[1]*zoom-SH/2,0,large.height-SH)
            scene=large.crop((round(cx),round(cy),round(cx)+SW,round(cy)+SH))
        im=Image.new('RGB',(W,H),PAPER);im.paste(scene,(20,112));d=FastDraw(im)
        d.text((30,22),'THE WELL-TEMPERED clAIvier  /  XXIV',font=font(13,True),fill='#9c5840')
        d.text((29,47),'All the threads',font=font(34,False,True),fill=INK)
        d.text((330,66),'Conceptual spatial rehearsal',font=font(17),fill=MUTED)
        stamp='DRAFT SCORE' if self.draft else 'SCORE-BOUND ANIMATIC'
        d.text((1020,28),stamp,font=font(12,True),fill='#9c5840')
        d.text((1020,53),f'{count} / {self.score.n} parts sounding',font=font(15,True),fill=INK)
        d.line((28,96,1250,96),fill=LINE,width=1)
        self.floorplan(d,beat,focus)
        if focus is not None:
            p=self.players[focus];entry=focus_entry
            d.text((1002,380),'FOLLOW THE ENTRY',font=font(11,True),fill=MUTED)
            textblock(d,(1000,404),p['instrument'],size=24,serif=True,width=248,max_lines=2,leading=29)
            d.text((1002,466),f"voice-{focus+1:02d}  ·  {p['zone']}",font=font(12),fill=MUTED)
            note=notes[focus];phase=((beat-note['t'])/max(.2,note['d']))*2 if note else 0
            player_glyph(d,(1066,596),95,p,self.score.colors[focus],note is not None,phase,True,False)
            textblock(d,(1133,508),entry.get('label','Subject'),size=13,bold=True,width=110,max_lines=3)
            if note:
                d.text((1133,568),note_name(note['p']),font=font(22,True),fill=INK)
                d.text((1133,597),'concert pitch',font=font(10),fill=MUTED)
            counter=[e for e in active if e['role']=='countersubject']
            if counter:
                cp=self.players[counter[0]['voice']]
                textblock(d,(1002,617),f"Countertheme: {cp['instrument']}",size=11,width=245,max_lines=1)
        else:
            title,body=self.score.explanation(beat)
            textblock(d,(1000,388),title,size=24,serif=True,width=248,max_lines=3,leading=30)
            textblock(d,(1002,492),body if any(e['role']=='fragment' for e in active) else 'Listen across the room. The floorplan preserves every voice’s location.',size=16,width=240,max_lines=5,leading=23)
        d.line((29,640,1250,640),fill=LINE,width=1)
        textblock(d,(30,653),self.score.marker(beat),size=18,bold=True,width=680,max_lines=1)
        clock=f'{int(seconds)//60}:{int(seconds)%60:02d}'
        d.text((1190,650),clock,font=font(21,True),fill=INK)
        d.text((30,687),'Sagrada Família-inspired diagram · symbolic instrumental gestures follow the score.',font=font(11),fill=MUTED)
        d.text((786,687),self.audio_label,font=font(11),fill=MUTED)
        return im

def orchestration_audio(score,design,start,length,target):
    data=copy.deepcopy(score.data);end=min(score.end,(start+length)/score.spb);begin=start/score.spb
    players={p['score_voice_index']:p for p in design['players']}
    for i,voice in enumerate(data['voices']):
        p=players[i];voice['gm_program']=p.get('gm_preview_program_zero_based',0)
        voice['pan']=round(64+63*clamp(p.get('pan',0),-1,1));events=[]
        for n in voice['events']:
            a=max(begin,n['t']);b=min(end,n['t']+n['d'])
            if b>a:events.append({**n,'t':a-begin,'d':b-a})
        voice['events']=events
    spec=importlib.util.spec_from_file_location('stage_music_renderer',ROOT/'tools/render_music.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.render_audio(data,target.with_suffix('.wav'),target,Path('/usr/share/sounds/sf2/FluidR3_GM.sf2'),chamber=True)
    return target

def main():
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--score',required=True);ap.add_argument('--design',required=True);ap.add_argument('--audio')
    ap.add_argument('--output',required=True);ap.add_argument('--seconds',type=float);ap.add_argument('--start-seconds',type=float,default=0)
    ap.add_argument('--fps',type=int,default=12);ap.add_argument('--draft',action='store_true');ap.add_argument('--preview-only',action='store_true')
    ap.add_argument('--expected-sha256');ap.add_argument('--audio-label')
    args=ap.parse_args();WORK.mkdir(parents=True,exist_ok=True)
    scorepath=Path(args.score);source_bytes=scorepath.read_bytes();source_hash=hashlib.sha256(source_bytes).hexdigest()
    if args.expected_sha256 and source_hash!=args.expected_sha256:raise RuntimeError('Frozen score hash mismatch.')
    score=Score(validate_score(json.loads(source_bytes)));score.source_sha256=source_hash
    design_bytes=Path(args.design).read_bytes();design=json.loads(design_bytes);design_hash=hashlib.sha256(design_bytes).hexdigest()
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    if not 1<=args.fps<=15:raise ValueError('Use 1–15 fps.')
    start=args.start_seconds;total=duration(args.audio) if args.audio else score.end*score.spb+3
    length=min(args.seconds or total-start,total-start)
    if start<0 or length<=0:raise ValueError('Excerpt lies outside the score.')
    label=args.audio_label or ('Provided orchestration reference' if args.audio else 'General MIDI orchestration sketch')
    stage=Stage(score,design,args.draft,label)
    preview=WORK/'previews'/out.stem;preview.mkdir(parents=True,exist_ok=True)
    for t in [0,min(8,length*.25),min(20,length*.6),max(0,length-1)]:stage.frame(start+t).save(preview/f'{t:07.2f}.png')
    if args.preview_only:print(json.dumps({'previews':str(preview),'seconds':length}));return
    track=Path(args.audio) if args.audio else orchestration_audio(score,design,start,length,WORK/(out.stem+'-gm.mp3'))
    silent=WORK/(out.stem+'-silent.mp4');began=time.monotonic()
    command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}',
             '-r',str(args.fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',str(silent)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for k in range(math.ceil(length*args.fps)):
            proc.stdin.write(stage.frame(start+k/args.fps).tobytes())
            if k and k%(args.fps*30)==0:print(json.dumps({'output':out.name,'rendered_seconds':k/args.fps,'total_seconds':length}),flush=True)
    finally:proc.stdin.close()
    if proc.wait():raise RuntimeError('Stage frame encoder failed.')
    temp=out.with_name(out.stem+'-muxing.mp4')
    command=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent)]
    if args.audio:command+=['-ss',str(start)]
    command+=['-i',str(track),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(length),'-movflags','+faststart',str(temp)]
    subprocess.run(command,check=True)
    if abs(duration(temp)-length)>1/args.fps+.02:raise RuntimeError('Stage movie has an unexpected duration.')
    if hashlib.sha256(scorepath.read_bytes()).hexdigest()!=source_hash:raise RuntimeError('Score changed while rendering.')
    publish_file(temp,out);silent.unlink()
    cue_path=export_cues(score,scorepath,out.with_suffix('.cues.json'),track)
    report={'schema':'clAIvier-spatial-rehearsal/v1','output':str(out),'source_score':str(scorepath),
            'source_sha256':source_hash,'production_design':str(Path(args.design)),
            'design_sha256':design_hash,'player_count':len(stage.players),
            'draft_score':args.draft,'start_seconds':start,'duration_seconds':length,'fps':args.fps,'width':W,'height':H,
            'audio':str(track),'audio_label':label,'render_seconds':round(time.monotonic()-began,2),'previews':str(preview),'cues':str(cue_path),
            'representation':'Conceptual spatial rehearsal. Fixed positions, exact score-driven note gates, symbolic instrumental gestures; no fingering or physical acoustic model.'}
    atomic_json(out.with_suffix('.stage.json'),report);print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':main()
