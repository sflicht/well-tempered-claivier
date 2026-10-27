from motifs import *
import itertools
def notes(f,t0,T): return [(t0+t,d,r+T) for t,d,r in FORMS[f]]
def bad(a,b):
    n=0
    for t,d,p in a:
        for u,e,q in b:
            s=max(t,u)
            if s< min(t+d,u+e) and (s*2)%1==0:  # overlap at 8th grid start
                iv=abs(p-q)%12
                w=2 if s%1==0 else 1
                if iv in(1,2,6,10,11): n+=w
    return n
for f1 in('S','M'):
  for f2 in('S','M','I','IM'):
    for dt in (.5,1,1.5,2,2.5,3):
      for T in range(12):
        sc=bad(notes(f1,0,0),notes(f2,dt,T))
        if sc<=1: print(f1,f2,dt,T,sc)
