# ===== v2 ADDITIONS: fill voices so the texture stays 4-6 after the exposition
# Ep1 b13-16: alto in slow suspensions between the fanfare canon voices, baritone in quarter-note counter-line
putseq('A',13,'F#5:8 D5:4 F#5:4  B4:4 D5:4 G4:8  R:16  D5:8 A4:8')
putseq('Br',13,'A3:8 D4:4 B3:4  B3:2 A3:2 G3:8 B3:4  C#4:4 E4:4 D4:4 A3:4  G3:8 A3:8')
# M1 b17-20: alto and baritone join under the B minor entry; for the F# minor entry the CS moves to the alto and the soprano gets a new upper line, tenor fills
putseq('A',17,'D5:4 F#4:8 B4:4  D5:4 B4:12')
putseq('Br',17,'R:4 D3:4 F#3:4 D3:4  B3:4 F#3:4 D3:8')
putseq('A',19,CSFsm)
putseq('S',19,'F#5:6 G#5:2 A5:8  C#6:8 A5:4 D6:4')
putseq('T',19,'A3:4 C#4:8 F#4:4  F#4:4 C#4:4 D4:8')
# b27: stretto I run-out filled (alto/tenor continue, bass walks into Ep3)
putseq('A',27,'G4:4 D5:4 G4:4 D5:4')
putseq('T',27,'G3:4 A3:4 C4:4 D4:4')
BARS['Bass'][26]='B2:1 A2:1 B2:1 C#3:1 D3:2 E3:2 C3:4 B2:4'
# Ep3 b28-31: tenor quarter-note counter-line under the bariolage
putseq('T',28,'G3:4 B3:4 D4:4 B3:4  D4:8 B3:4 D4:4  D4:4 A3:8 F#3:4  C#4:4 E4:4 E4:4 C#4:4')
# Stretto II b32-34: soprano and tenor join the three subject entries + CS; b34 run-out in 5-6 voices
putseq('S',32,'F#5:8 D6:8  C#6:4 A5:4 D6:4 E5:2 G5:2')
putseq('T',32,'F#4:8 A4:4 F#4:4  C#5:4 D5:4 B4:3 R:5  F#4:4 R:4 F#4:8')
putseq('A',34,'A4:4 E5:4 D5:4 F#5:4')
putseq('Cb',34,'F#2:4 A2:4 B1:4 F#2:4')
# Ep4 b35-38: the old slow alto line moves to the tenor; a new alto suspension line sits between it and the hemiola soprano
putseq('T',35,'F#4:8 G4:8  E4:4 C#4:4 F#4:8  D4:8 C#4:8  F#4:4 A4:4 R:8')
putseq('A',35,'D5:6 C#5:2 B4:6 D5:2  C#5:8 A4:8  D5:8 A#4:8  B4:16')
# Stretto III b39-41: soprano descant above the three entries + CS; b41 run-out filled
putseq('S',39,'C#6:4 E6:4 A5:4 E6:4  E6:6 F#6:2 A6:4 F#6:4  E6:4 E6:2 D6:2 C#6:4 A5:4')
putseq('T',41,'C#5:4 B4:8 C#5:4')
putseq('B',41,'E2:12 A2:4')
# Ep5 b42-46: rhythms de-synchronised (v1 had S/A/T repeating one rhythm for 5 bars)
putseq('A',43,'F#5:6 E5:2 D5:8  G5:4 G5:2 F#5:2 E5:8')
putseq('S',44,'E6:4 D6:4 C#6:6 B5:2  F#6:8 D6:8')
putseq('T',44,'E4:4 B4:4 C#5:2 B4:2 A4:2 G4:2')
# PEAK b47-50: baritone and (b50) tenor join -> six real voices
putseq('Br',47,'A3:4 D3:8 F#3:4  A3:8 D4:8  R:8 A3:8  F#3:8 G3:4 A3:4')
putseq('T',50,'F#4:4 D4:4 G4:4 D4:4')
# FINAL b51-56 re-voiced: b51 subject now in S (A5) at u0, alto answers at lag 7 (A4);
# b54 subject in tenor (A3), CS in alto, lag-9 entry moves down to the bass (A2) -> all 6 voices
for b in range(51,57): BARS['Soprano'][b-1]='R:16'; BARS['Alto'][b-1]='R:16'; BARS['Tenor'][b-1]='R:16'; BARS['Baritone'][b-1]='R:16'
putseq('S',51,OCT(SUBJ,1)); putseq('A',51,'R:7 '+SUBJ)
putseq('Br',51,OCT(T(CSA,-4,-7),-1)); putseq('T',51,'R:14 '+OCT(SUBJ,-1))
putseq('B',51,'D3:4 A2:4 B2:8  F#2:8 B2:8')
putseq('T',54,OCT(SUBJ,-1)); putseq('A',54,T(CSA,3,5))
putseq('S',54,'R:7 '+OCT(SUBJ,1)); putseq('B',54,'R:9 '+OCT(SUBJ,-2))
BARS['Soprano'][55]='C#6:1 B5:1 A5:1 B5:1 C#6:1 D6:2 F#6:1 E6:1 D6:2 C#6:2 B5:2 A5:1'
putseq('Br',54,'D3:4 F#3:4 A3:4 F#3:4  F#3:4 D4:4 R:8  A3:4 E3:4 A3:4 E3:4')
BARS['Alto'][55]='R:9 A4:3 B4:4'
BARS['Tenor'][55]='R:10 F#4:3 G4:3'
BARS['Alto'][54]='A5:3 B5:1 D6:2 C#6:2 B5:2 C#6:2 D6:4'
# b53 bridge between the two final strettos, 6 voices
BARS['Soprano'][52]='A5:8 G5:4 F#5:4'
BARS['Baritone'][52]='A3:8 D3:4 F#3:4'
BARS['Bass'][52]='A2:8 B2:4 A2:4'
