from v3.comp import *
import json
f0=dinv(0,74)
S=ln('C5:4 B4:2 D5:2 G4:2 Eb5:2 G4:2 F5:2 Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 G4:2')
CS=ln('D5:1 Eb5:1 F5:1 G5:1 Ab5:1 F5:1 G5:1 Ab5:1 G5:1 F5:1 Eb5:1 C5:1 D5:1 F5:1 G5:2 D5:2 C5:1 Bb4:1 Ab4:1 Bb4:1 C5:1 D5:1 Eb5:2 B4:2 C5:2')
def fi(p):
    r=f0(p)
    if r is None and p%12==10: r=f0(p+1)+1
    return r
inv=lambda l:[(fi(p),d) for p,d in l]
A=inv(S); CSI=inv(CS)
def toEb(l): return [(p+3+(1 if (p+3)%12 in(11,6,1) else 0),d) for p,d in l]
U=[];L=[]
def put(V,bar,line,off=0): V.append(((bar-1)*16+off,line))
put(U,1,S); put(L,3,A); put(U,3,CS,2)
put(U,5,ln('Eb5:1 D5:1 C5:1 D5:1 Eb5:2 G4:2 Ab4:1 G4:1 F4:1 G4:1 Ab4:2 C5:2 D5:1 C5:1 Bb4:1 C5:1 D5:2 F4:2 G4:1 F4:1 Eb4:1 F4:1 G4:2 Bb4:2'))
put(U,7,toEb(S)); put(L,7,toEb(CSI),2)
put(L,9,toEb(A)); put(U,9,toEb(CS),2)

def grid_of(V):
    return G(V,total=40*16)
def fill(V,O,bar,off,rh,chs,rng,above,tgt=None,start=None,end=None,seeds=4,beam=800,**kw):
    t0=(bar-1)*16+off
    seq=chs
    def ch(x):
        k=(x-t0)//4
        return CH.get(seq[k]) if 0<=k<len(seq) else None
    oth=grid_of(O) if O else [(None,False)]*(40*16)
    best=None
    for sd in range(seeds):
        try: line,c=gen(oth,rh,t0,kw.pop('pcs',CMIN) if False else kw.get('pcs_',CMIN),rng,above=above,chords=ch,seed=sd,target=(lambda t:tgt(t-t0)) if tgt else None,tw=.12,beam=beam,start=start,end=end,**{k:v for k,v in kw.items() if k!='pcs_'})
        except RuntimeError as e: continue
        if best is None or c<best[1]: best=(line,c)
    if best is None: raise SystemExit(f'fail bar {bar}')
    V.append((t0,best[0])); return best[0]
