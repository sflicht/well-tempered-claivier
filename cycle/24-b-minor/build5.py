"""Wave 5 (bars 37-41): the subject in two-fold augmentation in F# minor (Bass II) under
CS1 in augmentation (S3); the remaining voices enter; the harmony turns from F# minor
towards the dominant of B (F#7 in bar 42 = c0 of the convergence)."""
from xxiv import *

S2_F = octv(aug(tr(S, -5, -3), 2), -2)     # F#2:8 A2:4 G#2:4 B#1:12 C#2:4 A#2:12 B2:4 G2:12 F#2:4 D2:4 D#2:4 E2:4 E#2:4


def wave5(sc, b0=37):
    P = sc.put
    b = lambda k: b0 + k
    sc.theme('B2', b(0), 1, S2_F, 'Subject x2 in F# minor (bass)', 'S', scale=2, semis=-29)
    # CS1 in two-fold augmentation (S3), complete but for its last note, which the convergence takes over
    P('S3', b(0), 1, "A4:4 R:4 C#5:8~"); P('S3', b(1), 1, "C#5:8 B#4:4 G#5:4~"); P('S3', b(2), 1, "G#5:8 F#5:8~")
    P('S3', b(3), 1, "F#5:8 E5:8"); P('S3', b(4), 1, "D5:8 C#5:8~")
    # long-breath lines: S1 descant, S2 under it, A4 and T5 in the middle
    P('S1', b(0), 1, "C#6:12 D6:4"); P('S1', b(1), 1, "D#6:16"); P('S1', b(2), 1, "C#6:12 B5:4")
    P('S1', b(3), 1, "B5:12 A#5:4"); P('S1', b(4), 1, "B5:4 A5:4 C#6:8~")
    P('S2', b(0), 1, "C#6:4 A5:8 F#5:4~"); P('S2', b(1), 1, "F#5:8 G#5:4 E#5:4"); P('S2', b(2), 1, "F#5:8 E5:4 D5:4")
    P('S2', b(3), 1, "D5:8 G5:6 F#5:2"); P('S2', b(4), 1, "F#5:8 E5:4 B5:4")
    P('A4', b(0), 1, "C#5:12 B4:4"); P('A4', b(1), 1, "G#4:16~"); P('A4', b(2), 1, "G#4:4 F#4:12")
    P('A4', b(3), 1, "G4:8 E4:4 F#4:4~"); P('A4', b(4), 1, "F#4:8 G#4:8")
    P('T5', b(0), 1, "F#3:12 G#3:4~"); P('T5', b(1), 1, "G#3:16"); P('T5', b(2), 1, "C#4:12 D4:4")
    P('T5', b(3), 1, "D4:14 C#4:2"); P('T5', b(4), 1, "D4:12 C#4:4")
    # figures: U (Br2), the end of B3's U, R (A5, T4)
    P('S4', b(0), 1, "C#5:4 B4:2 A4:6")
    P('Br2', b(0), 1, "R:6 C#3:2 C#3:2 C#3:2 A3:4~"); P('Br2', b(1), 1, "A3:2 G#3:6")
    P('B4', b(0), 1, "A3:12 B3:4"); P('B4', b(1), 1, "R:4 G#3:12"); P('B4', b(2), 1, "R:8 F#3:8")
    P('B3', b(1), 1, "G#2:16")
    P('Br5', b(0), 1, "C#3:16"); P('Br5', b(1), 1, "D#3:12 C#3:4"); P('Br5', b(2), 1, "C#3:12")
    P('Br5', b(4), 3, "E3:4 G#2:4")
    P('A5', b(1), 1, "D#4:1 E#4:1 F#4:1 G#4:1 A#4:1 G#4:1 F#4:1 E#4:1 D#4:4 G#4:4")
    P('T4', b(2), 4, "D4:4"); P('T4', b(3), 1, "G3:1 A3:1 B3:1 D4:1 G4:1 D4:1 B3:1 A3:1")
    P('A1', b(2), 4, "F#5:4")
    P('T1', b(3), 3, "C#4:8")                                               # Tenor I returns
    # Tenor II: U landing on the seventh of F#7, then a long line into c0
    P('T2', b(1), 3.5, "G#3:2 G#3:2 G#3:2"); P('T2', b(2), 1, "E4:6 D#4:2 C#4:8"); P('T2', b(3), 1, "B3:8 C#4:8")
    P('T2', b(4), 1, "C#4:2 B3:2 B#3:4 C#4:8")
    # Baritone III: a slow line under the tenors
    P('Br3', b(0), 1, "C#3:8 F#3:8"); P('Br3', b(1), 1, "G#3:16"); P('Br3', b(2), 1, "G#3:12 F#3:4")
    P('Br3', b(3), 1, "B2:8 E3:8"); P('Br3', b(4), 1, "F#3:8 C#3:8")
    # Bass I returns; Baritone IV returns; Soprano IV
    P('B1', b(3), 1, "D3:8 E3:4 C#3:4"); P('B1', b(4), 1, "R:8 G#2:8")
    P('Br4', b(3), 3, "C#4:8"); P('Br4', b(4), 3, "G#3:8")
    P('S4', b(2), 3, "C#5:8~"); P('S4', b(3), 1, "C#5:4 B4:4"); P('S4', b(4), 1, "B4:4 D#5:4 C#5:8")
    P('A5', b(2), 1, "R:8 F#4:4 B4:4"); P('A5', b(3), 1, "B4:8")
    P('T3', b(2), 3, "F#3:8")
    P('A2', b(3), 3, "G4:8~"); P('A2', b(4), 1, "G4:4 F#4:4")               # Alto II returns
    # U in Alto III (landing on the Neapolitan's D) and in Alto V (landing on Bm/D); R in Tenor III into c0
    P('A3', b(1), 1, "D#5:12 B4:4"); P('A3', b(2), 1, "C#5:10 F#4:2 F#4:2 F#4:2"); P('A3', b(3), 1, "D5:6 C#5:10"); P('A3', b(4), 1, "B4:4 F#4:8 G#4:4")
    P('A5', b(4), 2, "A4:4 G#4:8")
    P('T3', b(4), 1, "R:4 F#3:1 E#3:1 F#3:1 G#3:1 A3:1 B3:1 B#3:1 C#4:1 C#4:4~")
    P('Br2', b(4), 3, "C#4:8~")
    P('S5', b(4), 3, "G#5:8"); P('A1', b(4), 3, "C#5:8~"); P('T4', b(4), 3, "G#3:8")       # the last voices enter


B, C, Cs, D, Ds, E, F, Fs, G, Gs, A, As = 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Es, Bs = F, C
PLAN5 = [(0, 3, [Fs, A, Cs], 'F#m'), (3, 4, [Gs, B, D, Fs], 'G#o7'), (4, 7, [Gs, Bs, Ds, Fs], 'G#7/B#'), (7, 8, [Cs, Es, Gs, B], 'C#7'),
         (8, 11, [Fs, As, Cs, E], 'F#7/A#'), (11, 12, [B, D, Fs], 'Bm'), (12, 14, [G, B, D], 'G'), (14, 15, [Cs, E, G, B], 'C#o7/G'),
         (15, 16, [Fs, As, Cs, E], 'F#7'), (16, 17, [B, D, Fs], 'Bm/D'), (17, 18, [Bs, Ds, Fs, A], 'B#o7/D#'), (18, 19, [Cs, E, Gs], 'C#m/E'),
         (19, 20, [Cs, Es, Gs, B], 'C#7/E#'), (20, 24, [Fs, As, Cs, E], 'F#7')]
PLAN5_BASE = 144
PLAN5 = [[PLAN5_BASE + a, PLAN5_BASE + b, pcs, lab] for a, b, pcs, lab in PLAN5]
