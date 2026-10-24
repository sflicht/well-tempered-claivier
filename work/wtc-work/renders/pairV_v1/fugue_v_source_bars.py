from lib5 import *
NV=['Soprano','Alto','Tenor','Baritone','Bass','Contrabass']
N=59
BARS={v:['R:16']*N for v in NV}
def put(b,**kw):
    ab={'S':'Soprano','A':'Alto','T':'Tenor','Br':'Baritone','B':'Bass','Cb':'Contrabass'}
    for k,v in kw.items():
        v=v.strip()
        assert units(v)==16,(b,k,units(v),v)
        BARS[ab[k]][b-1]=v
def putseq(v,b,s):
    ab={'S':'Soprano','A':'Alto','T':'Tenor','Br':'Baritone','B':'Bass','Cb':'Contrabass'}
    for i,bs in enumerate(splitbars(s)): BARS[ab[v]][b-1+i]=bs
def splitbars(s):
    """cut a token string into 16-unit bars; notes crossing a barline are tied; a short last bar is padded with rest"""
    out=[];cur=[];u=0
    for t in toks(s):
        p_,d=t.split(':'); tie=d.endswith('~'); d=int(d.rstrip('~'))
        while d>0:
            room=16-u; take=min(d,room)
            rest_=(take<d)
            cur.append(f"{p_}:{take}"+('~' if (p_!='R' and (rest_ or tie)) else ''))
            u+=take; d-=take
            if u==16: out.append(' '.join(cur));cur=[];u=0
    if cur: out.append(' '.join(cur+[f"R:{16-u}"]))
    return out
SUBJ1='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4'
SUBJ2='A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
SUBJ=SUBJ1+' '+SUBJ2
CSA1='E5:2 D5:2 C#5:2 B4:2 A4:2 B4:2 C#5:2 D5:2'
CSA2='E5:3 F#5:1 A5:2 G#5:2 F#5:2 E5:2 D5:2 C#5:2'
CSA=CSA1+' '+CSA2
def subj(oct_=0): return splitbars(OCT(SUBJ,oct_) if oct_ else SUBJ)
def ans(oct_=0): return splitbars(T(SUBJ,4+7*oct_,7+12*oct_))   # E5 start for oct_=0
def csA(o=0): return splitbars(T(CSA,7*o,12*o))
def csD(o=0): return splitbars(T(CSA,-4+7*o,-7+12*o))
# --- exposition entries (fan): A subj A4 | T ans E3 | B subj A2 | S ans E5 | Br subj A3 | Cb ans E2
SA4=subj(0); AE3=ans(-2); SA2=subj(-2); AE5=ans(0); SA3=subj(-1); AE2=ans(-3)
put(1,A=SA4[0]); put(2,A=SA4[1])
put(3,T=AE3[0],A=csA()[0]); put(4,T=AE3[1],A=csA()[1])
put(5,B=SA2[0],A=csD()[0]); put(6,B=SA2[1],A=csD()[1])
put(7,S=AE5[0],A=csA(-1)[0]); put(8,S=AE5[1],A=csA(-1)[1])
put(9,Br=SA3[0],S=csD(1)[0]); put(10,Br=SA3[1],S=csD(1)[1])
put(11,Cb=AE2[0],Br=csA(-1)[0]); put(12,Cb=AE2[1],Br=csA(-1)[1])

# ===== Episode 1 (b13-16): head-cell (rising 4th + tattoo) fanfare chain, echoed in canon one beat later, then 16th waves
putseq('S',13,'A5:4 D6:2 D6:1 D6:1 F#5:4 B5:2 B5:1 B5:1 D5:4 G5:2 G5:1 G5:1 B4:4 E5:2 E5:1 E5:1')
putseq('T',13,'R:4 F#4:4 B4:2 B4:1 B4:1 D4:4 G4:2 G4:1 G4:1 B3:4 E4:2 E4:1 E4:1 E4:4')
putseq('B',13,'D3:8 B2:8 G2:8 E3:8')
putseq('S',15,'E5:1 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:1 F#5:1 G5:1 A5:1 B5:1 C#6:1 D6:2 B5:1  G5:4 B5:2 A5:2 F#5:4 E5:2 C#5:2')
putseq('T',15,'A4:2 A4:1 A4:1 A4:12  B3:8 C#4:8')
putseq('B',15,'A2:8 D3:8 G2:8 F#2:8')

