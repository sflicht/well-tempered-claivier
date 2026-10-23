#!/usr/bin/env python3
"""Literal rewrite of Fugue VIII beats 80–114; source is never overwritten."""
from pathlib import Path
import copy, hashlib, json, re, sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'work/fugue_viii_complete/08-fugue-complete.json'
EXPECTED='63021ec26e8a931fb00b4229b6398673f59f673f618c4b0e4d40965fcc423deb'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
old=json.loads(SOURCE.read_text()); score=copy.deepcopy(old)
voices=score['voices']
base=[58,60,63,67,66,62,65,67,68]
phrases=[]

def midi(p):
    m=re.fullmatch(r'([A-G])([b#]?)([0-8])',p)
    return 12*(int(m[3])+1)+dict(C=0,D=2,E=4,F=5,G=7,A=9,B=11)[m[1]]+{'':0,'b':-1,'#':1}[m[2]]

def spell(p):
    return p[0].lower()+('es' if 'b' in p else 'is' if '#' in p else '')

def parse(text):
    return [(n,float(d)) for n,d in (a.split(':') for a in text.replace('|',' ').split())]

def P(vi,t,text,length,description,family='continuation',gain=0):
    notes=parse(text); assert abs(sum(d for p,d in notes)-length)<1e-9,(vi,t,description,sum(d for p,d in notes),length)
    start=t
    for j,(n,d) in enumerate(notes):
        if n!='r':
            # Accent and articulation belong to the composed gesture, not random
            # humanization. Sustained resolutions remain legato.
            accent=(5 if j in (0,2,4) else -2) if family in ('chant_retort','dance-fragment') else (2 if j==0 else 0)
            gate=.84 if family in ('chant_retort','dance-fragment') and d<=.75 else .98
            voices[vi]['events'].append(dict(t=round(t,6),d=d,p=midi(n),spell=spell(n),v=base[vi]+gain+accent,gate=gate,family=family,phrase_description=description,source='Fugue VIII passage revision: literal composed phrase'))
        t+=d
    phrases.append(dict(voice=vi,t=start,d=length,family=family,description=description))

# Boundaries respect the oboe's unchanged dance statement at76–84. Three
# cadential lines extend independently into the relative-major room.
ends={0:114,1:112,2:112,3:113.5,4:112,5:113,6:112,7:112,8:112}
starts={i:(84 if i==1 else 80) for i in range(9)}
for i,v in enumerate(voices):
    start,end=starts[i],ends[i]
    kept=[]
    for ev in v['events']:
        a,b=ev['t'],ev['t']+ev['d']
        if b<=start or a>=end: kept.append(ev)
        elif a<start or b>end: raise ValueError(('rewrite crosses old event',i,ev))
    v['events']=kept

# A three-beat reply: the chant's upper-neighbor turn becomes an accented
# question, with a dropped fourth and a return. Entries cross the barlines.
RETORT='Gb4:.75 F4:.25 Gb4:.5 Eb4:.5 Bb3:.5 Eb4:.5'

# Flute: a falling ribbon, then a delayed register leap and a leading note
# held across the tonic arrival. It does not participate in the little chase.
P(0,80,'Bb5:2.5 Ab5:.5 Gb5:1 F5:1 Eb5:1.5 Db5:.5 Cb5:1',8,'The flute falls through long and short spans above the three-beat replies')
P(0,88,'Eb5:1.5 F5:.5 Gb5:.5 F5:.5 Eb5:1 Gb5:1.5 Ab5:.5 Bb5:.75 Ab5:.25 Gb5:.5 F5:.5',8,'A turn interrupts the fall and opens a new upward question')
P(0,96,'Eb6:2.5 Db6:.5 Cb6:1 Bb5:1.5 Db6:.5 Gb6:1 F6:.5 Eb6:.5',8,'The high leap is delayed until the bass has finished its first argument')
P(0,104,'Cb6:1.5 Bb5:.5 Ab5:1 Db6:.5 Eb6:.5 F6:1 Eb6:.5 Db6:.5 F6:3 Gb6:1',10,'The upper leading note crosses the new tonic and resolves a beat late')

