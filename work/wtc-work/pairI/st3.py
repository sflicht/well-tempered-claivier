from cp import *
SUBJ=parse('C5:4 Db5:2 B4:2 D5:2 Bb4:2 Eb5:2 A4:2 Ab4:2 G4:2 F4:1 Eb4:1 D4:1 F4:1 Eb4:2 D4:2 C4:4')
SC=[0,2,3,5,7,8,11]  # C harmonic minor
def deg(p):  # midi->(octave*7+idx) for scale notes
    pc=p%12; return (p//12)*7+SC.index(pc)
def undeg(d): return (d//7)*12+SC[d%7]
def tinv(line,S,nw=9,key=0):
    out=[];w=0
    for idx,(p,d) in enumerate(line):
        if idx<nw: out.append((S-p,d))
        else: out.append((p,d))
    # tail diatonic mirror around the mirrored first-tail note
    t0=line[nw][0]; m0=S-t0
    # snap m0 to scale of key
    base=(m0-key)
    if (base%12) not in SC: return None
    dt0=deg(t0-key)
    for idx in range(nw,len(line)):
        p,d=line[idx]
        if (p-key)%12 not in SC: return None
        out[idx]=(undeg(deg(m0-key)-(deg(p-key)-dt0))+key,d)
    return out
if __name__=='__main__':
  res=[]
  for lag in range(2,16,2):
    for S in range(110,150):
      for k in range(-12,1):
        for key in (0,7,3,5,8,10):
          s=tr(SUBJ,k)
          if any((p-key)%12 not in SC for p,_ in s[9:]): continue
          i=tinv(s,S+2*k,key=key)
          if i is None: continue
          for lead in 'SI':
            A,B=(s,i) if lead=='S' else (i,s)
            gA=grid(A+[(None,lag)]);gB=grid([(None,lag)]+B)
            av=lambda g:sum(p for p,_ in g if p)/max(1,sum(1 for p,_ in g if p))
            up,lo=(gA,gB) if av(gA)>av(gB) else (gB,gA)
            r=check2(up,lo)
            c={t:sum(1 for q in r if q[0]==t) for t in('dis','dis8','cross','par')}
            sc=c['dis']*3+c['dis8']+c['cross']*2+c['par']*3
            res.append((sc,c['dis'],c['dis8'],c['cross'],c['par'],lag,S,lead,k,key))
  res.sort()
  seen=set()
  for r in res:
    kk=(r[5],r[7],(r[6])%12,r[9])
    if kk in seen: continue
    seen.add(kk);print(r)
    if len(seen)>30:break