# ===== M1 (b17-20): B minor subject + CS, then F# minor answer + CS
KSA={'F':1,'C':1,'G':1}
Bm=TD(SUBJ,-2); CSBm=TD(T(CSA,-4,-7),-2)
ANS=T(SUBJ,4,7); Fsm=TD(ANS,-2,KSA,KSA); CSFsm=TD(CSA,-2,KSA,KSA)
# minor-key countersubjects: the same line, with two notes recomposed where the minor mode makes a clash with the subject
CSBm='F#4:2 E4:2 D4:2 C#4:2 B3:4 D4:2 E4:2 F#4:3 G4:1 B4:2 A4:2 G4:2 E4:4 D4:2'
CSFsm='C#5:2 B4:2 A4:2 G#4:2 F#4:4 A4:2 B4:2 C#5:3 D5:1 F#5:2 E5:2 D5:4 B4:2 A4:2'
putseq('T',17,OCT(Bm,-1)); putseq('S',17,OCT(CSBm,1))
putseq('Br',19,OCT(Fsm,-2)); putseq('S',19,CSFsm)
# drum (tattoo-cell pedal) in the bass under M1
putseq('B',17,'D3:4 B2:2 B2:1 B2:1 B2:4 B2:2 B2:1 B2:1 B2:4 B2:2 B2:1 B2:1 B2:4 B2:2 B2:1 B2:1')
putseq('B',19,'F#2:4 F#2:2 F#2:1 F#2:1 F#2:4 F#2:2 F#2:1 F#2:1 F#2:4 F#2:2 F#2:1 F#2:1 F#2:4 B1:4')
# Ep2 b21-24: tresillo cascade, parallel tenths, walking-8th bass
Sc='D6:6 C#6:6 B5:4 A5:6 G5:6 F#5:4 E5:6 D5:6 C#5:4 B4:6 A4:6 G4:4'
putseq('S',21,Sc)
putseq('T',21,OCT(TD(Sc,-2),-1))
putseq('B',21,'B2:6 F#2:6 G2:4  D3:6 E3:6 F#2:4  A2:6 B2:6 F#2:4  G2:6 D3:6 G2:4')

# M2 b25-27: G/D triple stretto with CS

ls,sm=-4,-7
BASE=25
def stretto3(BASE,ls,sm,vS3='S',vS1='A',vCS='T',vS2='B',lag1=6,lag2=8):
    S1=T(SUBJ,ls,sm)
    S2=T(SUBJ,ls-3-7,sm-5-12)
    S3=T(SUBJ,ls+7,sm+12)
    CS=T(CSA,ls-4,sm-7)
    putseq(vS1,BASE,S1); putseq(vCS,BASE,CS)
    putseq(vS2,BASE,'R:%d '%lag1+S2)
    putseq(vS3,BASE,'R:%d '%(lag1+lag2)+S3)
stretto3(25,-4,-7)


# Ep3 b28-31: bariolage (inverted D pedal) over a quarter-note bass, tenor in answering 8ths
def bario(line):
    out=[]
    for n in line.split(): out+= ['D6:1',n+':1']
    return ' '.join(out)
