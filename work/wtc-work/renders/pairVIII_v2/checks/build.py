import json,sys
from cp import Score,fill,to_events
NV=9
NAMES=['Soprano I','Soprano II','Alto I','Alto II','Tenor I','Tenor II','Baritone','Bass I','Bass II']
ABBR=['S1','S2','A1','A2','T1','T2','Bar','B1','B2']
CENT=[81,76,71,66,60,55,50,45,39]
NBAR=32
S=Score(NV,NBAR*4,CENT)
PC={'Eb':3,'Bb':10,'Gb':6,'Ab':8,'Db':1,'Cb':11,'F':5,'Fb':4,'A':9,'C':0,'D':2}
CH="""0 Ebm|1 Ebm|2 Abm|3 Abm|4 Bb|5 Ebm|6 Abm|7 Bb7
8 Ebm|9 Ebm|10 Ebm|11 Cb|12 F7|13 Bbm|14 Bb|15 Bb7
16 Ebm|17 Ebm|18 Abm|19 Abm|20 Bb|21 Ebm|22 Abm|23 Bb7
24 Ebm|25 Ebm|26 Ebm|27 Cb|28 F7|29 Bbm|30 Bb|31 Bb7
32 Ebm|33 Ebm|34 Abm|35 Abm|36 Bb|37 Ebm|38 Cb|39 Bb7
40 Ebm|41 Ebm|42 Abm|43 Db7|44 Gb|45 Gb|46 Cb|47 Db7
48 Gb|49 Gb|50 Cb|51 Abm|52 Db|53 Gb|54 Ab|55 Ab7
56 Db|57 Db|58 Gb|59 Ebm|60 Ab|61 Db|62 Bbhd7|63 Eb7
64 Abm|65 Fb|66 Dbm|67 Eb7
68 Abm|69 Abm|70 Dbm|71 Dbm|72 Eb7|73 Abm|74 Abm|75 Fb|76 Bb7|77 Ebm
78 Ebm|79 F7|80 Bbm|81 Gb|82 Chd7|83 F7
84 Bbm|85 Bbm|86 Ebm|87 Ebm|88 F|89 Ebm|90 Ebm|91 F|92 Gb|93 Ebm|94 F|95 Bb7
96 Ebm|97 Gb|98 Fb|99 Fhd7|100 Bb7|101 Cb|102 Cb|103 Cb
104 Fb|105 Dbm|106 Gb|107 Cb
108 Ebm|109 Ebm|110 Abm|111 Abm|112 Bb|113 Abm|114 Abm|115 Bb7|116 Abm|117 Abm|118 Bb7|119 Ebm
120 Abm|121 Fhd7|122 Bb7|123 Bb7|124 Eb|125 Eb|126 Eb|127 Eb"""
QN={'m':'min','':'maj','7':'dom7','hd7':'hdim7','d7':'dim7'}
MINKEYS={}
for tok in CH.replace('\n','|').split('|'):
    b,c=tok.split();b=int(b)
    import re
    r,q=re.match(r'([A-G]b?)(.*)',c).groups()
    S.chord(b,PC[r],QN[q],force=True)
# tonal scales: local key per region
def key(b0,b1,tonic,mode):
    from forms import MIN,MAJ
    sc={(PC[tonic]+x)%12 for x in (MAJ if mode=='maj' else MIN)}
    if mode=='min': sc|={(PC[tonic]+11)%12,(PC[tonic]+9)%12}
    for b in range(b0,b1):
        r,q,bp,_,pcs=S.H[b]; S.H[b]=(r,q,bp,sc|pcs,pcs)
key(0,44,'Eb','min');key(44,56,'Gb','maj');key(56,62,'Db','maj');key(62,78,'Ab','min');key(78,80,'Eb','min');key(80,96,'Bb','min');key(96,102,'Eb','min');key(102,108,'Cb','maj');key(108,128,'Eb','min')
# ---- thematic plan (form, voice, beat, T semitones from Eb, octave)
P=[('S',2,0,0,0),
   ('A',1,8,0,0),('CSA',2,8,0,-2),
   ('S',4,16,0,-1),('CS',1,16,0,0),
   ('A',0,24,0,1),('CSA',4,24,0,-3),
   ('S',7,32,0,-2),('CS',0,32,0,0),
   ('H',2,40,0,0),('HM',1,44,3,1),
   ('SM',2,48,3,0),('CSM',4,48,3,-2),
   ('SM',7,56,-2,-1),('CSM',2,56,-2,-1),
   ('S',5,68,5,-1),('CS',2,68,5,-1),('A',3,72,5,-1),
   ('S',1,84,7,0),('S',0,87,7,1),('S',7,90,7,-2),
   ('S',0,96,0,2),('S',2,96,0,1),
   ('SM',3,102,8,-1),('CSM',1,102,8,-1),
   ('S',2,108,0,0),('S',0,111,0,1),('S',4,114,0,-1)]
