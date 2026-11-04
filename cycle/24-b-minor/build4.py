"""Wave 4 (bars 26-36): the subject in A minor (Tenor IV) answered half a bar later by the
inversion on B (Alto IV); the subject in E minor (Alto V) with CS1 (Alto II); then the
dominant pedal on C# (bars 32-36, Bass II): the subject's head climbs T5 -> A3 -> S4, CS1
sounds complete in S3, Fugue V's head (in C# major, on top in S1) and Fugue VIII's head (in F#
minor, Br2) join, and the pedal choir grows by about a voice a bar (8 -> 11 moving voices a bar; since the second
review a voice that could only double another rests)."""
from xxiv import *

S_A = tr(S, -2, -1)        # A4 C5 B4 D#4 E4 C#5 D5 Bb4 A4 F4 F#4 G4 G#4
S_E = tr(S, -7, -4)        # E4 G4 F#4 A#3 B3 G#4 A4 F4 E4 C4 C#4 D4 D#4
CS1_E = tr(CS1, -7, -4)    # (rest) B4 A#4 F#5 E5 D5 C5 B4 A4


def wave4(sc):
    P = sc.put
    # ---- bars 26-28: S in A (Tenor IV) + I on B (Alto IV, new) half a bar later, a fifth
    # apart in register would give parallel fifths (D#/G# -> E/A); an eleventh apart they are fourths
    sc.theme('T4', 26, 1, octv(S_A, -1), 'Subject in A minor', 'S', semis=-14)
    sc.theme('A4', 26, 3, I, 'Inversion on B, stretto with the subject', 'I')
    P('B2', 26, 1, "A2:12 G#2:2 C#3:2"); P('B2', 27, 1, "C#3:6 E3:8 D3:2"); P('B2', 28, 1, "D3:4 G2:2 E2:2 B1:4 A1:4")
    P('S3', 26, 1, "E5:6 F#5:8 E5:2"); P('S3', 27, 1, "G#5:6 G5:8 A5:2")
    P('S1', 28, 1, "D6:8 A5:8")
    P('A1', 26, 1, "C5:6 A4:2")
    P('T3', 26, 1, "C4:6 R:6 E4:4"); P('T3', 27, 1, "B3:6 G3:8 C4:2"); P('T3', 28, 1, "D4:6 E4:2 F#4:4 C#4:2 A3:2")
    P('Br3', 26, 1, "A3:8 F#3:4")
    P('Br2', 26, 1, "E4:6")
    P('B1', 27, 4, "R:2 C3:2"); P('B1', 28, 1, "Bb2:6 G#2:2 F#2:4 A2:4")   # Bass I returns: a slow line above the leaping bass
    P('A3', 27, 1, "G#4:6 A#4:8 C5:2")
    P('S1', 27, 3, "D6:8~")                                    # Soprano I returns, above the E half-diminished
    P('Br2', 28, 3, "R:2 A2:2 A2:2 A2:2")      # Baritone II: U, landing on a leaning F#
    # ---- bars 29-31: S in E minor (Alto V) with CS1 (Alto II, new); S1 descant; R in T4
    sc.theme('A5', 29, 1, S_E, 'Subject in E minor', 'S', semis=-7)
    P('A2', 29, 1, CS1_E + '~')
    sc.entries.append(('A2', sc.pos(29, 2), 'CS1 (E minor)', 'CS1', 1, -7, False))
    P('Br2', 29, 1, "F#3:6 E3:2 C#3:6 F#3:2"); P('Br2', 30, 1, "E3:6 C3:8 B2:2"); P('Br2', 31, 1, "R:4 G3:2 B2:2 E3:4")   # C (7th) -> B; was C -> D, doubling CS1's D5
    P('B2', 29, 1, "E2:8 F#2:6 B1:2"); P('B2', 30, 1, "E2:6 A2:2 D2:4 E2:4"); P('B2', 31, 1, "A2:2 A#2:2 D3:2 B2:2 E2:4 C#2:4"); P('B2', 32, 1, "F#2:8 G#2:6 C#2:2~")
    P('S1', 29, 1, "G5:8 F#5:6 B5:2"); P('S1', 30, 1, "B5:6 C6:6 B5:4"); P('S1', 31, 1, "A5:2 G5:4 F#5:2 G#5:8")
    P('A4', 29, 1, "B4:4 E5:10 D#5:2"); P('A4', 30, 1, "D5:6 C5:2")
    P('A1', 29, 1, "R:2 E4:2 E4:2 E4:2 C#5:8~"); P('A1', 30, 1, "C#5:2 B4:6 D5:4 B4:4")   # Alto I returns, knocking (U)
    P('T3', 29, 3, "F#3:8~"); P('T3', 30, 1, "F#3:6 E3:2")
    P('T2', 28, 3, "B3:8~"); P('T2', 29, 1, "B3:16~"); P('T2', 30, 1, "B3:16")   # Tenor II returns: a long breath
    P('T2', 31, 1, "C4:4 G3:4 B3:4 C#4:4~"); P('T2', 32, 1, "C#4:8")
    P('A4', 31, 3, "G#4:8"); P('T3', 31, 3, "G#3:8")
    P('T4', 30, 1, "B3:1 A3:1 G#3:1 A3:1 B3:1 D4:1 E4:1 D4:1 F3:1 A3:1 C4:1 A3:1 G#3:1 B3:1 E4:1 D4:1"); P('T4', 31, 1, "A3:4 B3:12"); P('T4', 32, 1, "A3:4")
    P('A2', 32, 1, "A4:8 G#4:8")
    P('A5', 31, 3, "E4:4 E#4:4"); P('A5', 32, 1, "F#4:8 D#4:6 C#4:2")
    # ---- bars 32-36: dominant pedal on C# (Bass II holds it from 32.4.5 to 36.4); over it the
    # subject's head climbs T5 -> A3 -> S4, CS1 sounds complete in S3, Fugue V's head (in C# major)
    # and Fugue VIII's head (in F# minor) join, and the pedal choir grows one voice a bar.
    # Harmony: 32 i | V/V-V ; 33-34 i6/4 | V(7) ; 35 V7 | i6/4 ; 36 V7 . . i  (-> 37 i, subject x2)
    P('T5', 32, 1, "F#3:4 A3:2 G#3:2 B#2:6 C#3:2")          # Tenor V enters: head in F# minor
    P('S3', 32, 1, "R:4 C#5:8 B#4:2 G#5:2~")                  # CS1, complete, in F# minor (S3, b32-34)
    P('S3', 33, 1, "G#5:4 F#5:8 E5:4"); P('S3', 34, 1, "D5:4 C#5:12")   # last note B delayed to 35.1 (no B/B#/C# at 34.4)
    P('S3', 35, 1, "B4:8 A4:8"); P('S3', 36, 1, "A4:4 G#4:8 A4:4~")
    P('T3', 32, 3, "G#3:1 A#3:1 B#3:1 C#4:1 D#4:1 C#4:1 B#3:1 G#3:1")
    P('S1', 32, 1, "A5:8 R:6 C#6:2~")      # breathes, re-enters with the pedal (its C# was a 4th over G#)
    # Soprano I, on top, sings Fugue V's head (D major -> C# major, an octave up) at 34.3-35.3: a foretaste
    # of the full Fugue V that it sings on top at b43 (review 2, #6; it was in Alto I, under three sopranos)
    P('S1', 33, 1, "C#6:8 D#6:4 C#6:4~"); P('S1', 34, 1, "C#6:8 G#5:4 C#6:2 C#6:1 C#6:1")
    P('S1', 35, 1, "E#6:2 E#6:1 E#6:1 G#6:4 F#6:8"); P('S1', 36, 1, "E#6:8 C#6:8~")
    for k in (33, 34, 35):
        P('B2', k, 1, "C#2:16~")
    P('B2', 36, 1, "C#2:16")
    # bar 33: head in Alto III
    P('A3', 33, 1, "F#4:4 A4:2 G#4:2 B#3:6 C#4:2")
    P('A3', 34, 1, "C#4:16"); P('A3', 35, 1, "C#4:16"); P('A3', 36, 1, "C#4:16")
    P('T5', 33, 1, "C#3:12 G#3:4~"); P('T5', 34, 1, "G#3:4 F#3:4 E#3:4 G#3:4~"); P('T5', 35, 1, "G#3:8 A3:8")
    P('T5', 36, 1, "G#3:16")
    P('A2', 33, 1, "C#5:8 G#4:8~"); P('A2', 34, 1, "G#4:4 A4:4")
    P('A5', 33, 1, "C#4:16")
    P('T2', 33, 1, "A3:16~"); P('T2', 34, 1, "A3:8 G#3:4")
    P('B3', 33, 4.5, "C#3:2"); P('B3', 34, 1, "C#3:2 C#3:2 A3:6 G#3:6")      # Bass III enters: U, knocking on the pedal
    P('Br5', 33, 1, "F#2:12 G#2:4"); P('Br5', 34, 1, "A2:8 C#3:8~"); P('Br5', 35, 1, "C#3:8")              # Baritone V enters
    P('Br3', 33, 1, "A2:8 G#2:8"); P('Br3', 34, 1, "F#2:8 G#2:8~"); P('Br3', 35, 1, "G#2:12 F#2:4"); P('Br3', 36, 1, "C#3:8")   # Baritone III rejoins
    P('S2', 33, 1, "A5:12 G#5:4")                                         # Soprano II returns
    # bar 34: head in Soprano IV; Fugue V's head (in C# major) on top, in Soprano I (above)
    P('S4', 34, 1, "F#5:4 A5:2 G#5:2 B#4:6 C#5:2")
    P('S4', 35, 1, "C#5:8 A5:8"); P('S4', 36, 1, "C#6:8 B5:4 A5:4")
    P('A1', 36, 1, "G#5:16"); P('A1', 37, 1, "A5:8")            # Alto I returns after Fugue V's head (now in S1)
    P('A4', 35, 2, "E#4:4 F#4:8")      # Alto IV returns
    P('B3', 36, 2.5, "C#3:2 C#3:2 C#3:2 A3:4~"); P('B3', 37, 1, "A3:2 G#3:2 F#3:4")  # U again, landing on the tonic
    P('A2', 35, 3, "C#5:8"); P('A2', 36, 1, "C#5:8")
    # bar 35.3: Fugue VIII's head (E-flat minor -> F# minor) in Baritone II, resolving into bar 37
    P('Br2', 35, 3, "F#3:4 C#4:4"); P('Br2', 36, 1, "D4:3 C#4:1 B3:2 A3:2 G#3:2 E#3:2 F#3:4")


