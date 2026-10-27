from forms import *
from st import fits,notes
CONS={0,3,4,7,8,9}
import itertools
def at(ns,x):
    for t,d,p in ns:
        if t<=x<t+d: return p
def test(f1,f2,k,T):
    a=notes(f1,0,0);b=notes(f2,T,k);bad=0;wk=0
    xs=sorted({t for t,_,_ in a+b})
    for x in xs:
        p=at(a,x);q=at(b,x)
        if p is None or q is None: continue
        iv=abs(p-q)%12
        lowp = p<q
        if iv not in CONS and not (iv==5):
            if x%1==0: bad+=1
            else: wk+=1
    # beats fit chord
    for x in range(int(k),6):
        p=at(a,x);q=at(b,x)
        if p is None or q is None: continue
        if not fits({p%12,q%12}): bad+=1
    return bad,wk
for f1 in ['S','SM']:
  for f2 in ['S','A','SM']:
    for k in [1,1.5,2,3,4]:
      for T in range(-19,20):
        bad,wk=test(f1,f2,k,T)
        if bad==0 and wk<=2: print(f1,f2,k,T,wk)
