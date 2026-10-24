from gen import *
from csdef import *
import sys
BL=16
U=[];L=[];KEYSP={};MARKS=[];LAB=[]
P=parse
def put(V,bar,line,off=0): V.append(((bar-1)*BL+off,line if isinstance(line,list) else P(line)))
def ks(b0,b1,d):
    for b in range(b0,b1+1): KEYSP[b]=d
GMs={1:'C#'}; DMs={1:'C#',10:'Bb'}; FMs={4:'E',1:'Db'}
# ---------------- Exposition (C minor)
put(U,1,SUBJ); put(L,1,'R:32'); LAB.append((0,1,'Subject'))
put(L,3,ANS); put(U,3,CS); LAB.append((1,3,'Answer (inversion)'))
# Episode 1 (b5-6): CS-head sequence i - iv - VII - III - V/v  -> G minor
put(U,5,'Eb5:1 G5:1 F5:1 Eb5:1 D5:1 C5:1 B4:1 C5:1  Ab5:1 C6:1 Bb5:1 Ab5:1 G5:1 F5:1 E5:1 F5:1')
put(L,5,'C3:2 Ab2:2 B2:2 G2:2  F3:2 Db3:2 E3:2 C3:2')
put(U,6,'D5:1 F5:1 Eb5:1 D5:1 C5:1 Bb4:1 A4:1 Bb4:1  G5:1 Bb5:1 Ab5:1 G5:1 F#5:1 A5:1 D6:1 A5:1')
put(L,6,'Bb2:2 G2:2 A2:2 F2:2  Eb3:2 C3:2 D3:4')
# Second exposition in G minor: subject above, inversion below
put(U,7,tr(SUBJ,7)); put(L,7,tr(CSI,7)); LAB.append((0,7,'Subject (G minor)'))
put(L,9,tr(ANS,-5)); put(U,9,tr(CS,-5)); LAB.append((1,9,'Inversion (G minor)'))
ks(7,10,GMs)
# Episode 2 (b11-12): CS-head model in the upper voice, sequence down a step; lower line in 8ths (generated, then reviewed)
put(U,11,'D5:1 C5:1 Bb4:1 A4:1 G4:1 A4:1 Bb4:1 C5:1 D5:2 G5:2 Eb5:2 C5:2')
put(U,12,'C5:1 Bb4:1 Ab4:1 G4:1 F4:1 G4:1 Ab4:1 Bb4:1 C5:2 G4:2 E4:2 Bb4:2')
put(L,11,'G3:2 D3:2 G2:2 F#2:2 G2:2 Bb2:2 C3:2 Eb3:2')
put(L,12,'F3:2 C3:2 F2:2 E2:2 C3:2 Bb2:2 G2:2 Bb2:2')
U[-1]=(U[-1][0],P('C5:1 Bb4:1 Ab4:1 G4:1 F4:1 G4:1 Ab4:1 Bb4:1 C5:2 G4:2 E4:2 G4:2'))
# ---------------- Canon by inversion (b13-19.2), F minor, diatonic mirror tonic<->dominant, lag = half bar
from gen import dinv
_f=dinv(5,67)
CAN=P(open('canon.txt').read())
put(U,13,CAN); LAB.append((0,13,'Canon by inversion (lead)'))
put(L,13,'Ab2:2 F2:2 Db3:2 C3:2')
put(L,13,[(_f(p),d) for p,d in CAN],8); LAB.append((1,13,'Canon (follower, diatonic mirror)'))
ks(13,19,FMs)
# Episode 3 (b19-20): broken chords Fm - Cm - Ab - F#dim7 - D7
put(U,19,'C5:1 Ab4:1 F4:1 Ab4:1 C5:1 F5:1 Ab5:1 F5:1 G5:1 Eb5:1 C5:1 Eb5:1 G5:1 C6:1 Eb6:1 C6:1')
put(L,19,'Eb3:4 G2:4',8)
put(U,20,'Ab5:1 Eb5:1 C5:1 Eb5:1 A5:1 F#5:1 Eb5:1 C5:1 D5:1 F#5:1 A5:1 C6:1 C6:1 A5:1 F#5:1 A5:1')
put(L,20,'Ab2:2 C3:2 F#2:2 A2:2 D3:2 F#2:2 A2:2 C3:2')
ks(20,20,GMs)
# ---------------- Stretto I (b21-23.2): subject in G above, subject in F below, at the half bar
_s=tr(SUBJ,7); _s[7:9]=[(_s[7][0],3),(_s[8][0],1)]; put(U,21,_s); LAB.append((0,21,'Stretto I: subject (G)'))
put(L,21,'G3:2 Bb3:2 C4:2 D4:2')
put(L,21,tr(SUBJ,-7),8); LAB.append((1,21,'Stretto I: subject (F), half bar later'))
ks(21,22,GMs)
put(U,23,'C5:2 Bb4:2 Ab4:2 C5:2')
# Episode 4 (b23.3-24): to the dominant; lower bariolage keeps G sounding on every 8th (implied pedal)
put(U,23,'Ab4:1 B4:1 D5:1 F5:1 B4:1 D5:1 G4:1 D5:1',8)
put(L,23,'Ab3:2 F3:2 D3:2 B2:2',8)
put(U,24,'Eb5:2 C5:2 B4:2 F5:2 G5:2 Ab5:2 B4:2 F5:2')
put(L,24,'G2:1 Eb3:1 G2:1 C3:1 G2:1 D3:1 G2:1 B2:1 G2:1 Eb3:1 G2:1 C3:1 G2:1 F3:1 G2:1 B2:1')
# ---------------- PEAK (b25-26): subject against its exact chromatic inversion, one eighth apart
INV=[(53,4),(52,2),(54,2),(51,2),(55,2),(50,2),(56,2)]
put(L,25,INV); LAB.append((1,25,'PEAK: inversion (wedge mirrored)'))
put(U,25,'D5:2'); put(U,25,SUBJ,2); LAB.append((0,25,'PEAK: subject, one eighth later'))
put(L,26,'A3:2 F3:2 Eb3:2 D3:2 B2:2 C3:2 G2:2 Ab2:2')
MARKS.append((25,'ff'))

