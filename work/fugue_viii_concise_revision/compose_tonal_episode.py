#!/usr/bin/env python3
"""Literal eight-bar tonal episode, local time0–32 -> complete time112–144."""
from pathlib import Path
import copy, json, re
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
old=json.loads((ROOT/'work/fugue_viii_passage_revision/08-fugue-passage-revised.json').read_text())
voices=[{**{k:v for k,v in x.items() if k!='events'},'events':[]} for x in old['voices']]
subjects=copy.deepcopy(old['subjects']); phrases=[]; fragments=[]
def midi(s):
 m=re.fullmatch(r'([A-G])([b#]?)([0-8])',s)
 return (int(m[3])+1)*12+dict(C=0,D=2,E=4,F=5,G=7,A=9,B=11)[m[1]]+{'':0,'b':-1,'#':1}[m[2]]
def spell(s):return s[0].lower()+('es' if 'b' in s else 'is' if '#' in s else '')
def add(v,t,text,description,vel=58,family='continuation'):
 start=t
 for tok in text.split():
  p,d=tok.split(':');d=float(d)
  if p!='r':
   voices[v]['events'].append({'t':t,'d':d,'p':midi(p),'spell':spell(p),'v':vel,'gate':.96 if d>=1 else .93,'family':family,'phrase_description':description,'source':'Fugue VIII concise revision: composed tonal episode'})
  t+=d
 phrases.append({'voice':v,'t':start,'d':t-start,'family':family,'description':description})
 return t
pred='F4:.5 Gb4:.5 Ab4:.5 Cb5:.75 Bb4:.25 Ab4:.5 F4:.5 Cb5:.5 r:.5 Eb5:.5 Db5:.5 Cb5:.5 Ab4:.75 Gb4:.25 F4:.5 Eb4:.5'
t=0;events=[]
for tok in pred.split():
 p,d=tok.split(':');d=float(d)
 if p!='r':events.append({'t':t,'d':d,'p':midi(p),'spell':spell(p)})
 t+=d
subjects['predominant_dance']={'events':events,'duration':8,'derivation':'Dance recast in the F half-diminished region; F–G-flat–A-flat–C-flat replaces the opening tonic arpeggio.'}
def head(v,t,subject,trans,label):
 for e in subjects[subject]['events'][:8]:
  pitch=e['p']+trans
  names=['c','des','d','ees','fes','f','ges','g','aes','a','bes','ces']
  voices[v]['events'].append({'t':t+e['t'],'d':e['d'],'p':pitch,'spell':names[pitch%12],'v':69,'gate':.93,'family':'dance-fragment','phrase_description':label,'source':'Fugue VIII concise revision: literal thematic head'})
 fragments.append({'voice':v,'t':t,'d':4,'source_subject':subject,'source_note_indices':list(range(8)),'transpose':trans,'technique':label})
 phrases.append({'voice':v,'t':t,'d':4,'family':'dance-fragment','description':label})

# Moving fundamental line; the single-bar final pedal is earned by seven bars of motion.
add(8,0,'Db2:2 Ab2:1 Db2:1 Gb2:2 Db3:1 Bb2:1 Cb2:2 Gb2:1 Eb2:1 F2:1 Ab2:1 Cb3:1 F2:1 Bb1:2 F2:1 Bb1:1 Eb2:2 Bb1:1 Eb2:1 Ab1:1 Eb2:1 Ab2:1 Cb2:1 Bb1:4','Db7–Gb–Cb–F half-diminished–Bb7–Eb minor–Ab minor–Bb7; moving bass before one final dominant bar',61)

# A head passes through changing functions and registers. The flute and bassoon
# enter only in the last three bars; there is no permanent orchestral pad.
head(3,0,'major_dance',-2,'D-flat dance head beneath the carried D-flat-seventh bridge tail')
head(4,4,'major_dance',3,'G-flat answer: the dance head moves to the inner voice')
head(2,8,'major_dance',-4,'C-flat answer continues the descending-fifth route')
head(1,12,'predominant_dance',0,'Diminished predominant version of the dance head')
head(7,16,'major_dance',-5,'B-flat dominant answer in the tenor')
head(0,20,'dance',12,'The original minor dance returns above the tonic arrival')
head(6,24,'dance',-7,'A-flat-minor answer below the descending upper lines')

