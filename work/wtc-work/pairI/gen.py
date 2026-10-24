"""Beam-search counterpoint helper (used as a sketching aid; results are reviewed and edited by hand)."""
from cp import *
import math,random
CONS={0,3,4,7,8,9}
BADMEL={6,10,11}          # tritone, m7, M7 forbidden as melodic leaps
def aug2(a,b):            # Ab-B type augmented 2nd
    return abs(a-b)==3 and {a%12,b%12} in ({8,11},{1,4},{3,6})
def gen(other, rhythm, t0, pcs, rng, above=True, start=None, end=None, chords=None, beam=1500, seed=0,
        canon=None, step_bias=1.0, leapcost=0.6, mindist=3, other_is_fixed=True, forbid_unison_beats=False, extra=None, target=None, tw=0.25, xrel=True, nochrom=True, sp=None, osc=1.5, runb=0.3, prev0=None):
    """other: grid list (pitch,attack) indexed by absolute 16th (may contain None).
    rhythm: durations of new line starting at t0.  pcs: allowed pitch classes (or fn(t)->set).
    chords: fn(t)->set of chord pcs or None. canon=(S,lag): derived follower = S-p delayed lag (other ignored then)."""
    random.seed(seed)
    onsets=[];t=t0
    for d in rhythm: onsets.append(t);t+=d
    T1=t
    # state: (cost, notes list, last_vertical)
    beams=[(0.0,[],None)]
    P0=prev0
    for j,(t,d) in enumerate(zip(onsets,rhythm)):
        allowed=pcs(t) if callable(pcs) else pcs
        new=[]
        for cost,notes,lastv in beams:
            prev=notes[-1] if notes else P0
            cands=range(rng[0],rng[1]+1)
            for p in cands:
                if p%12 not in allowed: continue
                if j==0 and start is not None and p!=start: continue
                if j==len(rhythm)-1 and end is not None and p!=end: continue
                c=cost
                if prev is not None:
                    mv=abs(p-prev)
                    if mv%12 in BADMEL and mv!=12 or mv>12 or aug2(p,prev): continue
                    if nochrom and mv==1 and SPELL[p%12][0]==SPELL[prev%12][0]: continue
                    if mv==0: c+=2.5
                    elif mv<=2: c+=0
                    else: c+=leapcost*mv/2*step_bias
                    if len(notes)>=2:
                        pm=notes[-2];l1=prev-pm
                        if abs(l1)>=5 and not (0<abs(p-prev)<=2 and (p-prev)*l1<0): c+=4
                        if abs(l1)>=3 and abs(p-prev)>=3 and (p-prev)*l1>0: c+=3   # two leaps same dir
                        if p==pm: c+=osc
                        if len(notes)>=3 and p==notes[-2] and prev==notes[-3]: c+=3
                        if 0<abs(l1)<=2 and 0<abs(p-prev)<=2 and l1*(p-prev)>0: c-=runb
                    # pending dissonance must resolve by step
                ok=True;lv=lastv
                for x in range(t,t+d):
                    if canon:
                        S,lag=canon;k=x-lag;q=None;qa=False
                        if k>=t0:
                            # find lead note at k
                            if k>=t: q=(S(p) if callable(S) else S-p);qa=(k==t)
                            else:
                                for jj in range(len(notes)-1,-1,-1):
                                    if onsets[jj]<=k: q=(S(notes[jj]) if callable(S) else S-notes[jj]);qa=(onsets[jj]==k);break
                        oa=qa
                    else:
                        if x>=len(other) or other[x][0] is None: lv=None;continue
                        q,oa=other[x]
                    if q is None: continue
                    a=(x==t)
                    if not(a or oa): continue
                    up,lo=(p,q) if above else (q,p)
                    if canon: up,lo=max(p,q),min(p,q)
                    if not canon and up-lo<mindist: ok=False;break
                    if canon and up-lo<1 and x%4==0: c+=2
                    i=(up-lo)%12
                    if x%2==0 and i not in CONS:
                        if x%4==0: ok=False;break
                        # offbeat 8th: allow only passing (step approach) in the new voice
                        if not(a and prev is not None and 0<abs(p-prev)<=2) and not(not a and oa): ok=False;break
                        c+=1.5
                    if x%2==1 and i not in CONS:
                        if a and not(prev is not None and 0<abs(p-prev)<=2): ok=False;break
                    if x%4==0 and i in(0,7): c+=0.8
                    if x%16==0 and i in(3,4,8,9): c-=0.3
                    if lv and lv!=(up,lo):
                        pi=(lv[0]-lv[1])%12
                        if pi==i and i in(0,7) and (up-lv[0])*(lo-lv[1])>0: ok=False;break
                        if i in(0,7) and x%4==0 and (up-lv[0])*(lo-lv[1])>0 and abs(p-(prev or p))>2: c+=1.5
                    lv=(up,lo)
                    if chords and x%4==0:
                        ch=chords(x)
                        if ch and p%12 not in ch: c+= 3 if x%8==0 else 1.2
                        if canon and ch and q is not None and qa and q%12 not in ch: c+=1.5 if x%8==0 else 0.6
                if not ok: continue
                if target: c+=tw*abs(p-target(t))
                if xrel and not canon:
                    L=SPELL[p%12][0]
                    for x in range(max(0,t-3),min(len(other),t+d+3)):
                        q=other[x][0]
                        if q is not None and SPELL[q%12][0]==L and q%12!=p%12: c+=5;break
                if extra: c+=extra(t,d,p,notes)
                c+=random.random()*0.05
                new.append((c,notes+[p],lv))
        if not new: raise RuntimeError(f'dead end at note {j} t={t}')
        new.sort(key=lambda s:s[0])
        # diversity: limit identical last-3 tails
        seen={};nb=[]
        for s in new:
            k=tuple(s[1][-4:])
            if seen.get(k,0)>=2: continue
            seen[k]=seen.get(k,0)+1;nb.append(s)
            if len(nb)>=beam:break
        beams=nb
    best=beams[0]
    return list(zip(best[1],rhythm)),best[0]
def dinv(tonic,K,scale=(0,2,3,5,7,8,11)):
    sc=[(tonic+i)%12 for i in scale]
    def f(p):
        r=(p-tonic)%12
        if (p%12) not in sc: return None
        d=7*((p-tonic)//12)+scale.index(r)
        d2=K-d; o,i=divmod(d2,7)
        return tonic+12*o+scale[i]
    return f
def G(lines,total=None):
    """concatenate list of (start16, line) into a grid"""
    end=max(s+length(l) for s,l in lines) if total is None else total
    g=[(None,False)]*end
    for s,l in lines:
        for k,v in enumerate(grid(l)): g[s+k]=v
    return g

def interp(pts):
    def f(t):
        for (t0,p0),(t1,p1) in zip(pts,pts[1:]):
            if t0<=t<=t1: return p0+(p1-p0)*(t-t0)/max(1,t1-t0)
        return pts[-1][1] if t>pts[-1][0] else pts[0][1]
    return f
