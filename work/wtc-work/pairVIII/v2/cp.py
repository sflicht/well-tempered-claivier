import random
from forms import FORMS, MIN, MAJ
Q={'maj':(0,4,7),'min':(0,3,7),'dim':(0,3,6),'dom7':(0,4,7,10),'dim7':(0,3,6,9),'hdim7':(0,3,6,10),'min7':(0,3,7,10)}
CONS={0,3,4,7,8,9}
class Score:
    def __init__(s,nv,nbeats,cent):
        s.nv=nv;s.n=nbeats*4;s.nb=nbeats;s.cent=cent
        s.G=[[-1]*s.n for _ in range(nv)];s.A=[[False]*s.n for _ in range(nv)];s.TH=[[None]*s.n for _ in range(nv)]
        s.H=[None]*nbeats  # (root_pc, qual, bass_pc or None, scale pcs)
        s.labels=[];s.ignore=set()
    def chord(s,b,root,q,bass=None,scale=None,force=False):
        pcs={(root+x)%12 for x in Q[q]}
        if scale is None: scale={(root+x)%12 for x in (MAJ if q in('maj','dom7') else MIN)}|pcs
        if s.H[b] and not force:
            assert s.H[b][4]==pcs,('chord conflict beat',b,s.H[b],pcs)
            return
        s.H[b]=(root%12,q,bass,set(scale)|pcs,pcs)
    def note(s,v,t,d,p,lab=None):
        a=int(round(t*4));l=int(round(d*4))
        for x in range(a,a+l):
            assert s.G[v][x]<0,('overlap',v,t,p)
            s.G[v][x]=p;s.TH[v][x]=lab
        s.A[v][a]=True
    def place(s,form,v,beat,T,mode_key,octv,lab=None,chords=True,trunc=None,keymode='min'):
        ns,cs=FORMS[form]
        for t,d,r in ns:
            if trunc is not None and t>=trunc: break
            if trunc is not None: d=min(d,trunc-t)
            s.note(v,beat+t,d,mode_key+T+r+12*octv,lab or form)
        if chords:
            sc={(mode_key+x)%12 for x in (MAJ if keymode=='maj' else MIN)}
            for b,rt,q in cs:
                if trunc is not None and b>=trunc: break
                s.chord(int(beat+b),mode_key+T+rt,q,scale=None)
        s.labels.append({'voice':v,'t':beat,'label':lab or form})
    def sounding(s,x,ex):
        return [(u,s.G[u][x]) for u in range(s.nv) if u!=ex and s.G[u][x]>=0 and u not in s.ignore]
def dis(a,b,lowest):
    iv=abs(a-b)%12
    return iv not in CONS and not (iv==5 and not lowest) and not(iv==6 and False)
PAT=[(1,),(.5,.5),(.5,.25,.25),(.25,.25,.5),(.75,.25),(1.5,'tie'),('tie',)]
def fill(S,v,b0,b1,bass=False,beam=120,seed=0,activity=1.0,start=None,hi=None,lo=None):
    """Beam-search a free melodic line for voice v over beats [b0,b1)."""
    rnd=random.Random(seed*7919+v*31+b0)
    c=S.cent[v]; lo=lo or c-9; hi=hi or c+9
    prev=start
    if prev is None and b0>0 and S.G[v][b0*4-1]>=0: prev=S.G[v][b0*4-1]
    beams=[(0.0,[],prev,0,(b0*4-1 if prev is not None else None))]  # cost, notes[(t,d,p)], last p, last dir, last-attack pair map
    pats=[(1,),(.5,.5),(.5,.25,.25),(.25,.25,.5),(.75,.25),('tie',)]
    for b in range(b0,b1):
        H=S.H[b]; root,q,bp,scale,pcs=H
        new=[]
        for cost,notes,lp,ld,lpt in beams:
            for pat in pats:
                if pat==('tie',):
                    if lp is None or not notes: continue
                    seqs=[[lp]]; durs=[1]
                else:
                    durs=list(pat); seqs=None
                cands=_cands(S,v,b,durs,lp,ld,lo,hi,scale,pcs,bass,bp,seqs,rnd,lpt)
                for cc,ps in cands:
                    pc=0 if pat!=('tie',) else 0
                    if pat==(1,): pc+=0.6*(1/activity)
                    if len(pat)==3: pc+=0.4*activity
                    tot=cost+cc+pc+rnd.random()*0.3
                    nn=notes+[(b+sum(durs[:i]),durs[i],ps[i],pat==('tie',)) for i in range(len(durs))]
                    d=ps[-1]-(ps[-2] if len(ps)>1 else (lp if lp is not None else ps[-1]))
                    new.append((tot,nn,ps[-1],(d>0)-(d<0),(b*4+int(round(sum(durs[:-1])*4))) if pat!=('tie',) else lpt))
        new.sort(key=lambda z:z[0])
        seen=set();beams=[]
        for z in new:
            k=(z[2],z[3],tuple(n[2] for n in z[1][-3:]))
            if k in seen: continue
            seen.add(k);beams.append(z)
            if len(beams)>=beam: break
    nxt=S.G[v][b1*4] if b1*4<S.n else -1
    if nxt>=0:
        beams=sorted(beams,key=lambda z:z[0]+(0 if abs(z[2]-nxt) in(1,2) else 1.5 if abs(z[2]-nxt)<=4 else 4 if abs(z[2]-nxt)<=7 else 12)+(15 if z[2]==nxt else 0))
    best=beams[0]
    for t,d,p,tie in best[1]:
        a=int(round(t*4));l=int(round(d*4))
        for x in range(a,a+l): S.G[v][x]=p
        if not tie: S.A[v][a]=True
    return best[0]
