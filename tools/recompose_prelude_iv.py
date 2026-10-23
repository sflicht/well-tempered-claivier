#!/usr/bin/env python3
"""A literal, newly authored Prelude IV; no chord/template search.

Each token specifies a pitch and its duration in sixteenth-note units.
The two complete lines below are the composition. The code only spells,
times, performs, and exports them. It never chooses or repairs a pitch.
"""
from pathlib import Path
import hashlib,json,re,sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'work/recomposition/prelude_iv'

# The opening rhythmic proposition is 2,1,1,2,3,1,1,1 sixteenths.
# Its target begins halfway through beat 2 and lasts beyond beat 3.
UPPER=[
 'E5:2 C#5:1 D#5:1 E5:2 G#5:3 F#5:1 E5:1 D#5:1',
 'C#5:3 B4:1 A4:2 G#4:3 B#4:1 D#5:1 B#4:1',
 'C#5:2 A4:1 B4:1 C#5:2 E5:3 D#5:1 C#5:1 B4:1',
 'A4:3 G#4:1 F#4:4 E4:1 D#4:1 G#4:1 B#4:1',
 'C#5:6 B4:3 A4:1 G#4:1 F#4:1',
 'G#4:4 F#4:4 E4:1 D#4:1 C#4:1 D#4:1',
 'E4:2 G#4:1 A4:1 B4:2 E5:3 D#5:1 C#5:1 B4:1',
 'G#4:4 F#4:1 E4:2 D#4:1 C#4:1 D#4:1 F#4:1 E4:1',
 'G#4:2 E4:1 F#4:1 G#4:2 B4:3 A4:1 G#4:1 E4:1',
 'E4:3 D#4:1 C#4:2 B3:3 D#4:1 F#4:1 D#4:1',
 'E4:2 C#4:1 D#4:1 E4:2 G#4:3 F#4:1 E4:1 D4:1',
 'C#4:3 B3:1 A3:2 B3:2 C#4:1 D#4:1 E#4:1 F#4:1',
 'A4:2 F#4:1 G#4:1 A4:2 C#5:3 B4:1 A4:1 F#4:1',
 'F#4:3 E4:1 D4:2 C#4:3 E#4:1 G#4:1 E#4:1',
 'F#4:2 D4:1 E4:1 F#4:2 A4:3 G#4:1 F#4:1 E4:1',
 'D4:3 C#4:1 B3:4 A3:1 G#3:1 C#4:1 E#4:1',
 'F#4:6 E4:3 D4:1 C#4:1 B3:1',
 'C#4:4 B3:4 A3:1 G#3:1 F#3:1 G#3:1',
 'A3:2 C#4:1 D4:1 E4:2 A4:3 G#4:1 F#4:1 E4:1',
 'E4:2 D#4:1 E4:1 F#4:2 G#4:1 A4:1 B4:2 C#5:1 D#5:1',
 'E5:2 C#5:1 D#5:1 E5:2 G#5:3 F#5:1 E5:1 D#5:1',
 'C#5:3 B4:1 A4:2 G#4:3 B#4:1 D#5:1 B#4:1',
 'C#5:2 A4:1 B4:1 C#5:2 E5:3 D#5:1 C#5:1 B4:1',
 'A4:3 G#4:1 F#4:4 E4:1 D#4:1 G#4:1 B#4:1',
 'C#5:2 E5:1 F#5:1 G#5:2 C#6:3 B5:1 A5:1 G#5:1',
 'F#5:3 E5:1 D#5:2 C#5:2 D#5:1 E5:1 F#5:2',
 'E5:2 C#5:1 D#5:1 E5:2 A5:3 G#5:1 F#5:1 E5:1',
 'D#5:2 B4:1 C#5:1 D#5:2 F#5:3 E5:1 D#5:1 C#5:1',
 'B4:3 A4:1 G#4:2 F#4:3 A4:1 C#5:1 B#4:1',
 'B#4:2 D#5:1 E5:1 F#5:2 G#5:3 F#5:1 E5:1 D#5:1',
 'C#5:3 B#4:1 A#4:2 G#4:3 B#4:1 D#5:1 B#4:1',
 'C#5:2 E5:1 D#5:1 C#5:8',
]
LOWER=[
 'C#3:8 E3:4',
 'F#3:6 G#3:6',
 'A3:8 C#3:4',
 'F#2:6 G#2:6',
 'E3:2 C#3:1 D#3:1 E3:2 G#3:3 F#3:1 E3:1 D#3:1',
 'C#3:3 B2:1 A2:2 G#2:3 B#2:1 D#3:1 B#2:1',
 'C#3:2 E3:1 F#3:1 G#3:2 E3:2 B2:2 D#3:2',
 'E3:2 G#2:2 A2:2 B2:6',
 'E3:8 G#2:4',
 'F#2:6 B2:6',
 'C#3:8 E3:4',
 'A2:6 G#2:2 F#2:2 C#3:2',
 'F#2:8 A2:4',
 'G#2:6 C#3:6',
 'D3:8 F#3:4',
 'B2:6 C#3:6',
 'A2:2 F#2:1 G#2:1 A2:2 C#3:3 B2:1 A2:1 G#2:1',
 'F#2:3 E2:1 D2:2 C#2:3 E#2:1 G#2:1 E#2:1',
 'F#2:2 A2:1 B2:1 C#3:2 A2:2 E2:2 G#2:2',
 'F#2:4 D#3:2 E3:2 G#2:2 A2:1 B2:1',
 'C#3:8 E3:4',
 'F#3:6 G#3:6',
 'A3:8 C#3:4',
 'F#2:6 G#2:6',
 'A2:4 C#3:2 E3:6',
 'F#3:2 D#3:2 B2:2 A2:2 G#2:2 F#2:2',
 'G#2:4 C#3:2 F#3:2 E3:2 B2:2',
 'B2:8 D#3:4',
 'E3:6 D#3:6',
 'G#2:12',
 'G#2:12',
 'C#2:12',
]

