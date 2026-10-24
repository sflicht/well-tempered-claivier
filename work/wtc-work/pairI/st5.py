from st3 import *
res=[]
for lag in range(2,16,2):
  for k in range(-19,20):
    A=SUBJ;B=tr(SUBJ,k)
    gA=grid(A+[(None,lag)]);gB=grid([(None,lag)]+B)
    av=lambda g:sum(p for p,_ in g if p)/max(1,sum(1 for p,_ in g if p))
    up,lo=(gA,gB) if av(gA)>av(gB) else (gB,gA)
    r=check2(up,lo)
    c={t:sum(1 for q in r if q[0]==t) for t in('dis','dis8','cross','par')}
    res.append((c['dis']*3+c['dis8']+c['cross']*2+c['par']*3,c,lag,k))
res.sort(key=lambda r:r[0])
for r in res[:12]:print(r)
