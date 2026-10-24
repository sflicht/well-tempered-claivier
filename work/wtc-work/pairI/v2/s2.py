from v2.comp import *
import json
f0=dinv(0,74)
S=ln('C5:4 B4:2 D5:2 Ab4:2 Eb5:2 G4:2 F5:2 Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 G4:2')
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
    return G(V,total=34*16)
def fill(V,O,bar,off,rh,chs,rng,above,tgt=None,start=None,end=None,seeds=4,beam=800,**kw):
    t0=(bar-1)*16+off
    seq=chs
    def ch(x):
        k=(x-t0)//4
        return CH.get(seq[k]) if 0<=k<len(seq) else None
    oth=grid_of(O) if O else [(None,False)]*(34*16)
    best=None
    for sd in range(seeds):
        try: line,c=gen(oth,rh,t0,kw.pop('pcs',CMIN) if False else kw.get('pcs_',CMIN),rng,above=above,chords=ch,seed=sd,target=(lambda t:tgt(t-t0)) if tgt else None,tw=.12,beam=beam,start=start,end=end,**{k:v for k,v in kw.items() if k!='pcs_'})
        except RuntimeError as e: continue
        if best is None or c<best[1]: best=(line,c)
    if best is None: raise SystemExit(f'fail bar {bar}')
    V.append((t0,best[0])); return best[0]
