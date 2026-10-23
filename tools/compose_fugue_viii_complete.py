#!/usr/bin/env python3
"""Fugue VIII: The procession finds a dance floor, complete formal version.

Literal phrases are composed in D and transposed a semitone into the cycle's
E-flat-minor slot. Thematic transposition/augmentation is explicit; there is
no chord-grid line insertion or frozen small-voice core.
"""
from pathlib import Path
import copy, hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from render_music import normalized_voices
OUT=ROOT/'work/fugue_viii_complete'
OLD=ROOT/'work/recomposition/nine_voice_experiment/nine-line-experiment.json'
old=json.loads(OLD.read_text())
voices=[{**{k:v for k,v in x.items() if k!='events'},'events':[]} for x in old['voices']]
base_velocity=[58,60,63,67,66,62,65,67,68]
phrases=[]; entries=[]; fragments=[]

THEMES={
 'chant':'F4:1.5 E4:.5 F4:1 D4:1 E4:.5 C4:.5 D4:1 D4:2',
 'dance':'D4:.5 E4:.5 F4:.5 A4:.75 G4:.25 F4:.5 D4:.5 A4:.5 r:.5 C5:.5 Bb4:.5 A4:.5 F4:.75 E4:.25 D4:.5 C4:.5',
 'bridge':'A3:1.5 D4:.5 E4:1 F4:1 A4:1.5 G4:.5 E4:1 C4:1',
 'major_chant':'F#4:1.5 E4:.5 F#4:1 D4:1 E4:.5 C#4:.5 D4:1 D4:2',
 'major_dance':'D4:.5 E4:.5 F#4:.5 A4:.75 G4:.25 F#4:.5 D4:.5 A4:.5 r:.5 C#5:.5 B4:.5 A4:.5 F#4:.75 E4:.25 D4:.5 C#4:.5',
 'major_bridge':'A3:1.5 D4:.5 E4:1 F#4:1 A4:1.5 G4:.5 E4:1 C#4:1',
 'altered_chant':'F4:1.5 Eb4:.5 F4:1 D4:1 Eb4:.5 C4:.5 D4:1 D4:2',
 'inverted_chant':'F4:1.5 G4:.5 F4:1 A4:1 G4:.5 Bb4:.5 A4:1 A4:2',
}

def parse(s):
    return [(p,float(d)) for p,d in (x.split(':') for x in s.replace('|',' ').split())]

def pitch(s):
    m=re.fullmatch(r'([A-G])([#b]?)(\d)',s)
    return 12*(int(m[3])+1)+dict(C=0,D=2,E=4,F=5,G=7,A=9,B=11)[m[1]]+{'':0,'#':1,'b':-1}[m[2]]

def lily(s):
    return s[0].lower()+('is' if '#' in s else 'es' if 'b' in s else '')

def default_spelling(p):
    return ['c','cis','d','ees','e','f','fis','g','gis','a','bes','b'][p%12]

def section_gain(t):
    if t<48:return -3
    if t<112:return 0
    if t<176:return -7
    if t<224:return 1
    if t<240:return 3
    if t<256:return -8
    if t<272:return -3+int((t-256)/4)
    if t<304:return 1
    if t<336:return 4
    if t<368:return 3
    if t<392:return 0
    return -2

def P(v,t,text,family='continuation',description='',length=None,gain=0,label=None,
      accent_origin=None,transpose=0,scale=1):
    parsed=parse(text); duration=sum(d for _,d in parsed)*scale
    if length is not None and abs(duration-length)>1e-8:
        raise ValueError((voices[v]['name'],t,description,duration,length))
    start=t; attack_origin=t if accent_origin is None else accent_origin
    sounding=[pitch(s)+transpose for s,d in parsed if s!='r']
    peak=max(sounding,default=60)
    for i,(s,d) in enumerate(parsed):
        d*=scale
        if s!='r':
            p=pitch(s)+transpose
            phase=round((t-attack_origin)%4,6)
            if 'dance' in family:
                accent=-3 if t<attack_origin else 5 if phase in (0,1.5,3) else -2
                gate=.77 if d<=.75 else .91
            elif 'chant' in family:
                accent=2 if i in (0,2) else 0;gate=.955
            else:
                accent=3 if p>=peak-2 else 0;gate=.94 if d<1 else .98
            event=dict(t=round(t,6),d=round(d,6),p=p,
                       spell=lily(s) if not transpose else default_spelling(p),
                       v=max(36,min(98,base_velocity[v]+gain+accent+section_gain(t))),
                       gate=gate,family=family,phrase_description=description,
                       source='Fugue VIII complete: literal phrase')
            if label and i==0:event['label']=label
            voices[v]['events'].append(event)
        t+=d
    phrases.append(dict(voice=v,t=start,d=duration,family=family,description=description))
    return t

def S(v,t,theme='chant',trans=0,scale=1,gain=2,label=None):
    P(v,t,THEMES[theme],theme,f'{theme.replace("_"," ")} statement',
      gain=gain,label=label,transpose=trans,scale=scale)
    entries.append(dict(voice=v,t=t,subject_id=theme,transpose=trans,scale=scale,
                        label=label or theme.replace('_',' ').capitalize()))

def H(v,t,trans=0,gain=3,major=False,label=None):
    key='major_dance' if major else 'dance'
    text=' '.join(THEMES[key].split()[:8])
    P(v,t,text,'dance-fragment','Dance head with its own accent origin',4,gain,label,
      transpose=trans)
    fragments.append(dict(voice=v,t=t,d=4,source_subject=key,
                          source_note_indices=list(range(8)),transpose=trans,
                          technique='Literal four-beat dance head'))

# I. EXPOSITION, bars 1-12. The ideas receive space before the first tutti.
S(5,0,'chant',-12,gain=5,label='Procession: chant')
P(5,8,'D3:2 F3:1 E3:1 C3:2 D3:1 F3:1 E3:2 C#3:1 A2:1',
  description='The horn continues through a twelve-beat descending answer',length=12)
S(1,8,'chant',7,gain=4,label='Answer toward the dominant')
S(4,8,'bridge',0,gain=0,label='Rising companion')
P(1,16,'A4:2 G4:1 F4:1 E4:1 F4:1 G4:2 F4:1 E4:1 D4:2',
  description='The answer opens into a twelve-beat arch and descent',length=12)
P(4,16,'B3:1 A3:1 G3:1 E3:1 F3:2 E3:1 D3:1',
  description='The companion turns downward while the oboe continues',length=8)
S(7,20,'chant',-24,gain=4,label='Chant below')
P(5,24,'A3:1.5 D4:.5 E4:1 F4:1 A3:2 G3:1 E3:1',
  'bridge','The opening horn adopts the rising companion',8)
H(3,26,12,gain=5,label='An interruption: dance head')
P(3,30,'C6:.5 Bb5:.5 A5:1 G5:.5 F5:.5 E5:1 F5:.5 E5:.5 D5:1',
  'dance-fragment','The interruption extends, then leaves a breathing space',6)
S(2,28,'chant',-5,gain=4,label='A lower answer')
P(7,28,'D2:1 F2:1 A2:1 G2:1 F2:1 E2:1 D2:1 C#2:1',
  description='The low chant continues toward the dominant',length=8)
P(4,28,'F3:2 A3:1 C4:1 D4:1 E4:1 F4:2 E4:1 D4:1 C4:1 B3:1',
  description='A sustained rise crosses the new answer and the dance',length=12)
S(6,34,'dance',-12,gain=4,label='The bassoon takes the dance')
S(0,36,'chant',12,gain=1,label='Chant above')
P(0,44,'F5:.5 E5:.5 D5:1 C#5:1 E5:1',description='A turn toward the first half cadence',length=4)
P(1,36,'D5:1.5 E5:.5 F5:1 A5:1 G5:2 F5:1 E5:1 D5:1 C#5:1 B4:1 A4:1',
  description='The oboe reaches up, then answers the low descending line',length=12)
P(2,36,'A3:1 C4:1 D4:1 E4:1 F4:1 E4:.5 D4:.5 C4:1 B3:1 A3:2 G3:1 E3:1',
  description='An independently paced continuation crosses the flute statement',length=12)
H(3,40,12,gain=1)
P(3,44,'E5:.5 F5:.5 G5:1 E5:1 C#5:1',description='The violin turns its head toward the cadence',length=4)
P(4,44,'A3:1 B3:.5 C#4:.5 D4:1 C#4:1',description='A suspended fourth resolves over the approaching dominant',length=4)
P(5,36,'G3:2 F3:1 E3:1 D3:2 F3:1 A3:1 G3:1 F3:1 E3:2',
  description='A broad horn descent maintains the old procession pace',length=12)
P(6,42,'D3:1 C3:.5 Bb2:.5 A2:1 C3:1 E3:1 A2:1',
  description='The dance tail closes into a six-beat dominant approach',length=6)
P(7,36,'D2:2 A2:1 C3:1 Bb2:2 A2:1 G2:1 F2:1 E2:1 C#2:1 A1:1',
  description='A long cello rise and fall supplies the first harmonic turn',length=12)
