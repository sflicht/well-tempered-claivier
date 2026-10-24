# Prelude I in C minor - v1. RH: unbroken 16th broken chords (rocking figure); LH: 8th-note bass + tenor.
# Wedge hint: in b9-14 and b24-29 the outer voices spread by half steps (bass falls, top rises).
from lit import parse_tok
def pn(s): return parse_tok(s+':1')[0]
NM={0:'C',1:'Db',2:'D',3:'Eb',4:'E',5:'F',6:'F#',7:'G',8:'Ab',9:'A',10:'Bb',11:'B'}
def nm(p,sp=None):
    sp=sp or NM; return f"{sp[p%12]}{p//12-1}"
# half-bar chord: (bass, tenor, x, [a,b,c,d], figure)
F1=[0,2,1,3,2,3,1,2]      # rocking up
F2=[3,2,1,2,0,1,2,1]      # falling back
F3=[0,1,2,3,1,2,3,2]      # climbing
def H(b,t,x,rh,fig=None): return (b,t,x,rh.split(),fig)
CH=[]
def bar(h1,h2=None):
    h2=h2 or (h1[0],h1[1],h1[2],h1[3],None)
    CH.append((h1,h2))
# A: C minor (b1-8)
bar(H('C3','G3','Eb3','Eb4 G4 C5 Eb5'))
bar(H('C3','Ab3','F3','F4 Ab4 C5 F5'))
bar(H('B2','G3','D3','D4 F4 Ab4 D5'),H('B2','G3','F3','D4 F4 G4 D5'))
bar(H('C3','G3','Eb3','Eb4 G4 C5 Eb5'),H('Bb2','G3','E3','E4 G4 C5 E5'))
bar(H('Ab2','F3','C3','F4 Ab4 C5 F5'))
bar(H('A2','F#3','C3','Eb4 F#4 C5 Eb5'),H('Ab2','F3','C3','D4 F4 B4 D5'))
bar(H('G2','D3','B2','D4 G4 B4 D5'),H('G2','F3','B2','D4 F4 B4 D5'))
bar(H('C3','G3','Eb3','Eb4 G4 C5 Eb5'),H('C3','G3','Eb3','C4 Eb4 G4 C5'))
# B: the wedge in the outer voices (b9-14): bass C B Bb A Ab G / top Eb E F F# G Ab
bar(H('C3','G3','Eb3','C4 G4 C5 Eb5'))
bar(H('B2','G3','E3','C4 G4 C5 E5'))
bar(H('Bb2','F3','D3','Ab4 Bb4 D5 F5'))
bar(H('A2','F#3','C3','A4 C5 D5 F#5'))
bar(H('Ab2','Eb3','C3','Eb4 G4 C5 G5'))
bar(H('G2','D3','B2','F4 B4 D5 Ab5'),H('G2','D3','F3','F4 B4 D5 G5'))
# C: towards Eb major (b15-20), circle of fifths
bar(H('C3','G3','Eb3','Eb4 G4 C5 Eb5'),H('C3','Bb3','E3','E4 G4 Bb4 E5'))
bar(H('F3','C4','Ab3','F4 Ab4 C5 F5'),H('F3','Eb3','A3','F4 A4 C5 Eb5'))
bar(H('Bb2','F3','D3','F4 Bb4 D5 F5'),H('Bb2','Ab3','D3','F4 Ab4 D5 F5'))
bar(H('Eb3','Bb3','G3','G4 Bb4 Eb5 G5'),H('Eb3','Bb3','G3','G4 Bb4 D5 G5'))
bar(H('Ab2','Eb3','C3','Ab4 C5 Eb5 G5'),H('A2','Eb3','C3','F#4 C5 Eb5 F#5'))
bar(H('Bb2','F3','D3','F4 Bb4 D5 F5'),H('Bb2','Ab3','D3','F4 Ab4 D5 F5'))
# D: Eb -> Fm -> back to C minor (b21-23)
bar(H('Eb3','Bb3','G3','G4 Bb4 Eb5 G5'),H('Db3','Bb3','G3','G4 Bb4 Eb5 G5'))
bar(H('C3','Ab3','F3','F4 Ab4 C5 F5'),H('B2','Ab3','F3','D4 F4 Ab4 D5'))
bar(H('C3','G3','Eb3','Eb4 G4 C5 Eb5'),H('D3','Ab3','F3','D4 F4 Ab4 C5'))
# E: dominant pedal; wedge again, wider: top rises G5 Ab5 A5 Bb5 B5 C6 over G pedal, inner line falls
bar(H('G2','D3','B2','D4 F4 B4 G5'))
bar(H('G2','D3','F3','B4 D5 F5 Ab5'))
bar(H('G2','Eb3','C3','C5 Eb5 F#5 A5'))
bar(H('G2','D3','Bb2','Bb4 D5 G5 Bb5'))
bar(H('G2','D3','F3','Ab4 B4 F5 B5'))
bar(H('G2','Eb3','C3','G4 C5 Eb5 C6'),H('G2','D3','B2','F4 B4 D5 B5'))
# F: coda on a tonic pedal, plagal colour, Picardy close
bar(H('C2','G2','Eb3','C4 Eb4 G4 C5'),H('C2','Bb2','E3','Bb3 E4 G4 Bb4'))
bar(H('C2','Ab2','F3','C4 F4 Ab4 C5'),H('C2','Ab2','F3','B3 D4 F4 Ab4'))
bar(H('C2','G2','Eb3','C4 Eb4 G4 C5'),H('C2','G2','E3','C4 E4 G4 C5'))
import itertools
CONS={0,3,4,7,8,9}
FIGSET=[F1,F2,F3,[0,3,1,2,0,3,1,2],[1,3,2,3,0,3,2,3],[3,1,2,0,3,1,2,1],[0,2,3,1,2,3,0,2],[2,0,1,3,1,2,0,3]]
LHSET=[(0,1,2,1),(0,2,1,2),(0,1,0,2),(0,2,0,1)]
def halfcost(rr,lh,fig,lo,prevpairs):
    # rr: rh pitches; lh: 4 lh pitches (8ths). Evaluate on 8th grid (4 points) and 16th successions
    c=0;pairs=[]
    for k in range(4):
        u=rr[fig[2*k]];l=lh[k];i=(u-l)%12
        pairs.append((u,l))
        if k%2==0 and i not in CONS: c+=4
        elif i in (1,11): c+=3
        elif i not in CONS: c+=0.5
    allp=prevpairs+pairs
    for (u0,l0),(u1,l1) in zip(allp,allp[1:]):
        i0=(u0-l0)%12;i1=(u1-l1)%12
        if i0==i1 and i0 in (0,7) and (u1-u0)*(l1-l0)>0: c+=5
        if i0==i1 and i0 in (0,7) and u0==u1 and l0==l1: c+=0.5
    # 16th-level: rh offbeat 16th vs lh held note, parallel octave by 16ths
    seq=[]
    for j in range(8): seq.append((rr[fig[j]],lh[j//2]))
    for (u0,l0),(u1,l1) in zip(seq,seq[1:]):
        if (u0-l0)%12==0 and (u1-l1)%12==0 and u0!=u1 and l0!=l1: c+=4
    return c,pairs
U=[];L=[];prevpairs=[];prevfig=None
for i,(h1,h2) in enumerate(CH):
    toks=[];lt=[]
    for k,h in enumerate((h1,h2)):
        b,t,x,rh,fig=h
        rr=[pn(s) for s in rh]; tri=[pn(b),pn(t),pn(x)]
        best=None
        for fg in FIGSET:
            for lo in LHSET:
                lh=[tri[j] for j in lo]
                c,pairs=halfcost(rr,lh,fg,lo,prevpairs[-1:])
                if fg is prevfig: c+=0.6
                if fg in (F1,F2): c-=0.4
                if best is None or c<best[0]: best=(c,fg,lh,pairs)
        c,fg,lh,pairs=best; prevpairs=pairs; prevfig=fg
        toks+=[nm(rr[j]) for j in fg]; lt+=[nm(p) for p in lh]
    U.append(' '.join(f"{s}:1" for s in toks))
    L.append(' '.join(f"{s}:2" for s in lt))
U.append('C4:1 E4:1 G4:1 C5:1 E5:12'); L.append('C2:4 G2:4 C3:8')
TAG='Prelude I v1'
BPM=72