# Oboe: the old dance finishes first. A leaping answer replaces the scalar
# arch, and the relative-major chant waits until the local Gb arrival at100.
P(1,84,'r:.5 Bb4:.5 Eb5:.75 F5:.25 Gb5:1.5 F5:.5',4,'A breath, a fourth, and a dotted turn answer the clipped middle replies',gain=2)
P(1,88,'Eb5:.5 Db5:.5 Cb5:1.5 Bb4:.5 Ab4:1',4,'The answer bends down in an unequal sentence')
P(1,92,'Eb5:1.5 Db5:.5 Cb5:1 Bb4:.5 r:.5',4,'A displaced upper answer ends with a small breath')
P(1,96,'Ab4:.75 Bb4:.25 Cb5:.5 Eb5:.5 Db5:.5 Cb5:.5 Bb4:1',4,'A rising question turns back toward the arriving major third',gain=1)
P(1,100,'Bb4:1.5 Ab4:.5 Bb4:1 Gb4:1 Ab4:.5 F4:.5 Gb4:1 Gb4:2',8,'The chant opens toward G-flat after the shortened chase',family='major_chant',gain=2)
P(1,108,'Ab4:1.5 Gb4:.5 F4:1 Ab4:1',4,'An oboe pickup leads directly into the new room')

# Clarinet: first retort, then an answer whose apex and closure occur before
# its companions. Its low-to-high leap at100 is a fresh bridge contraction.
P(2,80,RETORT,3,'First three-beat retort: the chant learns to interrupt','chant_retort',3)
P(2,83,'Db4:.5 Eb4:.5 F4:.75 Gb4:.25 Ab4:1 Gb4:1.5 F4:.5',5,'The retort pushes upward, then resolves its fourth above the bass')
P(2,88,'Eb4:.75 F4:.25 Gb4:.5 Ab4:.5 Cb5:.5 Bb4:.5 Ab4:.5 Gb4:.5 F4:1 Eb4:1.5 Db4:.5 Eb4:1',8,'The clarinet keeps an accented answer while another part takes its question')
P(2,96,'Cb4:1.5 Bb3:.5 Ab3:.5 Gb3:.5 Eb4:1',4,'The inner answer descends, then reaches a new third')
P(2,100,'Bb3:.5 Db4:.5 Gb4:.75 F4:.25 Eb4:1 Db4:1',4,'A compressed rising companion replaces the old quarter-note ladder')
P(2,104,'Eb4:.75 Db4:.25 Cb4:.5 Eb4:.5 Ab4:1 Cb5:1',4,'A dotted turn launches the clarinet toward the dominant seventh')
P(2,108,'Bb4:1 Ab4:.5 Gb4:.5 F4:.75 Eb4:.25 Db4:1',4,'An independent inner descent arrives before the upper suspensions')

# Violin: the second retort begins halfway through the third beat, then
# abandons the imitation. Its last C-flat is carried across the cadence.
P(3,80,'Eb5:1.5 Db5:.5 Cb5:.5',2.5,'The violin finishes its previous thought before interrupting')
P(3,82.5,'Gb5:.75 F5:.25 Gb5:.5 Eb5:.5 Bb4:.5 Eb5:.5',3,'Second three-beat retort, entering across the barline','chant_retort',1)
P(3,85.5,'Db5:.5 Cb5:1 Bb4:1',2.5,'The violin answer drops out of the chase into a longer fall')
P(3,88,'Cb5:1.5 Bb4:.5 Ab4:.5 Gb4:.5 F4:1',4,'A string descent opposes the rising cello dance')
P(3,92,'Eb4:1.5 Gb4:.5 Bb4:1 Gb4:1',4,'The violin turns upward by thirds while the bassoon remembers the chant')
P(3,96,'Db5:1.5 Cb5:.5 Bb4:1.5 Ab4:.5',4,'A descending sequence uses an uneven four-beat sentence')
P(3,100,'Gb4:.75 F4:.25 Gb4:.5 Db5:.5 Bb4:.5 Gb4:.5 Ab4:1',4,'The neighbor-turn returns with a new leap and different destination')
P(3,104,'Cb5:2.5 Bb4:.5 Ab4:1',4,'The violin holds its own summit while the other phrases continue')
P(3,108,'Gb4:1 F4:1 Ab4:.5 Bb4:.5 Cb5:1.5 Bb4:1',5.5,'The dominant seventh resolves half a beat after the bass arrives')

