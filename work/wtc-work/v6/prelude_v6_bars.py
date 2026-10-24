# Prelude IV v5 - literal bars (3/4, sixteenth units). U = upper line (R.H.), L = lower line (L.H.).
# Motif M = 2,1,1,2,3,1,1,1  (E5 C#5 D#5 E5 G#5 F#5 E5 D#5 in C# minor).
# v5: the hand that is not stating M plays continuous sixteenth broken chords (implied 2-3 voice writing);
# exceptions (dramatic): the V-pedal augmentation is accompanied by a V7 arpeggio (still sixteenths),
# the caesura bars 21-22 (held arrival + pedal alone) and the final bar.
# Helper S('..') only appends ':1' to bare tokens (timing); every pitch is written out literally.
U=[]; L=[]; TAG=[]
def S(s): return ' '.join(t if ':' in t else t+':1' for t in s.split())
def bar(u,l,tag=''):
    U.append(u); L.append(l); TAG.append(tag)
M0='E5:2 C#5:1 D#5:1 E5:2 G#5:3 F#5:1 E5:1 D#5:1'
# ---- A: C# minor (1-8)
bar(M0, S('C#3 G#3 E4 G#3 C#3 G#3 E4 G#3 G#2 D#3 F#3 D#3'),'A1 i: U states M; L broken C#m triads (C#-G#-E-G#), turning to V on beat 3')
bar('C#5:2 B4:3 A4:1 G#4:1 F#4:1 G#4:4', S('E3 G#3 C#4 G#3 F#3 A3 C#4 A3 G#2 D#3 B#3 D#3'),'A2 i6-ii6-V: U descends; L broken chords on E, F#m, G#')
bar(M0, S('C#4 G#3 C#3 G#3 A2 E3 A3 C#4 D#3 F#3 B#3 F#3'),'A3 i6-IV(A)-vii: M again; L rises through A major to D#dim')
bar('C#5:6 D#5:2 E5:4', S('C#3 G#3 E4 G#3 C#3 G#3 B3 G#3 A2 E3 A3 C#4'),'A4 i-IV: cadence-like; L keeps 16ths (B3 passing tone inside the C#m figure)')
bar(S('G#4 C#5 E5 C#5 C#5 A4 E5 A4 B#4 D#5 F#5 D#5'), 'E3:2 C#3:1 D#3:1 E3:2 G#3:3 F#3:1 E3:1 D#3:1','A5 HAND SWITCH: L states M (tenor); U plays 16ths: C#m, A major, G#dim/V')
bar('A5:2 F#5:1 G#5:1 A5:2 C#6:3 B5:1 A5:1 G#5:1', S('F#3 C#4 A3 C#4 F#3 C#4 F#4 C#4 E3 A3 C#4 A3'),'A6 iv: M up a fourth; L F#m, then D (iv6)')
bar('D#5:2 B#4:1 C#5:1 D#5:2 F#5:3 E5:1 D#5:1 C#5:1', S('G#2 D#3 B#3 D#3 G#2 D#3 B#3 F#3 D#3 F#3 B#3 F#3'),'A7 V: M on the dominant with leading tone; L G#7 -> D#dim')
bar('C#5:2 D#5:1 E5:1 G#5:4 F#5:2 E5:1 D#5:1', S('C#3 G#3 C#4 G#3 C#3 G#3 E4 B3 F#3 A3 B3 D#4'),'A8 i, then B7 (V of E) pivot into E major')
# ---- B: E major (9-14)
bar('G#5:2 E5:1 F#5:1 G#5:2 B5:3 A5:1 G#5:1 F#5:1', S('E3 B3 G#4 B3 E3 B3 G#4 B3 A2 E3 C#4 E3'),'B9 I: M in E major; L broken E triads, then A (IV)')
bar(S('B4 E5 G#5 E5 D#5 F#5 B4 D#5 G#4 B4 E5 B4'), 'G#3:2 E3:1 F#3:1 G#3:2 B3:3 A3:1 G#3:1 F#3:1','B10 HAND SWITCH: L states M in E (tenor); U 16ths: E, B, E6/4')
bar('B4:2 G#4:1 A4:1 B4:2 D#5:3 C#5:1 B4:1 A4:1', S('B2 F#3 D#4 F#3 B2 F#3 A3 D#4 F#3 A3 D#4 A3'),'B11 V7: M on B; L B7 arpeggios, 3rd up')
bar('G#4:4 B4:2 E5:2 G#5:4', S('E3 B3 E4 B3 E3 B3 G#3 B3 C#3 G#3 E4 G#3'),'B12 I -> vi: L broken E, then C#m under G#5')
bar('G#5:3 F#5:1 E5:2 F#5:3 E5:1 D#5:2', S('E3 B3 G#4 B3 C#3 E3 A3 E3 B2 F#3 A3 F#3'),'B13 I-IV-V7: L broken chords E, A, B7')
bar('B4:4 A4:2 G#4:2 E5:3 D5:1', S('B2 F#3 D#4 F#3 C#3 G#3 E4 G#3 E3 G#3 B3 D4'),'B14 V7-vi-I7: D natural (7th of E7) anticipates A major')
# ---- C: development (15-27)
bar('C#5:2 A4:1 B4:1 C#5:2 E5:3 D5:1 C#5:1 B4:1', S('A2 E3 A3 E3 A2 E3 A3 C#4 E3 B3 G#3 D4'),'C15 A major (bVI): sequence 1; L A major arpeggios, E7-ish beat 3')
bar(S('C#5 E5 A5 E5 C#5 F#5 A5 F#5 E5 G#5 B5 E5'), 'A3:2 F#3:1 G#3:1 A3:2 C#4:3 B3:1 A3:1 G#3:1','C16 HAND SWITCH, sequence 2: L states M in F#m; U 16ths F#m7, F#m, E')
bar('F#5:2 D5:1 E5:1 F#5:2 A5:3 G5:1 F#5:1 E5:1', S('F#3 A3 D4 A3 D3 B3 A3 B3 E3 G3 A3 C#4'),'C17 D major (Neapolitan 6/3): sequence 3; L D6/3, Bm7-ish, A7/E')
bar('D#5:2 B4:1 C#5:1 D#5:2 F#5:3 E5:1 D#5:1 C#5:1', S('B2 F#3 B3 F#3 D#3 F#3 B3 D#4 G#2 D#3 F#3 B3'),'C18 B major (VII), sequence step 4 (A - F#m - D - B, falling thirds); beat 3 turns to G#m7 (B natural) so F# is a prepared 7th; B -> B# in L at the next bar')
bar('E5:4 C#5:2 D#5:2 E5:4', S('G#2 D#3 B#3 D#3 F#3 G#3 B#3 D#4 G#2 D#3 B#3 D#3'),'C19 V pedal; M in augmentation (1); L G#7 arpeggios keep the pedal pulsing')
bar('G#5:6 F#5:2 E5:2 D#5:2', S('G#2 D#3 F#3 B#3 D#3 F#3 B#3 D#4 G#3 B#3 D#4 F#4'),'C20 augmentation (2); L arpeggio climbs through G#7 toward the arrival')
bar('D#5:2 F#5:4 B#4:1 D#5:1 F#5:1 D#5:1 B#4:1 D#5:1', S('G#2:6 D#3 G#3 B#3 D#4 G#3 B#3'),'C21 ARRIVAL (v6: the caesura is gone): the dominant 7th F#5 is held for 1.5 beats over the G# pedal, then 16ths run on at once - no silence anywhere')
bar('E5:1 C#5:1 D#5:1 E5:1 G#5:1 F#5:1 E5:1 D#5:1 B#4:1 C#5:1 D#5:1 F#5:1', S('G#2 D#3 G#3 D#3 G#2 D#3 B#3 D#3 G#2 D#3 F#3 B#3'),'C23 DROP: M as continuous sixteenths in U; L G#7 pedal arpeggios')
bar('G#5:1 F#5:1 E5:1 D#5:1 C#5:1 D#5:1 E5:1 F#5:1 G#5:1 A5:1 B5:1 C#6:1', S('G#2 D#3 B#3 F#3 C#3 G#3 C#4 G#3 C#4 A3 F#3 A3'),'C24 flurry rises; L V - i - iv')
bar('D#5:2 B#4:1 C#5:1 D#5:2 F#5:2 E5:2 C#5:1 D#5:1', S('G#2 D#3 G#3 B#3 D#4 B#3 G#3 D#3 C#3 E3 G#3 C#4'),'C25 hemiola begins: L 16ths in groups of 8 (3 x 8 over two bars of 3/4)')
bar('E5:2 G#5:2 F#5:2 D#5:1 E5:1 F#5:2 A5:2~', S('C#4 G#3 E3 C#3 F#3 A3 C#4 A3 F#3 A3 C#4 A3'),'C26 hemiola; ties the A5 into the approach')
bar('A5:4 G#5:2 F#5:2 D#5:2 F#5:2', S('G#2 B#2 D#3 F#3 G#3 F#3 D#3 B#2 G#2 B#2 F#3 D#3'),'C27 V7 approach (A over the dominant)')
# ---- D: shortened return (28-39)
bar('E5:2 C#5:1 D#5:1 E5:2 G#5:3 F#5:1 E5:1 D#5:1', S('G#3 C#4 E3 C#4 G#3 E3 C#4 E3 A2 C#3 E3 G#3'),'D28 i: return; L now falls (G#-E-C#) instead of rising')
bar('D#5:2 B#4:1 C#5:1 D#5:2 F#5:3 E5:1 D#5:1 C#5:1', S('B#2 F#3 D#4 F#3 B#2 G#3 D#4 G#3 F#3 B#3 D#4 B#3'),'D29 V: M on the dominant; L G#7/B# first inversion arpeggios')
bar(S('C#5 G#5 E5 G#5 C#5 A5 E5 A5 D#5 F#5 B#4 F#5'), 'E4:2 C#4:1 D#4:1 E4:2 G#4:3 F#4:1 E4:1 D#4:1','D30 HAND SWITCH: L states M in the middle register; U plays 16ths above')
bar('F#5:4 D5:4 A5:4', S('F#3 A3 D4 A3 F#3 A3 D4 F#4 A3 D4 F#4 A3'),'D31 Neapolitan (D): U long notes; L D major arpeggios')
bar('E5:2 C#5:1 B4:1 C#5:2 D#5:3 F##5:3', S('A2 E3 A3 E3 A2 D#3 C#3 A3 C#3 D#3 A3 F##3'),'D32 French 6th (A C# D# F##); L spells the whole chord as an arpeggio')
bar('G#5:4 A5:1 G#5:1 E5:3 C#5:3', S('G#2 E3 C#4 E3 C#3 E3 G#3 E3 G#2 C#3 E3 C#3'),'D33 i 6/4 over the G# bass')
bar('E5:2 C#5:1 D#5:1 E5:2 G#5:3 A5:1 B5:1 C#6:1', S('C#3 E3 G#3 E3 C#3 E3 A3 E3 F#2 A2 C#3 F#3'),'D34 i: M with rising tail; L moves to iv at the end')
bar('C#6:3 B5:1 A5:4 C#6:2 G#5:2', S('A3 E4 G#3 G3 F#3 D4 F3 D4 E3 B3 G#3 E4'),'D35 DESCENDING CHROMATIC BASS A-G#-G-F#-F-E (implied in L on every 2nd sixteenth), pivot E-D-C# above it')
bar('D#5:2 B#4:1 C#5:1 D#5:2 G#5:3 F#5:1 E5:1 D#5:1', S('G#2 B#2 D#3 F#3 G#2 B#2 D#3 F#3 G#2 D#3 F#3 B#3'),'D36 V: L G#7 rising arpeggios')
bar('C#5:2 E5:1 D#5:1 C#5:2 G#4:2 E5:2 G#5:2', S('E3 G#3 B3 G#3 C#3 E3 G#3 E3 C#3 G#3 E3 C#4'),'D37 i')
bar('G#5:3 F#5:3 E5:3 D#5:3', S('E3 G#3 C#4 G#3 E3 G#3 C#4 G#3 B#2 D#3 F#3 G#3'),'D38 tail G#-F#-E-D#; L i6 then V6/5')
bar('C#5:12', 'C#3:6 C#2:6','D39 end: final tonic (dramatic exception: octave C# below a held C#5)')

