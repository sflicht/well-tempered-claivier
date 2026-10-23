#!/usr/bin/env python3
"""Literal two-voice composition, not the cycle's former chord-template engine.

The arrays below are the authored musical text. Transposition is used only
for recurring thematic statements. Each episode is written as a pair of
lines; no solver chooses pitches or fills a prescribed harmony.
"""
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from render_music import normalized_voices
OUT=ROOT/'work/recomposition/fugue_i'

def pitch(s):
    m=re.fullmatch(r'([A-G])([#b]?)(\d)',s)
    return 12*(int(m[3])+1)+dict(C=0,D=2,E=4,F=5,G=7,A=9,B=11)[m[1]]+({'#':1,'b':-1,'':0}[m[2]])
def spelling(s):
    return s[0].lower()+('is' if '#' in s else 'es' if 'b' in s else '')
def seq(text):
    return [(s.split(':')[0],float(s.split(':')[1])) for s in text.split()]

# The subject begins on an eighth-note upbeat. Its last B belongs to the
# following C, so each entry opens into its continuation.
S=seq('C4:.5 E4:.5 D4:.25 C4:.25 B3:.5 C4:.5 G3:.5 A3:.5 '
      'B3:.5 C4:.5 D4:.5 G3:.5 E4:.75 D4:.25 C4:.5 B3:.5')
SM=seq('C4:.5 Eb4:.5 D4:.25 C4:.25 B3:.5 C4:.5 G3:.5 A3:.5 '
       'B3:.5 C4:.5 D4:.5 G3:.5 Eb4:.75 D4:.25 C4:.5 B3:.5')
# The first half-beat before this companion is a connecting note, authored
# in its context. The recurring 7.5-beat core is genuinely exchanged above
# and below the subject; fifths which become fourths are passing notes.
CS=seq('E4:.5 G4:1.5 A4:.5 B4:1 G4:1 F4:.5 G4:.5 '
       'C4:.75 B3:.25 C4:.5 D4:.5')
CSM=seq('Eb4:.5 G4:1.5 A4:.5 B4:1 G4:1 F4:.5 G4:.5 '
        'C4:.75 B3:.25 C4:.5 D4:.5')

voices=[{'name':'Upper voice','abbr':'I','clef':'treble','piano_pan':68,'events':[]},
        {'name':'Lower voice','abbr':'II','clef':'bass','piano_pan':60,'events':[]}]
entries=[]
def line(v,t,text,label=None,transpose=0,role='episode'):
    notes=seq(text) if isinstance(text,str) else text
    start=t
    for i,(s,d) in enumerate(notes):
        if s!='r':
            e={'t':round(t,6),'d':d,'p':pitch(s)+transpose,'source':'literal recomposition','role':role}
            if not transpose:e['spell']=spelling(s)
            if i==0 and label:e['label']=label
            # Stable metre and small phrase-directed differences, with no
            # timing randomisation. These are articulation choices, not
            # supposed evidence of musical success.
            metric=4 if t%4==0 else 2 if t%1==0 else 0
            e['v']=int(76+metric+(3 if role=='subject' else 0))
            e['gate']=.88 if d<=.5 else .96
            if d>=2:e['gate']=.99
            voices[v]['events'].append(e)
        t+=d
    return t-start
def theme(v,t,kind,trans,label):
    notes={'subject':S,'minor_subject':SM,'countersubject':CS,'minor_countersubject':CSM}[kind]
    line(v,t,notes,label,trans,'subject' if 'countersubject' not in kind else 'countersubject')
    entries.append({'voice':v,'t':t,'transpose':trans,'scale':1,'subject_id':kind,'label':label})

# Bars 1–4: C subject and G answer. The initial B->C continuation belongs
# to the upper voice while the answer begins underneath it.
theme(0,.5,'subject',12,'Subject')
line(0,8,'C5:.5')
theme(1,8.5,'subject',-5,'Answer')
theme(0,8.5,'countersubject',7,'Companion')

# Bars 5–6: recoil and ascending tail, steering to the dominant entry.
line(0,16,'G4:.5 B4:.5 D5:.5 C5:.25 B4:.25 A4:.5 F#4:.5 G4:.5 B4:.5 '
          'E5:.5 G5:.5 F#5:.5 E5:.25 D5:.25 C5:.5 A4:.5 F#4:.5 A4:.5')
line(1,16,'G3:1 F#3:1 D3:1 E3:1 C3:1 D3:1 E3:.5 F#3:.5 D3:1')

# Bars 7–8: the same answer now in the upper part, companion beneath it.
line(1,24,'C3:.5')
theme(0,24.5,'subject',7,'Subject in G')
theme(1,24.5,'countersubject',-17,'Companion below')

# Bars 9–10: the head starts in the low bass and rises from G to A.
# The last F# passes onward through G# into the minor entry, rather than
# cutting off at a four-beat module boundary.
line(0,32,'G4:.5 B4:.5 D5:1.5 E5:.5 F#5:.5 G5:.5 '
          'E5:.5 C5:.5 E5:1.5 F#5:.5 E5:1')
line(1,32,'G2:.5 G2:.5 B2:.5 A2:.25 G2:.25 F#2:.5 G2:.5 D2:.5 E2:.5 '
          'A2:.5 A2:.5 C3:.5 B2:.25 A2:.25 G#2:.5 A2:.5 E2:.5 F#2:.5')

