import json
import fugue_iv as F
from build import build
LEVEL=[0]*100
for b in range(33,37): LEVEL[b]=-8        # quiet link bars 34-37
for b in range(12,18): LEVEL[b]=-3
for i,b in enumerate(range(40,48)): LEVEL[b]=i*1.5   # build into the return
LEVEL[48]=-4
ENT=[('Tenor',1,2,'Subject I'),('Alto',3,2,'Answer II'),('Soprano',5,2,'Subject III'),('Baritone',7,2,'Answer IV'),('Bass',9,2,'Subject V'),
('Baritone',19,2,'Subject VI (E major)'),('Soprano',21,2,'Subject VII (E major)'),
('Alto',29,2,'Answer VIII (G# minor)'),('Bass',31,2,'Subject IX (G# minor)'),('Tenor',34,2,'Subject X (F# minor)'),('Alto',36,2,'Subject XI (C# minor)'),
('Bass',43,2,'Subject XII (C# minor)'),('Alto',43,3,'Answer XIII (stretto, half a bar later)'),('Soprano',46,2,'Subject XIV (C# minor)')]
BARS={'Soprano':F.S,'Alto':F.A,'Tenor':F.T,'Baritone':F.Br,'Bass':F.B}
meta={'score_tagline':'Hand-authored recomposition (first pass) - Claudia / Sam'}
print(build(BARS,ENT,LEVEL,meta,'fugue_iv.json'))
d=json.load(open('fugue_iv.json'))
for e in d['subject_entries']:
    if e['label'].startswith('Answer XIII'): e['t']+=2.0   # starts at sixteenth 6 = 1.5 beats
    if e['label'].startswith('Answer XIII'): e['t']-=0.5
json.dump(d,open('fugue_iv.json','w'),indent=1)
