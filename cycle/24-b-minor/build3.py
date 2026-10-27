"""Wave 3 (bars 18-25): the inversion's first entry (S1, E minor) answered half a bar
later by the subject in D (T3) -- a close stretto of the two mirror forms -- with the
texture deliberately thinned around the high entry; then low voices re-enter."""
from xxiv import *

I_E = tr(I, 5, 3)          # E5 C#5 D5 A#5 A5 C5 B4 D#5 E5 G#5 G5 F#5 F5
S_D = tr(S, -9, -5)        # D4 F4 E4 G#3 A3 F#4 G4 Eb4 D4 Bb3 B3 C4 C#4


def wave3(sc):
    P = sc.put
    # ---- bars 18-20: I in E (S1) + S in D (T3), half a bar apart
    sc.theme('S1', 18, 1, I_E, 'Inversion (E minor)', 'I', semis=5)
    P('S1', 20, 3, "E5:2 D5:2 C5:2 E5:2")
    sc.theme('T3', 18, 3, S_D, 'Subject in D, stretto with the inversion', 'S', semis=-9)
    P('B1', 18, 1, "E2:4 A2:2 D2:8 E2:2~")
    P('B1', 19, 1, "E2:6 B2:8 E2:2")
    P('B1', 20, 1, "Eb2:4 D2:4 C2:2 B1:2 A1:4")
    P('A1', 18, 1, "G4:6 F4:8 C4:2")
    P('A1', 19, 1, "B3:6")
    P('A3', 18, 1, "B3:4 A3:4")
    P('T2', 18, 1, "B3:4")
    P('Br2', 18, 1, "E4:4")
    P('A5', 19, 1, "E4:1 F#4:1 G#4:1 B4:1 D5:1 B4:1 A4:8 G4:2~")
    P('A5', 20, 1, "G4:4 A4:4 E4:8~")
    P('S2', 20, 1, "Bb4:4 C5:4 G4:4 A4:4")

    # ---- bars 21-23: arrival in D minor; the bass hands over to the subject in C (Bass II),
    # a CS1-shaped suspension line above it (S3), U in T2 landing on the 7th of C7
    P('S1', 21, 1, "F5:4")
    P('S2', 21, 1, "A4:4 B4:4 C5:8~"); P('S2', 22, 1, "C5:6 B4:2 C5:6 A4:2")
    P('S3', 21, 4, "G5:8 F#5:2 D6:6 C6:8 Bb5:4 Ab5:2 C6:2 D6:4")
    P('A1', 21, 3, "G4:8"); P('A1', 22, 1, "A4:1 F#4:1 A4:1 D5:1 C5:1 A4:1 G4:1 F#4:1 G4:6 A4:2")
    P('A1', 23, 1, "Ab4:6 Bb4:2 C5:6 D5:2")
    P('A3', 22, 1, "D4:8 R:6 F4:2"); P('A3', 23, 1, "F4:6 E4:2 F4:2 F#4:2 G4:4")
    P('A5', 21, 1, "E4:4 F4:4 Eb4:8")
    P('T2', 22, 1, "R:2 D3:2 D3:2 D3:2 Bb3:6 A3:2"); P('T2', 23, 1, "F3:6 G3:2 Ab3:2")
    P('T3', 21, 1, "D4:12 C4:4"); P('T3', 22, 1, "A3:8 G3:6 C4:2"); P('T3', 23, 1, "Bb3:8 Eb4:2 D4:6~")
    P('Br2', 21, 1, "F3:4 G3:12")
    P('B1', 21, 1, "D2:4 G2:4")
    sc.theme('B2', 21, 3, tr(S, -23, -13), 'Subject in C (bass)', 'S', semis=-23)

    # ---- bars 24-25: C major after the bass subject; two low voices knock their way in with U
    P('S3', 24, 1, "C6:6 B5:2 C6:6 B5:2"); P('S3', 25, 1, "A5:8 E5:8")
    P('A1', 24, 1, "E5:8 C5:8"); P('A1', 25, 1, "D5:8 B4:8")
    P('A3', 24, 1, "G4:8 A4:8"); P('A3', 25, 1, "B4:4 C5:2 B4:2")
    P('T3', 24, 1, "D4:4 C4:4 E4:8~"); P('T3', 25, 1, "E4:4 D4:12")
    P('Br3', 24, 1, "R:6 E3:2 E3:2 E3:2 C4:4~"); P('Br3', 25, 1, "C4:2 B3:2 A3:4 G#3:8")
    P('Br2', 24, 4, "R:2 A3:2"); P('Br2', 25, 1, "A3:2 A3:2 F4:6 E4:2 E4:4")    # Baritone II returns (U)
    P('B2', 24, 1, "C3:8 A2:8"); P('B2', 25, 1, "D3:8 E3:8")


B, C, Cs, D, Ds, E, F, Fs, G, Gs, A, As = 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Eb, Bb = Ds, As
PLAN3 = [(0, 1, [E, G, B], 'Em'), (1, 1.5, [A, Cs, E, G], 'A7'), (1.5, 2, [D, F, A], 'Dm'), (2, 3.5, [Bb, D, F], 'Bb'),
         (3.5, 4, [A, C, E], 'Am'), (4, 5.5, [E, Gs, B, D], 'E7'), (5.5, 7.5, [B, Ds, Fs, A], 'B7'), (7.5, 8, [E, G, B], 'Em/G'),
         (8, 9, [Eb, G, Bb], 'Eb'), (9, 9.5, [D, Fs, A, C], 'D7'), (9.5, 10, [D, F, A], 'Dm'), (10, 10.5, [C, E, G, Bb], 'C7'),
         (10.5, 11, [G, B, D], 'G'), (11, 11.5, [A, C, E], 'Am'), (11.5, 12, [A, Cs, E, G], 'A7'), (12, 13, [D, F, A], 'Dm'), (13, 14, [G, B, D, F], 'G7'), (14, 15.5, [C, Eb, G], 'Cm'),
         (15.5, 16, [G, B, D], 'G/D'), (16, 17.5, [D, Fs, A, C], 'D7/F#'), (17.5, 18, [G, B, D], 'G'), (18, 19.5, [C, E, G, Bb], 'C7/E'),
         (19.5, 20, [F, A, C], 'F'), (20, 21.5, [Bb, Cs, F, Gs], 'Bbm7/Db'), (21.5, 22, [C, E, G, Bb], 'C7'), (22, 22.5, [F, Gs, C], 'Fm/Ab'),
         (22.5, 23, [D, Fs, A, C], 'D7/A'), (23, 23.5, [G, Bb, D], 'Gm/Bb'), (23.5, 24, [G, B, D, F], 'G7/B'), (24, 26, [C, E, G], 'C'), (26, 28, [A, C, E], 'Am'), (28, 30, [B, D, F, A], 'Bo7/D'), (30, 32, [E, Gs, B, D], 'E7'), (32, 34, [A, C, E], 'Am')]
PLAN3 = [[68 + a, 68 + b, pcs, lab] for a, b, pcs, lab in PLAN3]
