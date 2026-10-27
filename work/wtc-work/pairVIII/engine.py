import json
from motifs import FORMS
SP={0:'c',1:'des',2:'d',3:'ees',4:'e',5:'f',6:'ges',7:'g',8:'aes',9:'a',10:'bes',11:'ces'}
TEMPL={'maj':(0,4,7),'min':(0,3,7),'dim':(0,3,6),'dom7':(0,4,7,10)}
def cands(scale):
    s=set(scale);out=[]
    for r in scale:
        for k,t in TEMPL.items():
            pcs=[(r+x)%12 for x in t]
            if all(p in s for p in pcs): out.append((r,k,pcs))
    return out
SCALES={}
def realize(NV,CENT,E,NB,KEY,PEDAL,ACT,lo_hi=7,final=None,meterbeats=4,step=1):
    tot=NB*meterbeats; n=int(tot*4)
    grid=[[None]*n for _ in range(NV)]   # (pitch, onset?)
    theme=[[False]*n for _ in range(NV)]
    labels=[]
    for t0,v,f,T,oc in sorted(E):
        ns=FORMS[f]
        mean=sum(r for _,_,r in ns)/len(ns)+63+T
        k=round((CENT[v]-mean)/12) if oc is None else oc
        for t,d,r in ns:
            p=63+T+r+12*k; s=int(round((t0+t)*4)); l=int(round(d*4))
            for x in range(s,s+l):
                assert grid[v][x] is None,(v,t0,f,x)
                grid[v][x]=(p,x==s); theme[v][x]=True
        labels.append({'voice':v,'t':t0,'label':f})
    for b,(v,p) in PEDAL.items():
        s=(b-1)*meterbeats*4
        for x in range(s,s+meterbeats*4):
            if grid[v][x] is None: grid[v][x]=(p,x==s or grid[v][x-1] is None or grid[v][x-1][0]!=p); theme[v][x]=True
    # harmony per beat
    chords=[]
    for bt in range(int(tot/step)):
        b=int(bt*step//meterbeats)+1; sc=SCALES[KEY[b]]
        w={}
        for v in range(NV):
            for k in range(int(4*step)):
                x=int(bt*step*4)+k
                if grid[v][x]:
                    w[grid[v][x][0]%12]=w.get(grid[v][x][0]%12,0)+(3 if k==0 else (1.5 if k%2==0 else .5))
        best=None
        for r,kd,pcs in cands(sc):
            s=sum(val if pc in pcs else -val*1.2 for pc,val in w.items())
            s+= .8 if r==sc[0] else (.5 if r==sc[4] else 0)
            if kd=='dom7': s-=.3
            if kd=='dim': s-=.6
            if chords and chords[-1][0]==r: s+=.4
            if best is None or s>best[0]: best=(s,r,kd,pcs)
        chords.append(best[1:])
    if final:
        for bt in range(len(chords)-int(meterbeats/step),len(chords)): chords[bt]=final
    # fillers
    prevp=[None]*NV
    for bt,(r,kd,pcs) in enumerate(chords):
        b=int(bt*step//meterbeats)+1; s=int(bt*step*4); L=int(step*4)
        lt=(SCALES[KEY[b]][0]-1)%12
        for v in sorted(range(NV),key=lambda v:-v):  # bass up
            if any(grid[v][s+k] is not None for k in range(L)):
                last=[grid[v][x][0] for x in range(s,s+L) if grid[v][x]]
                prevp[v]=last[-1]; continue
            if v not in ACT.get(b,[]): prevp[v]=None; continue
            now=[(u,grid[u][s][0]) for u in range(NV) if u!=v and grid[u][s]]
            prv=[(u,grid[u][s-1][0]) for u in range(NV) if u!=v and s>0 and grid[u][s-1]]
            pd=dict(prv); nowd=dict(now)
            present={p%12 for _,p in now}
            best=None
            for p in range(CENT[v]-lo_hi,CENT[v]+lo_hi+1):
                if p%12 not in pcs: continue
                c=0
                pp=prevp[v]
                c+= abs(p-pp)*0.7 if pp is not None else abs(p-CENT[v])*.3
                if pp is not None and abs(p-pp)>7: c+=6
                if p%12 not in present: c-=2.5
                if p%12==lt and lt in present: c+=6
                if v==NV-1 and p%12!=r: c+=5
                for u,q in now:
                    if q==p: c+=6
                    if (u<v and q<p) or (u>v and q>p): c+=2.5
                    if pp is not None and u in pd:
                        a=(pd[u]-pp)%12; bb=(q-p)%12
                        if a==bb and a in(0,7) and p!=pp and q!=pd[u] and (p-pp)*(q-pd[u])>0: c+=12
                if best is None or c<best[0]: best=(c,p)
            p=best[1]; hold=prevp[v]==p and s>0 and grid[v][s-1] is not None and not theme[v][s-1]
            for k in range(L): grid[v][s+k]=(p,k==0 and not hold)
            prevp[v]=p
    return grid,theme,chords,labels
def events(grid,theme,NV,vel):
    V=[]
    for v in range(NV):
        ev=[];x=0;n=len(grid[v])
        while x<n:
            if grid[v][x] is None: x+=1;continue
            p=grid[v][x][0];s=x;x+=1
            while x<n and grid[v][x] and grid[v][x][0]==p and not grid[v][x][1]: x+=1
            ev.append({'t':s/4,'d':(x-s)/4,'p':p,'spell':SP[p%12],'v':vel(v,s/4,theme[v][s]),'gate':.95 if (x-s)>2 else .9})
        V.append(ev)
    return V
