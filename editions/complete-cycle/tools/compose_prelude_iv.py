#!/usr/bin/env python3
"""Emit the original 32-bar Prelude IV from explicitly composed note material.

The lists are the composition, not a random chord-to-note generator. Durations
are quarter-note beats. Three independent monophonic staves are used so that
the quiet cantabile and the middle current can receive different dynamics.
"""
from __future__ import annotations
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def n(name):
    if name == 'r':
        return None
    m = re.fullmatch(r'([A-G])([#b]*)(-?\d+)', name)
    if not m:
        raise ValueError(name)
    letter, accidental, octave = m.groups()
    return 12 * (int(octave) + 1) + {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[letter] + accidental.count('#') - accidental.count('b')

def eq(names, d=.5):
    return [(s,d) for s in names.split()]

# Invocation: the fugue's fifth and upper neighbor are opened out in time.
upper = [
 [('C#5',3),('G#5',1)],
 [('A5',1),('G#5',1),('F#5',1),('E5',1)],
 [('D#5',1.5),('E5',.5),('F#5',1),('D#5',1)],
 [('E5',3),('r',1)],
 [('E5',1),('G#5',.5),('A5',.5),('G#5',1),('F#5',1)],
 [('E5',1),('D#5',1),('C#5',1),('B#4',1)],
 [('C#5',2),('G#4',1),('A4',.5),('G#4',.5)],
 [('F#4',1),('E4',1),('D#4',1),('E4',1)],
 # Relative-major light; inner eighth notes supply motion beneath the song.
 [('E5',1),('F#5',.5),('G#5',.5),('B5',1),('G#5',1)],
 [('A5',2),('G#5',.5),('F#5',.5),('E5',1)],
 [('C#6',1),('A5',1),('G#5',1),('F#5',1)],
 [('D#5',1),('F#5',1),('A5',.5),('G#5',.5),('F#5',.5),('D#5',.5)],
 [('E5',2),('B5',1),('G#5',1)],
 [('E5',1),('G#5',.5),('A5',.5),('G#5',1),('E5',1)],
 [('F#5',1),('E5',1),('D#5',1),('C#5',1)],
 [('B#4',1),('D#5',1),('F#5',1),('D#5',1)],
 # Current: the figuration moves to the upper register and doubles its pace.
 eq('C#5 E5 G#5 C#6 B5 G#5 E5 G#5 A5 G#5 E5 C#5 D#5 E5 F#5 G#5',.25),
 eq('A4 C#5 F#5 A5 G#5 F#5 C#5 F#5 G#5 F#5 E5 D#5 C#5 A4 G#4 F#4',.25),
 eq('F#4 A4 C#5 F#5 D#5 C#5 A4 C#5 D#5 F#5 A5 C#6 B5 A5 F#5 D#5',.25),
 eq('G#4 B#4 D#5 G#5 F#5 D#5 B#4 D#5 F#5 G#5 B#5 D#6 C#6 B#5 G#5 D#5',.25),
 # Deceptive arrival opens the register; activity gradually releases.
 eq('E5 A5 C#6 E6 D#6 C#6 B5 A5'),
 [('C#6',1),('B5',.5),('A5',.5),('G#5',.5),('F#5',.5),('E5',.5),('C#5',.5)],
 [('A5',1),('F#5',1),('E5',.5),('D5',.5),('C#5',.5),('D5',.5)],
 [('D#5',1),('B#4',1),('C#5',.5),('B#4',.5),('G#4',1)],
 # High return, exposed and quiet rather than louder because it is higher.
 [('C#6',2),('G#6',1),('A6',.5),('G#6',.5)],
 [('F#6',1),('E6',1),('D#6',1),('C#6',1)],
 [('B#5',1),('D#6',1),('G#5',1),('r',1)],
 [('C#6',2),('E5',1),('C#5',1)],
 [('C#5',1),('D5',1),('F#5',1),('A5',1)],
 eq('G#5 F#5 E5 D#5 C#5 B#4 D#5 G#5'),
 [('C#6',1),('G#5',.5),('E5',.5),('C#5',1),('G#4',1)],
 [('G#4',1),('C#5',3)],
]

middle = [
 [('E4',2),('G#4',2)],
 [('C#4',2),('F#4',1),('G#4',1)],
 [('B3',2),('A#3',1),('B3',1)],
 [('G#3',2),('B3',1),('E4',1)],
 [('C#4',2),('A3',1),('C#4',1)],
 [('C#4',2),('D#4',1),('F#4',1)],
 [('E4',2),('D#4',1),('C#4',1)],
 [('A3',1),('G#3',1),('F#3',1),('G#3',1)],
 eq('E3 B3 E4 G#4 B4 G#4 E4 B3'),
 eq('A3 C#4 E4 A4 E4 C#4 B3 C#4'),
 eq('C#4 F#4 A4 C#5 A4 F#4 E4 F#4'),
 eq('B3 F#4 A4 F#4 D#4 F#4 A4 D#4'),
 eq('E4 G#4 B4 E5 D#5 B4 G#4 E4'),
 eq('C#4 E4 G#4 C#5 B4 G#4 E4 D#4'),
 eq('A3 C#4 F#4 A4 F#4 D#4 C#4 A3'),
 eq('G#3 B#3 D#4 G#4 F#4 D#4 B#3 D#4'),
 [('C#4',1.5),('G#4',.5),('A4',.5),('G#4',.5),('F#4',1)],
 [('A3',1),('C#4',1),('E4',1),('D#4',1)],
 [('C#4',2),('A3',1),('F#3',1)],
 [('F#3',2),('D#4',1),('B#3',1)],
 [('C#4',2),('E4',2)],
 [('A3',2),('C#4',1),('F#4',1)],
 [('D4',2),('A3',1),('D4',1)],
 [('F#4',2),('D#4',1),('B#3',1)],
 [('G#4',1),('E4',1),('C#4',1),('E4',1)],
 [('A4',1),('G#4',1),('F#4',1),('E4',1)],
 [('D#4',2),('B#3',1),('G#3',1)],
 [('E4',2),('G#4',1),('E4',1)],
 [('A3',1),('F#3',1),('A3',1),('D4',1)],
 [('B#3',2),('D#4',1),('F#4',1)],
 [('E4',2),('G#3',1),('E3',1)],
 [('E4',4)],
]

bass = [
 [('C#2',4)],
 [('F#2',2),('C#3',2)],
 [('B2',2),('F#2',2)],
 [('E2',4)],
 [('A2',2),('F#2',2)],
 [('G#2',4)],
 [('C#3',2),('B2',1),('A2',1)],
 [('F#2',1),('G#2',1),('B2',1),('E3',1)],
 [('E2',2),('G#2',2)],
 [('A2',3),('E3',1)],
 [('F#2',2),('A2',2)],
 [('B2',4)],
 [('E2',2),('B2',1),('E3',1)],
 [('C#3',2),('G#2',2)],
 [('F#2',2),('D#3',2)],
 [('G#2',4)],
 [('C#2',4)],
 [('F#2',2),('A2',2)],
 [('D#2',2),('F#2',2)],
 [('G#2',4)],
 [('A1',2),('A2',2)],
 [('F#2',2),('A2',2)],
 [('F#2',4)],
 [('G#2',4)],
 [('C#2',4)],
 [('F#2',2),('G#2',2)],
 [('G#2',4)],
 [('C#3',2),('B2',1),('A2',1)],
 [('F#2',4)],
 [('G#2',4)],
 [('C#2',2),('C#3',2)],
 [('C#2',4)],
]

bar_energy = [64,66,65,60,66,67,62,62,71,72,75,73,71,70,71,73,
              77,78,79,80,84,76,72,69,63,64,61,59,60,62,58,51]
section_dynamic = {0:'p',8:'mp',16:'mf',20:'f',24:'p',28:'pp'}

def build_voice(bars, name, abbr, clef, offset):
    assert len(bars) == 32
    events=[]
    for b, notes in enumerate(bars):
        assert abs(sum(d for p,d in notes)-4) < 1e-9, (name,b+1,notes)
        t=4*b
        for i,(pitch,d) in enumerate(notes):
            p=n(pitch)
            # Slight metric weighting, and softer running notes beneath held song.
            accent = 3 if t%4==0 else (1 if t%1==0 else -2)
            vel=max(35,min(100,bar_energy[b]+offset+accent))
            event={'t':t,'d':d,'p':p,'v':vel}
            if i==0 and name=='Cantabile' and b in section_dynamic:
                event['dynamic']=section_dynamic[b]
            if p is not None:
                # Explicit B-sharp spelling is valuable in the dominant passages.
                if pitch.startswith('B#'):
                    event['spell']='bis'
                events.append(event)
            t+=d
    return {'name':name,'abbr':abbr,'clef':clef,'events':events}

data={
 'metadata':{
  'title':'The Well-Tempered clAIvier',
  'subtitle':'IV. Prelude in C-sharp minor',
  'composer':'Composed with ChatGPT / Sam',
  'instrument':'Piano - three-layer study score',
  'key':'C#','mode':'minor','meter':[4,4],'bpm':80,
  'tempo_text':'Andante cantabile, con respiro',
  'markers':[
   {'t':0,'label':'Invocation'},
   {'t':32,'label':'First light'},
   {'t':64,'label':'Current'},
   {'t':88,'label':'Neapolitan'},
   {'t':96,'label':'Return'},
   {'t':116,'label':'Close'},
  ],
  'composition_notes':[
   'Original32-bar prelude, composed explicitly in three monophonic layers.',
   'The rising fifth and semitone upper neighbor anticipate Fugue IV.',
   'E-major cantabile gives way to a sixteenth-note current and an A-major deceptive arrival.',
   'D-major over F-sharp supplies the Neapolitan color in bars23 and29.',
   'The final tonic remains minor, reserving the fugue\'s brighter final third.',
   'This free prelude is not represented as a strict-species contrapuntal exercise.',
  ],
 },
 'voices':[
  build_voice(upper,'Cantabile','C.','treble',0),
  build_voice(middle,'Inner current','I.','treble',-16),
  build_voice(bass,'Bass','B.','bass',-10),
 ],
}

# Basic score validation: every part fits32 complete bars, has no overlapping
# notes, all positions are exactly on the sixteenth-note grid, all pitches and
# velocities fit MIDI, and final pitch is C# in melody and bass.
for v in data['voices']:
    end=0
    for e in v['events']:
        assert e['t']>=end and e['d']>0
        assert (e['t']*4).is_integer() if isinstance(e['t'],float) else True
        assert (e['d']*4).is_integer() if isinstance(e['d'],float) else True
        assert 0<=e['p']<=127 and 1<=e['v']<=127
        end=e['t']+e['d']
    assert end==128,(v['name'],end)
assert data['voices'][0]['events'][-1]['p']%12==1
assert data['voices'][2]['events'][-1]['p']%12==1

output=ROOT/'work'/'prelude_iv.json'
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':str(output),'bars':32,'quarter_beats':128,'seconds_at_nominal_tempo':96,
                  'note_counts':[len(v['events']) for v in data['voices']],
                  'pitch_ranges':[[min(e['p'] for e in v['events']),max(e['p'] for e in v['events'])] for v in data['voices']],
                  'basic_validation':'passed'}))