# Viola: a broad rising companion now opposes the cello's descent; the
# fourth retort is brief and its continuation occupies a different register.
P(4,80,'Bb3:1 Eb4:.5 F4:.5 Gb4:1.5 F4:.5',4,'The rising companion stretches against the cello instead of doubling it')
P(4,84,'Eb4:.5 Db4:.5 Cb4:1 Bb3:1.5 Ab3:.5',4,'The inner string line reaches down independently')
P(4,88,RETORT,3,'Fourth retort: a middle-string reply above the cello dance','chant_retort',1)
P(4,91,'F4:.5 Gb4:.5 Ab4:1 Gb4:1.5 F4:.5 Eb4:1',5,'The viola turns upward, then delays a six-five resolution over B-flat')
P(4,96,'Ab3:1.5 Bb3:.5 Db4:1 Ab3:1',4,'A broken-fourth answer gives the relative-major turn a different pace')
P(4,100,'Db4:2 Eb4:.5 F4:.5 Gb4:1',4,'The viola sustains before taking a small rising pickup')
P(4,104,'Ab4:.5 Gb4:.5 F4:1 Eb4:1.5 Db4:.5',4,'The inner phrase releases its high point early')
P(4,108,'Cb4:1.5 Bb3:.5 Ab3:1 Db4:1',4,'A falling seventh and a fourth close the viola before the room opens')

# Horn: wide, slower gestures remain melodic; a transposed retort arrives
# late and high enough to escape the bassoon/cello register.
P(5,80,'Eb3:1.5 Gb3:.5 Bb3:1 Ab3:.5 Gb3:.5',4,'The horn rises broadly against the falling upper ribbon')
P(5,84,'F3:1.5 Eb3:.5 Cb3:1 Bb2:1',4,'A measured downward answer reaches a low fifth')
P(5,88,'Eb3:1.5 Cb3:.5 Bb2:1',3,'The horn leaves room before its displaced reply')
P(5,91,'Cb4:.75 Bb3:.25 Cb4:.5 Ab3:.5 Eb3:.5 Ab3:.5',3,'Fifth retort, transposed upward a fourth from the lower version','chant_retort',2)
P(5,94,'Db3:1 Eb3:1',2,'The reply moves through a first inversion and releases into the tonic')
P(5,96,'Eb3:1 Ab3:.5 Cb4:.5 Bb3:1.5 Ab3:.5',4,'The broad companion rises against the strings descent')
P(5,100,'Gb3:2 F3:.5 Eb3:.5 Db3:1',4,'A lower sentence takes its own breath before the dominant')
P(5,104,'Cb3:1.5 Db3:.5 Eb3:1 F3:1',4,'The horn approaches the dominant through an uneven ascent')
P(5,108,'Ab3:1.5 Gb3:.5 F3:1 Ab3:1.5 Gb3:.5',5,'A ninth over the new tonic resolves half a beat late')

