exec(open('v5/head.py').read())
EbM={3,5,7,8,10,0,2}; FMIN={5,7,8,10,0,1,4,3}; GMIN={7,9,10,0,2,3,6,5}
CH.update({'Gm':{7,10,2},'D7':{2,6,9,0},'Ao':{9,0,3,7},'Cm7':{0,3,7,10},'Eb7':{3,7,10,1}})
# undo v2 E1 (keep exposition + Eb entries); new E1 b5-6: head-motif sequence, varied rhythm
U=[x for x in U if x[0]!=4*16]
put(U,5,ln('Eb5:3 D5:1 F5:2 B4:2 C5:1 D5:1 Eb5:2 F5:3 Eb5:1 G5:2 Bb4:2 D5:1 Eb5:1 F5:2 G5:4 F5:2 Ab5:2'))
fill(L,U,5,0,[4,2,2,1,1,2,4,4,2,2,4,2,2],['Cm','Cm','Fm','Fm','Bb7','Bb7','Eb','Eb'],(41,58),False,tgt=lambda t:50-t//8,start=48,pcs_=CMIN)
# E2 b11-12 (upper line kept from v2), lower in mixed values
put(U,11,ln('G5:1 F5:1 Eb5:1 D5:1 Eb5:2 Bb4:2 C5:1 Db5:1 Eb5:1 C5:1 Ab4:2 C5:2 Bb4:1 C5:1 Db5:1 Bb4:1 G4:2 E5:2 F5:1 E5:1 G5:1 Bb5:1 E5:2 G5:2'))
fill(L,U,11,0,[3,1,2,2,4,2,2,1,1,2,4,4,4],['Eb','Eb','Ab','Ab','Go7','Go7','C7','D7'],(40,57),False,tgt=lambda t:48,pcs_=FMIN|{2,6,9})
# b13-16 CANON PER AUGMENTATIONEM in G minor: L = subject augmented from G2; U = subject (G5) then its inversion from D6
aug=lambda l:[(p,2*d) for p,d in l]
put(L,13,aug(tr(S,-17)))
put(U,13,tr(S,7))
Ig=[(p+7+12,d) for p,d in A]  # inversion, G-minor, high
fill(U,L,15,0,[2,1,1,2,2,3,1,4, 1,1,1,1,2,2,1,1,2,4],['Gm','Gm','Cm','Cm','D7','D7','Gm','Gm'],(67,91),True,tgt=lambda t:86-t//3,pcs_=GMIN,start=86)
# E3 b17-18 G minor -> F minor: falling 5ths sequence from CS cell, syncopated
fill(U,L,17,0,[3,1,2,2,3,1,2,2,3,1,2,2,4,4],['Gm','Cm7','Cm7','F','Bb','Eb','Eb','Ab'],(64,86),True,tgt=lambda t:82-t//3,pcs_=EbM|{9})
fill(L,U,17,0,[2,2,4,2,2,4,2,2,4,1,1,2,4],['Gm','Cm7','Cm7','F','Bb','Eb','Db','C7'],(38,58),False,tgt=lambda t:50-t//4,pcs_=FMIN|{9,2})
# b19-24 canon by inversion, F minor, WIDE range, mixed rhythm
fc=dinv(5,67)
crh=[4,2,1,1,2,2, 3,1,2,2,4, 1,1,1,1,2,2,4, 2,2,1,1,1,1,4]*3
tot=0;R=[]
for d in crh:
    if tot+d>88: break
    R.append(d);tot+=d
if tot<88: R.append(88-tot)
noerep=lambda t,d,p,notes:(40 if notes and p==notes[-1] else 0)+(3 if len(notes)>=3 and p in notes[-3:-1] else 0)
t0=18*16
def chc(x):
    k=(x-t0)//8; seq=['Fm','Fm','Bbm','C7','Fm','Db','Bbm','Go7','C7','Fm','Do','C7']
    return CH.get(seq[k]) if 0<=k<len(seq) else None
best=None
for sd in range(6):
    try: line,c=gen(None,R,t0,FMIN-{3},(58,88),canon=(fc,8),chords=chc,seed=sd,start=72,target=lambda t:[72,79,84,86,80,72,65,60,62,67,70][min(10,(t-t0)//8)],tw=.5,beam=1500,extra=noerep,osc=4,runb=1.2)
    except RuntimeError as e: print(e);continue
    if best is None or c<best[1]: best=(line,c)
CAN=best[0]; U.append((t0,CAN)); L.append((t0+8,[(fc(p),d) for p,d in CAN]))
fill(L,U,19,0,[2,2,2,2],['Fm','Fm'],(41,57),False,start=41)
print('CANON',nm_line(CAN), min(p for p,d in CAN),max(p for p,d in CAN))
# b24.3 - 26 BUILD: rising sequence over chromatic bass climb, accelerating rhythm, to V
fill(U,L,24,8,[1]*8,['Fm','C7'],(65,84),True,tgt=lambda t:72,pcs_=FMIN)
fill(U,L,25,0,[4,2,2, 2,2,1,1,2, 1,1,2,1,1,2, 1,1,1,1,1,1,1,1],['Cm','Cm','Ab','Ab','Fm','D7','G7','G7'],(67,88),True,tgt=lambda t:70+t//2,end=83,pcs_=CMIN|{6,9})
put(L,25,ln('C3:4 Bb2:4 Ab2:4 C3:4 F2:2 Ab2:2 F#2:2 C3:2 G2:2 F2:2 Eb2:2 D2:2'))
# b27-28 PEAK: subject at C6 + inversion a QUARTER later (densest stretto), over V tension
put(U,27,tr(S,12)[:15]+ln('C6:1 D6:1 Eb6:1 F6:1'))
_a=[];_t=0
for p,d in A:
    if _t+d>=26: _a.append((p-12,26-_t)); break
    _a.append((p-12,d)); _t+=d
put(L,27,_a+ln('G2:2'),4)
put(L,27,ln('C3:4'))
# b29 deceptive + Neapolitan; b30 bariolage on V
put(U,29,ln('G6:4'))
fill(U,L,29,4,[1,1,1,1,2,2,1,1,1,1],['Ab','Db','Db'],(68,92),True,tgt=lambda t:86-t,start=86,pcs_=CMIN|{1})
put(L,29,ln('Ab2:2 C3:2 Eb3:2 C3:2 F2:2 Ab2:2 Db3:2 F3:2'))
put(L,30,ln('G2:1 B2:1 G2:1 D3:1 G2:1 F3:1 G2:1 Ab3:1 G2:1 F3:1 G2:1 D3:1 G2:1 F3:1 D3:1 G2:1'))
fill(U,L,30,0,[2,1,1,2,1,1,1,1,1,1,2,2],['G7','G7','G7','G7'],(65,84),True,tgt=lambda t:79-t//2,end=71,pcs_=CMIN)
# b31-33 final stretto over TONIC PEDAL (extra pedal voice), then minor close without pedal
put(U,31,S)
put(L,31,ln('R:8'))
put(L,31,tr(S,-12),8)
put(L,33,ln('Ab3:2 F3:1 Ab3:1 G3:2 G2:2'),8)
put(U,33,ln('D5:2 Eb5:2 G5:2 Eb5:2 C5:1 Bb4:1 Ab4:1 C5:1 D5:2 B4:2'))
put(U,34,ln('C5:4 G4:4 Eb4:8')); put(L,34,ln('C3:8 C2:8'))
open('v5/lit.txt','w').write('\n'.join(dump(U,'U')+dump(L,'L'))+'\n') if False else None
def dump(V,name):
    return [f"put({name},{st//16+1},'{nm_line(l)}',{st%16})" for st,l in sorted(V,key=lambda z:z[0])]
open('v5/lit.txt','w').write('\n'.join(dump(U,'U')+dump(L,'L'))+'\n')