for f,v,b,T,o in P: S.place(f,v,b,T,63,o,lab=f,chords=False)
# pedals
S.note(8,108,16,39,'ped')
S.ignore={8}
# final chord (Picardy) bar 32
FIN=[91,87,82,79,75,70,67,58,51]
for v,p in enumerate(FIN):
    S.note(v,124,4,p,'fin')



# free spans: voice -> list of (b0,b1)
ACT={
 7:[(38,56),(62,90),(102,124)],
 8:[(92,96)],
 6:[(70,96),(108,124)],
 5:[(64,68),(78,96),(119,124)],
 4:[(14,16),(22,24),(30,48),(56,68),(78,96),(108,114),(120,124)],
 3:[(80,96),(108,124)],
 2:[(6,8),(14,40),(43,48),(54,56),(62,68),(74,96),(120,124)],
 1:[(14,16),(22,40),(40,43),(48,56),(62,68),(78,84),(90,96),(108,111),(117,124)],
 0:[(30,32),(38,40),(80,87),(108,111),(117,124)],
}
import random
# ---- PEAK (96-101): homophonic massing. Subject in S1 doubled at the octave by A1; the other seven voices
# strike full chords in the subject's own rhythm (Beethoven-style block statement), bass doubled in octaves.
ON=[0,1,2,3,3.5,4,4.5,5]
prevm={}
for i,o in enumerate(ON):
    t=96+o; d=(ON[i+1]-o) if i+1<len(ON) else 1
    r,q,bp,sc,pcs=S.H[int(t)]
    x=int(t*4)
    bass=min(range(36,48),key=lambda p:(p%12!=r, abs(p-prevm.get(7,43))))
    S.note(7,t,d,bass,'mass');S.note(8,t,d,bass-12,'mass')
    top=S.G[0][x]
    used={bass%12,top%12,S.G[2][x]%12}
    for v in (6,5,4,3,1):
        prevm.setdefault(v,None)
        c=S.cent[v]; pv=prevm.get(v) or c
        need=[pc for pc in pcs if pc not in used]
        def cost(p):
            k=abs(p-pv)+0.3*abs(p-c)
            if need and p%12 not in need: k+=4
            if p>=top-1: k+=50
            for u in range(9):
                q=S.G[u][x]
                if q<0 or u==v: continue
                if q==p: k+=20
                if i>0:
                    px=int((96+ON[i-1])*4); q0=S.G[u][px]; p0=prevm.get(v)
                    if q0>=0 and p0 is not None and q0!=q and p0!=p and abs(q-p)%12 in(0,7) and abs(q0-p0)%12==abs(q-p)%12 and (q-q0)*(p-p0)>0: k+=30
            return k
        p=min(range(c-8,c+9),key=lambda p:cost(p) if p%12 in pcs else 999)
        S.note(v,t,d,p,'mass');used.add(p%12);prevm[v]=p
    prevm[7]=bass
for v in sorted(ACT,reverse=True):
    for b0,b1 in ACT[v]:
        # split around thematic notes
        b=b0
        while b<b1:
            if any(S.G[v][x]>=0 for x in range(b*4,b*4+4)): b+=1;continue
            e=b
            while e<b1 and not any(S.G[v][x]>=0 for x in range(e*4,e*4+4)): e+=1
            act=1.6 if 84<=b<104 else 1.0
            c=fill(S,v,b,e,bass=(v>=7),seed=int(sys.argv[2]) if len(sys.argv)>2 else 0,activity=act)
            b=e
# B2 at peak is real bass; final chord restore
DYN=[(0,58),(40,62),(48,60),(64,66),(78,72),(84,80),(96,100),(102,48),(108,70),(120,84),(124,80)]
def dyn(t):
    v=58
    for b,x in DYN:
        if t>=b: v=x
    return v
def vel(v,t,th):
    x=dyn(t)+(8 if th else -4)+(3 if t%1==0 else 0)
    return max(30,min(115,x))
V=to_events(S,vel)
voices=[{'name':NAMES[i],'abbr':ABBR[i],'clef':'treble' if i<4 else 'bass','piano_pan':40+i*6,'events':V[i]} for i in range(NV)]
meta={'title':'The Well-Tempered clAIvier','subtitle':'Fugue VIII in E-flat minor - v2','composer':'Recomposed by Claudia / Sam','instrument':'Piano','key':'Eb','mode':'minor','meter':[4,4],'bpm':66,'tempo_text':'Andante maestoso','movement_number':8,'piece_type':'fugue','edition':'v2','score_tagline':'Harmony-first v2 - Claudia / Sam',
 'markers':[{'t':0,'label':'mp'},{'t':40,'label':'episode'},{'t':48,'label':'Gb major'},{'t':68,'label':'stretto I (1 bar)'},{'t':84,'label':'stretto II (3 beats), cresc.'},{'t':96,'label':'ff'},{'t':96,'label':'ff, subject in massed chords'},{'t':102,'label':'subito pp, Cb major'},{'t':108,'label':'tonic pedal, final stretto'}]}
json.dump({'metadata':meta,'voices':voices,'subject_entries':S.labels},open(sys.argv[1],'w'),indent=1)