# Bassoon: concise turns replace its old scalar fall, then an unchanged
# chant is supported by a bass route that avoids an unprepared low clash.
P(6,80,'Bb3:.75 Ab3:.25 Gb3:1 Eb3:1.5 F3:.5',4,'The bassoon answers with a quick turn and a long lower destination')
P(6,84,'Ab3:.5 Gb3:.5 F3:.75 Eb3:.25 Gb3:1.5 Eb3:.5',4,'A dotted answer rebounds to G-flat above the lower horn')
P(6,88,'Ab3:1.5 Gb3:.5 F3:.5 Eb3:.5 Cb3:1',4,'The bassoon makes space beneath the raised cello dance')
P(6,92,'Gb3:1.5 F3:.5 Gb3:1 Eb3:1 F3:.5 Db3:.5 Eb3:1 Eb3:2',8,'The bassoon keeps the measured chant while the retorts disperse','chant',3)
P(6,100,'Gb3:.75 Ab3:.25 Bb3:1 Db4:1 Cb4:.5 Bb3:.5',4,'A dotted upward answer crosses the other parts descending lines')
P(6,104,'Ab3:1 Eb3:.5 F3:.5 Gb3:1 Ab3:1',4,'A broken fourth and a small rise carry the bassoon toward the cadence')
P(6,108,'F3:1.5 Eb3:.5 Db3:1 F3:1',4,'The bassoon reaches the leading note before its tonic resolution')

# Cello: no octave scale with viola. The third retort becomes the dance,
# now one octave higher than the old masked Eb2 version.
P(7,80,'Eb3:1.5 Db3:.5 Bb2:1 Eb3:1',4,'The cello falls before rising, opposing the viola companion')
P(7,84,'F3:1',1,'A held pickup prepares the cello interruption')
P(7,85,'Gb4:.75 F4:.25 Gb4:.5 Eb4:.5 Bb3:.5 Eb4:.5',3,'Third retort, raised into the cello tenor register','chant_retort',1)
P(7,88,'Eb3:.5 F3:.5 Gb3:.5 Bb3:.75 Ab3:.25 Gb3:.5 Eb3:.5 Bb3:.5',4,'The cello takes the dance head an octave above its former position','dance-fragment',2)
P(7,92,'Gb3:1 Bb3:.5 Db4:1.5 Eb4:.5 Bb3:.5',4,'The cello rises through a fourth while the oboe falls, then turns at its own apex')
P(7,96,'Ab3:.5 Bb3:.5 Cb4:.75 Bb3:.25 Ab3:1.5 Gb3:.5',4,'A quick rise and long falling answer follows the upper leap')
P(7,100,'Eb3:1.5 Gb3:.5 Bb3:1.5 Ab3:.5',4,'The cello rebuilds its arch slowly under the major chant')
P(7,104,'Gb3:.75 F3:.25 Eb3:.5 Ab3:.5 Cb4:.5 Bb3:.5 Ab3:1',4,'A transformed retort changes the direction of the cello answer')
P(7,108,'Ab3:1 Db4:.5 Cb4:.5 Bb3:1 Ab3:.5 F3:.5',4,'The cello turns down to the leading note while the bass sustains')

# Bass: the original subject remains the structural arrival of the ninth
# voice. Later rhythm changes with the harmonic route, not on every beat.
P(8,80,'Gb2:1.5 F2:.5 Gb2:1 Eb2:1 F2:.5 Db2:.5 Eb2:1 Eb2:2',8,'The ninth voice gives the complete chant beneath the new chase','chant',4)
P(8,88,'Ab2:1.5 Gb2:.5 F2:1 Eb2:1 Cb2:2 Bb1:1 Eb2:1',8,'An unequal bass sentence turns through subdominant, lowered sixth and a passing first inversion')
P(8,96,'Ab2:1.5 Gb2:.5 Eb2:1 Cb2:1 Gb2:2 Eb2:.5 F2:.5 Gb2:1',8,'A plagal opening into G-flat avoids a premature dominant cadence')
P(8,104,'Ab1:1.5 Bb1:.5 Cb2:1 Ab1:1 Db2:1.5 Ab1:.5 Db2:2',8,'The bass changes pace and settles on the relative-major dominant')

