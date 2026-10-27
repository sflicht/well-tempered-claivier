"""Wave 5 (bars 35-39): the subject in two-fold augmentation in F# minor (Bass II) under
CS1 in augmentation (S3); the remaining voices enter; the harmony turns from F# minor
towards the dominant of B (F#7 in bar 40 = c0 of the convergence)."""
from xxiv import *

S2_F = octv(aug(tr(S, -5, -3), 2), -2)     # F#2:8 A2:4 G#2:4 B#1:12 C#2:4 A#2:12 B2:4 G2:12 F#2:4 D2:4 D#2:4 E2:4 E#2:4


def wave5(sc):
    P = sc.put
    sc.theme('B2', 35, 1, S2_F, 'Subject x2 in F# minor (bass)', 'S', scale=2, semis=-29)
    # ---- bar 35: F#m | G#o7
    P('Br5', 35, 1, "C#3:12 B2:4")
    P('B4', 35, 1, "A3:12 B3:4")
    P('T5', 35, 1, "F#3:4")
    P('A3', 35, 1, "C#4:12 F#4:4")
    P('S1', 35, 1, "C#6:12 D6:4")
    P('S3', 35, 1, "F#5:4 R:4 C#5:8~")                     # CS1 in augmentation begins (C# held)
    P('S4', 35, 1, "C#5:4 B4:2 A4:6 D5:4")
    P('Br2', 35, 3, "R:2 F#3:2 F#3:2 F#3:2")                 # U, landing on D# in bar 36

    # ---- bar 36: G#7/B# | C#7
    P('S3', 36, 1, "C#5:8 B#4:4 G#5:4~"); P('S3', 37, 1, "G#5:8 F#5:8~"); P('S3', 38, 1, "F#5:8 E5:8")
    P('B3', 36, 1, "G#2:16")
    P('Br5', 36, 1, "D#3:12 C#3:4")
    P('B4', 36, 1, "G#3:16")
    P('A3', 36, 1, "F#4:12 E#4:4")
    P('S1', 36, 1, "D#6:16")
    P('Br2', 36, 1, "D#4:6 C#4:10")
    P('A5', 36, 1, "D#4:1 E#4:1 F#4:1 G#4:1 A#4:1 G#4:1 F#4:1 E#4:1 D#4:4 G#4:4")
    P('T2', 36, 3, "R:2 G#3:2 G#3:2 G#3:2")

    # ---- bar 37: F#7/A# | Bm
    P('S1', 37, 1, "C#6:12 B5:4")
    P('A3', 37, 1, "F#4:16")
    P('Br5', 37, 1, "C#3:12")
    P('B4', 37, 1, "G#3:4 F#3:12")
    P('T2', 37, 1, "E4:6 D#4:2 C#4:8")
    P('A5', 37, 1, "C#5:12 D5:4")
    P('Br2', 37, 1, "C#4:8")

    # ---- bar 38: G | C#o7/G | F#7
    P('S1', 38, 1, "B5:12 A#5:4")
    P('S2', 38, 1, "R:8 G5:6 F#5:2")                          # Soprano II returns
    P('A3', 38, 1, "G4:12 E4:4")
    P('A5', 38, 1, "D5:8 C#5:8")
    P('T2', 38, 1, "B3:12 C#4:4")
    P('T4', 38, 1, "G3:1 A3:1 B3:1 D4:1 G4:1 D4:1 B3:1 A3:1")
    P('B1', 38, 1, "D3:8 E3:4 C#3:4")                              # Bass I returns

    # ---- bar 39: Bm/D | B#o7/D# | C#m/E | C#7/E#  -> c0 (F#7)
    P('S1', 39, 1, "B5:4 A5:4 G#5:8")
    P('S2', 39, 1, "F#5:8 E5:4 B5:4")
    P('A3', 39, 1, "F#4:8 G#4:8")
    P('A5', 39, 1, "D5:4 A4:4 E4:4 C#5:4")
    P('T2', 39, 1, "C#4:2 B3:2 B#3:4 C#4:4 G#3:4")
    P('B1', 39, 1, "B2:4 F#2:4 C#3:8")
    P('Br5', 39, 3, "E3:4 G#2:4")
    P('Br2', 39, 2, "F#3:12")                                 # held F#: suspended over C#m/C#7, the c0 note
    P('T3', 39, 1, "F#3:4 D#4:4 G#3:4 C#4:4")                  # Tenor III rejoins, rising to c0's C#
    P('S4', 39, 1, "B4:4 D#5:4 C#5:4")


B, C, Cs, D, Ds, E, F, Fs, G, Gs, A, As = 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Es, Bs = F, C
PLAN5 = [(0, 3, [Fs, A, Cs], 'F#m'), (3, 4, [Gs, B, D, Fs], 'G#o7'), (4, 7, [Gs, Bs, Ds, Fs], 'G#7/B#'), (7, 8, [Cs, Es, Gs, B], 'C#7'),
         (8, 11, [Fs, As, Cs, E], 'F#7/A#'), (11, 12, [B, D, Fs], 'Bm'), (12, 14, [G, B, D], 'G'), (14, 15, [Cs, E, G, B], 'C#o7/G'),
         (15, 16, [Fs, As, Cs, E], 'F#7'), (16, 17, [B, D, Fs], 'Bm/D'), (17, 18, [Bs, Ds, Fs, A], 'B#o7/D#'), (18, 19, [Cs, E, Gs], 'C#m/E'),
         (19, 20, [Cs, Es, Gs, B], 'C#7/E#'), (20, 24, [Fs, As, Cs, E], 'F#7')]
PLAN5 = [[136 + a, 136 + b, pcs, lab] for a, b, pcs, lab in PLAN5]