NAT={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def parse(token):
 name,d=token.split(':'); m=re.fullmatch(r'([A-G])([#b]*)(-?\d+)',name)
 if not m:raise ValueError(token)
 letter,acc,octave=m.groups();alter=acc.count('#')-acc.count('b')
 return 12*(int(octave)+1)+NAT[letter]+alter,int(d),letter.lower()+('is'*alter if alter>=0 else 'es'*(-alter))

def line(bars,lower=False):
 events=[]
 # Phrasing points are authored here; no random timing or humanisation.
 levels=[79,78,77,76,74,74,78,76,77,75,77,78,80,78,78,79,78,77,80,84,83,80,79,80,88,86,85,83,80,85,80,72]
 for b,bar in enumerate(bars):
  unit=0;tokens=bar.split()
  for k,token in enumerate(tokens):
   p,d,spell=parse(token)
   base=levels[b]-(10 if lower else 0)
   if lower and b in [4,5,16,17]:base+=8
   # The long syncopated target receives the weight earned by its approach.
   velocity=base+(4 if unit==6 and d==3 else 0)-(3 if d==1 else 0)
   if unit==0:velocity+=1
   gate=.91 if d==1 else .95 if d<=3 else .985
   events.append({'t':b*3+unit/4,'d':d/4,'p':p,'spell':spell,'v':velocity,'gate':gate,'source':'literal_phrase_authorship','bar':b+1})
   unit+=d
  if unit!=12:raise ValueError(f'Bar {b+1} has {unit} sixteenths: {bar}')
 if not lower:
  # Written ties deliberately prepare the sevenths at bars 10, 14 and 20.
  for boundary in [27,39,57]:
   before=next(e for e in events if e['t']+e['d']==boundary)
   after=next(e for e in events if e['t']==boundary)
   assert before['p']==after['p']
   before['d']+=after['d'];before['gate']=.985
   before['authored_tie_across_bar']=True
   events.remove(after)
 return events

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 if len(UPPER)!=32 or len(LOWER)!=32:raise ValueError('Expected 32 fully written bars')
 score={'metadata':{'title':'The Well-Tempered clAIvier','subtitle':'Prelude IV in C-sharp minor — new composition study','composer':'Composed with ChatGPT / Sam','instrument':'Piano','key':'C#','mode':'minor','meter':[3,4],'bpm':96,'tempo_text':'Allegro inquieto; lightly sprung','movement_number':4,'piece_type':'prelude','edition':'Recomposition study','score_tagline':'Original composition - recomposition study','character':'One rhythmic gesture exchanged and intensified','markers':[{'t':0,'label':'Allegro inquieto'},{'t':12,'label':'The gesture in the bass'},{'t':24,'label':'E major'},{'t':48,'label':'Bass reply'},{'t':60,'label':'Return'},{'t':87,'label':'Dominant pedal'}],'composition_notes':['Completely new, literally authored 32-bar prelude. No notes from the earlier Prelude IV are reused as a compositional template.','The opening sixteenth-unit rhythm 2,1,1,2,3,1,1,1 drives toward a target held across beat 3, followed by a descending tail.','The bass receives the gesture in bars 5-6 and 17-18; the upper line continues across changing bass harmony with prepared suspensions.','E major is approached by actual 4-3 suspensions; E7 turns to A, then the C# dominant to F# minor.','Bar 20 expands the rising portion of the cell, recovering the original register before the tonic return.','The returning idea leads to a higher C# in bar 25, faster bass harmonic movement, ii half-diminished and a dominant pedal; only the final bar gives the closing tonic.','This study is newly composed for listening and musical judgment, not certified as Bach-level writing or strict-species counterpoint.']},'voices':[{'name':'Upper line','abbr':'R.H.','clef':'treble','piano_pan':69,'events':line(UPPER)},{'name':'Lower line','abbr':'L.H.','clef':'bass','piano_pan':59,'events':line(LOWER,True)}],'literal_bars':{'unit':'sixteenth note','upper':UPPER,'lower':LOWER},'composition_record':{'method':'Literal authorship of both full lines; no chord-template generation, constraint search or automatic pitch repair.','replaces_prior_music':False,'basis':'New audition study responding to the listener critique of rhythmic inertia and decorative stylistic blocks.'}}
 target=OUT/'prelude-iv-new.json';target.write_text(json.dumps(score,indent=2)+'\n')
 print(json.dumps({'path':str(target),'bars':32,'written_seconds':60,'notes':sum(len(v['events']) for v in score['voices']),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))

if __name__=='__main__':main()
