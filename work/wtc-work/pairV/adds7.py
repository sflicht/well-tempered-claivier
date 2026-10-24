# ===== v3 CHANGES (only Stretto I b25-27 and Contrabass b35-46) =====
import os
SUBJ_G=T(SUBJ,-4,-7); CS_G=T(CSA,-8,-14)          # subject on D4 (G major), CS on D4
for b in range(25,28):
    for v in NV: BARS[v][b-1]='R:16'
_P=dict(x.split('=') for x in os.environ.get('ST1','A=0:0 S=4:7 Br=8:-7 cT=4:0').split())
for v,spec in _P.items():
    if v=='CS': continue
for v,spec in _P.items():
    lag,sh=map(int,spec.split(':'))
    if v.startswith('c'):  # countersubject
        putseq(v[1:],25,('R:%d '%lag if lag else '')+TD(CS_G,sh))
    else:
        putseq(v,25,('R:%d '%lag if lag else '')+TD(SUBJ_G,sh))
# foundation: contrabass G pedal (b25-27.2) -> D (dominant) -> G at b28; bass free line
putseq('Cb',25,'G1:40 D2:8 G1:8 R:8')
putseq('B',25,'G2:8 G2:4 E2:4  B2:4 G2:4 C3:4 B2:4  C3:4 A2:4 D3:4 D2:4')
# run-out b27 after the entries end: everybody keeps going into Episode 3
BARS['Soprano'][26]=BARS['Soprano'][26].split(' R:')[0]+' '+'C6:4 B5:2 A5:2 C6:4'
BARS['Alto'][26]='G4:4 E4:4 F#4:4 A4:4'
BARS['Tenor'][26]=BARS['Tenor'][26].split(' R:')[0]+' '+'D4:4 F#4:4'
BARS['Baritone'][26]=BARS['Baritone'][26].split(' R:')[0]+' '+'A3:4 C4:4'
putseq('B',27,'E3:4 A2:4 D3:8')
BARS['Tenor'][26]='C4:2 B3:2 E4:4 D4:8'
BARS['Baritone'][26]=BARS['Baritone'][26].replace('A3:4 C4:4','A3:8')
putseq('Cb',27,'G1:8 F#1:8')
BARS['Tenor'][26]='C4:2 D4:2 C4:4 A3:4 F#3:4'
BARS['Alto'][26]='G4:4 A4:4 F#4:4 A4:4'
putseq('B',25,'G2:8 G2:4 B2:4  D3:4 G2:8 B2:4')
BARS['Soprano'][26]=BARS['Soprano'][26].replace('C6:4 B5:2 A5:2 C6:4','C6:4 A5:4 C6:4')
BARS['Tenor'][26]='C4:2 B3:2 C4:4 A3:8'   # CS ends literally (C4 B3), then free
BARS['Soprano'][26]=BARS['Soprano'][26].replace('C6:4 A5:4 C6:4','C6:4 D6:4 C6:4')
putseq('B',25,'G2:16  B2:4 G2:8 B2:4')
putseq('B',26,'D3:4 G2:8 B2:4')
# ---- Contrabass b35-46: real lines instead of rests
putseq('Cb',39,'A1:16~ A1:16~ A1:12 R:4')                                 # Stretto III: A pedal under the three entries
# ---- Contrabass b35-38 (Ep4) and b42-46 (Ep5): real lines instead of rests
putseq('Cb',35,'B1:8 G1:8  A1:8 F#1:8  B1:8 A#1:4 F#1:4  D2:8 B1:8')
putseq('Cb',42,'A1:16  D2:8 B1:8  G1:8 C#2:8  F#2:8 G2:8  B1:8 E2:8')
# ---- v3 labels / markers for Stretto I
LAB=[l for l in LAB if l[1]!=25]+[('Alto',25,2,'S1'),('Soprano',25,2,'S2'),('Baritone',25,2,'S3'),('Tenor',25,2,'CS')]
LAB.sort(key=lambda l:l[1])
ENT=[(v,b,min(n,2)) for (v,b,n,l) in LAB if b>=25]
MARKS=[(b,('Stretto I (G): 3 entries a beat apart + CS, 6 voices, G pedal' if b==25 else l)) for b,l in MARKS]