P(8,40,'A1:1.5 D2:.5 E2:1 F2:1 A2:1 G2:1 E2:1 A1:1',
  'bridge','The ninth voice bends the bridge into the half cadence',8,gain=1,label='Ninth voice: bent bridge')

# II. THE DANCE ARGUMENT, bars 13-28. Roles migrate; the full texture arrives
# in stages. The final eight beats point firmly toward the relative major.
P(0,56,'A5:1 C6:1 Bb5:1 A5:1 G5:1 F5:1 E5:2 D5:.5 E5:.5 F5:1 G5:1 A5:1',
  description='The flute answers the dance with an uneven twelve-beat fall and recovery',length=12)
S(0,72,'bridge',12,gain=0)
P(0,80,'D6:3 C6:1 Bb5:1 A5:1 G5:2 F5:1.5 E5:.5 D5:1 F5:1 A5:1 G5:1 E5:1 C#5:1',
  description='A long upper descent crosses the lower chant entrances',length=16)
H(0,96,15,gain=2,major=True,label='A brighter dance head')
P(0,100,'Bb5:1 A5:.5 G5:.5 F5:1 E5:1 G5:1 Bb5:1 A5:1 G5:1 E5:1 D5:1 C5:2',
  description='The high phrase settles toward the new dominant',length=12)
P(1,48,'F5:2 E5:1 D5:1 C5:2 D5:1 E5:1 F5:1 G5:1 A5:2',
  description='The oboe keeps a broad sentence while the first dance statements run',length=12)
P(1,64,'A4:1.5 D5:.5 E5:1 F5:1 A5:1 G5:.5 F5:.5 E5:1 D5:1 C5:2 B4:1 A4:1',
  'bridge','A bridge expands to twelve beats and crosses the violin chant',12)
S(1,76,'dance',7,gain=3,label='Dance on the dominant')
P(1,84,'E5:1 F5:1 G5:1 A5:1 C6:2 Bb5:1 A5:1 G5:1 F5:1 E5:1 C5:1',
  description='The fast statement opens into a new long arc',length=12)
S(1,96,'major_chant',3,gain=2,label='The chant opens toward the relative major')
P(1,104,'E4:1 F4:1 G4:1 A4:1 Bb4:1 A4:1 G4:1 E4:1',
  description='The oboe reaches the leading note of the relative-major cadence',length=8)
S(2,48,'dance',0,gain=4,label='Dance in the clarinet')
P(2,56,'A3:1 C4:.5 D4:.5 E4:1 F4:1 G4:2 F4:1 E4:1 D4:2 C4:1 B3:1',
  description='The clarinet stretches its dance tail into a twelve-beat descent',length=12)
P(2,72,'C4:2 D4:1 E4:1 G4:1 F4:.5 E4:.5 D4:1 C4:1',
  description='An independent rise answers the viola entry',length=8)
P(2,80,'B3:1 C4:1 D4:2 E4:1 F4:1 A4:2 G4:1 E4:1 F4:.5 E4:.5 D4:1',
  description='The clarinet climbs against the flute descent',length=12)
P(2,92,'C#4:1 D4:1 E4:1 F4:1 G4:1 A4:1 Bb4:1 A4:1 G4:2 F4:1 E4:1',
  description='A twelve-beat ascent and recoil reaches the next cadence',length=12)
P(2,104,'D4:1 E4:1 F4:1 G4:1 E4:1 D4:1 C4:1 Bb3:1',
  description='The clarinet supplies a descending seventh into the dominant',length=8)
S(3,48,'dance',12,gain=4,label='The dance takes hold')
P(3,56,'D5:.5 F5:.5 A5:1 G5:.5 F5:.5 E5:1 D5:1 C5:1 B4:1 A4:1',
  'dance-fragment','The violin lengthens the dance before taking the chant',8)
S(3,64,'chant',12,gain=3,label='The dancer adopts the chant')
P(3,72,'D5:1 F5:1 A5:2 G5:1 F5:.5 E5:.5 D5:1 C5:1 Bb4:1 A4:1 G4:1 F4:1',
  description='A twelve-beat violin descent overlaps the next head',length=12)
H(3,84,0,gain=2)
P(3,88,'E5:.5 D5:.5 C5:1 Bb4:1 A4:1 G4:.5 A4:.5 Bb4:1 C5:1 D5:1',
  description='The head turns upward after a falling continuation',length=8)
P(3,96,'C5:2 A4:1 F4:1 G4:1 A4:1 Bb4:2 A4:1 G4:1 F4:2 E4:1 G4:1 Bb4:1 C5:1',
  description='A new sixteen-beat violin arch spans the relative-major approach',length=16)
S(4,56,'bridge',0,gain=0)
P(4,64,'Bb3:1 A3:1 G3:1 F3:1 E3:1 F3:1 G3:1 A3:1',
  description='The viola bends downward and then rises toward its chant',length=8)
S(4,72,'chant',0,gain=3,label='The chant in the inner strings')
P(4,80,'C4:1 D4:1 E4:1 F4:1 G4:2 F4:1 E4:1 D4:1 C4:1 Bb3:1 A3:1',
  description='The inner phrase takes a different twelve-beat route',length=12)
H(4,92,3,gain=1,major=True)
P(4,96,'A4:1 G4:1 F4:2 E4:1 D4:1 C4:2 Bb3:1 A3:1 G3:2 C4:1 D4:1 E4:1 G4:1',
  description='The viola descends while the upper voices announce a brighter turn',length=16)
P(5,56,'D3:3 F3:1 E3:2 C3:2 D3:1 E3:1 F3:2 G3:1 A3:1 G3:1 E3:1',
  description='The horn remembers the procession across four bars',length=16)
H(5,72,-12,gain=4,label='The horn learns the dance')
P(5,76,'F3:1 E3:.5 D3:.5 C3:1 D3:1 F3:2 A3:1 G3:1 F3:1 E3:1 D3:2',
  description='The horn head becomes a broad independent continuation',length=12)
P(5,88,'A2:2 C3:1 E3:1 G3:1 F3:1 E3:1 C#3:1',
  description='The lower horn arch points briefly back to the tonic',length=8)
P(5,96,'D3:2 F3:1 A3:1 G3:2 F3:2 E3:1 F3:1 G3:2 C4:1 Bb3:1 A3:1 G3:1',
  description='The broad line continues through the relative-major turn',length=16)
S(6,48,'bridge',-12,gain=0)
P(6,60,'D3:.5 E3:.5 F3:1 A3:1 C4:1 Bb3:1 A3:1 G3:.5 F3:.5 E3:1 D3:1 C3:1 Bb2:1 A2:1',
  'dance-fragment','A pickup turns the bassoon into a twelve-beat answer',12)
P(6,72,'F3:1 E3:1 D3:2 C3:1 D3:1 E3:1 G3:1',
  description='The bassoon descent has its own pace beneath the new entries',length=8)
P(6,80,'A3:2 G3:1 F3:1 E3:1 D3:1 C3:1 B2:1 A2:2 D3:1 E3:1',
  description='A long fall creates room for the bass chant',length=12)
S(6,92,'chant',-12,gain=3,label='The dance yields to a lower chant')
P(6,100,'F3:1 A3:1 C4:1 Bb3:1 A3:1 G3:1 F3:2 E3:1 D3:1 C3:2',
  description='The bassoon carries a twelve-beat route into the new dominant',length=12)
P(7,48,'D2:2 F2:1 A2:1 Bb2:1 A2:1 G2:1 F2:1',
  description='The cello answers the first half cadence',length=8)
S(7,56,'dance',-12,gain=3,label='The cello takes the quick material')
P(7,64,'E3:.5 F3:.5 G3:1 A3:1 G3:1 F3:2 E3:1 D3:1 C3:1 Bb2:1 A2:2',
  description='The cello dance opens into a twelve-beat descent',length=12)
P(7,76,'G2:1 A2:1 Bb2:2 C3:1 D3:1 E3:1 F3:1 C3:1 F3:1 E3:1 A2:1',
  description='A second long arch rises under the bass chant',length=12)
H(7,88,-24,gain=1)
P(7,92,'F2:1.5 A2:.5 C3:1 D3:1 E3:.5 F3:.5 G3:1 A3:3 G3:.5 F3:.5 E3:1 C3:1',
  description='The cello enlarges the head into an extended ascent',length=12)
P(7,104,'A2:1 Bb2:1 C3:1 D3:1 E3:1 G3:1 F3:1 E3:1',
  description='The cello approaches the new tonic through its leading note',length=8)
P(8,48,'D2:2 A1:1 D2:1 F2:2 E2:1 C2:1',
  description='The ninth voice continues after the first cadence, then breathes',length=8)
P(8,64,'D2:2 F2:1 E2:1 D2:2 C2:1 A1:1 Bb1:2 D2:1 F2:1 E2:1 D2:1 C#2:1 A1:1',
  description='A low sixteen-beat route prepares a thematic bass entrance',length=16)