# Bars 11–12: A-minor statement, its raised 6 and 7 carry the ascending
# tail. The connector B over G# belongs to the previous phrase.
line(1,40,'G#2:.5')
line(0,40,'B4:.5')
theme(1,40.5,'minor_subject',-15,'Subject in A minor')
theme(0,40.5,'minor_countersubject',9,'Minor companion')

# Bars 13–16: one continuous descending-third development. The A and F
# heads are in the upper part; D transfers the head to the lower part.
line(0,48,'A4:.5 C5:.5 B4:.25 A4:.25 G#4:.5 A4:.5 E4:.5 F4:.5 G4:.5 '
          'F4:.5 A4:.5 G4:.25 F4:.25 E4:.5 F4:.5 C4:.5 D4:.5 E4:.5 '
          'D4:1 A4:1 F4:1 G4:1 '
          'F#4:.5 G4:.5 D5:.5 C5:.5 B4:.5 A4:.5 F#4:.5 B4:.5')
line(1,48,'A2:1 E3:1 C3:1 D3:1 '
          'F2:1 C3:1 A2:1 Bb2:1 '
          'D3:.5 F3:.5 E3:.25 D3:.25 C#3:.5 D3:.5 A2:.5 B2:.5 C#3:.5 '
          'D3:.5 C3:.5 B2:.5 A2:.5 G2:.5 F2:.5 D2:.5 G2:.5')

# Bars 17–20: C returns first in the bass, then upstairs. The companion
# makes its largest arch here; the exchanged return completes that arch.
line(0,64,'C5:.5')
line(1,64,'C3:.5')
theme(1,64.5,'subject',-12,'Subject returns below')
theme(0,64.5,'countersubject',12,'Companion above')
line(1,72,'C3:.5')
theme(0,72.5,'subject',12,'Subject returns above')
theme(1,72.5,'countersubject',-12,'Companion below')

# Bars 21–22: the head is displaced half a beat earlier, then transferred
# to the lower part underneath an upper B held across the barline.
line(0,80,'C5:.5 E5:.5 D5:.25 C5:.25 B4:.5 C5:.5 G4:.5 A4:.5 B4:1.5 '
          'A4:.5 F4:.5 E4:.5 G4:.5 F4:.5 E4:.5')
line(1,80,'C3:.5 G2:.5 F2:.5 G2:.5 A2:.5 E3:.5 F3:.5 G3:.5 '
          'E3:.5 G3:.5 F3:.25 E3:.25 D3:.5 E3:.5 C3:.5 D3:.5 E3:.5')

# Bars 23–25: the recoil is recalled over the predominant; F->F#->G
# directs the final dominant. The last ascending subject tail finally
# receives the C withheld by every complete statement.
line(0,88,'F4:.5 A4:.5 G4:.25 F4:.25 E4:.5 D4:.5 E4:.5 F4:.5 F#4:.5 '
          'G4:.5 A4:.5 B4:.5 C5:.5 D5:.5 G4:.5 B4:1 C5:4')
line(1,88,'A2:1 C3:1 F2:1 D3:1 G2:4 C3:4')

for voice in voices:voice['events'].sort(key=lambda e:e['t'])
def template(notes):
    t=0;ev=[]
    for s,d in notes:ev.append({'t':t,'d':d,'p':pitch(s)});t+=d
    return {'events':ev,'duration':t}
score={
 'metadata':{'title':'The Well-Tempered clAIvier','subtitle':'I. Fugue in C major — an open-ended subject',
  'number':1,'movement_number':1,'piece_type':'fugue','key':'C','mode':'major','meter':[4,4],
  'bpm':116,'tempo_text':'Allegro, leggiero e risoluto','composer':'Original composition for Sam',
  'instrument':'Piano — two independent parts','edition':'Recomposition study',
  'score_tagline':'Original composition - recomposition study','draft':True,'voice_order':'high_to_low',
  'score_layout':{'paper':'a4','staff_size':16,'staff_distance':11},
  'markers':[{'t':32,'label':'Bass takes the head'},{'t':48,'label':'Descending sequence'},
             {'t':64,'label':'Return'},{'t':88,'label':'Closing tail'}]},
 'voices':voices,'subjects':{'subject':template(S),'minor_subject':template(SM),
                            'countersubject':template(CS),'minor_countersubject':template(CSM)},
 'subject_entries':entries,
 'sections':[{'t':0,'end':16,'label':'Subject and real answer'},
             {'t':16,'end':32,'label':'Recoil episode and upper dominant entry'},
             {'t':32,'end':48,'label':'Bass head sequence and A-minor entry'},
             {'t':48,'end':64,'label':'Descending-third sequence; head changes hands'},
             {'t':64,'end':80,'label':'Tonic return in both registral orders'},
             {'t':80,'end':100,'label':'Earlier head, transferred head, final tail and cadence'}],
 'composition_record':{'method':'Literal phrase-level note authorship; recurring themes transposed, episodes individually composed.',
  'old_cycle_source_reused':False,'claimed_stretto':False,'audio_listening_evaluation':False,
  'theme_boundary':'The first played subject note is an eighth-note upbeat. The opening eighth rest is not part of its sounding prototype; preceding connecting notes may occupy that slot in later entries.',
  'musical_risk':'Compact tonal argument with recognizable sequence patterns; this is an audition study, not a claim of Bach-level quality.'}}
normalized_voices(score)
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'01-fugue-recomposed.json').write_text(json.dumps(score,indent=2)+'\n')
print(json.dumps({'score':str(OUT/'01-fugue-recomposed.json'),'quarter_beats':100,'seconds':100*60/116,
                  'events':[len(v['events']) for v in voices],'thematic_statements':len(entries)},indent=2))