B, C, Cs, D, Ds, E, F, Fs, G, Gs, A, As = 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Eb, Bb, Es = Ds, As, F
PLAN4 = [(0, 1.5, [A, C, E], 'Am'), (1.5, 3, [B, Ds, Fs, A], 'B7/A'), (3, 3.5, [E, Gs, B], 'E/G#'), (3.5, 4, [A, Cs, E], 'A/C#'),
         (4, 5.5, [Cs, Es, Gs, B], 'C#7'), (5.5, 7.5, [E, G, Bb, D], 'E-half-dim7'), (7.5, 8, [D, Fs, A, C], 'D7'),
         (8, 8.5, [Bb, D, F], 'Bb/D'), (8.5, 9, [Bb, D, Fs], 'Bb+/D'), (9, 9.5, [G, Bb, D], 'Gm'), (9.5, 10, [E, Gs, B, D], 'E7'),
         (10, 10.5, [B, Ds, Fs, A], 'B7'), (10.5, 11, [B, D, Fs, A], 'Bm7'), (11, 11.5, [A, Cs, E], 'A'), (11.5, 12, [A, C, E], 'Am'),
         (12, 13.5, [E, G, B], 'Em'), (13.5, 14, [E, G, B, Fs], 'Em(9)'), (14, 15.5, [Fs, As, Cs, E], 'F#7'),
         (15.5, 16, [B, Ds, Fs], 'B'), (16, 17.5, [E, Gs, B, D], 'E7'), (17.5, 18, [A, C, E], 'Am'), (18, 19, [D, F, A, C], 'Dm7'),
         (19, 20, [E, Gs, B, D], 'E7'), (20, 20.5, [A, C, E], 'Am'), (20.5, 21, [As, Cs, E, G], 'A#o7'), (21, 21.5, [D, G, B, Fs], 'G/D'),
         (21.5, 22, [B, Ds, Fs, A], 'B7'), (22, 23, [E, Gs, B], 'E'), (23, 24, [Cs, Es, Gs, B], 'C#7')]
Bs = C
PLAN4 += [(24, 26, [Fs, A, Cs], 'F#m'), (26, 27.5, [Gs, Bs, Ds], 'G#'), (27.5, 28, [Cs, Es, Gs], 'C#'),                 # bar 32
          (28, 30, [Fs, A, Cs], 'F#m/C#'), (30, 31, [Gs, Bs, Ds, Fs], 'G#7/C# (pedal)'), (31, 32, [Cs, Es, Gs], 'C#'),  # bar 33
          (32, 34, [Fs, A, Cs], 'F#m/C#'), (34, 35, [Cs, Es, Gs], 'C#'), (35, 36, [Cs, Es, Gs, B], 'C#7'),              # bar 34
          (36, 38, [Cs, Es, Gs, B], 'C#7'), (38, 40, [Fs, A, Cs], 'F#m/C#'),                                             # bar 35
          (40, 42, [Cs, Es, Gs, B], 'C#7'), (42, 43, [Cs, Es, Gs], 'C#'), (43, 44, [Fs, A, Cs], 'F#m')]                  # bar 36
PLAN4 = [[100 + a, 100 + b, pcs, lab] for a, b, pcs, lab in PLAN4]