def _cands(S,v,b,durs,lp,ld,lo,hi,scale,pcs,bass,bp,seqs,rnd,lpt):
    out=[]
    if seqs is None:
        firsts=[p for p in range(lo,hi+1) if p%12 in pcs]
        seqs=[]
        for f in firsts:
            if lp is not None and abs(f-lp)>9: continue
            seqs.append([f])
        # extend
        for i in range(1,len(durs)):
            ns=[]
            for sq in seqs:
                q=sq[-1]
                for p in range(q-5,q+6):
                    if p==q or p<lo or p>hi: continue
                    if p%12 not in scale: continue
                    step=abs(p-q)<=2
                    if not step and p%12 not in pcs: continue
                    ns.append(sq+[p])
            seqs=ns
    for sq in seqs:
        c=_cost(S,v,b,durs,sq,lp,ld,pcs,bass,bp,scale,lpt)
        if c<1e8: out.append((c,sq))
    out.sort(key=lambda z:z[0])
    return out[:14]
def _cost(S,v,b,durs,sq,lp,ld,pcs,bass,bp,scale,lpt):
    c=0.0;t=b*4;prev=lp;pdir=ld;pt=lpt
    for i,(d,p) in enumerate(zip(durs,sq)):
        x=t;l=int(round(d*4));t+=l
        tie=(i==0 and len(sq)==1 and durs==[1] and p==lp and False)
        # melodic
        if prev is not None:
            m=p-prev;am=abs(m)
            if am==0: c+=2.5 if i>0 else 1.2
            elif am<=2: c+=0
            elif am<=4: c+=0.8
            elif am<=7: c+=2.5
            else: c+=7
            if am in(6,10,11) : c+=8
            dr=(m>0)-(m<0)
            if pdir and abs(pdir)>0 and getattr(_cost,'lastleap',0)>4 and dr==pdir: c+=4
            _cost.lastleap=am;pdir=dr
            if i>0 and p%12 not in pcs:
                # non-chord tone must be approached by step; must be on weak sub-position
                if am>2: c+=40
        onbeat=(x%4==0)
        if not (p%12 in pcs):
            if onbeat: c+=60
            # must leave by step: check next note in seq
            if i+1<len(sq):
                if abs(sq[i+1]-p)>2: c+=40
            else: c+=25  # last note of beat non-chord: risky
        # vertical over its duration
        for xx in range(x,x+l):
            snd=S.sounding(xx,v)
            if not snd: continue
            low=min([q for _,q in snd]+[p])
            att=(xx==x)
            for u,q in snd:
                iv=abs(p-q)%12
                both=att or S.A[u][xx]
                if not both: continue
                if q==p: c+=6
                if (u<v and q<p) or (u>v and q>p): c+=6
                bad=iv in(1,2,6,10,11) or (iv==5 and min(p,q)==low)
                if bad:
                    if xx%4==0: c+=45 if p%12 in pcs else 25
                    elif xx%2==0: c+=6 if iv in(1,11) else 2
                    else: c+=1
                # parallels with u
                if att and pt is not None and prev is not None and prev!=p:
                    y=pt
                    for z in range(x-1,pt,-1):
                        if S.A[u][z]: y=z;break
                    q0=S.G[u][y] if y>=0 else -1
                    if q0>=0 and q0!=q:
                        a0=abs(q0-prev)%12;a1=abs(q-p)%12
                        if a0==a1 and a0 in(0,7) and (q-q0)*(p-prev)>0: c+=80
                        elif a1 in(0,7) and (q-q0)*(p-prev)>0 and abs(p-prev)>2 and abs(q-q0)>2: c+=4
            # leading tone doubling
        if bass or not any(u>v for u,_ in S.sounding(x,v)):
            if onbeat:
                want=bp if bp is not None else S.H[b][0]
                if p%12!=want: c+=14 if x%8==0 else 6
        prev=p;pt=x
    return c
def to_events(S,vel):
    V=[]
    for v in range(S.nv):
        ev=[];x=0
        while x<S.n:
            if S.G[v][x]<0: x+=1;continue
            p=S.G[v][x];s=x;x+=1
            while x<S.n and S.G[v][x]==p and not S.A[v][x]: x+=1
            ev.append({'t':s/4,'d':(x-s)/4,'p':p,'v':vel(v,s/4,S.TH[v][s] is not None),**({'th':S.TH[v][s]} if S.TH[v][s] else {})})
        V.append(ev)
    return V
