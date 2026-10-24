import sys,numpy as np
from analyze import *
f=sys.argv[1]
d=load(f);G,A,n=grid(d);V=d['voices'];nv=len(V)
ab=[v['abbr'] for v in V]
res=[]
for i in range(nv):
  for j in range(i+1,nv):
    prev=None;px=None
    for x in range(n):
      if G[i,x]<0 or G[j,x]<0: prev=None;continue
      if not(A[i,x] or A[j,x]): continue
      cur=(G[i,x],G[j,x])
      if prev and prev!=cur:
        a=(prev[1]-prev[0])%12;b=(cur[1]-cur[0])%12
        da=np.sign(cur[0]-prev[0]);db=np.sign(cur[1]-prev[1])
        if a==b and a in(0,5,7) and da==db and da!=0:
          print(f"b{x//12+1}.{(x%12)/4+1:.2f} {ab[i]}{ab[j]} {'8ve' if a==0 else ('5th' if a==5 else '4th')}: {nm(prev[0])}/{nm(prev[1])} -> {nm(cur[0])}/{nm(cur[1])}  (prev@{px%12/4+1:.2f})")
      prev=cur;px=x
