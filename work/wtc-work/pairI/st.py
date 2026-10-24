from cp import *
SUBJ=parse('C5:4 Db5:2 B4:2 D5:2 Bb4:2 Eb5:2 A4:2 Ab4:2 G4:2 F4:1 Eb4:1 D4:1 F4:1 Eb4:2 D4:2 C4:4')
res=[]
for lag in range(2,16,2):
  for S in range(100,150):
    for lead in ('S','I'):
      for ktr in range(-12,13):
        s=tr(SUBJ,ktr); i=mirror(SUBJ,S)
        A,B=(s,i) if lead=='S' else (i,s)
        B=[(None,lag)]+B
        A=A+[(None,lag)]
        gA,gB=grid(A),grid(B)
        # decide which is upper by average
        av=lambda g:sum(p for p,_ in g if p)/max(1,sum(1 for p,_ in g if p))
        up,lo=(gA,gB) if av(gA)>av(gB) else (gB,gA)
        r=check2(up,lo)
        ov=[x for x in range(len(gA)) if gA[x][0] and gB[x][0]]
        if len(ov)<16: continue
        dis=sum(1 for t in r if t[0]=='dis');d8=sum(1 for t in r if t[0]=='dis8');cr=sum(1 for t in r if t[0]=='cross');pa=sum(1 for t in r if t[0]=='par')
        res.append((dis*3+d8+cr*2+pa*3,dis,d8,cr,pa,lag,S,lead,ktr))
res.sort()
for r in res[:25]: print(r)
print('---best per (lag,S%12)')
best={}
for r in res:
    k=(r[5],(r[6]-2*0)%12 if False else (r[6]+2*r[8])%12)
    if k not in best: best[k]=r
for k in sorted(best,key=lambda k:best[k][0])[:30]: print(k,best[k])
print('--- S10')
seen=set()
for r in res:
    if (r[6]+2*r[8])%12==10 and (r[5],r[7]) not in seen and r[5]<16:
        seen.add((r[5],r[7]));print(r)