S(8,80,'chant',-24,gain=4,label='The chant reaches the ninth voice')
P(8,88,'D2:1 E2:1 F2:1 A2:1 G2:1 F2:1 E2:1 C#2:1 D2:2 F2:1 E2:1 C2:2 G1:1 Bb1:1',
  description='The bass moves through tonic, its dominant, and toward the relative major',length=16)
P(8,104,'A1:1 Bb1:1 C2:2 G1:1 Bb1:1 C2:2',
  description='The bass establishes the new dominant for the opening room',length=8)

# III. A ROOM OPENS, bars 29-44. Relative-major warmth, silence between
# players, and phrases of three, four and five bars change the time scale.
S(1,112,'major_chant',3,gain=3,label='A warmer memory of the chant')
P(1,124,'G4:1 A4:1 Bb4:2 A4:1 G4:1 F4:2 E4:1 F4:1 G4:1 A4:1',
  description='The oboe answers after a complete bar of breath',length=12)
P(1,144,'D5:2 C5:1 Bb4:1 A4:2 G4:1 F4:1 E4:1 F4:1 G4:2',
  description='A broad descending oboe line opens the subdominant space',length=12)
H(1,156,5,gain=-1,label='A quiet dance memory')
P(1,160,'C5:2 Bb4:1 A4:1 G4:2 F4:1 E4:1 D4:1 F4:1 A4:1 G4:1 F4:1 E4:1 C#4:1 E4:1',
  description='The warm phrase bends back toward the minor dominant',length=16)
P(2,112,'A3:2 C4:2 D4:1 E4:1 F4:2 E4:1 D4:1 C4:2',
  description='The clarinet receives the cadence and rises through a new twelve-beat line',length=12)
S(2,124,'major_bridge',3,gain=-1,label='The rising idea opens out')
P(2,132,'F4:1 E4:.5 D4:.5 C4:2 Bb3:1 A3:1 G3:2',
  description='The long rise releases into a quiet descent',length=8)
S(2,148,'major_bridge',-4,gain=-1)
P(2,156,'Bb3:2 A3:1 G3:1 F3:1 G3:1 A3:1 C4:1',
  description='The clarinet falls, then answers the short dance memory',length=8)
P(2,168,'G3:2 A3:1 Bb3:1 A3:1 G3:1 E3:1 A3:1',
  description='A low clarinet arc gathers on the dominant',length=8)
S(3,128,'major_chant',15,gain=1,label='The warm chant changes register')
P(3,136,'E5:1 D5:1 C5:1 A4:1 G4:2 F4:2',
  description='The violin continues downward, then leaves the room open',length=8)
P(3,152,'D5:1 C5:1 Bb4:2 A4:1 G4:1 F4:2 Eb4:1 F4:1 G4:1 A4:1',
  description='The violin follows a separate twelve-beat curve below its previous statement',length=12)
H(3,164,0,gain=-1)
P(3,168,'C5:1 Bb4:1 A4:2 G4:1 F4:1 E4:1 C#4:1',
  description='The violin dance tail points to the minor return',length=8)
P(4,120,'C4:3 D4:1 E4:2 F4:2 G4:1 F4:1 E4:1 D4:1 C4:2 A3:1 F3:1',
  description='An unhurried inner arch crosses both upper statements',length=16)
S(4,136,'major_chant',-4,gain=2,label='The chant moves to the subdominant')
P(4,148,'F3:2 A3:1 Bb3:1 C4:1 D4:1 Eb4:2 D4:1 C4:1 Bb3:1 A3:1',
  description='A twelve-beat viola arch gathers a new flat into the harmony',length=12)
P(4,160,'G3:2 Bb3:1 D4:1 C4:2 Bb3:1 A3:1 G3:1 F3:1 E3:1 D3:1 C#3:1 E3:1 G3:1 A3:1',
  description='The inner descent carries the route through the minor subdominant',length=16)
P(5,128,'F3:2 A3:1 C4:1 Bb3:2 A3:2 G3:1 F3:1 E3:1 C3:1',
  description='A twelve-beat horn sentence accompanies the high chant',length=12)
P(5,144,'Bb2:2 D3:1 F3:1 Eb3:2 D3:1 C3:1 Bb2:1 A2:1 G2:2',
  description='The horn descends through the new subdominant space',length=12)
P(5,156,'A2:2 C3:1 D3:1 E3:2 F3:1 E3:1 D3:2 C#3:1 A2:1',
  description='The low horn line turns the harmony back toward the opening key',length=12)
P(5,172,'A3:1 G3:1 E3:1 C#3:1',
  description='A short dominant answer enters after a bar of silence',length=4)
P(6,112,'F3:2 C3:1 A2:1',description='A brief bassoon arrival, then silence',length=4,gain=-3)
P(6,132,'F3:1 G3:1 A3:2 C4:1 Bb3:1 A3:2 G3:1 F3:1 Eb3:1 D3:1',
  description='The bassoon rises while the clarinet descends',length=12)
S(6,144,'major_chant',-16,gain=1,label='The lower warm chant')
P(6,160,'Bb2:2 A2:1 G2:1 F2:2 G2:1 A2:1 Bb2:1 C3:1 D3:1 E3:1 F3:1 E3:1 D3:1 C#3:1',
  description='The bassoon descent reverses into a long dominant approach',length=16)
P(7,112,'F3:3 E3:1 D3:2 C3:2 Bb2:3 A2:1 G2:2 C3:2',
  description='A long cello descent gives the newly opened room a lower melody',length=16,gain=1)
P(7,132,'F2:2 A2:1 C3:1 D3:2 E3:1 F3:1 G3:1 F3:1 Eb3:1 D3:1',
  description='The cello begins a new phrase after a bar of breath',length=12)
S(7,152,'major_chant',-16,gain=2,label='The chant passes into the cello')
P(7,160,'A2:1 G2:1 F2:2 G2:1 A2:1 Bb2:2 C3:1 D3:1 E3:1 F3:1 E3:1 D3:1 C#3:1 A2:1',
  description='The cello rises through the recovering minor harmony',length=16)
P(8,112,'F1:2 C2:1 F2:1',description='The bass names the arrival, then gives space',length=4,gain=-3)
P(8,128,'F2:2 E2:1 D2:1 C2:2 Bb1:2 A1:1 Bb1:1 C2:2',
  description='A quiet bass melody traces the relative-major area',length=12)
P(8,144,'Bb1:2 F2:1 D2:1 Eb2:2 D2:1 C2:1',
  description='The bass opens the subdominant region',length=8)
P(8,156,'Bb1:2 D2:1 F2:1 G2:2 F2:1 Eb2:1 D2:2 C2:1 Bb1:1 A1:2 E2:1 G2:1 F2:1 E2:1 C#2:1 A1:1',
  description='A five-bar bass route crosses the other phrase endings and reaches the dominant',length=20)
S(0,144,'major_chant',8,gain=-1,label='A low flute memory')
P(0,152,'A4:1 Bb4:1 C5:1 D5:1 F5:2 Eb5:1 D5:1 C5:1 Bb4:1 A4:1 F4:1',
  description='The flute opens its warm chant into a new arch',length=12)
P(0,168,'E5:1 F5:1 G5:2 F5:1 E5:1 D5:1 C#5:1',
  description='The flute leaves its silence with a dominant-pointing descent',length=8)

# IV. THE GROUND SHIFTS, bars 45-60. Three displaced semitone slips disturb
# the recovered tonic. The hurried chant and the low dance chase wait until
# beat 208; the two arguments then pursue different continuations.
P(0,176,'D5:2 A5:1 F5:1 E5:1 Eb5:1 D5:2 C5:1 D5:.5 Eb5:.5 F5:1 A5:1 G5:2 F5:1 Eb5:1',
  description='The flute receives the tonic, then catches the chromatic disturbance',length=16)
P(0,200,'F5:1.5 Eb5:.5 D5:1 C5:1 Bb4:1 A4:1 G4:1 A4:1',
  description='A quiet upper recollection precedes the sudden hurry',length=8)
S(0,208,'chant',12,scale=.5,gain=5,label='The procession suddenly hurries')
P(0,212,'F5:.5 A5:.5 G5:1 E5:.5 D5:.5 C5:1 Bb4:1 D5:.5 F5:.5 A5:2 G5:1 F5:1 E5:1 D5:1',
  'dance-fragment','The hurried chant breaks into a new twelve-beat flight',12,gain=2)
S(0,224,'inverted_chant',12,gain=2,label='The chant turns upward')
P(0,232,'G5:2 F5:1 E5:1 D5:.5 C#5:.5 B4:1 C#5:1 E5:1',
  description='The upper inversion descends to the dominant',length=8)
S(1,180,'altered_chant',0,gain=2,label='The disturbed chant answers late')
P(1,188,'F4:.5 G4:.5 A4:1 C5:1 Bb4:1 A4:1 G4:1 F4:1 Eb4:1 D4:2 C4:1 A3:1',
  description='A twelve-beat oboe line moves through the flattened note and out of it',length=12)
P(1,200,'D4:1 F4:.5 A4:.5 G4:1 F4:1 E4:.5 F4:.5 G4:1 A4:2 C5:1 Bb4:1 A4:1 G4:1',
  description='The oboe keeps its own longer phrase as the upper chase begins',length=12)