putseq('S',28,bario('B5 A5 B5 G5 A5 F#5 G5 E5')+' '+bario('G5 F#5 G5 E5 F#5 D5 E5 C#5')+' '+bario('D5 C#5 D5 B4 C#5 A4 B4 G4')+' E6:2 D6:2 C#6:4 A5:4 C#6:2 A5:2')
putseq('B',28,'G2:4 D3:4 G2:4 D3:4  B2:4 F#3:4 B2:4 F#3:4  F#2:4 D3:4 F#2:4 D3:4  A2:4 E3:4 A2:4 E3:4')
putseq('A',28,'B4:2 A4:2 B4:2 G4:2 G4:2 A4:2 B4:2 D5:2  G4:2 B4:2 A4:4 G4:2 A4:2 F#4:2 B4:2  A4:2 B4:2 A4:2 G4:2 F#4:2 E4:2 D4:2 F#4:2  E5:8 C#5:4 E5:4')

# M3 b32: D major, lag 7+7 triple stretto with CS (all unison-type entries, pure D)
def stretto3D(BASE,vS2,vS1,vS3,vCS,lag1=7,lag2=7,o2=1,o3=-1,ocs=-1):
    S1=SUBJ; S2=OCT(SUBJ,o2); S3=OCT(SUBJ,o3); CS=OCT(T(CSA,-4,-7),ocs)
    putseq(vS1,BASE,S1); putseq(vCS,BASE,CS)
    putseq(vS2,BASE,'R:%d '%lag1+S2)
    putseq(vS3,BASE,'R:%d '%(lag1+lag2)+S3)

stretto3D(32,'Br','A','B','Cb',7,7,-1,-2,-2)
putseq('S',33,'R:8 D6:4 E5:2 G5:2  F#5:4 C#6:4 D6:4 A5:4')

# Ep4 b35-38: hemiola (3+3+2) 16th arpeggios, descending-fifths sequence; slow alto suspensions; bass leaping 8ths
def hm(a,b,c,d,e):   # 3+3+2 grouping: notes a b c | a b c | d e  (each a 16th)
    return ' '.join(x+':1' for x in (a,b,c,a,b,c,d,e))
putseq('S',35,' '.join([hm('D6','B5','F#5','B5','D6'),hm('B5','G5','E5','G5','B5'),
                       hm('C#6','A5','E5','A5','C#6'),hm('D6','A5','F#5','A5','D6'),
                       hm('B5','G5','D5','G5','B5'),hm('C#6','A#5','F#5','A#5','C#6'),
                       'D6:2 F#6:2 D6:2 B5:2 F#5:4 D5:4']))
putseq('A',35,'F#4:8 G4:8  E4:4 C#4:4 F#4:8  D4:8 C#4:8  F#4:4 A4:4 R:8')
putseq('B',35,'B2:2 F#3:2 B2:2 D3:2  E3:2 B2:2 E3:2 B2:2  A2:2 E3:2 A2:2 E2:2  F#2:2 A2:2 D3:2 A2:2  G2:2 D3:2 G2:2 B2:2  F#2:2 C#3:2 F#2:2 C#3:2  B2:4 F#2:4 B1:8')

# generic stretto from a search template: template computed in D, then every entry shifted uniformly by (sl,sm)
TSH={'uni':(0,0),'5up':(4,7),'5dn':(-4,-7),'4dn':(-3,-5),'4up':(3,5)}
def strettoG(BASE,sh,tpl,vs):   # vs = (vS1,vS2,vS3,vCS)
    l1,l2,n2,o2,n3,o3,ocs=tpl[:7]
    a2=TSH[n2];a3=TSH[n3]
    S1=T(SUBJ,sh[0],sh[1])
    S2=T(SUBJ,sh[0]+a2[0]+7*o2,sh[1]+a2[1]+12*o2)
    S3=T(SUBJ,sh[0]+a3[0]+7*o3,sh[1]+a3[1]+12*o3)
    CS=T(CSA,sh[0]-4+7*ocs,sh[1]-7+12*ocs)
    putseq(vs[0],BASE,S1); putseq(vs[3],BASE,CS)
    putseq(vs[1],BASE,'R:%d '%l1+S2)
    putseq(vs[2],BASE,'R:%d '%(l1+l2)+S3)
M4=(7,4,'uni',-1,'uni',1,-2,0)






strettoG(39,(-3,-5),M4,('T','Br','A','B'))

