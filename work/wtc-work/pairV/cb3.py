import itertools,re
from cbsrch import build,score
import cbsrch
s=open('adds7.py').read()
s=re.sub(r"putseq\('Cb',35,.*\)\n","putseq('Cb',35,'B1:8 G1:8  A1:8 F#1:8')\n",s)
open('adds7.py','w').write(s)
cbsrch.base=open('fugue_v6_bars.py').read()+s
q=['B1','A#1','C#2','D2','F#1','G1','E2','F#2']
A=[f'{a}:8 {b}:8' for a in ['B1','G1','D2','E2'] for b in ['A#1','C#2','F#1','F#2']]+[f'{a}:8 {b}:4 {c}:4' for a in ['B1','G1','D2'] for b in ['A#1','F#1','C#2'] for c in ['A#1','C#2','F#1','E2'] if b!=c]
B=['B1:16','D2:8 B1:8','D2:4 F#1:4 B1:8','B1:4 D2:4 F#2:8','F#2:4 D2:4 B1:8','B1:8 F#1:8','D2:16','B1:4 C#2:4 D2:8']
res=[]
for a in A:
  for b in B:
    o=build({37:a,38:b}); res.append((score(o,[36,37,38,39]),a,b))
res.sort(); print(res[:8])
