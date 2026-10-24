import json,sys,collections
import numpy as np
NAMES=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def nm(p): return NAMES[p%12]+str(p//12-1)
def load(f):
    d=json.load(open(f)); return d
def grid(d,bar_beats=3):
    V=d['voices']; end=max(e['t']+e['d'] for v in V for e in v['events'])
    n=int(round(end*4))
    G=np.full((len(V),n),-1,int); A=np.zeros((len(V),n),bool)  # pitch sounding, attack
    for i,v in enumerate(V):
        for e in v['events']:
            s=int(round(e['t']*4)); l=int(round(e['d']*4))
            G[i,s:s+l]=e['p']; A[i,s]=True
    return G,A,n
CONS={0,3,4,7,8,9}
def dis(a,b,lowest=False):
    iv=abs(a-b)%12
    if iv in (1,2,6,10,11): return True
    if iv==5 and lowest: return True
    return False
def report(f,b0=1,b1=None,verbose=False):
    d=load(f); G,A,n=grid(d); V=d['voices']; nv=len(V)
    bl=12
    nb=n//bl
    b1=b1 or nb
    out=[]
    # per-beat sonority
    for b in range(b0-1,b1):
        for beat in range(3):
            x=b*bl+beat*4
            if x>=n: continue
            ps=[G[i,x] for i in range(nv)]
            snd=[p for p in ps if p>=0]
            pcs=sorted(set(p%12 for p in snd))
            att=sum(A[i,x] for i in range(nv))
            # dissonant pairs
            low=min(snd) if snd else None
            flags=[]
            for i in range(nv):
                for j in range(i+1,nv):
                    if ps[i]>=0 and ps[j]>=0 and dis(ps[i],ps[j],lowest=(min(ps[i],ps[j])==low)):
                        # classify
                        kind='AA' if A[i,x] and A[j,x] else ('A-held' if (A[i,x] or A[j,x]) else 'held')
                        flags.append(f"{V[i].get('abbr',V[i]['name'][:2])}{nm(ps[i])}/{V[j].get('abbr',V[j]['name'][:2])}{nm(ps[j])}[{kind}]")
            if verbose or flags:
                out.append(f"b{b+1}.{beat+1} "+' '.join(nm(p) if p>=0 else '--' for p in ps)+f"  pcs={len(pcs)} att={att} "+' '.join(flags))
    return out
def stats(f):
    d=load(f); G,A,n=grid(d); V=d['voices']; nv=len(V); bl=12
    nb=n//bl
    res={}
    # pcs per beat, 4+ share (beats where >=4 voices sounding)
    cnt=collections.Counter(); 
    full=0
    for x in range(0,n,4):
        ps=[G[i,x] for i in range(nv) if G[i,x]>=0]
        if len(ps)>=4: cnt[len(set(p%12 for p in ps))]+=1
    res['pcs_on_beats_(>=4 voices)']=dict(sorted(cnt.items()))
    # density per bar (attacks per beat)
    dens=[A[:,b*bl:(b+1)*bl].sum()/3 for b in range(nb)]
    res['density_per_bar']=[round(x,1) for x in dens]
    # parallels: consecutive attacks pairs. beat-level
    par=[]
    for i in range(nv):
        for j in range(i+1,nv):
            prev=None
            for x in range(0,n):
                if G[i,x]<0 or G[j,x]<0: prev=None; continue
                if not (A[i,x] or A[j,x]): continue
                cur=(G[i,x],G[j,x])
                if prev and prev!=cur:
                    a=(prev[1]-prev[0])%12; b=(cur[1]-cur[0])%12
                    da=np.sign(cur[0]-prev[0]); db=np.sign(cur[1]-prev[1])
                    if a==b and a in (0,5,7) and da==db and da!=0 and (x%4==0 or True):
                        # only report if both at beat-ish (x%2==0) 
                        if x%2==0: par.append((x//12+1,(x%12)/4+1,V[i].get('abbr',''),V[j].get('abbr',''),'8ve' if a==0 else ('5th' if a==5 else '4th')))
                prev=cur
    res['parallels(eighth grid)']=par
    # crossing
    cr=[]
    for x in range(n):
        ps=[G[i,x] for i in range(nv)]
        last=None
        for i in range(nv):
            if ps[i]<0: continue
            if last is not None and ps[i]>last[0]: cr.append((x//12+1,(x%12)/4+1,V[last[1]].get('abbr',''),V[i].get('abbr','')));break
            last=(ps[i],i)
    res['crossings']=cr[:20]
    # bar similarity
    sims=[]
    for a in range(nb):
        for b in range(a+1,nb):
            ra=G[:,a*bl:(a+1)*bl]; rb=G[:,b*bl:(b+1)*bl]
            s=(ra==rb).all(axis=0)
            m=(ra>=0).any(axis=0)|(rb>=0).any(axis=0)
            if (ra>=0).sum()>12:
                f=((ra==rb)&(ra>=0)).sum()/max(1,(ra>=0).sum())
                if f>0.55: sims.append((a+1,b+1,round(f,2)))
    res['similar_bars(exact pitch grid >55%)']=sims
    return res
if __name__=='__main__':
    f=sys.argv[1]; b0=int(sys.argv[2]) if len(sys.argv)>2 else 1; b1=int(sys.argv[3]) if len(sys.argv)>3 else None
    for l in report(f,b0,b1,verbose='-v' in sys.argv): print(l)
    if '-s' in sys.argv:
        for k,v in stats(f).items(): print(k,v)