S(1,212,'chant',7,scale=.5,gain=4,label='A hurried dominant answer')
P(1,216,'A4:1.5 C5:.5 E5:1 G5:1 F5:1 E5:.5 D5:.5 C5:1 B4:1 A4:2 G4:1 F4:1',
  description='The oboe answer rises above the chase, then crosses its next boundary',length=12)
P(1,228,'E4:1 G4:1 Bb4:2 A4:1 G4:1 F4:1 E4:1 D4:1 C#4:1 B3:1 A3:1',
  description='A twelve-beat descent prepares the sudden retreat',length=12)
P(2,176,'F4:2 A4:1 G4:1 F4:.5 Eb4:.5 D4:1 C4:2 Bb3:1 C4:.5 D4:.5 Eb4:1 F4:1',
  description='The clarinet rises against the first semitone cascade',length=12)
S(2,192,'altered_chant',-12,gain=1,label='The disturbed chant in the middle register')
P(2,200,'D3:1 A3:.5 C4:.5 Eb4:1 D4:1 C4:1 Bb3:1 A3:1 G3:1',
  description='A low clarinet arc descends as the violin prepares its interruption',length=8)
P(2,208,'F3:1 A3:1 C4:1 D4:1',description='The clarinet keeps a spacious ascent inside the hurry',length=4)
S(2,212,'bridge',0,gain=0,label='The broad rising idea resists the chase')
P(2,220,'Bb3:1 A3:.5 G3:.5 F3:2 G3:.5 A3:.5 Bb3:1 D4:2 C4:1 Bb3:1 A3:1 G3:1',
  description='A displaced inner arch spans the start of the inversion',length=12)
P(2,232,'E3:1 G3:1 A3:1 C#4:1 D4:1 C#4:1 B3:1 G3:1',
  description='The clarinet leaves a dominant seventh to resolve after the cut',length=8)
P(3,176,'A4:3 G4:1 F4:.5 G4:.5 A4:1 C5:1 Bb4:1 A4:2 G4:1 F4:1 Eb4:2 D4:1 C4:1 D4:.5 Eb4:.5 F4:1 A4:1 G4:1',
  description='A five-bar violin sentence crosses the chromatic entries without copying them',length=20)
H(3,200,0,gain=1,label='The violin remembers the dance head')
P(3,204,'C5:.5 Bb4:.5 A4:1 G4:.5 F4:.5 E4:1 D4:1',
  'dance-fragment','A five-beat tail delays the next chant entrance',5)
S(3,209,'chant',0,scale=.5,gain=5,label='The hurried chant follows one beat later')
P(3,213,'F4:.5 G4:.5 A4:1 C5:1 E5:1 D5:1 C5:.5 Bb4:.5 A4:2 G4:1 F4:1 E4:1 D4:1',
  description='The violin chase becomes an independent twelve-beat ascent and return',length=12)
P(3,225,'Bb4:1 A4:1 G4:2 F4:1 E4:.5 D4:.5 C4:1 Bb3:1 A3:1 C#4:1 E4:1 G4:1',
  description='The violin starts its dominant route one beat after the upper inversion',length=12)
P(3,237,'F4:.5 E4:.5 D4:1 C#4:1',description='A short leading-note tail tightens the retreat',length=3)
P(4,176,'E4:1 Eb4:1 D4:1 C4:1 Bb3:.5 C4:.5 D4:.5 Eb4:.5 F4:1 Eb4:1',
  'chromatic-exchange','First chromatic semitone slip, in the viola',8,gain=3,label='The floor slips: first voice')
S(4,184,'altered_chant',0,gain=2,label='The chant absorbs the flattened note')
P(4,192,'A3:1.5 C4:.5 D4:1 Eb4:1 F4:2 Eb4:1 D4:1 C4:1 Bb3:1 A3:1 F3:1',
  description='A displaced viola arch spans the lower chant answer',length=12)
P(4,204,'G3:2.5 A3:.5 Bb3:1 D4:1 C4:1 A3:1 F3:1 E3:1 F3:.5 G3:.5 A3:2 C4:1 Bb3:1 A3:1 G3:1',
  description='The viola maintains a long irregular sentence beneath the short chase heads',length=16)
H(4,220,-7,gain=2,label='The dance head moves to the subdominant')
P(4,224,'F4:2 Eb4:1 D4:1 C4:1 Bb3:.5 A3:.5 G3:2 A3:1 C#4:1 E4:2 G4:1 F4:1 E4:1 C#4:1',
  description='The viola closes the disturbed region through a directed dominant rise',length=16)
P(5,176,'F3:1.5 E3:.5 Eb3:1 D3:1 C3:1 D3:1 F3:1 A3:1 G3:1 F3:1 Eb3:1 D3:1',
  'chromatic-exchange','Second semitone slip follows in the horn, then grows into twelve beats',12,gain=2,label='The floor slips: second voice')
P(5,192,'Bb2:3 A2:1 G2:2 F2:2 Eb3:1 D3:1 C3:1 D3:1 F3:1 G3:1 A3:1 C4:1',
  description='A broad horn descent and recovery takes a different pace',length=16)
H(5,208,-12,gain=5,label='Low chase: horn')
P(5,212,'F3:1 E3:.5 D3:.5 C3:1 D3:1 F3:2 A3:1 G3:1 F3:1 G3:1 A3:1 Bb3:1 D4:1 C4:1 Bb3:1 A3:1',
  description='The horn leaves the shared head for its own four-bar rising continuation',length=16)
P(5,228,'G3:2 E3:1 G3:1 Bb3:1 A3:1 G3:1 F3:1 E3:2 C#3:1 A2:1',
  description='The horn falls into the dominant while the bassoon answers above it',length=12)
P(6,176,'A2:.5 G2:.5 F2:1 E2:1 Eb2:1 D2:.5 C3:.5 Bb2:.5 A2:.5 G2:1 A2:1',
  'chromatic-exchange','Third semitone slip follows in the bassoon a register below the horn',8,gain=3,label='The floor slips: third voice')
P(6,184,'Bb2:1 D3:1 F3:2 Eb3:1 D3:1 C3:1 Bb2:1 A2:1 C3:1 D3:1 Eb3:1',
  description='The low disturbance becomes a twelve-beat answering arch',length=12)
H(6,196,-7,gain=1)
P(6,200,'D4:.5 C4:.5 Bb3:1 A3:1 G3:1 F3:1 Eb3:1 D3:1 C3:1',
  description='The bassoon descends while the upper dancer begins again',length=8)
P(6,208,'Bb2:1 D3:1 F3:1 A3:1 G3:1 F3:.5 E3:.5 D3:2 C3:1 D3:1 E3:1 F3:1 A3:1 G3:1 F3:1 E3:1',
  description='The bassoon keeps an independent broad arch around the three-part low chase',length=16)
P(6,224,'G2:1 Bb2:1',description='A two-beat pickup delays the lower inversion',length=2)
S(6,226,'inverted_chant',-12,gain=3,label='The lower inversion answers two beats later')
P(6,234,'G3:1 F3:1 E3:1 D3:1 C#3:1 A2:1',
  description='The bassoon inversion contracts into the cadence',length=6)
P(7,176,'D3:3 C3:1 Bb2:2 A2:2 G2:1 Bb2:1 C3:1 Eb3:1 D3:2 C3:1 Bb2:1',
  description='The cello receives the tonic and moves beneath the chromatic exchange',length=16)
S(7,192,'altered_chant',-24,gain=2,label='A low disturbed memory')
P(7,200,'G2:1 A2:.5 Bb2:.5 C3:1 D3:1 Eb3:2 D3:1 C3:1 Bb2:1 A2:1',
  description='A ten-beat cello arch delays its dance entrance',length=10)
H(7,210,-12,gain=5,label='Low chase: cello')
P(7,214,'C3:.5 D3:.5 E3:1 F3:1 G3:1 A3:1 G3:.5 F3:.5 E3:1 D3:1 C3:1 Bb2:1',
  description='The cello leaves the head with an ascent distinct from horn and bass',length=10)
P(7,224,'G2:1 A2:.5 Bb2:.5 C3:1 D3:1 C3:2 Bb2:1 G2:1 E2:1 G2:1 Bb2:2 A2:1 G2:1 E2:1 C#2:1',
  description='The cello turns the pursuit through subdominant and dominant',length=16)
P(8,176,'D2:2 A1:1 D2:1 F2:1 Eb2:1 D2:2 C2:2 Bb1:1 C2:1 Eb2:1 D2:1 C2:1 Bb1:1',
  description='The bass names the recovered tonic before yielding to the chromatic descent',length=16)
P(8,192,'G1:2 D2:1 F2:1 Eb2:2 D2:1 C2:1 Bb1:2 A1:1 G1:1 A1:2 C2:1 E2:1 A1:1',
  description='A seventeen-beat bass route crosses the coming chase boundary',length=17)