EbM={3,5,7,8,10,0,2}; FMIN={5,7,8,10,0,1,4,3}; GMIN={7,9,10,0,2,3,6,5}
# E1 lower (b5-6) 8ths
fill(L,U,5,0,[2]*16,['Cm','Cm','Fm','Fm','Bb7','Bb7','Eb','Eb'],(41,57),False,tgt=lambda t:52-t//6,start=48)
# E2 (b11-12) upper free 16th/8th line, then lower 8ths
put(U,11,ln('G5:1 F5:1 Eb5:1 D5:1 Eb5:2 Bb4:2 C5:1 Db5:1 Eb5:1 C5:1 Ab4:2 C5:2 Bb4:1 C5:1 Db5:1 Bb4:1 G4:2 E5:2 F5:1 E5:1 G5:1 Bb5:1 E5:2 G5:2'))
fill(L,U,11,0,[2]*16,['Eb','Eb','Ab','Ab','Go7','Go7','C7','C7'],(41,57),False,tgt=lambda t:50,pcs_=FMIN|{2})
# canon b13 - 18.2 : lead upper, follower = dinv(5,67) lag 8
fc=dinv(5,67)
crh=[2,2,1,1,2, 1,1,1,1,2,2, 2,1,1,1,1,2, 1,1,2,2,2]*4
tot=0;R=[]
for d in crh:
    if tot+d>88: break
    R.append(d);tot+=d
if tot<88: R.append(88-tot)
noerep=lambda t,d,p,notes:(40 if notes and p==notes[-1] else 0)+(6 if notes and abs(p-notes[-1])>7 else 0)+(3 if len(notes)>=3 and p in notes[-3:-1] else 0)
t0=12*16
def chc(x):
    k=(x-t0)//8; seq=['Fm','Fm','Bbm','C7','Fm','Db','Bbm','Go7','C7','Fm','Do','C7']
    return CH.get(seq[k]) if 0<=k<len(seq) else None
best=None
for sd in range(6):
    try: line,c=gen(None,R,t0,FMIN-{3},(62,80),canon=(fc,8),chords=chc,seed=sd,start=72,target=lambda t:[72,75,79,80,77,74,70,67,65,65][min(9,(t-t0)//10)],tw=.35,beam=1500,extra=noerep,osc=4,runb=1.2)
    except RuntimeError as e: print(e);continue
    if best is None or c<best[1]: best=(line,c)
CAN=best[0]; U.append((t0,CAN)); L.append((t0+8,[(fc(p),d) for p,d in CAN]))
fill(L,U,13,0,[2,2,2,2],['Fm','Fm'],(41,57),False,start=41,end=None)
print('CANON',nm_line(CAN))

# E3 b18.3-20: F minor -> G minor (lead ended b18.2, follower ends b18.4)
fill(U,L,18,8,[1]*8,['Fm','C7'],(65,82),True,tgt=lambda t:72,pcs_=FMIN)
fill(U,L,19,0,[1,1,1,1,2,2]*2+[1,1,2]*4,['Fm','Fm','Cm','Cm','Ab','Ab','D7','D7'],(65,84),True,tgt=lambda t:72+t//6,pcs_=CMIN|{6,9})
fill(L,U,19,0,[2]*16,['Fm','Fm','Cm','Cm','Ab','Ab','D7','D7'],(40,57),False,tgt=lambda t:50-t//8,pcs_=CMIN|{6,9})
# Stretto I in G minor: subject at G5 (U) b21.1, subject at G3 (L) half bar later
put(U,21,tr(S,7)); put(L,21,tr(S,-17),8)
fill(L,U,21,0,[2,2,2,2],['Gm','D7'],(40,55),False,start=43,pcs_=GMIN)
# E4: drive (b23-24) into the dominant of C minor; U 16ths rising toward B5, L 8ths
fill(U,L,23,0,[1]*8,['Gm','Cm'],(67,86),True,tgt=lambda t:74,pcs_=GMIN|{8})
fill(U,L,23,8,[1]*24,['Cm','Ab','Fm','Do','G7','G7'],(67,88),True,tgt=lambda t:74+t//3,end=83,pcs_=CMIN)
fill(L,U,23,8,[2]*12,['Cm','Ab','Fm','Do','G7','G7'],(40,57),False,tgt=lambda t:50-t//4,end=43,pcs_=CMIN)
# PEAK b25-26: subject at C6 (U) b25.1; inversion from G2 (L) one beat later; deceptive cadence to Ab at b27.1
put(U,25,tr(S,12)[:15]+ln('C6:1 D6:1 B5:1 D6:1 F6:1 D6:1'))
put(L,25,ln('C3:2 Eb3:2 G2:4 Ab2:2 F2:2 B2:2 Eb2:2 C3:2 D2:2 G2:1 Ab2:1 G2:1 Eb2:1 D2:1 Eb2:1 F2:1 Ab2:1 G2:4'))
# E5 b27-28: deceptive Ab, Neapolitan, dominant implied by re-struck G2 (bariolage)
put(U,27,ln('C6:4'))
fill(U,L,27,4,[1,1,1,1,2,2,1,1,1,1],['Ab','Db','Db'],(68,86),True,tgt=lambda t:82-t//2,start=82,pcs_=CMIN|{1})
put(L,27,ln('Ab2:2 C3:2 Eb3:2 C3:2 F2:2 Ab2:2 Db3:2 F3:2'))
put(L,28,ln('G2:1 B2:1 G2:1 D3:1 G2:1 F3:1 G2:1 Ab3:1 G2:1 F3:1 G2:1 D3:1 G2:1 F3:1 D3:1 G2:1'))
fill(U,L,28,0,[2,1,1,2,1,1,1,1,1,1,2,2],['G7','G7','G7','G7'],(65,84),True,tgt=lambda t:79-t//2,end=71,pcs_=CMIN)
# Final cadential stretto b29-31: subject C5 (U), subject C4 (L) half a bar later; re-struck C bass first
put(U,29,S)
put(L,29,ln('C3:1 G2:1 C3:1 Eb3:1 G2:1 D3:1 G3:1 F3:1'))
put(L,29,tr(S,-12),8)
put(L,31,ln('Ab3:2 F3:1 Ab3:1 G3:2 G2:2'),8)
put(U,31,ln('D5:2 Eb5:2 G5:2 Eb5:2 C5:1 Bb4:1 Ab4:1 C5:1 D5:2 B4:2'))
put(U,32,ln('C5:16')); put(L,32,ln('C3:16'))
json.dump({'U':U,'L':L},open('v2/stage.json','w'))
def dump(V,name):
    out=[]
    for st,l in sorted(V,key=lambda z:z[0]):
        out.append(f"put({name},{st//16+1},'{nm_line(l)}',{st%16})")
    return out
open('v2/lit.txt','w').write('\n'.join(dump(U,'U')+dump(L,'L'))+'\n')