# Annotation contract: only exact complete themes and fragments get the
# machine-checked outlines. Free continuations stay prose annotations.
score['subjects']['chant_retort']={'events':[], 'duration':3}
t=0
for n,d in parse(RETORT):
    score['subjects']['chant_retort']['events'].append(dict(t=t,d=d,p=midi(n),spell=spell(n)))
    t+=d
preserve={(8,80),(6,92)}
score['subject_entries']=[e for e in score['subject_entries'] if not(80<=e['t']<112) or (e['voice'],e['t']) in preserve]
score['subject_entries'].append(dict(voice=1,t=100,subject_id='major_chant',transpose=3,scale=1,label='Chant in the relative major'))
score['subject_entries'].sort(key=lambda e:(e['t'],e['voice']))
score['motivic_fragments']=[e for e in score['motivic_fragments'] if not 80<=e['t']<112]
for vi,t,tr in [(2,80,0),(3,82.5,12),(7,85,0),(4,88,0),(5,91,-7)]:
    score['motivic_fragments'].append(dict(voice=vi,t=t,d=3,source_subject='chant_retort',source_note_indices=list(range(6)),transpose=tr,scale=1,technique='Compressed and extended chant head: three-beat retort',label='Chant-head retort'))
score['motivic_fragments'].append(dict(voice=7,t=88,d=4,source_subject='dance',source_note_indices=list(range(8)),transpose=-12,technique='Dance head raised one octave from the earlier version',label='Raised cello dance'))
score['motivic_fragments'].sort(key=lambda e:(e['t'],e['voice']))

score['phrase_map']=[e for e in score['phrase_map'] if not(e['t']<ends[e['voice']] and e['t']+e['d']>starts[e['voice']])]+phrases
score['phrase_map'].sort(key=lambda e:(e['t'],e['voice']))
ann=score['pedagogy']['annotations']
ann=[e for e in ann if e['end']<=80 or e['t']>=128]
ann += [
 dict(t=80,end=88,title='A three-beat question crosses the barline',text='The chant remains in the bass. Its neighbor-turn becomes a short retort in clarinet, violin and cello; their continuations differ.'),
 dict(t=88,end=96,title='The reply changes register and owner',text='The cello dance is raised an octave. Viola and horn take the three-beat retort while the bassoon keeps the measured chant.'),
 dict(t=96,end=104,title='The high leap waits',text='The flute finally leaps upward. The bass opens into G-flat and the oboe brings back the warmer chant.'),
 dict(t=104,end=112,title='Different routes to one cadence',text='Short turns, sustained notes and the changing bass rhythm gather toward D-flat seventh.'),
 dict(t=112,end=128,title='The room opens in stages',text='The bass arrives first. Violin and horn resolve half a beat later; the flute leading note waits a full beat. The upper lines then leave space.')]
score['pedagogy']['annotations']=sorted(ann,key=lambda x:x['t'])
score['metadata']['edition']='Passage revision audition — three-beat retorts'
score['metadata']['score_tagline']='Fugue VIII — passage revision audition'
score['composition_record']['passage_revision']={'source_sha256':EXPECTED,'rewritten_beats':[80,114],'new_device':'Three-beat chant retort with unequal entry delays and divergent continuations','claims':'Literal written composition; no auditory evaluation or strict-style certification'}
for v in voices:v['events'].sort(key=lambda e:e['t'])

sys.path.insert(0,str(ROOT/'tools'))
from verify_fugue_viii_deliverables import score_checks, theme_checks
checks={'score':score_checks(score),'themes':theme_checks(score)}
dest=HERE/'08-fugue-passage-revised.json'
dest.write_text(json.dumps(score,indent=2,ensure_ascii=False)+'\n')
(HERE/'source-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps({'score':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'checks':checks['score'],'exact_annotations':checks['themes']['literal_entries_and_fragments_verified']},indent=2))