# Ep5 b42-46: running stepwise 8ths (tenor) under 7-6-type tied syncopations (S/A), quarter-note arpeggiated bass; rising sequence toward the dominant
putseq('S',42,'C#6:6 B5:2 A5:6 G#5:2  D6:6 C#6:2 B5:6 A5:2  E6:6 D6:2 C#6:6 B5:2  F#6:6 E6:2 D6:6 C#6:2  D6:6 C#6:2 B5:6 G#5:2')
putseq('A',42,'E5:8 C#5:8  F#5:8 D5:8  G5:8 E5:8  A5:8 B5:8  F#5:8 G#5:8')
putseq('T',42,'C#4:2 D4:2 E4:2 F#4:2 A4:2 B4:2 C#5:2 E4:2  D4:2 E4:2 F#4:2 A4:2 B4:2 A4:2 G4:2 F#4:2  E4:2 G4:2 B4:2 G4:2 C#5:2 B4:2 A4:2 G4:2  D4:2 F#4:2 A4:2 D5:2 B4:2 A4:2 G4:2 E4:2  F#4:2 A4:2 B4:2 A4:2 E4:2 G#4:2 B4:2 E5:2')
putseq('B',42,'A2:4 C#3:4 F#2:4 A2:4  B2:4 D3:4 G2:4 B2:4  E2:4 G2:4 A2:4 C#3:4  D3:4 F#3:4 G2:2 A2:2 B2:4  B2:4 D3:4 E2:4 B2:4')

# PEAK b47-50: augmentation of subject (Bass) + augmented CS (Contrabass) over A; normal-speed S1 (Alto) / S2 (Soprano, lag 9)
def AUG(s): return ' '.join(t.split(':')[0]+':'+str(int(t.split(':')[1].rstrip('~'))*2) for t in toks(s))
CSAUG=AUG(T(CSA,-4,-7)).replace('F#4:4 E4:4','F#4:6 E4:2').replace('D4:4 E4:4','D4:6 E4:2').replace('B4:4 A4:4','B4:6 A4:2')
putseq('B',47,OCT(AUG(SUBJ),-2))
putseq('Cb',47,OCT(CSAUG,-2))
putseq('S',47,OCT(SUBJ,1))
putseq('T',47,'R:9 '+OCT(SUBJ,-1))
# peak run-out b49-50: soprano rises to the apex (B6) over the aug subject's closing descent; alto in 8ths
putseq('S',49,'C#6:2 E6:2 A6:4 F#6:2 A6:2 E6:2 C#6:2  D6:2 F#6:2 B6:4 G6:2 F#6:2 F#6:2 A6:2')
putseq('A',49,'E5:4 A4:4 D5:2 F#5:2 C#5:2 E5:2  F#5:2 D5:2 B4:2 D5:2 D5:2 B4:2 A4:2 D5:2')
putseq('A',47,'C#5:4 D5:4 F#4:4 D5:4  A4:4 D5:4 F#5:4 B4:4')

# FINAL b51-: tonic pedal D2 + triple stretto (lag 7,7, S2 up an octave, S3 down an octave) with CS
putseq('Cb',51,'D2:48')
putseq('A',51,SUBJ); putseq('Br',51,OCT(T(CSA,-4,-7),-1))
putseq('S',51,'R:7 '+OCT(SUBJ,1)); putseq('T',51,'R:14 '+OCT(SUBJ,-1))
# pass 2 b54: much tighter (lag 7 then 2), still over the D2 pedal; S2 an octave up, S3 an octave down
putseq('Cb',51,'D2:144')
putseq('A',54,SUBJ); putseq('T',54,T(CSA,-4,-7))
putseq('S',54,'R:7 '+OCT(SUBJ,1)); putseq('Br',54,'R:9 '+OCT(SUBJ,-1))