# Episode 5 (b27-28): cadenza; upper run, then the wedge spreading from G over a dominant bass
put(U,27,'Eb4:1 F4:1 G4:1 Ab4:1 C5:1 Eb5:1 Ab5:1 G5:1 F5:1 Eb5:1 D5:1 F5:1 Ab5:1 B5:1',2)
put(U,28,'G5:1 Ab5:1 F#5:1 A5:1 F5:1 Bb5:1 E5:1 B5:1 C6:1 G5:1 F5:1 D5:1 B4:1 G4:1 D5:1 B4:1')
put(L,27,'Ab2:2 C3:2 Eb3:2 C3:2 F2:2 Ab2:2 D3:2 C3:2')
put(L,28,'G3:4 D3:2 G2:2 C3:2 Ab2:2 G2:4')
# ---------------- Final stretto over a tonic pedal (b29-31): subject above, subject an octave lower 3/4 bar later
put(U,29,SUBJ); LAB.append((0,29,'Final stretto: subject'))
put(L,29,'C3:2 Eb3:2 F3:2 G3:2 F3:2 G3:2')
put(L,29,tr(SUBJ,-12),12); LAB.append((1,29,'Final stretto: subject at the octave, 3/4 bar later'))
put(U,31,'Ab4:2 B4:2 C5:2 B4:2 C5:2 D5:2 Eb5:2 D5:2')
put(L,31,'G3:2 B3:2',12)
# Coda (b32-34): the wedge made literal - the two voices spread by half steps from C, 3 octaves; Db->C, B->C
WU=[(72+i,2) for i in range(12)]; WL=[(60-i,2) for i in range(12)]
put(U,32,WU); put(L,32,WL); LAB.append((0,32,'Coda: the wedge, both voices'))
put(U,33,'C6:8',8); put(L,33,'C3:8',8)
put(U,34,'C6:4 G5:4 E5:8'); put(L,34,'C3:16')
EXTRA=[('Pedal',['R:16']*28+['C2:16~']*5+['C2:16'])]
KEYSP[32]={1:'C#',3:'D#',6:'F#',8:'G#',10:'A#'};KEYSP[33]={1:'Db',3:'Eb',6:'Gb',8:'Ab',10:'Bb'}
MARKS.append((29,'f'))
BPM=63; TEMPO='Andante sostenuto'
def LEVEL(b):
    return {25:84,26:82,21:78,22:78,27:80,28:80}.get(b, 74 if b>=29 else 70)
