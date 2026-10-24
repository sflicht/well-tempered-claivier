"""Implied-voice check for the prelude (analysis). A hand playing continuous 16ths is split per beat into
 implied BASS (lowest note of the 4-note beat group) and implied TOP (highest note). The sixteenth-grid checks in chk.py
 see each hand as ONE line; this adds: (a) tertian-chord fit of each beat group of the 16th hand, (b) 5ths/8ves between the
 implied bass of the 16th hand and the melody hand on successive beats, (c) the same for implied top, (d) implied-bass leaps
 (> a 6th) between beats, (e) implied bass/top crossing the other hand at beat starts."""
import sys,numpy as np
from chk import load,nm,chords_for
d,G,A,SP,bl,nb=load(sys.argv[1]);n=G.shape[1]
out={'nonfit':[],'par_bass':[],'par_top':[],'bass_leap':[],'cross':[],'groups':0,'fit':0}
for h,o in((0,1),(1,0)):
    seq=[]  # per beat: (low, high) of hand h, plus o's sounding note at beat start
    for x in range(0,n,4):
        if A[h,x:x+4].sum()<4: seq.append(None);continue          # not a 16th beat for this hand
        ps=[int(G[h,x+k]) for k in range(4)]
        out['groups']+=1
        if chords_for({p%12 for p in ps}) or len({p%12 for p in ps})<3: out['fit']+=1
        else: out['nonfit'].append(f"b{x//bl+1}.{(x%bl)//4+1} {'RH' if h==0 else 'LH'} {'/'.join(nm(p) for p in ps)}")
        seq.append((min(ps),max(ps),int(G[o,x]) if G[o,x]>=0 else None,x))
    prev=None
    for s in seq:
        if s is None: prev=None;continue
        lo,hi,om,x=s
        if om is not None:
            if om<lo and h==1: pass
            if h==0 and om>lo: out['cross'].append(f"b{x//bl+1}.{(x%bl)//4+1} RH-16ths dips below LH")
            if h==1 and om<hi and om>lo: pass
        if prev:
            plo,phi,pom,px=prev
            if om is not None and pom is not None:
                for nmx,a1,a2,b1,b2 in(('bass',plo,pom,lo,om),('top',phi,pom,hi,om)):
                    ia=(a2-a1)%12;ib=(b2-b1)%12
                    if ia==ib and ia in(0,7,5) and np.sign(b1-a1)==np.sign(b2-a2)!=0 and a1!=a2:
                        out['par_'+nmx].append(f"b{x//bl+1}.{(x%bl)//4+1} {nm(a1)}/{nm(a2)}->{nm(b1)}/{nm(b2)}")
            if abs(lo-plo)>9: out['bass_leap'].append(f"b{x//bl+1}.{(x%bl)//4+1} {nm(plo)}->{nm(lo)}")
        prev=s
print('16th-groups checked',out['groups'],'chord-fit',out['fit'])
for k in('nonfit','par_bass','par_top','bass_leap','cross'): print(k,len(out[k]),out[k])
