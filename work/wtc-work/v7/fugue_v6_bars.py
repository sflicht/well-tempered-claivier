# Fugue IV v5 - literal bars (3/4, sixteenth units). Voices: S A T Br B.  R = rest, '~' ties.
# Countersubject CS: bar a = long note (6) + six sixteenths; bar b = 3,1,2,2,4 (dotted-8th, 16th, 8th, 8th, half).
S=[];A=[];T=[];Br=[];B=[];TAG=[]
R='R:12'
def bar(s=R,a=R,t=R,br=R,b=R,tag=''):
    S.append(s);A.append(a);T.append(t);Br.append(br);B.append(b);TAG.append(tag)
bar(t='G#4:2 E4:1 D#4:1 B3:2 F#4:6',tag='1 Subject N (T) C#m')
bar(t='A4:4 F#4:2 D#4:2 B#3:2 C#4:2',tag='2')
bar(a='D#5:2 B4:1 A#4:1 F#4:2 C#5:6', t='G#3:6 E4:1 D#4:1 C#4:1 B3:1 A#3:1 B3:1', tag='3 Answer (A) G#m + countersubject CS (T)')
bar(a='E5:4 C#5:2 A#4:2 F##4:2 G#4:2', t='E4:3 F#4:1 E4:2 D#4:2 B3:4',tag='4')
bar(s='G#5:2 E5:1 D#5:1 B4:2 F#5:6', a='B3:6 D#4:1 E4:1 C#4:1 D#4:1 E4:1 G#4:1', t='E3:4 G#3:4 A3:4', tag='5 Subject N (S) C#m + CS (A)')
bar(s='A5:4 F#5:2 D#5:2 B#4:2 C#5:2', a='A4:3 B4:1 A4:2 G#4:2 F#4:4', t='F#3:6 G#3:6',tag='6')
bar(s='F#5:6 G#5:1 F#5:1 A5:1 G#5:1 B5:1 A5:1', br='D#4:2 B3:1 A#3:1 F#3:2 C#4:6',tag='7 Answer (Br) G#m + CS (S)')
bar(s='B5:3 G#5:1 E5:2 C#5:2 D#5:4', br='E4:4 C#4:2 A#3:2 F##3:2 G#3:2', tag='8')
bar(br='B2:6 C#3:1 B2:1 D#3:1 E3:1 F#3:1 G#3:1', b='G#2:2 E2:1 D#2:1 B1:2 F#2:6',tag='9 Subject N (B) C#m + CS (Br)')
bar(br='C#3:3 E3:1 D#3:2 F#3:2 G#3:4', b='A2:4 F#2:2 D#2:2 B#1:2 C#2:2',tag='10')
bar(a='E4:6 C#4:1 D#4:1 E4:1 F#4:1 E4:1 A4:1', br='G#3:6 A3:6', b='C#2:6 F#2:4 B1:2~', tag='11 codetta: C#m - F#m (CS run in A)')
# ======== v6 ========  E-major contrast section (b12-19), reworked: quicker harmonic rhythm, walking basses, no block chords
bar(s='R:8 D#5:1 E5:1 F#5:1 G#5:1', a='A4:3 G#4:1 F#4:2 D#4:2 B3:4', br='D#3:2 F#3:2 B3:2 A3:2 F#3:2 D#3:2', b='B1:6 B2:6', tag='12 B7 pivot to E major: S pickup into N+, Br arpeggio in eighths')
bar(s='B5:2 G#5:1 F#5:1 E5:2 B5:6', a='G#4:6 D#5:1 C#5:1 B4:1 C#5:1 D#5:1 E5:1', br='B3:2 D#4:2 B3:2 A3:2 D#4:2 B3:2', b='E2:2 F#2:2 G#2:2 A2:2 B2:2 G#2:2', tag='13 N+ (S, E major) + CS (A); bass walks up in eighths')
bar(s='E6:4 C#6:2 B5:2 A5:2 G#5:2', a='C#5:3 B4:1 A4:2 F#4:2 D#4:4', br='G#3:4 E4:2 C#4:2 D#4:2 B3:2', b='E2:2 G#2:2 A2:2 B2:4 G#2:2', tag='14 N+ tail + CS tail; IV then V')
bar(s='D#6:4 G#5:2 F#5:2 G#5:2 F#5:2', a='B4:2 E4:2 G#4:2 B4:4 G#4:2', t='G#3:6 D#4:1 C#4:1 B3:1 C#4:1 D#4:1 E4:1', b='B2:2 G#2:1 F#2:1 E2:2 B2:6', tag='15 N+ in the bass (E major) with CS in T (invertible: CS now above N); S/A free')
bar(s='E5:6 D#5:2 F#5:2 G#5:2', a='G#4:4 C#4:2 F#4:4 B3:2', t='C#4:3 B3:1 A3:2 F#3:2 D#3:4', b='E3:4 C#3:2 B2:2 A2:2 G#2:2', tag='16 N+ bass tail + CS tail in T; descending bass scale E-C#-B-A-G#')
bar(s='C#6:2 A5:1 B5:1 C#6:2 E6:6', a='A4:2 C#5:2 E5:2 A4:2 C#5:2 E5:2', t='F#3:2 A3:2 E4:2 C#4:2 A3:2 C#4:2', b='A2:6 C#3:6', tag='17 E major: IV - A/C# (head cell in S; A and T in eighths)')
bar(s='G#5:2 A5:1 B5:1 C#6:2 B5:2 G#5:4', a='C#5:2 B4:2 G#4:2 B4:4 G#4:2', t='G#3:6 C#4:4 B3:2', b='C#3:6 E#2:6', tag='18 C#7 (V of F#m): leading tone E# only in the bass, resolves to F#')
bar(s='A5:6 G#5:2 F#5:2 E#5:1 F#5:1', a='C#5:2 A4:1 G#4:1 E4:2 B4:6', t='A3:6 B3:1 C#4:1 A3:1 B3:1 A3:1 B3:1', b='F#2:4 C#3:2 D3:6', tag='19 Subject N (A) F#m + CS (T); S now a stepwise line (not a held pedal) that ends on the E# leading tone')
bar(s='F#5:4 G#5:4 A5:2 B5:2', a='D5:4 B4:2 G#4:2 E#4:2 F#4:2', t='F#4:3 E4:1 D4:2 B3:2 C#4:4', b='D3:4 G#2:4 C#3:2 F#2:2', tag='20 N tail (A) + CS tail (T); S climbs F#-G#-A')
bar(s='D#6:2 B5:1 A5:1 F#5:2 G#5:2 E5:1 D5:1 B4:2', t='F#3:1 D#3:1 A3:1 F#3:1 B3:1 A3:1 D4:1 B3:1 G#3:1 B3:1 E4:1 D4:1', b='B2:6 E2:6', tag='21 episode: head cell in S (B7 - E7), arpeggio-CS in T')
bar(s='A5:3 B5:1 E5:2 F#5:3 D#5:1 C5:2', t='C#4:1 E4:1 A3:1 E4:1 C#4:1 A3:1 C4:1 A3:1 F#3:1 A3:1 C4:1 A3:1', b='A2:12', tag='22 (A - D#o7 over A pedal)')
bar(s='B#5:2 G#5:1 F#5:1 D#5:2 G#5:2 E5:1 D#5:1 B4:2', t='D#4:1 F#4:1 B#3:1 D#4:1 G#3:1 B#3:1 G#3:1 B3:1 E4:1 B3:1 G#3:1 E3:1', b='G#2:6 E2:6', tag='23 (G#7 - C#m: S ends with real head)')
bar(s='A5:6 B#5:6', t='C#4:3 E4:1 F#3:2 B#3:2 D#4:1 F#4:1 G#4:2', b='F#2:6 G#2:6', tag='24 F#m - G#7 (prepare stretto)')
bar(s='G#5:2 E5:1 D#5:1 B4:2 F#5:6', a='E4:6 G#4:1 F#4:1 D#4:1 E4:1 F#4:1 G#4:1', t='R:4 G#3:2 E3:1 D#3:1 B2:2 F#3:2~', b='E2:10 D#2:2', tag='25 STRETTO, 1-beat offset: N (S, C#m) with CS (A) beneath; N (T, two octaves lower) enters one beat later')
bar(s='A5:4 F#5:2 D#5:2 B#4:2 C#5:2', a='C#5:3 B4:1 A4:2 F#4:2 A4:4', t='F#3:4 A3:4 F#3:2 D#3:2', b='F#2:12', tag='26 stretto tails: S N tail, CS tail (A, adapted), T N bar 1 tail')
bar(s='G#5:4 E5:2 F#5:2 A5:2 C#6:2', a='D#4:2 E4:2 G#4:2 E4:2 C#5:2 A4:2', t='B#2:2 C#3:2 E3:2 G#3:2 A3:2 E4:2', b='G#2:6 F#2:6', tag='27 end of stretto (T N tail closes on C#), C#m - F#m')
# ---- episode 2: descending parallel 3rds (S/A eighths) over a descending-fifths chain, T in contrary eighths
bar(s='D#6:2 C#6:2 B5:2 A5:2 G#5:2 F#5:2', a='B5:2 A5:2 G#5:2 F#5:2 E5:2 D#5:2', t='F#4:4 D#4:2 E4:2 B3:2 D#4:2', b='B1:2 F#2:2 B2:2 E2:2 G#2:2 B2:2', tag='28 episode 2: parallel 3rds S/A descending (B7 - E)')
bar(s='C#6:2 B5:2 A5:2 G#5:2 F#5:2 E5:2', a='A5:2 G#5:2 F#5:2 E5:2 D#5:2 C#5:2', t='E4:4 C#4:2 F#4:4 A4:2', b='A2:2 E2:2 A2:2 D#2:2 A2:2 F#2:2', tag='29 sequence a step lower (A - D#o7)')
bar(s='D#5:2 F#5:2 A5:2 B#5:2 A5:2 G#5:2', a='F#4:2 A4:2 B#4:2 D#5:2 F#5:2 D#5:2', t='A3:2 F#3:2 D#3:2 F#3:2 A3:2 F#3:2', b='D#2:12', tag='30 D#o7 prolonged over a D# pedal (dominant of G#m): S/A rising 6ths, T falling arpeggio')
bar(s='R:6 G#5:6~', br='F#3:6 A#3:1 G#3:1 E3:1 G#3:1 F#3:1 A#3:1', b='D#3:2 B2:1 A#2:1 F#2:2 C#3:6', tag='31 Answer N (B, G#m) + CS (Br)')
bar(s='G#5:4 C#5:8', br='B3:3 G#3:1 E3:2 C#3:2 D#3:4', b='E3:4 C#3:2 A#2:2 F##2:2 G#2:2', tag='32')
# ---- episode 3: contrary 16th-note scales between pairs of voices (S up/T down; A up/Br down; S down/B up)
bar(s='C#5:1 D#5:1 E5:1 F#5:1 G#5:2 A5:1 B5:1 C#6:2 E6:1 F#6:1~', a='G#4:6 C#5:6', t='E4:1 D#4:1 C#4:2 B3:2 A3:1 G#3:1 F#3:2 C#4:2', br='C#3:6 A2:6', b='E2:6 F#2:6', tag='33 episode 3: contrary 16th scales, S up / T down (C#m/E - F#m)')
bar(s='F#6:6 D#6:6', a='F#4:1 G#4:1 A4:2 B#4:2 D#5:6', t='D#4:6 F#4:6', br='A3:1 G#3:1 F#3:1 E3:1 D#3:2 D#3:6', b='F#2:6 G#2:6', tag='34 contrary scales A up / Br down (D#o7/F# - G#7)')
bar(s='C#6:4 B5:2 E5:6', a='E5:6 G#4:6', t='E4:12', br='G#3:6 B3:6', b='C#2:1 D#2:1 E2:1 F#2:1 G#2:1 A2:1 E2:6', tag='35 bass rises in 16ths against S (C#m - C#7)')
bar(s='C#6:2 A5:1 G#5:1 E5:2 B5:6', a='C#5:6 D5:1 C#5:1 B4:1 C#5:1 D5:1 E5:1', t='A3:4 B3:4 D4:4', br='F#3:8 D3:4', b='F#2:4 E2:4 D2:4', tag='36 Subject N (S) F#m + CS (A)')
bar(s='D6:4 B5:2 G#5:2 E#5:2 F#5:2', a='F#4:3 G#4:1 B4:2 D5:2 G#4:4', t='A3:4 D4:4 B3:4', br='F#3:4 D3:8', b='D2:4 G#2:8')
# ---- BUILD toward the climax (b38-42): voices enter one by one, tessitura climbs, head cell in sequence, dominant pedal stretto
bar(s='C#5:4 E5:2 A5:3 G#5:1 A5:2', a='A4:2 F#4:1 E4:1 C#4:2 C#5:2 A4:2 B4:2', t='A3:6 C#4:6', b='F#2:6 A2:6', tag='38 BUILD 1: F#m - A; head cell (A) in sequence, S rises, 3 voices + bass')
bar(s='E5:3 F#5:1 G#5:2 G#5:3 A5:1 B5:2', a='G#4:2 E4:1 D#4:1 E4:2 B4:2 G#4:1 F#4:1 E4:2', t='G#3:4 B3:2 E4:4 B3:2', br='E3:6 G#3:6', b='C#3:6 E3:6', tag='39 BUILD 2: C#m - E; head cell a step higher, Br enters')
bar(s='G#5:2 E5:1 D#5:1 B4:2 F#5:6', a='R:4 G#4:2 E4:1 D#4:1 B3:2 F#4:2', t='R:8 G#3:2 E3:1 D#3:1', b='G#2:12', tag='40 dominant pedal on G#: head cell in stretto (S, A, T) at one-beat offsets')
bar(s='C#6:4 B5:4 A5:4', a='G#4:6 A4:1 B4:1 C#5:1 B4:1 C#5:1 B4:1', t='C#4:6 E4:6', br='G#3:2 E3:1 D#3:1 B2:2 F#3:6', b='C#2:4 G#2:4 A2:4', tag='41 Subject N (Br) C#m + CS (A) - the return')
bar(s='C#6:4 F#5:8', a='C#5:3 B4:1 A4:2 F#4:2 D#4:4', br='A3:4 F#3:2 D#3:2 B#2:2 C#3:2', b='F#2:8 G#2:4', tag='42 F#m - D#o7 - G#7')
bar(s='E5:6 G#5:1 F#5:1 D#5:1 E5:1 G#5:1 A5:1', a='G#4:2 E4:1 D#4:1 B3:2 F#4:6', t='E3:4 G#3:2 F#3:2 B3:4', br='B2:6 D#3:2 F#3:4', b='G#2:3 E2:3 D#2:2 B1:4', tag='43 CLIMAX I: N in A (C#m), CS in S (octave inversion), augmentation in the bass, 5 voices')
bar(s='C#6:3 B5:1 A5:2 F#5:2 A5:4', a='A4:4 F#4:2 D#4:2 B#3:2 C#4:2', t='C#4:2 A3:2 C#4:2 A3:2 F#3:2 A3:2', br='A2:2 C#3:2 F#3:2 C#3:2 A2:2 C#3:2', b='F#2:12', tag='44 CLIMAX I (cont.): N tail in A, CS tail in S, augmentation sounds F#; T and Br in broken-chord eighths')
bar(s='C#6:2 E6:2 F#6:2 G#6:2 F#6:4', a='C#5:8 A4:4', t='A4:1 G#4:1 A4:1 B4:1 A4:1 B4:1 A4:1 G#4:1 D#4:2 E4:2', br='A3:2 E4:2 A3:2 C#4:2 F#3:2 A3:2', b='A2:8 F#2:4', tag='45 CLIMAX I PEAK: densest texture, S to G#6 (highest note of the piece), T in running 16ths, augmentation on A - F#')
bar(s='F#6:4 D#6:4 C#6:4', a='A4:4 F#4:4 E4:4', t='C4:4 A3:4 E4:4', br='F#3:4 B#2:4 G#3:4', b='D#2:4 B#1:4 C#2:4', tag='46 CLIMAX I RELEASE: S falls from G#6/F#6 by step to C#6, augmentation closes on C#m, motion stops (all voices in quarters)')
bar(s='C#6:4 G#5:4 A5:4', a='C#5:6 F#4:1 A4:1 D5:1 F#4:1 D5:1 A4:1', t='C#4:2 A3:1 G#3:1 E3:2 B3:6', br='C#3:6 B2:2 F#3:4', b='F#2:4 E2:4 D2:4', tag='47 Subject N (T) F#m + CS (A)')
bar(s='F#5:8 G#5:4', a='A4:3 G#4:1 B4:2 D5:2 B4:4', t='D4:4 B3:2 G#3:2 E#3:2 F#3:2', br='F#3:4 B2:8', b='D2:4 G#2:8', tag='48 F#m - sequence to the Neapolitan')
bar(s='C#6:3 B5:1 A5:2 A5:3 G#5:1 F#5:2', a='A4:3 B4:1 C#5:2 D5:3 E5:1 D5:2', t='F#3:6 B3:3 A3:1 G#3:2', br='C#3:6 F#3:6', b='F#2:6 D2:6', tag='49 F#m - Neapolitan (D): S falling dotted figure against A rising, contrary motion, new material')
bar(s='A5:4 G#5:2 F#5:2 D#5:4', a='F#5:4 E5:4 B#4:4', t='D4:4 G#4:4 D#4:4', br='F#3:4 G#3:8', b='D2:4 E2:4 G#2:4', tag='50 Neapolitan D (6) - E - dominant: bass rises D-E-G#, pre-dominant to the pedal')
bar(s='G#5:2 E5:1 D#5:1 B#4:2 F#5:6~', a='E4:6 G#4:1 F#4:1 D#4:1 F#4:1 G#4:1 A4:1', t='R:4 G#3:2 E3:1 D#3:1 B#2:2 F#3:2~', br='R:8 G#2:2 E2:1 D#2:1', b='G#1:12~', tag='51 FINAL PEDAL STRETTO: N-dom in S (x0), T (x4), Br (x8) at one-beat offsets, CS in A, pedal G#1 in the bass')
bar(s='F#5:4 G#5:2 A5:2 G#5:4~', a='G#4:4 B#4:4 D#5:4', t='F#3:4 D#4:4 B#3:4', br='D#2:8 D#3:4', b='G#1:12', tag='52 pedal stretto tails: G#7 over the G#1 pedal, all five voices sounding, rising to the half-cadence climax')
bar(s='G#5:6 A5:2 C#6:2 A5:2', a='E5:6 C#5:6', t='C#4:6 F#4:6', br='C#3:6 C#3:6', b='C#2:6 A2:6', tag='53 RELEASE: G#7 resolves to i (leading tones rise), then iv6; texture thins')
bar(s='C#6:6 B#5:6', a='A4:6 B#4:6', t='F#4:6 D#4:6', br='A3:6 G#3:6', b='F#2:6 G#2:6', tag='54 iv - V, the voices settle toward the cadence')
bar(s='B#5:4 D#6:2 F#6:2 D#6:4', a='D#5:4 F#5:8', t='B#3:4 F#4:8', br='G#2:4 D#3:4 G#3:4', b='G#2:12', tag='55 V7, last dominant before the Picardy tonic')
bar(s='C#6:12', a='E#5:12', t='G#4:12', br='G#3:12', b='C#2:12', tag='56 Picardy: C# major, held')
ENT=[('Tenor',1,2),('Alto',3,2),('Soprano',5,2),('Baritone',7,2),('Bass',9,2),
     ('Soprano',13,2),('Bass',15,2),('Alto',19,2),('Soprano',25,2),('Tenor',25,2),
     ('Bass',31,2),('Soprano',36,2),('Baritone',41,2),('Alto',43,2),('Bass',43,4),('Tenor',47,2),
     ('Soprano',51,2),('Tenor',51,2),('Baritone',51,2)]
LEVEL=lambda b:0
VOL={'Soprano':106,'Alto':100,'Tenor':100,'Baritone':98,'Bass':87}
