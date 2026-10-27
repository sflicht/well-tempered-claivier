import sys,numpy as np
from chk import load,nm
d,G,A,SP,bl,nb=load(sys.argv[1]);n=G.shape[1]
prev=None
for x in range(n):
    if G[0,x]<0 or G[1,x]<0: prev=None;continue
    if not(A[0,x] or A[1,x]):continue
    cur=(G[0,x],G[1,x],x)
    if prev and prev[:2]!=cur[:2]:
        a=abs(prev[1]-prev[0])%12;b=abs(cur[1]-cur[0])%12
        da=np.sign(cur[0]-prev[0]);db=np.sign(cur[1]-prev[1])
        if a==b and a in(0,7) and da==db and da!=0 and prev[0]!=prev[1]:
            print(f"bar{x//bl+1} x{x%bl}: U {nm(prev[0])}->{nm(cur[0])}  L {nm(prev[1])}->{nm(cur[1])}  (prev x{prev[2]%bl}) att U{A[0,x]} L{A[1,x]}")
    prev=cur
