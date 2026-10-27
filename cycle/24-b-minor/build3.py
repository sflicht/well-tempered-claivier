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
    P('A1', 19, 1, "D4:6")
    P('A3', 18, 1, "B3:4 A3:4")
    P('T2', 18, 1, "B3:4")
    P('Br2', 18, 1, "E4:4")
    P('A5', 19, 1, "E4:1 F#4:1 G#4:1 B4:1 D5:1 B4:1 A4:8 G4:2~")
    P('A5', 20, 1, "G4:4 A4:4 E4:2 D4:2 E4:4")
    P('S2', 20, 1, "Bb4:4 C5:6 B4:2 A4:4")


B, C, Cs, D, Ds, E, F, Fs, G, Gs, A, As = 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Eb, Bb = Ds, As
PLAN3 = [(0, 1, [E, G, B], 'Em'), (1, 1.5, [A, Cs, E, G], 'A7'), (1.5, 2, [D, F, A], 'Dm'), (2, 3.5, [Bb, D, F], 'Bb'),
         (3.5, 4, [A, C, E], 'Am'), (4, 5.5, [E, Gs, B, D], 'E7'), (5.5, 7.5, [B, Ds, Fs, A], 'B7'), (7.5, 8, [E, G, B], 'Em/G'),
         (8, 9, [Eb, G, Bb], 'Eb'), (9, 9.5, [D, Fs, A, C], 'D7'), (9.5, 10, [D, F, A], 'Dm'), (10, 10.5, [C, E, G, Bb], 'C7'),
         (10.5, 11, [G, B, D], 'G'), (11, 11.5, [A, C, E], 'Am'), (11.5, 12, [A, Cs, E, G], 'A7'), (12, 14, [D, F, A], 'Dm')]
PLAN3 = [[68 + a, 68 + b, pcs, lab] for a, b, pcs, lab in PLAN3]