H(8,209,-24,gain=5,label='Low chase: bass')
P(8,213,'G2:1 F2:.5 E2:.5 D2:2 C2:1 A1:1 Bb1:1 D2:1 F2:1 E2:1 D2:1',
  description='The bass head continues through an eleven-beat falling and rising route',length=11)
P(8,224,'G1:2 Bb1:1 D2:1 E2:2 G2:1 Bb2:1 A1:2 E2:1 G2:1 F2:1 E2:1 C#2:1 A1:1',
  description='The bass turns the minor subdominant through the half-diminished chord into the dominant',length=16)

# V. ONLY A MEMORY, bars 61-68. The cello takes twice the original time;
# the opening resolution is brief and the answering phrases leave real air.
P(2,240,'F3:2',description='The clarinet seventh resolves as the ensemble falls away',length=2,gain=-3)
P(3,240,'D4:4',description='The violin leading note reaches the quiet tonic',length=4,gain=-4)
P(7,240,'D2:2',description='The cello resolves the low leading note before remembering the chant',length=2,gain=-1)
S(7,242,'chant',-12,scale=2,gain=3,label='The chant takes twice the time')
P(1,244,'A4:2 G4:1 F4:1 E4:2 D4:2',
  description='A quiet eight-beat reply leaves space around the augmented chant',length=8,gain=-2)
P(2,248,'A3:1 C4:1 D4:2 C4:1 Bb3:1 A3:1 G3:1',
  description='The clarinet answers midway through the long cello sentence',length=8,gain=-2)
P(0,252,'A4:1.5 G4:.5 F4:1 E4:1 D4:2',
  description='A six-beat flute recollection overlaps only the end of the cello chant',length=6,gain=-3)
P(7,258,'D3:2 F3:1 A3:1 G3:2 F3:1 E3:1 D3:1 C3:1 Bb2:1 G2:1 A2:1 C#3:1',
  description='The cello continues for fourteen beats toward a new dominant gathering',length=14,gain=0)
P(4,258,'G3:3 Bb3:1 D4:2 C4:1 Bb3:1 A3:1 G3:1 F3:1 E3:1',
  description='The viola reenters with a spacious subdominant arch',length=12,gain=-1)
P(1,260,'D4:2 F4:1 E4:1 D4:1 C4:1 Bb3:2 A3:1 C#4:1 E4:1 G4:1',
  description='A twelve-beat oboe answer gradually recovers the leading note',length=12)
P(2,260,'Bb3:2 A3:1 G3:1 F3:1 G3:.5 A3:.5 Bb3:1 D4:1',
  description='The clarinet moves against the quiet oboe ascent',length=8,gain=-1)
P(5,264,'G2:2 Bb2:1 D3:1 E3:1 G3:1 C#3:1 A2:1',
  description='The horn returns only when the harmonic route begins to tighten',length=8,gain=-1)
P(8,264,'G1:3 D2:1 C2:1 Bb1:1 A1:2',
  description='The bass enters late and turns the subdominant toward the dominant',length=8,gain=-1)
P(3,264,'Bb4:2 A4:1 G4:1 F4:1 E4:.5 D4:.5 C4:1 Bb3:1 A3:1 B3:1 C4:1 D4:1',
  description='A three-bar violin line crosses the beginning of the gathering',length=12)

# VI. GATHERING, bars 69-72. Motion earns the pedal. The bass walks for two
# bars; the sustained dominant appears only in the second half of the build.
P(8,272,'E2:1 F2:1 G2:1 E2:1 A1:1 G1:1 A1:2',
  description='The bass walks toward the dominant before becoming a pedal',length=8,gain=1)
P(8,280,'A1:8',description='The eight-beat dominant pedal supports moving upper lines',length=8,gain=2)
P(7,272,'D3:1 C3:1 Bb2:1 G2:1 A2:2 C#3:1 E3:1 G3:2 F3:1 E3:1 D3:1 C#3:1 B2:1 A2:1',
  description='The cello crosses the changing bass route with its own rise and fall',length=16)
P(2,272,'G3:2 Bb3:1 D4:1 C4:1 Bb3:1 A3:2 G3:1 E3:1 C#3:1 E3:1',
  description='The clarinet gathers, descends, and leaves room for the premature bridge',length=12)
S(2,284,'bridge',0,gain=2,label='The rising idea anticipates the return')
P(5,272,'C3:2 Bb2:1 G2:1 A2:1 C#3:1 E3:1 G3:1',
  description='The horn turns its minor memory into a dominant ascent',length=8)
P(5,284,'A3:1 G3:1 F3:1 E3:1 D3:2 F3:1 A3:1',
  description='The horn descent crosses the return without restarting at the boundary',length=8,gain=1)
P(4,272,'G3:1 A3:.5 Bb3:.5 C4:1 D4:1 E4:1 D4:1 C#4:1 A3:1',
  description='The inner strings answer the walking bass with an opposing arch',length=8)
P(4,280,'Bb3:2 A3:1 G3:1 F3:1 E3:1 D3:1 C#3:1',
  description='A prepared flattened ninth falls through a dominant-pointing descent',length=8)
P(1,272,'F4:2 E4:1 D4:1',description='The oboe resolves its previous seventh, then turns toward the dance',length=4)
H(1,276,7,gain=3,major=True,label='The dance urges the dominant onward')
P(1,280,'G5:1 F5:1 E5:2 D5:1 C#5:1 B4:1 A4:1',
  description='The oboe head opens into a descending dominant sentence',length=8)
P(0,274,'Bb4:1 A4:1 G4:2 E4:1 F4:1 G4:1 A4:1',
  description='A delayed flute reentry grows without immediately filling the texture',length=8)
P(0,284,'Bb4:1 A4:1 G4:1 E4:1',description='A short high answer increases the dominant pressure',length=4)
P(3,276,'C#5:1.5 E5:.5 G5:1 Bb5:1 A5:2 G5:1 F5:1 E5:1 D5:1 C#5:2',
  description='The violin reaches the dominant ninth and resolves its long suspension',length=12,gain=2)
P(6,276,'E3:1 G3:1 A3:2 C#4:1 E4:1.5 D4:.5 C#4:1 A3:1 B3:.5 C#4:.5 E4:1 C#4:1',
  description='The bassoon reappears late, sustaining and turning above the inner descent',length=12,gain=1)

# VII. RETURN IN PURSUIT, bars 73-84. The return has crossing phrase lengths,
# delayed chant entries and a moving bass. A single horn line introduces the
# raised third before the major signature; the change is earned melodically.
P(0,288,'A5:1.5 G5:.5 F5:1 E5:1 D5:2 E5:1 F5:1 A5:1 C6:1 Bb5:1 A5:1',
  description='The flute answers the returning chant with a separate twelve-beat arch',length=12,gain=1)
S(0,304,'inverted_chant',12,gain=2,label='The upper chant opens upward again')
P(0,312,'D6:1.5 C6:.5 Bb5:1 A5:1 G5:1 F5:1 E5:2 D5:1 E5:1 F5:1 G5:1',
  description='The inverted chant releases through a suspended upper descent',length=12)
P(0,324,'E5:2 C#5:1 A4:1 D5:3 E5:1 F5:1 E5:1 D5:2 E5:1 F#5:1 A5:1 G5:1',
  description='A four-bar flute sentence crosses the major turn instead of restarting there',length=16)
P(1,288,'D5:3 E5:1 F5:1 A5:.5 G5:.5 F5:1 E5:1 D5:1 C5:1 Bb4:1 A4:1',
  description='The oboe receives the tonic and descends against the violin chant',length=12)
S(1,300,'chant',0,gain=3,label='The chant returns inside the ensemble')
P(1,308,'G4:.5 A4:.5 Bb4:1 D5:2 C5:1 Bb4:.5 A4:.5 G4:1 F4:1 E4:1 D4:1 C#4:1 E4:1',
  description='The oboe line changes direction while the lower statements continue',length=12)
H(1,320,7,gain=3,major=True,label='The dominant dance head returns')
P(1,324,'G5:1 F5:1 E5:2 D5:1 F5:.5 A5:.5 G5:1 F5:1 E5:1 D5:1 C#5:1 E5:1',
  description='The oboe folds its head through a new twelve-beat approach to the major third',length=12)
P(2,292,'D4:1.5 C4:.5 Bb3:1 A3:1 G3:2 F3:1 E3:1 D3:1 F3:.5 A3:.5 C4:1 D4:1 Eb4:1 D4:1 C4:1 Bb3:1',
  description='The clarinet bridge unfolds downward and then rises across the subdominant turn',length=16)
S(2,312,'chant',-5,gain=2,label='A lower answer inside the return')
P(2,320,'G3:1 A3:1 C#4:1 E4:1 G4:1 F4:.5 E4:.5 D4:2 C#4:1 D4:1 E4:1 G4:1',
  description='A delayed clarinet ascent crosses the returning minor tonic',length=12)
P(2,332,'F4:1 E4:1 D4:2 C#4:1 E4:1 F#4:2 G4:1 F#4:1 E4:1 D4:1',
  description='The clarinet sheds its minor third gradually through the key change',length=12)
