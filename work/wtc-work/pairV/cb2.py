import itertools,json
from cbsrch import build,score
base={35:'B1:8 G1:8',36:'A1:8 F#1:8',42:'A1:8 A1:8',45:'F#2:8 G2:8',46:'B1:8 E2:8'}
opts={37:['B1:8 A#1:8','D2:8 C#2:8','E2:8 C#2:8','G1:8 F#1:8','B1:8 C#2:8','D2:8 A#1:8','E2:4 D2:4 C#2:8'],
      38:['B1:16','D2:16','B1:8 D2:8','F#1:8 B1:8','D2:8 F#2:8','B1:4 C#2:4 D2:8','D2:4 C#2:4 B1:8'],
      43:['B1:8 B1:8','D2:8 E2:8','B1:8 E2:8','D2:8 B1:8','F#2:8 E2:8','B1:4 C#2:4 D2:8'],
      44:['E2:8 C#2:8','C#2:8 A1:8','G1:8 A1:8','E1:8 E2:8','G1:8 C#2:8','E2:8 E1:8']}
best=[]
for a in opts[37]:
  for b in opts[38]:
    o=build({**base,37:a,38:b}); best.append((score(o,[36,37,38,39]),a,b))
best.sort(); print(best[:4])
b2=[]
for a in opts[43]:
  for b in opts[44]:
    o=build({**base,43:a,44:b}); b2.append((score(o,[42,43,44,45]),a,b))
b2.sort(); print(b2[:4])
for bb in (35,36,42,45,46):
    print(bb,score(build(base),[bb]))
