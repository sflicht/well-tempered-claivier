#!/usr/bin/env python3
"""Compose the 23 companion preludes for the clAIvier working cycle.

Every movement has its own specified motive, rhythmic design, tonal itinerary,
registration and formal arc. These are free keyboard preludes: the construction
is not advertised as strict species counterpoint. Prelude IV is copied without
changing a byte from the accepted first audition.

The construction is deterministic and inspectable. A note's explicit spelling,
harmonic role and motif identity travel with it into the teaching animation.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import math
import re
import shutil
import statistics

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'work/cycle_preludes'

@dataclass
class Plan:
    number:int
    key:str
    mode:str
    meter:tuple[int,int]
    bpm:int
    character:str
    style:str
    tempo:str
    progression:str
    motive:tuple[int,...]
    explanation:str
    voices:int=3


PLANS=[
Plan(1,'C','major',(4,4),84,'Aperture','aperture','Andante, limpido',
 'I I6 ii6 V I IV I6 V vi V/vi vi IV ii6 V/V V V I I6 IV ii6 iii vi ii6 V I IV iv I6 ii6 I64 V I',
 (0,1,2,3,2,1,2,1),'An eight-note rising-and-folding arpeggio opens the cycle; an inner song gradually emerges.'),
Plan(2,'C','minor',(4,4),104,'Sparks','toccata','Allegro, incisivo',
 'i i6 iv V i VI ii_dim6 V III VII III VI iv V/V V V i VII VI V iv i6 N6 V i6 i64 V i',
 (0,2,1,3,2,0,1,2),'Two hands exchange short sixteenth-note bursts before the upper current becomes continuous.'),
Plan(3,'C#','major',(12,8),96,'Glass bells','bells','Moderato, luminoso',
 'I I6 vi iii IV I6 ii6 V iii V/vi vi IV ii6 V/V V V I IV iv I6 ii6 I64 V I',
 (2,0,3,1,4,2),'Isolated bell attacks occupy different registers; the silence between attacks is part of the phrase.',4),
Plan(5,'D','major',(6,8),102,'Mirrored gigue','gigue','Allegro giocoso',
 'I V I6 IV ii6 V I V vi V/vi vi iii IV ii6 V/V V I IV I6 V vi iii ii6 V I IV iv I6 ii6 I64 V I',
 (0,2,1,3,2,1),'The opening leap and answering descent are varied over a compound-duple dance.'),
Plan(6,'D','minor',(3,4),58,'Sarabande','sarabande','Lento, con gravita',
 'i V6 i6 iv VII III VI ii_dim6 V i6 iv V III VII III V/III III VI iv i6 ii_dim6 V i VI iv i6 N6 V i iv V i',
 (2,1,0,1,2,0),'A measured triple dance gives weight to the second beat and space to the cadence.',4),
Plan(7,'Eb','major',(4,4),72,'Columns and windows','columns','Maestoso, ma cantabile',
 'I IV I6 ii6 V I vi iii IV ii6 V/V V vi V/vi vi IV I6 iv N6 V I IV V I',
 (2,1,3,2,0,1),'Four broad layers alternate sustained columns with more mobile melodic windows.',4),
Plan(8,'Eb','minor',(12,8),96,'Night loom','weave','Andante sostenuto',
 'i VI iv i6 ii_dim6 V i V III VII III VI iv V/V V V i iv N6 V VI iv V i',
 (1,2,0,1,3,2),'A slow melody floats above a quiet, continuously woven inner line.'),
Plan(9,'E','major',(3,4),92,'Arabesque','arabesque','Allegretto, leggiero',
 'I iii vi IV ii6 V I V vi ii6 V/V V I6 IV ii6 V iii vi IV ii6 V/vi vi IV V I I6 iv I6 ii6 I64 V I',
 (0,1,3,2,4,3,2,1,0,2,1,2),'The right hand unfolds twelve sixteenth notes per bar, returning to a recognisable folded contour.'),
Plan(10,'E','minor',(4,4),82,'Question and echo','echo','Andante, parlando',
 'i i6 iv V i VI ii_dim6 V III VII VI III iv i6 V/V V i VII VI V III VI iv V i iv N6 V i6 iv V i',
 (0,2,1,0),'A short question in the upper register is answered below; the middle section narrows the gap.'),
Plan(11,'F','major',(6,8),94,'Pastorale','pastorale','Andantino pastorale',
 'I IV I IV I6 ii6 V I vi iii IV I6 ii6 V I V IV I6 ii6 V vi V/vi vi IV I6 IV ii6 V/V V V I IV iv I6 ii6 V I IV V I',
 (0,1,0,2,1,0),'A lilting dotted cell and gently repeated bass create a pastoral compound-duple movement.'),
Plan(12,'F','minor',(4,4),76,'Ground and embers','ground','Andante, ostinato',
 'i VII VI V i VII VI V i VII VI V i VII VI V i VII VI V iv III ii_dim6 V i6 i64 V i',
 (3,2,1,0,2,1),'A four-bar descending ground supports progressively smaller rhythmic values, then releases.'),
Plan(13,'F#','major',(5,4),102,'Prisms','prisms','Con moto, in cinque',
 'I vi IV ii6 V I iii vi IV ii6 V/V V I IV iv I6 vi V/vi vi ii6 I64 V I I',
 (0,2,1,3,2,4,3,1,2,0),'Five-quarter bars are divided first into two plus three beats and then into three plus two.',4),
Plan(14,'F#','minor',(3,4),86,'Turning chaconne','chaconne','Moderato, sempre danzante',
 'i V6 i6 iv VII III ii_dim6 V i V6 i6 iv VII III ii_dim6 V i V6 i6 iv VII III ii_dim6 V III VII VI V iv i6 N6 V i VI iv V i6 i64 V i',
 (1,2,0,1,3,1),'An eight-bar harmonic circuit returns with changed melodic shape, rhythmic density and register.'),
Plan(15,'G','major',(7,8),108,'Uneven clock','clock','Allegretto, preciso',
 'I V I6 IV ii6 V I V vi iii IV ii6 V/V V I V I6 IV vi iii ii6 V/vi vi IV I ii6 V/V V vi iii IV V I IV iv I6 ii6 I64 V I',
 (0,1,2,1,3,2,0),'Seven eighth notes are grouped three-plus-two-plus-two, with an inner part phrased two-plus-two-plus-three.',4),
Plan(16,'G','minor',(4,4),76,'Lament and current','lament','Andante, poi mosso',
 'i VII VI V i iv i6 V III VI iv ii_dim6 V/V V V V i VI iv V III iv N6 V i6 i64 V i',
 (3,2,1,0,1,2),'The opening descending line later becomes the outline of rapid figuration.'),
Plan(17,'Ab','major',(4,4),76,'Hanging garden','garden','Andante cantabile',
 'I I6 IV ii6 V vi IV V I6 V/vi vi iii IV ii6 V/V V I IV iv I6 vi IV ii6 V I6 I64 V I',
 (1,3,2,0,1,2),'Long melodic spans are set over delicate inner arpeggios; the late return rises an octave.'),
Plan(18,'G#','minor',(6,8),100,'Low mirrors','mirrors','Moderato, oscuro',
 'i V i6 iv VII III VI V i VII VI V III VI iv V/V V V i VI iv i6 ii_dim6 V III iv N6 V i iv V i',
 (0,2,1,3,1,2),'Two figures mirror their direction in the middle and low registers, with a dark compound-duple tread.'),
Plan(19,'A','major',(9,8),110,'Multiplying daylight','nine','Allegro fluente',
 'I IV I6 ii6 V I vi iii IV V/V V I vi V/vi vi IV I iii IV ii6 vi IV ii6 V I IV iv I6 ii6 I64 V I',
 (0,1,2,3,1,2,4,2,1),'Three compound beats carry related but differently turned three-note figures.',4),
Plan(20,'A','minor',(5,4),96,'Interleaved currents','interleave','Con moto, elastico',
 'i VI iv V III VII VI V i VII iv i6 ii_dim6 V/V V V i iv N6 V i6 i64 V i',
 (2,0,1,3,2,1),'Upper and middle phrases divide the five-quarter measure differently, while the bass marks its span.',4),
Plan(21,'Bb','major',(4,4),88,'Answering bells','bell_echo','Moderato, sereno',
 'I I IV IV I6 I6 V V vi vi iii iii IV IV ii6 V iii vi IV I6 ii6 V/V V V I IV iv I6 ii6 I64 V I',
 (2,3,1,0),'High and low bell figures answer across adjacent bars; later the exchange contracts into one bar.',4),
Plan(22,'Bb','minor',(3,4),70,'Passacaglia','passacaglia','Largo, con fermezza',
 'i VII VI V iv V VI V i VII VI V iv V VI V i VII VI V iv V VI V i VII VI V iv V VI V i III iv N6 i64 V i i',
 (2,1,0,2,3,1),'An eight-bar ground returns through five levels of texture before a restrained final tonic.'),
Plan(23,'B','major',(12,8),112,'Bright mechanism','mechanism','Allegro luminoso',
 'I iii vi IV ii6 V/V V I vi V/vi vi IV iii vi ii6 V I IV iv I6 ii6 I64 V I',
 (0,2,1,3,1,2,4,3),'A rapid upper mechanism sits above three half-note pulses and four dotted-quarter bass pulses.',4),
Plan(24,'B','minor',(4,4),82,'Threshold','threshold','Sostenuto, poi con moto',
 'i i6 VI iv V V i V III VII VI III iv V/V V V i VII VI V III VI iv V i VI iv i6 N6 V VI V i iv ii_dim6 V i6 i64 V i',
 (0,2,3,1,2,0,1,3),'Five keyboard layers accumulate, open into distant registers, and withdraw before the final fugue.',5),
]

NATURALS={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
LETTERS='CDEFGAB'

def key_pc(key):
    return (NATURALS[key[0]]+key.count('#')-key.count('b'))%12

def lily_spelling(letter,pc):
    difference=(pc-NATURALS[letter]+6)%12-6
    assert abs(difference)<=2,(letter,pc,difference)
    return letter.lower()+('is'*difference if difference>=0 else 'es'*(-difference))

def roman(n):
    out=''
    for val,letters in [(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]:
        while n>=val:out+=letters;n-=val
    return out

def key_name(p):
    names={'C#':'C-sharp','Eb':'E-flat','F#':'F-sharp','Ab':'A-flat','G#':'G-sharp','Bb':'B-flat'}
    return names.get(p.key,p.key)+' '+p.mode

def harmony(label,p):
    original=label
    inversion=0
    if label.endswith('64'):label=label[:-2];inversion=2
    elif label.endswith('6'):label=label[:-1];inversion=1
    major={'I':(0,0,'M'),'ii':(1,2,'m'),'iii':(2,4,'m'),'IV':(3,5,'M'),
           'V':(4,7,'M'),'vi':(5,9,'m'),'iv':(3,5,'m'),'N':(1,1,'M')}
    minor={'i':(0,0,'m'),'ii_dim':(1,2,'d'),'III':(2,3,'M'),'iv':(3,5,'m'),
           'v':(4,7,'m'),'V':(4,7,'M'),'VI':(5,8,'M'),'VII':(6,10,'M'),
           'I':(0,0,'M'),'N':(1,1,'M')}
    secondary={'V/V':(1,2,'M'),'V/vi':(2,4,'M'),'V/III':(6,10,'M')}
    step,offset,quality=secondary[label] if label in secondary else (major if p.mode=='major' else minor)[label]
    intervals={'M':[0,4,7],'m':[0,3,7],'d':[0,3,6]}[quality]
    tonic=key_pc(p.key);root=(tonic+offset)%12
    pcs=[(root+j)%12 for j in intervals]
    tonic_letter=LETTERS.index(p.key[0])
    spell={pc:lily_spelling(LETTERS[(tonic_letter+step+2*i)%7],pc) for i,pc in enumerate(pcs)}
    return dict(roman=original,root=root,pcs=pcs,spell=spell,bass_pc=pcs[inversion],
                inversion=inversion,quality=quality,root_degree=step+1)

def close_pc(pc,target,low=21,high=108):
    choices=[p for p in range(low,high+1) if p%12==pc]
    return min(choices,key=lambda p:(abs(p-target),-p))

def palette(h,center):
    root=close_pc(h['root'],center,36,96)
    intervals={'M':[0,4,7],'m':[0,3,7],'d':[0,3,6]}[h['quality']]
    return [root+12*(i//3)+intervals[i%3] for i in range(-6,10)]

def chord_pitch(h,base,rank):
    intervals={'M':[0,4,7],'m':[0,3,7],'d':[0,3,6]}[h['quality']]
    return base+12*(rank//3)+intervals[rank%3]

def scale_spelling(p,pc):
    degrees=[0,2,4,5,7,9,11] if p.mode=='major' else [0,2,3,5,7,8,10]
    tonic=key_pc(p.key);li=LETTERS.index(p.key[0])
    for i,d in enumerate(degrees):
        if (tonic+d)%12==pc:return lily_spelling(LETTERS[(li+i)%7],pc)
    if (tonic+11)%12==pc:return lily_spelling(LETTERS[(li+6)%7],pc)
    return None

def neighbor(p,pitch,h):
    # A short upper neighbor returns immediately to its consonant anchor.
    for d in [1,2]:
        q=pitch+d
        if scale_spelling(p,q%12) and q%12 not in h['pcs']:return q
    return None

def make_score(p):
    chords=[harmony(x,p) for x in p.progression.split()]
    bars=len(chords);barlen=p.meter[0]*4/p.meter[1]
    total=bars*barlen
    names={2:['Melody','Bass'],3:['Melody','Inner figure','Bass'],
           4:['Melody','Upper inner','Lower inner','Bass'],
           5:['Melody','Upper inner','Middle','Lower inner','Bass']}[p.voices]
    voices=[dict(name=name,abbr=['M.','U.','I.','L.','B.'][i] if p.voices==5 else name[0]+'.',
                 clef='bass' if i>=p.voices-2 and (i>1 or p.voices==2) else 'treble',events=[])
            for i,name in enumerate(names)]
    sections=[]
    boundary_bars=sorted(set([0,8,min(16,bars-8),bars-8,bars-4]))
    labels=['Opening cell','Contrasting span','Development','Return','Cadence']
    for i,b in enumerate(boundary_bars):
        end=boundary_bars[i+1]*barlen if i+1<len(boundary_bars) else total
        label=labels[i] if len(boundary_bars)==5 else ['Opening cell','Contrasting span','Return','Cadence'][i]
        sections.append(dict(t=b*barlen,end=end,label=label,
          explanation=(p.explanation if i==0 else
                       'The final harmonic progression closes in the movement\'s tonic.' if b==bars-4 else
                       'The characteristic figure returns with changed harmony, density or register.')))
    harmonic=[]
    motif_events=[]
    previous_bass=40

    def add(v,t,d,pitch,h,velocity=67,role='motif',ornament=False,label=None):
        if d<=0:return
        if pitch is None:return
        assert 0<=pitch<=127,(p.number,v,t,pitch)
        spelling=h['spell'].get(pitch%12) or scale_spelling(p,pitch%12)
        event=dict(t=round(t,6),d=round(d,6),p=int(pitch),v=int(max(30,min(100,velocity))),
                   source='authored texture',role=role,motif_id=f'P{p.number:02d}-{p.style}',
                   harmony=h['roman'],gate=.95 if p.style in ['toccata','clock','mechanism','gigue'] else .985)
        if spelling:event['spell']=spelling
        if label:event['label']=label
        if ornament:event['role']='returning neighbor'
        voices[v]['events'].append(event)

    def emit(v,start,durations,ranks,base,h,velocity,role='motif',decorate=False):
        t=start
        for j,d in enumerate(durations):
            rank=ranks[j%len(ranks)]
            pitch=chord_pitch(h,base,rank)
            if decorate and j==0 and d>=1.5:
                n=neighbor(p,pitch,h)
                if n is not None:
                    add(v,t,d-1,pitch,h,velocity,role)
                    add(v,t+d-1,.5,n,h,velocity-4,role,True)
                    add(v,t+d-.5,.5,pitch,h,velocity-1,role)
                    t+=d;continue
            add(v,t,d,pitch,h,velocity+(2 if j==0 else -2 if d<.5 else 0),role)
            t+=d

    for b,h in enumerate(chords):
        t=b*barlen;phase=min(3,int(4*b/bars));pos=b%8
        # A stable register is widened only in specified late returns.
        top=close_pc(h['root'],70,60,84)
        if p.style=='mirrors':top-=12
        if p.style in ['garden','bells'] and bars-8<=b<bars-4:top+=12
        if p.style=='threshold' and 24<=b<32:top+=12
        dynamic=[66,72,79,63][phase]
        if p.style in ['sarabande','bells','weave','garden']:dynamic-=8
        if p.style in ['toccata','mechanism','clock']:dynamic+=5
        if b==bars-1:dynamic=53 if p.mode=='minor' else 59
        motif=list(p.motive)
        if phase==1:motif=motif[2:]+motif[:2]
        if phase==2 and p.style not in ['ground','passacaglia','chaconne']:motif=list(reversed(motif))
        if b%4==3:motif=motif[-2:]+motif[:-2]
        harmonic.append(dict(t=t,d=barlen,bar=b+1,roman=h['roman'],pitch_classes=h['pcs'],
                             bass_pitch_class=h['bass_pc'],label=h['roman'],
                             inversion=h['inversion']))
        if b%4==0:
            motif_events.append(dict(t=t,d=barlen,voice=0,id=f'P{p.number:02d}-{p.style}',
                                     label='Characteristic figure',relationship='harmonically varied contour'))
        if b==bars-1:
            final_top=close_pc(key_pc(p.key),top+3,60,100)
            final_pitches=[final_top]
            for i in range(1,p.voices-1):
                relative=p.voices-1-i
                target=final_top-8-8*(i-1)
                pc=h['pcs'][1 if i%2 else 2]
                final_pitches.append(close_pc(pc,target,28,96))
            final_pitches.append(close_pc(key_pc(p.key),34,24,48))
            for i,pitch in enumerate(final_pitches):add(i,t,barlen,pitch,h,dynamic-3*i,'final tonic')
            continue

        # Upper part: each style has a specified rhythmic identity.
        if p.style=='aperture':
            emit(0,t,[.5]*8,motif,top,h,dynamic)
        elif p.style=='toccata':
            emit(0,t,[.25]*(8 if phase in [0,3] else 16),motif,top,h,dynamic)
        elif p.style=='bells':
            for j,(at,d) in enumerate([(0,.75),(1.5,.5),(3.5,1),(5,.75)]):
                add(0,t+at,d,chord_pitch(h,top,motif[j]),h,dynamic,'bell figure')
        elif p.style=='gigue':
            emit(0,t,[1,.5,.5,.5,.5],motif,top,h,dynamic)
        elif p.style=='sarabande':
            emit(0,t,[1,1.5,.5],motif,top,h,dynamic,decorate=b%4==2)
            # The second beat has the characteristic sarabande weight.
            for e in voices[0]['events']:
                if e['t']==t+1:e['v']=min(96,e['v']+5)
        elif p.style=='columns':
            ds=[2,2] if phase in [0,3] else [1,.5,.5,1,1]
            emit(0,t,ds,motif,top,h,dynamic,decorate=b%4==2)
        elif p.style=='weave':
            emit(0,t,[1.5,1.5,3],motif,top,h,dynamic,decorate=b%4==1)
        elif p.style=='arabesque':
            emit(0,t,[.25]*12,motif,top,h,dynamic)
        elif p.style=='echo':
            emit(0,t,[.5,.5,1],motif,top,h,dynamic)
            if phase==2:emit(0,t+3,[.5,.5],motif[1:],top,h,dynamic-6)
        elif p.style=='pastorale':
            emit(0,t,[.75,.25,.5,1,.5],motif,top,h,dynamic)
        elif p.style in ['ground','lament']:
            ds=[2,1,1] if phase in [0,3] else [.5]*8 if phase==1 else [.25]*16
            emit(0,t,ds,motif,top,h,dynamic,decorate=phase==0 and b%4==2)
        elif p.style=='prisms':
            emit(0,t,[.5]*10,motif,top,h,dynamic)
            for e in voices[0]['events']:
                if t<=e['t']<t+barlen and (e['t']-t) in ([0,2] if phase%2==0 else [0,3]):e['v']+=4
        elif p.style in ['chaconne','passacaglia']:
            ds=([1,.5,.5,1] if phase==0 else [.5]*6 if phase==1 else [.25]*12 if phase==2 else [1.5,.5,1])
            emit(0,t,ds,motif,top,h,dynamic,decorate=False)
        elif p.style=='clock':
            emit(0,t,[.5]*7,motif,top,h,dynamic)
            for e in voices[0]['events']:
                if t<=e['t']<t+barlen and (e['t']-t) in [0,1.5,2.5]:e['v']+=4
        elif p.style=='garden':
            emit(0,t,[2,1,1],motif,top,h,dynamic,decorate=b%4==2)
        elif p.style=='mirrors':
            emit(0,t,[.5]*6,motif,top,h,dynamic)
        elif p.style=='nine':
            emit(0,t,[.5]*9,motif,top,h,dynamic)
        elif p.style=='interleave':
            emit(0,t,[1,.5,.5,1,1,1],motif,top,h,dynamic)
        elif p.style=='bell_echo':
            if b<16:
                if b%2==0:emit(0,t,[.5,.5,1],motif,top+12,h,dynamic)
            else:emit(0,t,[.5,.5,1],motif,top+12,h,dynamic)
        elif p.style=='mechanism':
            emit(0,t,[.25]*24,motif,top,h,dynamic)
        elif p.style=='threshold':
            ds=[2,1,1] if phase==0 else [.5]*8 if phase==1 else [.25]*16 if phase==2 else [1.5,.5,1,1]
            emit(0,t,ds,motif,top,h,dynamic,decorate=False)
        else:raise ValueError(p.style)

        # Inner parts: distinct roles and pulse structures across the cycle.
        inner_base=top-12
        if p.style=='toccata':
            emit(1,t+2,[.25]*8,[2,1,0,2,1,3,2,0],inner_base,h,dynamic-11)
            if phase in [1,2]:emit(1,t,[1,1],[1,2],inner_base,h,dynamic-14)
        elif p.style=='echo':
            emit(1,t+2,[.5,.5,1],motif,inner_base,h,dynamic-9,'echo')
        elif p.style=='bell_echo':
            if b<16:
                if b%2:emit(1,t,[.5,.5,1],motif,inner_base+12,h,dynamic-10,'answering bell')
            else:emit(1,t+2,[.5,.5,1],motif,inner_base+12,h,dynamic-10,'answering bell')
            emit(2,t,[2,2],[1,2],inner_base-12,h,dynamic-20,'sustained middle')
        elif p.style in ['weave','garden','aperture']:
            if p.style=='aperture':
                emit(1,t,[2,1,1],[1,2,1] if phase!=2 else [2,1,0],inner_base,h,dynamic-16,'inner song')
            else:
                emit(1,t,[.5]*int(2*barlen),[0,2,1,2,0,1],inner_base,h,dynamic-20,'inner arpeggio')
        elif p.style=='bells':
            for j,(at,d) in enumerate([(.5,1),(2.5,.75),(4.5,.75)]):
                add(1,t+at,d,chord_pitch(h,inner_base,[1,2,0][j]),h,dynamic-12,'middle bell')
            for j,(at,d) in enumerate([(1,1.25),(4,1.25)]):
                add(2,t+at,d,chord_pitch(h,inner_base-12,[2,1][j]),h,dynamic-16,'low bell')
        elif p.style=='columns':
            emit(1,t,[2,2],[1,2],inner_base,h,dynamic-12,'upper chord')
            emit(2,t,[4],[2],inner_base-12,h,dynamic-15,'lower chord')
        elif p.style=='sarabande':
            emit(1,t,[1,2],[1,2],inner_base,h,dynamic-14,'dance harmony')
            emit(2,t,[3],[2],inner_base-12,h,dynamic-18,'sustained lower voice')
        elif p.style in ['prisms','clock','interleave']:
            if p.style=='prisms':ds=[1.5,1.5,2]
            elif p.style=='clock':ds=[1,1,1.5]
            else:ds=[1.5,1.5,2]
            emit(1,t,ds,[1,2,0],inner_base,h,dynamic-13,'cross-grouped phrase')
            emit(2,t,[barlen],[2],inner_base-12,h,dynamic-19,'harmonic span')
        elif p.style=='mechanism':
            emit(1,t,[2,2,2],[1,2,0],inner_base,h,dynamic-13,'three half-note pulses')
            emit(2,t,[3,3],[2,1],inner_base-12,h,dynamic-19,'long inner line')
        elif p.style=='nine':
            emit(1,t,[1.5,1.5,1.5],[1,2,0],inner_base,h,dynamic-13,'compound-beat line')
            emit(2,t,[3,1.5],[2,1],inner_base-12,h,dynamic-18,'broad inner line')
        elif p.style=='threshold':
            emit(1,t,[1,1,2],[1,2,0],inner_base,h,dynamic-12,'upper answering line')
            if b>=8:emit(2,t,[.5]*8,[2,0,1,2,1,0,2,1],inner_base-12,h,dynamic-22,'middle current')
            if b>=16 and b<bars-4:emit(3,t,[2,2],[1,2],inner_base-24,h,dynamic-20,'deep layer')
        elif p.style=='mirrors':
            emit(1,t,[.5]*6,[2,0,1,0,2,1],inner_base,h,dynamic-13,'contrary figure')
        elif p.style in ['ground','passacaglia','chaconne','lament']:
            if phase in [0,3]:
                ds=[barlen/2,barlen/2]
                emit(1,t,ds,[1,2],inner_base,h,dynamic-17,'ground variation')
            else:
                emit(1,t,[1]*int(barlen),[2,1,0,1],inner_base,h,dynamic-16,'inner continuation')
        else:
            pulse=1.5 if p.meter[1]==8 else 1
            emit(1,t,[pulse]*round(barlen/pulse),[1,2,0,1],inner_base,h,dynamic-15,'inner pulse')

        # Bass preserves the stated inversion; octave changes do not change it.
        bass_index=p.voices-1
        bass_target=34 if p.style in ['bells','threshold','passacaglia'] else 39
        bass=close_pc(h['bass_pc'],.65*previous_bass+.35*bass_target,26,52)
        previous_bass=bass
        if p.style in ['gigue','pastorale','mirrors','nine','mechanism']:
            pulse=1.5;count=round(barlen/pulse)
            for j in range(count):add(bass_index,t+j*pulse,pulse,bass+(12 if j%2 and phase==2 else 0),h,dynamic-9,'bass pulse')
        elif p.style=='clock':
            for at,d in [(0,1.5),(1.5,1),(2.5,1)]:add(bass_index,t+at,d,bass,h,dynamic-9,'3+2+2 bass')
        elif p.style=='sarabande':
            add(bass_index,t,1,bass,h,dynamic-8,'bass')
            add(bass_index,t+1,2,bass,h,dynamic-6,'second-beat weight')
        elif p.style in ['prisms','interleave']:
            add(bass_index,t,2,bass,h,dynamic-9,'bass span')
            add(bass_index,t+2,3,bass,h,dynamic-11,'bass span')
        else:add(bass_index,t,barlen,bass,h,dynamic-9,'ground' if p.style in ['ground','passacaglia','chaconne'] else 'bass span')

        # Explicit leading-note arrival in the last dominant bar.
        if b==bars-2 and h['roman']=='V':
            top_events=[e for e in voices[0]['events'] if t<=e['t']<t+barlen]
            if top_events:
                event=top_events[-1]
                leading=(key_pc(p.key)+11)%12
                event['p']=close_pc(leading,event['p'],60,100)
                event['spell']=h['spell'][leading]
                event['role']='leading-note cadence'

    for voice in voices:
        voice['events'].sort(key=lambda e:e['t'])
        voice['clef']='bass' if statistics.median(e['p'] for e in voice['events'])<60 else 'treble'
    metadata=dict(title='The Well-Tempered clAIvier',subtitle=f'{roman(p.number)}. Prelude in {key_name(p)}',
                  composer='ChatGPT / composed for Sam',instrument=f'Piano — {p.voices}-layer study score',
                  key=p.key,mode=p.mode,meter=list(p.meter),bpm=p.bpm,tempo_text=p.tempo,
                  movement_number=p.number,piece_type='prelude',character=p.character,draft=True,
                  markers=[dict(t=s['t'],label=s['label']) for s in sections],sections=sections,
                  composition_notes=[p.explanation,
                    'An original deterministic composition from movement-specific motives, harmonic plan and keyboard textures.',
                    'This free prelude is not a strict-species counterpoint exercise.',
                    'The printed study staves expose layers; two-hand playability was not a constraint.'])
    data=dict(metadata=metadata,voices=voices,
              pedagogy=dict(kind='free prelude',characteristic_figure=p.explanation,harmony=harmonic,
                            motifs=motif_events,sections=sections,
                            teaching_limits='Motive labels identify harmonically varied figures, not exact fugal subject statements.'),
              composition_record=dict(plan=p.__dict__,bars=bars,quarter_beats=total,
                                      duration_seconds=total*60/p.bpm))
    return data

def validate(data):
    errors=[];m=data['metadata'];barlen=m['meter'][0]*4/m['meter'][1]
    duration=data['composition_record']['quarter_beats']
    counts=[];neighbors=0;chord_notes=0
    for vi,v in enumerate(data['voices']):
        end=0
        for ei,e in enumerate(v['events']):
            if e['t']<end-1e-6:errors.append(['overlap',vi,e])
            if e['d']<=0 or e['t']<0 or e['t']+e['d']>duration+1e-6:errors.append(['duration',vi,e])
            if not 21<=e['p']<=108:errors.append(['outside_standard_piano_range',vi,e['t'],e['p']])
            if not 1<=e['v']<=127:errors.append(['velocity',vi,e])
            if abs(round(e['t']*4)-e['t']*4)>1e-6 or abs(round(e['d']*4)-e['d']*4)>1e-6:errors.append(['non_binary_grid',vi,e])
            if not e.get('spell'):errors.append(['missing_spelling',vi,e])
            else:
                name=e['spell'];natural=NATURALS[name[0].upper()]
                accidental=name[1:].count('is')-name[1:].count('es')
                if (natural+accidental)%12!=e['p']%12:errors.append(['spelling_pitch_mismatch',vi,e])
            h=data['pedagogy']['harmony'][min(len(data['pedagogy']['harmony'])-1,int(e['t']//barlen))]
            if e.get('role')=='returning neighbor':
                neighbors+=1
                if not 0<ei<len(v['events'])-1:errors.append(['neighbor_without_flanks',vi,e])
                else:
                    before,after=v['events'][ei-1],v['events'][ei+1]
                    if (before['p']!=after['p'] or not 1<=abs(e['p']-before['p'])<=2 or
                        abs(before['t']+before['d']-e['t'])>1e-6 or abs(e['t']+e['d']-after['t'])>1e-6 or
                        before['p']%12 not in h['pitch_classes']):
                        errors.append(['invalid_returning_neighbor',vi,e])
            else:
                chord_notes+=1
                if e['p']%12 not in h['pitch_classes']:errors.append(['nonornamental_nonchord_note',vi,e])
            end=e['t']+e['d']
        if abs(end-duration)>1e-6:errors.append(['missing_final_sonority',vi,end,duration])
        counts.append(len(v['events']))
    return dict(errors=errors,note_counts=counts,note_count=sum(counts),
                verified_chord_tone_events=chord_notes,verified_returning_neighbors=neighbors,
                pitch_ranges=[[min(e['p'] for e in v['events']),max(e['p'] for e in v['events'])] for v in data['voices']],
                bars=duration/barlen,duration_seconds=data['composition_record']['duration_seconds'],
                scope='event integrity, explicit spelling, duration, piano register, chord membership and returning-neighbor context; not a strict-counterpoint certificate')

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    summaries=[]
    for p in PLANS:
        data=make_score(p);review=validate(data)
        if review['errors']:raise ValueError((p.number,review['errors'][:6]))
        filename=f'{p.number:02d}-prelude.json'
        (OUT/filename).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
        summaries.append(dict(number=p.number,key=key_name(p),character=p.character,
                              filename=filename,style=p.style,meter=list(p.meter),bpm=p.bpm,
                              voices=p.voices,**review))
    accepted=ROOT/'work/prelude_iv.json'
    shutil.copyfile(accepted,OUT/'04-prelude.json')
    old=json.loads(accepted.read_text());end=max(e['t']+e['d'] for v in old['voices'] for e in v['events'])
    summaries.append(dict(number=4,key='C-sharp minor',character='Invocation and current',
                          filename='04-prelude.json',preserved_accepted_audition=True,
                          sha256=hashlib.sha256(accepted.read_bytes()).hexdigest(),
                          meter=[4,4],bpm=80,voices=3,bars=32,duration_seconds=end*60/80,
                          note_count=sum(len(v['events']) for v in old['voices'])))
    summaries.sort(key=lambda s:s['number'])
    report=dict(title='The Well-Tempered clAIvier — prelude cycle',status='24 working-draft preludes present; IV preserved',
                total_seconds=sum(s['duration_seconds'] for s in summaries),movements=summaries,
                method='Distinct specified tonal itineraries, motives, meter, texture and formal arcs. No random sampling.',
                limits='Generated event scores were reviewed symbolically. Artistic judgment still requires listening; no parity with Bach is claimed.')
    (OUT/'prelude-cycle-review.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'movements':24,'newly_composed':23,'accepted_IV_preserved':True,
                      'seconds':report['total_seconds'],'notes':sum(s['note_count'] for s in summaries),
                      'output':str(OUT)},indent=2))

if __name__=='__main__':main()
