from gen import *
from cp import parse,tobars
import sys
f=dinv(5,67)
hand=parse(open(sys.argv[1]).read().replace('|',' '))
R=[d for _,d in hand]; t0=192
tg={};t=t0
for p,d in hand:
    for x in range(t,t+d): tg[x]=p
    t+=d
tw=float(sys.argv[2]) if len(sys.argv)>2 else 1.0
pcs={5,7,8,10,0,1,4}
best=None
for seed in range(3):
    r=gen([],R,t0,pcs,(60,82),canon=(f,8),start=hand[0][0],seed=seed,beam=3000,target=lambda t:tg[t],tw=tw,osc=1.5,runb=0.2)
    if best is None or r[1]<best[1]: best=r
lead=[x[0] if isinstance(x,tuple) else x for x in best[0]]
print(best[1]);print(tobars(list(zip(lead,R))))
open(sys.argv[1]+'.out','w').write(' '.join(f"{n}:{d}" for n,d in zip([__import__('cp').n(p) for p in lead],R)))
