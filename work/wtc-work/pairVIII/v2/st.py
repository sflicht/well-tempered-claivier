from forms import *
from cp import Q
def fits(pcs):
    return [(r,q) for r in range(12) for q,t in Q.items() if pcs<= {(r+x)%12 for x in t}]
def chords(f,T,k):
    return {b+k:frozenset((T+r+x)%12 for x in Q[q]) for b,r,q in FORMS[f][1]}
def notes(f,T,k): return [(t+k,d,r+T) for t,d,r in FORMS[f][0]]
CONS={0,3,4,7,8,9}
for f1 in ['S','SM']:
  for f2 in ['S','A','SM']:
    for k in [1,2,3,4,5]:
      for T in range(-12,13):
        c1=chords(f1,0,0);c2=chords(f2,T,k)
        ok=all(fits(c1[b]|c2[b]) for b in c1 if b in c2)
        if not ok: continue
        bad=0
        for t,d,p in notes(f1,0,0):
          for u,e,q in notes(f2,T,k):
            s=max(t,u)
            if s<min(t+d,u+e) and s%.5==0:
              if abs(p-q)%12 not in CONS|{5}: bad+=1
        if bad<=1: print(f1,f2,k,T,bad,[fits(c1[b]|c2[b])[0] for b in c1 if b in c2])