S(3,288,'chant',12,gain=4,label='The chant returns in the violin')
H(3,298,12,gain=3,label='A dance head interrupts after a breath')
P(3,302,'F5:.5 G5:.5 A5:1 C6:1 Bb5:1 A5:1.5 G5:.5 F5:1 Eb5:1 D5:2 F5:1 A5:1 G5:1 F5:.5 E5:.5 D5:1 C#5:1',
  description='A four-bar violin flight crosses both inner chant entries',length=16)
P(3,318,'E5:1.5 G5:.5 Bb5:1 A5:1 G5:2 F5:1 E5:1 D5:1 C#5:1 B4:1 A4:1',
  description='The violin turns its high arch downward through the dominant',length=12)
P(3,330,'F5:1 E5:1 D5:2 A4:1 C#5:1',
  description='A six-beat violin tail approaches the new tonic through its leading note',length=6)
P(4,288,'D3:2 F3:1 A3:1 C4:1.5 Bb3:.5 A3:1 G3:1 F3:.5 G3:.5 A3:1 C4:1 D4:1',
  description='The viola makes a new twelve-beat rise from the returning root',length=12)
P(4,300,'E4:1 D4:1',description='A two-beat turn delays the inner chant entrance',length=2)
S(4,302,'chant',-12,gain=3,label='The inner chant follows two beats later')
P(4,310,'E3:1 F3:.5 G3:.5 A3:2 C4:1 D4:1 E4:1 F4:1 G4:2 F4:1 E4:1 D4:1 C#4:1 B3:1 A3:1',
  description='The viola grows beyond its statement into a four-bar independent arch',length=16)
P(4,326,'C4:1 D4:1 F4:2 E4:1 D4:.5 C4:.5 Bb3:1 A3:1 G3:1 A3:1 B3:1 C#4:1',
  description='The inner line crosses the major boundary with an ascending sixth and seventh',length=12)
P(5,292,'C4:2 Bb3:1 A3:1 G3:1 F3:.5 E3:.5 D3:2 E3:1 F3:1 G3:2 Bb3:1 A3:1 G3:1 F3:1',
  description='The horn carries a broad four-bar sentence beneath the changing foreground',length=16)
S(5,308,'inverted_chant',-12,gain=2,label='The horn turns the chant upward')
P(5,316,'E3:1.5 G3:.5 A3:1 C#4:1 E4:2 D4:1 C#4:1 B3:1 A3:1 G3:1 E3:1',
  description='The horn inversion rises toward the dominant before relaxing',length=12)
P(5,328,'D3:2 A2:1 D3:1 E3:1 F#3:1 G3:1 A3:1 D4:2 C#4:1 B3:1',
  description='The horn alone first raises the third, preparing the major arrival before its boundary',length=12,gain=1,label='The horn begins to brighten')
P(6,288,'D4:1 C4:.5 Bb3:.5 A3:1 F3:1',
  description='The bassoon leading note resolves upward before the line descends to its statement',length=4)
S(6,292,'chant',-12,gain=3,label='The returning chant moves to the bassoon')
P(6,300,'F3:1 E3:1 D3:2 C3:1 D3:.5 Eb3:.5 F3:1 G3:1 Bb3:1 A3:1 G3:1 D3:1',
  description='The bassoon descent reverses into a new subdominant arch',length=12)
H(6,312,-12,gain=3,label='The bassoon answers with the quick head')
P(6,316,'C3:.5 D3:.5 E3:1 G3:2 A3:1 G3:.5 F3:.5 E3:1 C#3:1 D3:2 F3:1 A3:1 G3:1 F3:1 E3:1 D3:1',
  description='A long bassoon route combines syncopation, a suspension and a tonic return',length=16)
P(6,332,'A2:2 D3:1 E3:1 F#3:1 A3:1 G3:1 E3:1',
  description='The bassoon reaches the major third after the horn has prepared it',length=8)
P(7,288,'D3:1.5 F3:.5 A3:2 G3:1 F3:.5 E3:.5 D3:1 C3:1 Bb2:2 A2:1 G2:1 F2:1 G2:1 A2:1 Bb2:1',
  description='The cello begins a four-bar falling sentence while the violin states the chant',length=16)
S(7,304,'altered_chant',-12,gain=2,label='The cello remembers the chromatic disturbance')
P(7,312,'D3:2 C3:1 Bb2:1 A2:1 C#3:.5 E3:.5 G3:2 F3:1 E3:1 D3:2 F3:1 E3:1 G3:1 A3:1',
  description='The cello continuation drives independently toward the dominant and back',length=16)
P(7,328,'F3:1 E3:.5 D3:.5 C3:2 Bb2:.5 A2:1.5 G2:1 A2:1 D3:2 E3:1 F#3:1',
  description='A twelve-beat cello line carries a minor memory across the major arrival',length=12)
P(8,288,'D2:2 A1:1 D2:.5 F2:.5 E2:1 D2:.5 C2:.5 Bb1:2 A1:1 C2:1 D2:1 F2:1 G2:1 F2:.5 E2:.5 D2:2',
  description='A moving sixteen-beat bass melody reclaims the tonic without becoming a chord pad',length=16)
P(8,304,'G1:2 D2:1 F2:1 Eb2:2 D2:1 C2:1 Bb1:1 C2:1 D2:2',
  description='The bass takes its own twelve-beat route through the minor subdominant',length=12)
P(8,316,'A1:2 E2:1 G2:1 F2:1 E2:.5 D2:.5 C#2:2 D2:1 F2:1 E2:1 C#2:1',
  description='A dominant descent briefly releases into the tonic before the final approach',length=12)
P(8,328,'D2:2 A1:1 D2:1 F2:1 E2:1 D2:1 A1:1',
  description='The bass keeps the minor third briefly while the horn prepares the new color',length=8)

# VIII. THE PROCESSION TAKES FLIGHT, bars 85-96. Three players breathe
# just after the new color arrives. The full nine-line texture regathers at
# 348. The expanded bridge saves its highest, longest point for 360-363;
# several other sentences continue across that point and across 368.
P(0,340,'F#5:2 E5:1 D5:1 C#5:1 E5:.5 F#5:.5 G5:2 A5:1 B5:1 C#6:1 A5:1',
  description='The flute gathers height while three lower players leave room',length=12,gain=1)
S(0,352,'major_bridge',24,scale=2,gain=2,label='The rising idea takes flight')
P(0,368,'D6:3 C#6:1 B5:2 A5:2 G5:1 F#5:1 E5:2 D5:1 E5:1 F#5:1 A5:1',
  description='The high arrival releases through a sixteen-beat descent',length=16,gain=-1)
S(1,336,'major_chant',12,gain=3,label='The chant opens fully into major')
P(1,344,'B4:2 D5:1 G5:1 F#5:1 E5:.5 D5:.5 C#5:1 B4:1 A4:1 C#5:1 E5:1 G5:1',
  description='The bright chant continues into a separate twelve-beat sentence',length=12)
P(1,356,'F#5:3 E5:1 D5:1 C#5:.5 B4:.5 A4:2 B4:1 D5:1 G5:1 F#5:1 E5:1 D5:1',
  description='A fourteen-beat oboe arch crosses the high point and resolves its ninth after the return',length=14)
H(1,370,12,gain=1,major=True,label='The dance survives the long arrival')
P(1,374,'C#5:1 B4:1 A4:2 G4:1 F#4:1 E4:1 D4:1 C#4:1 E4:1',
  description='A ten-beat oboe descent relaxes toward the final turn',length=10,gain=-1)
H(2,344,-12,gain=2,major=True,label='A quiet lower dance head')
P(2,348,'B3:1.5 D4:.5 G4:2 F#4:1 E4:.5 D4:.5 C#4:1 B3:1 A3:2 C#4:1 E4:1 F#4:1 G4:1 A4:1 B4:1',
  description='The clarinet grows from a held ascent into a four-bar rising sentence',length=16)
P(2,364,'A4:2 G4:1 F#4:1 E4:1 D4:.5 C#4:.5 B3:2 A3:1 B3:1 C#4:1 D4:1',
  description='The clarinet reaches and then descends across the tonic arrival',length=12,gain=-1)
P(2,376,'G3:1 B3:.5 D4:.5 F#4:1 E4:1 D4:1 C#4:1 B3:1 A3:1',
  description='An eight-beat clarinet arch keeps motion alive below the relaxing upper lines',length=8,gain=-1)
P(3,336,'D5:1 F#5:1',description='The violin resolves before its displaced major dance head',length=2)
H(3,338,12,gain=2,major=True,label='A displaced bright dance head')
P(3,342,'C#6:.5 B5:.5 A5:2 G5:1 F#5:1 E5:1 D5:2 B4:1 D5:.5 G5:.5 F#5:1 E5:1 D5:1 C#5:1 B4:1 A4:1',
  description='The violin holds a ninth across the changing bass, then follows its own four-bar descent',length=16)
