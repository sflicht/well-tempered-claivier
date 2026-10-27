exec(open('v4/head.py').read())
CH.update({'Gm':{7,10,2},'D7':{2,6,9,0},'Ao':{9,0,3},'Ao7':{9,0,3,7},'Cm7':{0,3,7,10},'Fm7':{5,8,0,3},'Abmaj':{8,0,3},'Dm':{2,5,9},'F':{5,9,0},'Eo':{4,7,10},'Bb':{10,2,5}})
CMIN=set([0,2,3,5,7,8,11]); CNAT=set([0,2,3,5,7,8,10]); EbM={3,5,7,8,10,0,2}; FMIN={5,7,8,10,0,1,4}; GMIN={7,9,10,0,2,3,6}
S=ln('C5:4 Eb5:2 D5:2 C5:2 B4:2 C5:4 Ab5:4 G5:2 Gb5:1 F5:1 Eb5:2 D5:2 C5:4')
Sv=ln('C5:4 Eb5:2 D5:2 C5:2 B4:2 C5:4 Ab5:6 F5:1 G5:1 Eb5:2 D5:2 C5:4')   # stretto variant (leader)
D={0:3,2:3,3:4,5:3,6:3,7:3,8:4,10:4,11:3,1:3,4:3,9:3}
toMaj=lambda l:[(p+D[p%12],d) for p,d in l]   # C minor -> Eb major (degree map)
A=tr(S,-17)  # answer at the 5th below (G minor)
# --- countersubject: distinctive syncopated profile, mostly diatonic, generated once then fixed
csr=[6,1,1,2,2,4, 2,2,2,2,1,1,1,1,4]
best=None
from gen import gen
chA=lambda x:CH.get(['Gm','Gm','D7','Gm','Cm','Gm','D7','Gm'][(x-32)//4]) if 32<=x<64 else None
for sd in range(8):
    try: line,c=gen(G([(32,A)],total=40*16),csr,32,GMIN|{5},(65,82),above=True,chords=chA,seed=sd,start=74,end=70,target=lambda t:76-(t-32)//8,tw=.15,beam=1500)
    except RuntimeError: continue
    if best is None or c<best[1]: best=(line,c)
CSg=best[0]; CS=tr(CSg,5)  # CS in C minor (for subject)
print('CS(G)',nm_line(CSg))
# EXPOSITION
put(U,1,S); put(L,3,A); put(U,3,CSg)
# E1 b5-6: circle of fifths Cm-Fm-Bb-Eb, head motif in U, CS cell in L
fill(U,None,5,0,[4,2,2,2,2,4, 4,2,2,2,2,4],['Cm','Cm','Fm','Fm','Bb7','Bb7','Eb','Eb'],(67,82),True,tgt=lambda t:79-t//6,start=75,pcs_=CNAT)
fill(L,U,5,0,[2,1,1,2,2,4,2,1,1,2,2,4,4],['Cm','Cm','Fm','Fm','Bb7','Bb7','Eb','Eb'],(41,58),False,tgt=lambda t:50,start=48,pcs_=CNAT)
# RELATIVE MAJOR b7-10
put(L,7,tr(toMaj(S),-12)); CSE=toMaj(CS); put(U,7,CSE)
put(U,9,toMaj(S))
fill(L,U,9,0,[4,2,2,2,2,4,2,1,1,2,2,4,2,2],['Eb','Eb','Bb7','Eb','Ab','Eb','Bb7','Eb'],(41,60),False,tgt=lambda t:50,pcs_=EbM)
# E2 b11-12: Eb -> Ab -> Dø -> G7 -> Cm -> Fm  (circle of fifths to subdominant)
fill(U,L,11,0,[3,1,2,2,3,1,2,2,3,1,2,2,4,4],['Eb','Ab','Ab','Do','Do','G7','Cm','C7'],(65,84),True,tgt=lambda t:79-t//4,pcs_=CMIN|{10,4})
fill(L,U,11,0,[4,4,4,4,4,4,2,2,4],['Eb','Ab','Ab','Do','Do','G7','Cm','C7'],(40,57),False,tgt=lambda t:48,pcs_=CMIN|{10,4})
# b13-16 CANON PER AUGMENTATIONEM in F minor (subdominant)
aug=lambda l:[(p,2*d) for p,d in l]
put(L,13,aug(tr(S,-19)))
put(U,13,tr(S,5))
fill(U,L,15,0,[2,1,1,2,2,4, 2,2,1,1,2,4,4],['Fm','Fm','Bbm','Bbm','C7','C7','Fm','Fm'],(65,89),True,tgt=lambda t:82-t//3,pcs_=FMIN|{3},beam=2000)
# E3 b17-18 F minor -> G minor via circle of fifths
fill(U,L,17,0,[3,1,2,2,3,1,2,2,3,1,2,2,4,4],['Fm','Bb7','Bb7','Eb','Ab','Ao','D7','D7'],(64,86),True,tgt=lambda t:80-t//4,pcs_={0,2,3,5,7,8,10,6,9})
fill(L,U,17,0,[4,2,2,4,2,2,4,4,4,4],['Fm','Bb7','Bb7','Eb','Ab','Ao','D7','D7'],(38,58),False,tgt=lambda t:48,pcs_={0,2,3,5,7,8,10,6,9})
# b19-24 CANON BY INVERSION in G minor (dominant), wide range
fc=dinv(7,69)
crh=[4,2,1,1,2,2, 3,1,2,2,4, 1,1,1,1,2,2,4, 2,2,1,1,1,1,4]*3
tot=0;R=[]
for d in crh:
    if tot+d>88: break
    R.append(d);tot+=d
if tot<88: R.append(88-tot)
noerep=lambda t,d,p,notes:(40 if notes and p==notes[-1] else 0)+(3 if len(notes)>=3 and p in notes[-3:-1] else 0)
t0=18*16
def chc(x):
    k=(x-t0)//8; seq=['Gm','Gm','Cm','D7','Gm','Eb','Cm','Ao7','D7','Gm','Ao','D7']
    return CH.get(seq[k]) if 0<=k<len(seq) else None
best=None
for sd in range(6):
    try: line,c=gen(None,R,t0,GMIN,(60,88),canon=(fc,8),chords=chc,seed=sd,start=74,target=lambda t:[74,79,84,86,81,74,67,62,65,69,72][min(10,(t-t0)//8)],tw=.5,beam=1500,extra=noerep,osc=4,runb=1.2)
    except RuntimeError as e: print(e);continue
    if best is None or c<best[1]: best=(line,c)
CAN=best[0]; U.append((t0,CAN)); L.append((t0+8,[(fc(p),d) for p,d in CAN]))
fill(L,U,19,0,[4,4],['Gm','Gm'],(41,57),False,start=43,pcs_=GMIN)
print('CANON',nm_line(CAN),min(p for p,d in CAN),max(p for p,d in CAN))
fill(U,L,24,8,[2,2,2,2],['Gm','G7'],(65,80),True,tgt=lambda t:71,pcs_=CMIN,end=67)
# ---- HAND-WRITTEN BUILD b25-26 ----
put(U,25,ln('G4:2 C5:2 Eb5:2 D5:1 C5:1 B4:2 D5:2 F5:2 Eb5:1 D5:1'))
put(L,25,ln('C3:8 G2:8'))
put(U,26,ln('C5:1 D5:1 Eb5:1 F5:1 G5:1 Ab5:1 G5:1 F5:1 Eb5:1 F5:1 G5:1 A5:1 B5:1 C6:1 D6:1 B5:1'))
put(L,26,ln('Ab2:4 Eb2:4 F#2:4 G2:4'))
# ---- PEAK b27-28: subject at C6, subject two octaves below a QUARTER later ----
put(U,27,tr(Sv,12)); put(L,27,ln('C3:4')); put(L,27,tr(S,-12),4)
# b29 deceptive Ab + Neapolitan, b30 V bariolage (hand)
put(U,29,ln('Eb6:2 C6:2 F5:2 Ab5:2 Db6:2 C6:1 Bb5:1 B5:2 G5:2'))
put(L,29,ln('Ab3:4 Db3:4 G2:4'),4)
put(L,30,ln('G2:1 B2:1 G2:1 D3:1 G2:1 F3:1 G2:1 Ab3:1 G2:1 F3:1 G2:1 D3:1 G2:1 F3:1 D3:1 G2:1'))
put(U,30,ln('D6:2 B5:2 G5:2 B5:2 Eb6:2 D6:1 C6:1 B5:2 G5:2'))
# b31-32 final stretto over tonic pedal (quarter lag, octave)
put(U,31,Sv); put(L,31,ln('R:4')); put(L,31,tr(S,-12),4)
put(U,33,ln('Eb5:4 F5:2 C5:2 D5:2 B4:2 D5:2 B4:2')); put(L,33,ln('Ab3:4 G3:4 G2:4'),4)
put(U,34,ln('C5:4 G4:4 Eb4:8')); put(L,34,ln('C3:8 C2:8'))
def dump(V,name):
    return [f"put({name},{st//16+1},'{nm_line(l)}',{st%16})" for st,l in sorted(V,key=lambda z:z[0])]
open('v4/lit.txt','w').write('\n'.join(dump(U,'U')+dump(L,'L'))+'\n')
