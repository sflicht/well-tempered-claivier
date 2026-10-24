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
bar(a='A4:3 G#4:1 F#4:2 D#4:2 B3:4', br='F#3:12', b='B1:6 B2:6', tag='12 B7: pivot to E major (vi = C#m)')
bar(s='B5:2 G#5:1 F#5:1 E5:2 B5:6', a='G#4:6 D#5:1 C#5:1 B4:1 C#5:1 D#5:1 E5:1', b='E2:4 G#2:2 B2:6', tag='13 Subject N+ (S, E major) + CS (A)')
bar(s='E6:4 C#6:2 B5:2 A5:2 G#5:2', a='C#5:3 B4:1 A4:2 F#4:2 D#4:4', b='E2:4 A2:2 B2:4 G#2:2',tag='14')
bar(s='G#5:12', t='G#3:6 B3:1 A3:1 G#3:1 A3:1 B3:1 C#4:1', b='B2:2 G#2:1 F#2:1 E2:2 B2:6',tag='15 Subject N+ (B, E major) + CS (T)')
bar(s='G#5:8 E5:4', t='G#3:3 F#3:1 E3:2 D#3:2 C#3:4', b='E3:4 C#3:2 B2:2 A2:2 G#2:2', tag='16')
bar(s='C#6:2 A5:1 B5:1 C#6:2 E6:6', t='E4:6 C#4:1 B3:1 A3:1 B3:1 C#4:1 E4:1', b='A2:6 C#3:6~', tag='17 E major: IV - A/C# (head cell in S, CS-run in T)')
bar(s='B5:3 A5:1 G#5:2 E#5:2 G#5:4', b='C#3:6 E#2:6',tag='18 C#7 (V of F#m)')
bar(s='A5:12', a='C#5:2 A4:1 G#4:1 E4:2 B4:6', t='A3:6 B3:1 C#4:1 A3:1 B3:1 A3:1 B3:1', b='F#2:4 C#3:2 D3:6', tag='19 Subject N (A) F#m + CS (T)')
bar(s='A5:4 G#5:8', a='D5:4 B4:2 G#4:2 E#4:2 F#4:2', t='F#4:3 E4:1 D4:2 B3:2 C#4:4', b='D3:4 G#2:4 C#3:2 F#2:2',tag='20')
bar(s='D#6:2 B5:1 A5:1 F#5:2 G#5:2 E5:1 D5:1 B4:2', t='F#3:1 D#3:1 A3:1 F#3:1 B3:1 A3:1 D4:1 B3:1 G#3:1 B3:1 E4:1 D4:1', b='B2:6 E2:6', tag='21 episode: head cell in S (B7 - E7), arpeggio-CS in T')
bar(s='A5:3 B5:1 E5:2 F#5:3 D#5:1 C5:2', t='C#4:1 E4:1 A3:1 E4:1 C#4:1 A3:1 C4:1 A3:1 F#3:1 A3:1 C4:1 A3:1', b='A2:12', tag='22 (A - D#o7 over A pedal)')
bar(s='B#5:2 G#5:1 F#5:1 D#5:2 G#5:2 E5:1 D#5:1 B4:2', t='D#4:1 F#4:1 B#3:1 D#4:1 G#3:1 B#3:1 G#3:1 B3:1 E4:1 B3:1 G#3:1 E3:1', b='G#2:6 E2:6', tag='23 (G#7 - C#m: S ends with real head)')
bar(s='A5:6 B#5:6', t='C#4:3 E4:1 F#3:2 B#3:2 D#4:1 F#4:1 G#4:2', b='F#2:6 G#2:6', tag='24 F#m - G#7 (prepare stretto)')