P(3,358,'C#5:2 E5:1 F#5:1 G5:1.5 A5:.5 B5:2 A5:1 G5:1 F#5:2 E5:1 D5:.5 C#5:.5 B4:2 A4:1 G4:1 F#4:1 E4:1',
  description='A five-bar violin arch crosses both the high point and the later relaxation',length=20)
P(3,378,'D4:1 E4:1 F#4:1 G4:1 E4:1 C#4:1',
  description='A six-beat violin turn approaches the final predominant',length=6,gain=-1)
P(4,338,'D4:2 F#4:1 A4:1 G4:1 F#4:1 E4:1 D4:1',
  description='The viola continues across the new key while other low voices breathe',length=8)
H(4,346,-7,gain=2,major=True,label='The dance head enters on a different beat')
P(4,350,'B3:2 A3:1 G3:1 F#3:1 E3:.5 F#3:.5 F#3:2 A3:1 C#4:1 E4:1 F#4:1 G4:2 F#4:1 E4:1',
  description='The viola delays its own high point beneath the enlarged bridge',length=16)
H(4,366,0,gain=2,major=True,label='The quick head crosses the tonic arrival')
P(4,370,'B3:1 D4:1 F#4:2 E4:1 D4:.5 C#4:.5 B3:1 A3:1 G3:1 A3:1 B3:1 D4:1',
  description='The viola follows the last head with a separate twelve-beat release',length=12,gain=-1)
P(4,382,'C#4:1 E4:1',description='A short inner turn reaches the last predominant',length=2,gain=-1)
P(5,344,'G3:3 B3:1 D4:1 C#4:.5 B3:.5 A3:1 G3:1 E3:2 G3:1 B3:1 C#4:1 E4:1 F#4:2',
  description='The horn returns after a breath with a four-bar rise independent of the flute',length=16,gain=1)
P(5,360,'B3:2 D4:1 G4:1 F#4:2 E4:1 D4:1 C#4:1 E4:.5 D4:.5 B3:2 A3:1 G3:1 F#3:2 E3:1 F#3:1 G3:1 B3:1',
  description='The horn reaches its own peak late and descends for five bars',length=20)
P(5,380,'A3:1 G3:1 E3:1 C#3:1',description='The horn descent points to the final harmonic turn',length=4,gain=-1)
H(6,348,-7,gain=2,major=True,label='The last reentry restores all nine')
P(6,352,'E3:1 G3:.5 A3:.5 C#4:2 B3:1 A3:1 F#3:1 E3:1 G3:2 B3:1 D4:1 E4:1 D4:1 C#4:1 A3:1',
  description='The bassoon follows a sixteen-beat route through dominant, mediant and subdominant colors',length=16)
S(6,368,'major_chant',-12,gain=2,label='The chant returns below the high arrival')
P(6,376,'G3:1.5 F#3:.5 E3:1 D3:1 C#3:1 E3:1 G3:1 A3:1',
  description='The low chant opens into a last independently timed arch',length=8,gain=-1)
P(7,344,'B2:2 D3:1 G3:1 E3:1 F#3:.5 G3:.5 B3:2 A3:1 G3:1 E3:1 C#3:1',
  description='The cello reenters after a full bar of breath and rises for twelve beats',length=12)
H(7,356,-12,gain=2,major=True,label='A bright cello dance below the expanding bridge')
P(7,360,'G2:2 B2:1 D3:1 E3:1 G3:1 A3:2 F#3:1 E3:.5 D3:.5 C#3:1 B2:1 A2:2 D3:1 F#3:1 E3:1 D3:1',
  description='An eighteen-beat cello route crosses the high arrival and continues its descent',length=18)
P(7,378,'B2:1 D3:1 E3:2 D3:1 C#3:1',
  description='The cello keeps a six-beat tail beneath the final upper relaxation',length=6,gain=-1)
P(8,336,'D2:3 A1:1 B1:2 D2:1 F#2:1',
  description='The bass confirms the new tonic, then begins moving again',length=8,gain=1)
P(8,344,'G1:2 D2:1 B1:1 E2:2 G2:1 B2:1 A2:1 G2:1 E2:1 C#2:1',
  description='A twelve-beat bass route moves through predominant and dominant',length=12)
P(8,356,'F#1:2 A1:1 C#2:1 G1:2 B1:1 D2:1 E2:1 G2:1 A1:2',
  description='The bass supports the delayed high point and makes the final dominant explicit',length=12)
P(8,368,'D2:2 A1:1 D2:1 F#2:1 E2:1 D2:1 B1:1 G1:2 B1:1 D2:1 C#2:1 E2:1 A1:2',
  description='A sixteen-beat bass melody releases the arrival into one final turn',length=16,gain=-1)

# IX. LAST TURN HOME, bars 97-100. G major -> E half-diminished -> A7 -> D.
# The remembered flat sixth darkens one bar. Individual appoggiaturas and
# leading notes resolve at different moments; only the final two beats align.
P(0,384,'D6:1 B5:1 G5:1 E5:1 D5:1 G5:1 Bb5:1 A5:1 G5:2 F#5:1 E5:1 F#5:1 E5:.5 D5:.5 D6:2',
  description='The flute remembers the darker sixth and relaxes into the last high tonic',length=16,gain=-2)
P(1,384,'G4:2 F#4:1 E4:1 D4:1 E4:.5 G4:.5 Bb4:2 A4:1 G4:.5 F#4:.5 E4:1 C#4:1 D4:.5 E4:.5 F#4:1 A4:2',
  description='The oboe keeps a melodic cadence through the final arrival',length=16,gain=-1)
P(2,384,'G3:2 B3:1 D4:1 E4:1 D4:.5 C4:.5 Bb3:1 G3:1 A3:1 G3:1 F#3:1 E3:1 D3:1 F#3:1 D4:2',
  description='The clarinet descends through the dominant seventh before reaching the final chord',length=16,gain=-1)
P(3,384,'B4:1 D5:.5 G5:.5 F#5:1 E5:1 D5:2 Bb4:1 G4:1 A4:1 C#5:.5 E5:.5 G5:1 F#5:1 E5:.5 D5:1.5 F#5:2',
  description='The violin resolves its upper ninth after the bass has arrived',length=16,gain=-1)
P(4,384,'D4:1 B3:1 G3:2 E3:1 G3:1 Bb3:1 D4:1 E4:1 D4:.5 C#4:.5 B3:1 A3:1 E4:1.5 D4:.5 A3:2',
  description='The viola delays its final ninth resolution until the last half beat before the chord',length=16,gain=-1)
P(5,384,'B3:3 A3:1 G3:2 Bb3:1 D4:1 C#4:2 B3:1 A3:1 G3:1 F#3:1 D3:2',
  description='The horn fourth resolves to the major third a beat after the tonic bass arrives',length=16,gain=-1)
P(6,384,'B3:2 A3:1 G3:1 G3:1 Bb3:.5 A3:.5 G3:1 E3:1 A3:1 C#4:1 E4:1 D4:1 C#4:.5 D4:1.5 F#3:2',
  description='The bassoon leading note resolves half a beat after the tonic arrival',length=16,gain=-1)
P(7,384,'D3:2 B2:1 G2:1 Bb2:1 D3:1 E3:1 G3:1 E3:1 G3:1 F#3:.5 E3:.5 D3:.5 C#3:.5 D3:1 E3:.5 F#3:.5 A2:2',
  description='The cello keeps moving through its cadence until the final two beats',length=16,gain=-1)
P(8,384,'G1:3 D2:1 E2:2 G2:1 Bb1:1 A1:3 E2:1 D2:4',
  description='The bass makes the final predominant, mixed-mode chord, dominant and tonic unmistakable',length=16,gain=-1)

# SCORE_CONTINUATION

# SCORE_CONTINUATION

COMPLETE=True

SECTIONS=[
 (0,48,'Procession and interruption','A measured chant, a rising companion and a clipped dance enter separately; the first paragraph reaches the dominant.'),
 (48,112,'The dance takes hold','Roles migrate across the nine players. Distinct longer phrases and delayed heads build toward the relative-major cadence.'),
 (112,176,'A room opens','The relative major opens with three to five lines and actual silences; the ensemble returns by stages through the minor subdominant.'),
 (176,240,'The ground shifts','Unequally delayed chromatic slips disturb the tonic. A later hurried chant and one-beat low dance chase lead to another dominant.'),
 (240,272,'Only a memory','Three cadential resolutions yield to an augmented cello chant with sparse answers, then the lower instruments return.'),
 (272,288,'Gathering','A moving bass earns an eight-beat dominant pedal; upper lines sustain, turn and cross the coming boundary.'),
 (288,336,'Return in pursuit','Delayed chant statements, inversion and displaced dance heads run through unequal phrase lengths. The horn prepares the major third.'),
 (336,384,'The procession takes flight','Brief breaths precede the full nine-line return. An augmented rising figure reaches the delayed crest, then the parts descend independently.'),
 (384,400,'Last turn home','A-flat major, F half-diminished, B-flat seventh and E-flat major; the individual resolutions precede the brief final chord.'),
]