# Violin: one continuous upper sentence, including a seventh that resolves
# at16 and a dominant seventh that resolves at20.
add(3,4,'Bb4:1 Ab4:1 F4:1 Gb4:1 Eb4:1 Gb4:1 Bb4:1 Gb4:1 Ab4:1 Cb5:1 Ab4:1 F4:1 Bb4:1 D5:1 F5:1 Ab5:1 Gb5:1 F5:.5 Eb5:.5 Db5:2 Cb5:1 Bb4:1 Ab4:2 Bb4:1 D5:1 F5:1 Ab5:1','An upper answering sentence rises through the predominant, answers the prepared inner seventh and resolves a dominant seventh, and finally prepares G-flat in the return',59)

# Inner answer: its E-flat is genuinely tied across the harmonic change12.
add(4,8,'Cb5:1 Bb4:.5 Ab4:.5 Gb4:1 Eb4:5 D4:1 F4:1 Ab4:1 Gb4:.5 F4:.5 Eb4:2','The inner head descends to a prepared E-flat seventh, resolves to D on the dominant, and withdraws after tonic arrival',57)

# The opening clarinet tail is supplied by the parent score at local0–4:
# Db5:1.5 Cb5:.5 Ab4:1 F4:1. Do not duplicate it here.
add(2,12,'Cb4:1 Db4:.5 Eb4:.5 F4:1 Ab4:1 F4:1','A rising answer leaves the predominant and settles on F above the dominant, then rests',57)

# Cello enters as an independent counterline before taking the dominant head.
add(7,0,'F3:1 Ab3:1 Cb4:2 Bb3:2 Ab3:1 Gb3:1','The dominant seventh C-flat resolves to B-flat at the relative-major arrival',57)
add(7,20,'Gb4:1','The tenor dance rises to the minor third and leaves space',57)
add(7,28,'Bb2:1 C3:.5 D3:.5 F3:1 D3:1','A late tenor ascent finishes on the leading note D, to rise to E-flat at the return',60)

# Oboe and flute leave before the final cadence rather than forcing everyone
# to sustain it. Their last notes resolve into the dominant before the rests.
add(1,16,'Bb4:1','The diminished head resolves its C-flat downward into the dominant root, then rests',57)
add(1,24,'Eb5:1 Db5:.5 Cb5:.5 Bb4:.5 Ab4:.5 Gb4:1 F4:1','An upper descent turns the subdominant into the dominant, then breathes before its reentry',58)
add(0,24,'Ab5:1 Gb5:.5 F5:.5 Eb5:1 Cb5:1.5 Bb4:.5','The high dance falls to C-flat, carries the prepared flat ninth across the dominant, and resolves down to B-flat',57)
add(6,28,'D4:1 F4:1 Ab4:1 Gb4:.5 F4:.5','The lower head continues on the dominant and points down toward E-flat',60)

for v in voices:
 v['events'].sort(key=lambda e:e['t'])
 for a,b in zip(v['events'],v['events'][1:]):
  assert a['t']+a['d']<=b['t']+1e-8,(v['name'],a,b)
 assert all(e['t']>=0 and e['t']+e['d']<=32 for e in v['events'])
for f in fragments:
 expected=[(f['t']+subjects[f['source_subject']]['events'][i]['t'], subjects[f['source_subject']]['events'][i]['d'],subjects[f['source_subject']]['events'][i]['p']+f['transpose']) for i in f['source_note_indices']]
 actual={(e['t'],e['d'],e['p']) for e in voices[f['voice']]['events']}
 assert all(x in actual for x in expected),f
score={'metadata':{**old['metadata'],'subtitle':'VIII. Concise revision — tonal episode','edition':'Local-time subsection for assembly','key_changes':[],'markers':[],'planned_beats':32,'global_start_beat':112},'voices':voices,'subjects':subjects,'subject_entries':[],'motivic_fragments':fragments,'phrase_map':phrases,'sections':[{'t':0,'end':32,'d':32,'label':'Tonal episode','detail':'D-flat seventh, G-flat, C-flat, F half-diminished, B-flat seventh, E-flat minor, A-flat minor, B-flat seventh.'}], 'pedagogy':{'characteristic_figure':'A dance head passes through a descending-fifth harmonic sequence and changes register.','annotations':[]},'composition_record':{'local_beats':[0,32],'global_beats':[112,144],'carried_voice_from_parent':{'voice':2,'local_beats':[0,4],'notes':'Db5:1.5 Cb5:.5 Ab4:1 F4:1'},'listening_evaluation':False,'note':'This is a composed subsection for review, not a historical counterpoint certificate.'}}
(HERE/'tonal-episode.json').write_text(json.dumps(score,indent=2)+'\n')
print('Wrote tonal-episode.json',sum(len(v['events']) for v in voices),'notes; seven exact thematic heads.')