bar(s='G#5:2 E5:1 D#5:1 B4:2 F#5:6', t='R:4 G#4:2 E4:1 D#4:1 B3:2 F#4:2', br='E3:4 G#2:8', b='C#2:4 E2:8', tag='25 STRETTO, 1-beat offset: Subject N (S, C#m) then N (T) one beat later')
bar(s='A5:4 F#5:2 D#5:2 B#4:2 C#5:2', t='F#4:4 A4:4 F#4:2 D#4:2', br='F#3:12', b='F#2:6 G#2:6',tag='26 stretto tails')
bar(s='G#5:6 A5:6', t='B#3:2 C#4:2 E4:1 G#4:1 A3:1 C#4:1 F#4:1 C#4:1 A3:1 F#3:1', br='E3:12', b='G#2:6 F#2:6', tag='27 end of stretto: C#m - F#m, T figuration')
bar(s='F#5:4 A5:2 B#5:6', t='C4:1 A3:1 F#4:1 A3:1 C4:1 F#4:1 D#4:1 B#3:1 F#4:1 B#3:1 D#4:1 G#3:1', br='F#3:6 B#2:6', b='D#2:6 G#2:6', tag='28 D#o7 - G#7')
bar(s='C#6:4 A5:2 F#5:6', t='C#4:1 E4:1 A3:1 E4:1 C#4:1 A4:1 C#4:1 F#4:1 A4:1 F#4:1 C#4:1 A3:1', br='E3:6 F#3:6', b='A2:12', tag='29 DECEPTIVE: G#7 -> A, then D#o7 over A pedal')
bar(s='D#6:6 C#6:6', t='F#4:1 D#4:1 C#4:1 D#4:1 F#4:1 C#4:1 A#3:1 C#4:1 D#4:1 C#4:1 A#3:1 D#4:1', br='D#3:6 A#2:6', b='D#2:12', tag='30 D#o7/F# - D#7 (V of G#m)')
bar(s='R:6 G#5:6~', br='F#3:6 A#3:1 G#3:1 E3:1 G#3:1 F#3:1 A#3:1', b='D#3:2 B2:1 A#2:1 F#2:2 C#3:6', tag='31 Answer N (B, G#m) + CS (Br)')
bar(s='G#5:4 C#5:8', br='B3:3 G#3:1 E3:2 C#3:2 D#3:4', b='E3:4 C#3:2 A#2:2 F##2:2 G#2:2', tag='32')
bar(s='D#5:6 E5:6', a='G#4:12', t='B3:6 C#4:6', br='D#3:6 G#3:6', b='G#2:8 E2:4', tag='33 episode: G#m - C#m/E')
bar(s='F#5:12', a='F#4:4 A4:2 B4:6~', t='C#4:6 D#4:6', br='A3:12', b='A2:4 C#3:2 B2:6', tag='34 F#m/A - B7 (A held as prepared 7th)')
bar(s='E5:6 E#5:6', a='B4:6 C#5:6', t='B3:12', br='G#3:12', b='G#2:6 C#3:6', tag='35 E/G# - C#7')
bar(s='C#6:2 A5:1 G#5:1 E5:2 B5:6', a='C#5:6 D5:1 C#5:1 B4:1 C#5:1 D5:1 E5:1', t='A3:4 B3:4 D4:4', br='F#3:8 D3:4', b='F#2:4 E2:4 D2:4', tag='36 Subject N (S) F#m + CS (A)')
bar(s='D6:4 B5:2 G#5:2 E#5:2 F#5:2', a='F#4:3 G#4:1 B4:2 D5:2 G#4:4', t='A3:4 D4:4 B3:4', br='F#3:4 D3:8', b='D2:4 G#2:8')
bar(s='A5:2 F#5:1 E#5:1 C#5:2 D5:6', a='C#5:6 A4:6', t='A3:12', br='C#3:6 F#3:6', b='F#2:12', tag='38 F#m - Neapolitan 6th (D/F#)')
bar(s='D#5:6 E5:6', a='F#4:6 E4:6', t='B#3:6 C#4:6', br='A2:6 C#3:6', b='F#2:6 G#2:6~', tag='39 D#o7/F# - cadential 6/4')
bar(s='D#5:2 F#5:2 G#5:2 F#5:2 D#5:2 B#4:2', a='F#4:12', t='B#3:6 D#4:6', br='D#3:6 B#2:6', b='G#2:12', tag='40 G#7 dominant preparation')
bar(s='C#6:4 B5:4 A5:4', a='G#4:6 A4:1 B4:1 C#5:1 B4:1 C#5:1 B4:1', t='C#4:6 E4:6', br='G#3:2 E3:1 D#3:1 B2:2 F#3:6', b='C#2:4 G#2:4 A2:4', tag='41 Subject N (Br) C#m + CS (A) - the return')
bar(s='C#6:4 F#5:8', a='C#5:3 B4:1 A4:2 F#4:2 D#4:4', br='A3:4 F#3:2 D#3:2 B#2:2 C#3:2', b='F#2:8 G#2:4', tag='42 F#m - D#o7 - G#7')
bar(s='G#5:2 E5:1 D#5:1 B4:2 F#5:6', a='G#4:6 A4:6~', t='E4:6 F#4:6', br='G#3:6 F#3:6', b='G#2:3 R:1 E2:2 D#2:2 B1:4', tag='43 Subject N (S, C#m) against the bass in augmentation')
bar(s='A5:3 B5:1 A5:2 D#5:1 E5:1 B#4:1 D#5:1 C#5:2', a='A4:12', t='F#4:4 D#4:4 F#4:4', br='F#3:8 D#3:4', b='F#2:12', tag='44 augmentation continues (head to tail)')
bar(s='F#5:4 E5:4 F#5:4~', a='A4:4 C#5:8', t='C#4:8 A3:4', br='F#3:8 C#3:4', b='A2:8 F#2:4', tag='45 augmented tail')
bar(s='F#5:8 E5:4', a='D#5:8 C#5:4', t='A3:4 G#3:4 C#4:4', br='F#3:4 D#3:4 E3:4', b='D#2:4 B#1:4 C#2:4', tag='46 augmented tail closes on C#m')
bar(s='C#6:4 G#5:4 A5:4', a='C#5:6 F#4:1 A4:1 D5:1 F#4:1 D5:1 A4:1', t='C#4:2 A3:1 G#3:1 E3:2 B3:6', br='C#3:6 B2:2 F#3:4', b='F#2:4 E2:4 D2:4', tag='47 Subject N (T) F#m + CS (A)')
bar(s='F#5:8 G#5:4', a='A4:3 G#4:1 B4:2 D5:2 B4:4', t='D4:4 B3:2 G#3:2 E#3:2 F#3:2', br='F#3:4 B2:8', b='D2:4 G#2:8', tag='48 F#m - sequence to the Neapolitan')
bar(s='A5:6 D6:6', a='A4:8 F#4:4', t='F#3:6 A3:6', br='C#3:4 D3:8', b='F#2:12', tag='49 F#m - Neapolitan 6th (D/F#)')
bar(s='D6:6 E6:6', a='F#5:6 C#5:6', t='A3:6 E4:6', br='D3:6 C#3:6', b='F#2:6 G#2:6~', tag='50 Neapolitan 6th prolonged - cadential 6/4')
bar(s='G#5:2 E5:1 D#5:1 B#4:2 F#5:6', a='R:4 G#4:2 E4:1 D#4:1 B#3:2 F#4:2~', br='R:8 G#3:2 E3:1 D#3:1', b='G#2:12~', tag='51 STRETTO ON THE FINAL PEDAL: N-dom at 4-unit offsets (S, A, Br) over G#2')
bar(s='D#5:6 B#4:6', a='F#4:4 D#4:4 B#3:4', br='B#2:2 F#3:6 D#3:4', b='G#2:12', tag='52 stretto tails close on G#7')
bar(s='C#6:4 B5:2 A5:6', a='E5:6 C#5:6', t='E4:6 F#4:6', br='G#3:6 F#3:6', b='C#2:6 A2:6', tag='53 i - iv6 (7th resolves, leading tone resolves)')
bar(s='B#5:6 C#6:6', a='F#5:6 E5:6', t='D#4:6 C#4:6', br='A3:6 G#3:6~', b='F#2:6 G#2:6~', tag='54 D#o7/F# - cadential 6/4')
bar(s='B#5:4 D#6:4 B#5:4', a='F#5:12', t='D#4:12', br='G#3:4 D#3:4 G#3:4', b='G#2:12', tag='55 V7')
bar(s='C#6:12', a='E#5:12', t='C#4:12', br='G#3:12', b='C#2:12', tag='56 Picardy')

# thematic entries: (voice, first bar, bars) -- gets the entry accent in the performance
ENT=[('Tenor',1,2),('Alto',3,2),('Soprano',5,2),('Baritone',7,2),('Bass',9,2),
     ('Soprano',13,2),('Bass',15,2),('Alto',19,2),('Soprano',25,2),('Tenor',25,2),
     ('Bass',31,2),('Soprano',36,2),('Baritone',41,2),('Soprano',43,2),('Bass',43,4),('Tenor',47,2),
     ('Soprano',51,2),('Alto',51,2),('Baritone',51,2)]
LEVEL=lambda b:0
VOL={'Soprano':106,'Alto':100,'Tenor':100,'Baritone':98,'Bass':87}
