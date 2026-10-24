from gen import *
from cp import tobars,length
import sys
f=dinv(5,67)
R=[4,2,2,2,2,2,2, 1,1,1,1,2,2,4,2,2, 2,1,1,2,2,1,1,1,1,4, 2,2,2,2,1,1,1,1,2,2, 1,1,1,1,1,1,1,1,2,2,2,2, 2,2,2,2,4,4]
assert sum(R)==96
Fm={5,8,0};Bbm={10,1,5};C7={0,4,7,10};Db={1,5,8};E7={4,7,10,1}
pl=[Fm,Fm,Bbm,C7,Fm,Db,Bbm,E7,Fm,C7,Fm,C7]
t0=192
ch=lambda t: pl[(t-t0)//8] if t0<=t<t0+96 else None
pcs={5,7,8,10,0,1,4}
out=[]
for seed in range(int(sys.argv[1]) if len(sys.argv)>1 else 4):
    r=gen([],R,t0,pcs,(62,79),canon=(f,8),chords=ch,start=72,seed=seed,beam=2500,target=interp([(192,72),(230,76),(260,70),(287,72)]),tw=0.15)
    lead=r[0] if isinstance(r,tuple) else r
    print(seed, r[1] if isinstance(r,tuple) else '')
    print(' L:',tobars(list(zip(lead,R))) if False else lead)