# CODA b56 u7 ... : cadence over the held D2 pedal (IV - V7 - I with a last high flourish)
BARS['Soprano'][55]='C#6:1 B5:1 A5:1 B5:1 C#6:1 D6:2 F#6:1 E6:1 D6:2 C#6:2 B5:2 A5:1'
BARS['Alto'][55]='R:9 A4:3 B4:4'
BARS['Tenor'][55]='R:10 F#4:3 G4:3'
putseq('S',57,'D6:1 C#6:1 D6:1 F#6:1  G6:1 F#6:1 E6:1 B5:1  C#6:1 D6:1 E6:1 G6:1  F#6:1 E6:1 D6:1 C#6:1  A6:1 F#6:1 D6:1 F#6:1  G6:1 D6:1 B5:1 D6:1  E6:1 C#6:1 A5:1 C#6:1  F#6:1 E6:1 D6:1 C#6:1  D6:16')
putseq('A',57,'F#5:1 E5:1 F#5:1 A5:1  B5:1 A5:1 G5:1 F#5:1  E5:1 F#5:1 G5:1 B5:1  A5:1 G5:1 F#5:1 E5:1  F#5:1 D5:1 A4:1 D5:1  B4:1 D5:1 G5:1 B4:1  C#5:1 E5:1 A4:1 E5:1  A5:1 F#5:1 E5:1 D5:1  A5:16')
putseq('T',57,'A4:4 D5:4 C#5:4 A4:4  A4:4 G4:4 E4:4 F#4:4  F#4:16')
putseq('Br',57,'D4:4 B3:4 E4:4 A3:4  D4:4 D4:4 C#4:4 D4:4  D4:16')
putseq('B',57,'D3:4 G2:4 A2:4 D3:4  F#3:4 B2:4 A2:4 A2:4  A3:16')

# ---- metadata: bpm, markers, entry labels, dynamic arc
BPM=108
MARKS=[(1,'Exposition (6 voices)'),(13,'Episode 1'),(17,'Middle entries: B minor, F# minor'),(21,'Episode 2'),
       (25,'Stretto I (G/D) with CS'),(28,'Episode 3'),(32,'Stretto II (D, tight) with CS'),(35,'Episode 4'),
       (39,'Stretto III with CS'),(42,'Episode 5 (rising)'),(47,'PEAK: augmentation + CS + subject'),
       (51,'Final stretto over D pedal'),(54,'Tight stretto (lags 7+2)'),(57,'Coda')]
LAB=[('Alto',1,2,'S'),('Tenor',3,2,'A'),('Bass',5,2,'S'),('Soprano',7,2,'A'),('Baritone',9,2,'S'),('Contrabass',11,2,'A'),
     ('Tenor',17,2,'S (Bm)'),('Baritone',19,2,'A (F#m)'),
     ('Alto',25,2,'S1'),('Bass',25,2,'S2'),('Soprano',25,2,'S3'),
     ('Alto',32,2,'S1'),('Baritone',32,2,'S2'),('Bass',32,2,'S3'),('Contrabass',32,2,'CS'),
     ('Tenor',39,2,'S1'),('Baritone',39,2,'S2'),('Alto',39,2,'S3'),
     ('Bass',47,4,'S aug'),('Contrabass',47,4,'CS aug'),('Soprano',47,2,'S'),('Tenor',47,2,'S'),
     ('Alto',51,2,'S1'),('Soprano',51,2,'S2'),('Tenor',51,2,'S3'),('Baritone',51,2,'CS'),
     ('Alto',54,2,'S1'),('Soprano',54,2,'S2'),('Baritone',54,2,'S3'),('Tenor',54,2,'CS')]
ENT=[(v,b,min(n,2)) for (v,b,n,l) in LAB if b>=25]
def LEVEL(b):
    if b<12: return 0
    if b<25: return -2
    if b<28: return 2
    if b<32: return -3
    if b<35: return 3
    if b<39: return -3
    if b<42: return 4
    if b<47: return 2+ (b-42)
    if b<51: return 9
    if b<54: return 5
    if b<57: return 8
    if b<59: return 5
    return 3