ANNOTATIONS=[
 (0,8,'One measured voice','The horn gives the chant its own space before anyone answers.'),
 (8,20,'Answer and rising companion','The oboe answers higher. The viola introduces a separate rising idea beneath it.'),
 (20,26,'A lower memory','The cello takes the chant while the earlier voices follow different continuations.'),
 (26,34,'A clipped interruption','The violin interrupts with a four-beat dance head. Its three accents are separated by 3 + 3 + 2 half-beats.'),
 (34,40,'The roles begin to move','The bassoon takes the dance; the flute takes the chant. Their phrase endings differ.'),
 (40,48,'The last player enters','The bass bends the rising idea toward the first dominant cadence. Every player has now entered.'),
 (48,64,'The dance takes hold','Clarinet and violin briefly share the dance in octaves. The surrounding lines keep the broader procession pace.'),
 (64,80,'The dancer becomes the singer','The violin takes the chant; the inner strings and horn pass the rising idea and dance between them.'),
 (80,92,'Nine overlapping phrases','The bass states the chant, the flute descends, and the clarinet climbs. The flute holds G-flat over the moving bass, then resolves to F.'),
 (92,104,'A head passes between players','Short dance heads pass through cello, viola and flute, while longer sentences continue across them.'),
 (104,112,'A directed cadence','The moving parts gather around D-flat seventh, preparing the relative major.'),
 (112,128,'A room opens','G-flat major arrives; most players leave space. The quiet cello descent and upper answers become easier to follow.'),
 (128,144,'Longer breathing','Three- and four-bar phrases enter at different times. Silence is part of the counterpoint.'),
 (144,160,'A warmer shared memory','The chant briefly appears in octave colors while the other lines begin the return toward minor.'),
 (160,176,'The route tightens','The separate lines recover the leading note and reach a B-flat-major dominant before the ground shifts.'),
 (176,192,'One chromatic slip, unequal delays','F–F-flat–E-flat passes through three registers. The horn follows the viola after one and a half beats; the bassoon joins half a beat later.'),
 (192,208,'The disturbance spreads','The altered chant moves lower. Longer phrases delay the coming chase instead of starting it immediately.'),
 (208,216,'Two chases at once','Flute and violin hurry the chant. Horn, bass and cello enter the dance head one beat apart, then continue differently.'),
 (216,232,'The answers keep changing','The broad rising idea resists the short heads; the chant also turns upward. Phrase endings remain displaced.'),
 (232,240,'Toward a sudden retreat','The lines narrow toward another B-flat dominant. Its seventh will resolve when the ensemble falls away.'),
 (240,258,'Only a memory','Three lines resolve the cadence. The cello then takes twice the chant’s original time, with sparse answering phrases.'),
 (258,272,'The lower room returns','Viola, horn and bass enter gradually. A quiet minor route begins gathering toward the dominant.'),
 (272,280,'Motion earns the pedal','The bass still walks. Different upper lines enter around it instead of arriving as one block.'),
 (280,288,'Dominant pressure','Only now does the bass hold B-flat. Sustained notes, turns and a rising idea cross the coming return.'),
 (288,302,'Return in pursuit','The violin states the chant; bassoon and oboe follow later. Other players continue phrases already in motion.'),
 (302,320,'Changing foreground','An inner chant, an upward inversion, a chromatic memory and displaced dance heads pass between the parts.'),
 (320,332,'The last minor approach','The separate lines move through the dominant and recover the tonic before the color begins to change.'),
 (332,340,'One voice begins to brighten','The horn introduces G, the major third, before the other parts settle into the new color.'),
 (340,348,'A breath before the crest','Horn and cello pause for a bar; bassoon waits longer. The continuing upper phrases preserve the motion.'),
 (348,360,'Nine lines gather again','The last reentry restores all nine. The flute enlarges the rising figure to twice its length while short dance heads continue below.'),
 (360,368,'The delayed high point','The flute reaches B-flat for three beats, then falls. Violin, horn, clarinet and cello follow their own overlapping arches.'),
 (368,384,'Release with motion still inside','The bass arrives on E-flat. A low chant, delayed resolutions and descending phrases carry the release through another four bars.'),
 (384,392,'A shadow in the last turn','A-flat major turns through F half-diminished. C-flat briefly recalls the opening minor world.'),
 (392,398,'Different resolutions','B-flat seventh gives way to E-flat. Appoggiaturas and leading notes settle at different moments after the bass arrives.'),
 (398,400,'One brief shared arrival','The final two beats settle into a shared E-flat-major chord.'),
]

def make_template(text):
    t=0;events=[]
    for s,d in parse(text):
        if s!='r':events.append(dict(t=t,d=d,p=pitch(s),spell=lily(s)))
        t+=d
    return dict(events=events,duration=t)

def to_eflat(score):
    mapping={'c':'des','cis':'d','des':'eeses','d':'ees','dis':'e','ees':'fes',
             'e':'f','eis':'fis','f':'ges','fis':'g','ges':'aeses','g':'aes',
             'gis':'a','aes':'beses','a':'bes','ais':'b','bes':'ces','b':'c'}
    for group in [score['voices'],list(score['subjects'].values())]:
        for part in group:
            for event in part['events']:
                if event.get('p') is None:continue
                event['p']+=1
                event['spell']=mapping[event['spell']]
    return score

def main():
    for v,c in zip(voices,['#2d759a','#b45d2a','#377449','#9a4eaa','#967b24',
                           '#b24f5f','#227e76','#6f5ab4','#79674d']):
        v['events'].sort(key=lambda e:e['t']);v['color']=c
    borrowed=copy.deepcopy(old['composition_record']['borrowed_material'])
    borrowed['source_reference_pitches']=borrowed['pitches']
    borrowed['pitches']='G-flat F G-flat E-flat F D-flat E-flat E-flat'
    borrowed['pitch_context']='The pitches field gives the complete score in concert E-flat minor; source_reference_pitches gives the D-centered reference used while composing.'
    borrowed['treatment']='New measured rhythm, register, modal variants and developments, transposed into the cycle\'s E-flat-minor slot; the dance and rising phrase families are original.'
    score=dict(metadata=dict(title='The Well-Tempered clAIvier',
          subtitle='VIII. The procession finds a dance floor',
          movement_number=8,number=8,piece_type='fugue',key='Eb',mode='minor',
          meter=[4,4],bpm=108,tempo_text='Con moto; deadpan, then increasingly airborne',
          key_changes=[dict(t=336,key='Eb',mode='major')],
          composer='Traditional chant fragment; new music composed for Sam',
          instrument='Nine chamber players - open score at sounding pitch',
          edition='Complete-form audition' if COMPLETE else 'Composition checkpoint',draft=True,
          lesson_rendering='chamber',
          score_tagline='Fugue VIII - complete-form audition' if COMPLETE else 'Incomplete composition checkpoint',
          score_layout=dict(paper='a3',staff_size=13,staff_distance=9,indent_mm=25),
          markers=[dict(t=0,label='Procession and interruption'),dict(t=48,label='The dance takes hold'),
                   dict(t=112,label='A room opens'),dict(t=176,label='The ground shifts'),
                   dict(t=240,label='Only a memory'),dict(t=272,label='Gathering'),
                   dict(t=288,label='Return in pursuit'),dict(t=336,label='The procession takes flight'),
                   dict(t=384,label='Last turn home')]),
        voices=copy.deepcopy(voices),subjects={k:make_template(v) for k,v in THEMES.items()},
        subject_entries=entries,motivic_fragments=fragments,phrase_map=phrases,
        sections=[dict(t=t,end=end,d=end-t,label=label,detail=detail)
                  for t,end,label,detail in SECTIONS],
        pedagogy=dict(characteristic_figure='A measured chant, a clipped 3+3+2 dance and a broad rising figure exchange roles across nine moving parts.',
          annotations=[dict(t=t,end=end,title=title,text=text)
                       for t,end,title,text in ANNOTATIONS]),
        composition_record=dict(complete_form_written=COMPLETE,planned_beats=400,
          actual_beats=max(e['t']+e['d'] for v in voices for e in v['events']),
          prior_experiment_sha256=hashlib.sha256(OLD.read_bytes()).hexdigest(),
          borrowed_material=borrowed,
          method='Literal revisable phrase writing; explicit thematic transformations; no harmonic-fill solver.',
          final_key='E-flat major',
          chromatic_exchange=dict(voices=[4,5,6],head_starts=[176,177.5,178],concert_pitches=['F','F-flat','E-flat']),
          low_chase=dict(voices=[5,8,7],head_starts=[208,209,210]),
          delayed_crest=dict(voice=0,phrase_start=352,phrase_end=368,high_note='B-flat6',high_note_start=360,high_note_end=363),
          audio_listening_evaluation=False))
    to_eflat(score);normalized_voices(score)
    OUT.mkdir(parents=True,exist_ok=True)
    target=OUT/'08-fugue-complete.json';target.write_text(json.dumps(score,indent=2)+'\n')
    print(json.dumps(dict(score=str(target),complete_form=COMPLETE,
       beats=score['composition_record']['actual_beats'],notes=sum(len(v['events']) for v in voices)),indent=2))

if __name__=='__main__':main()
