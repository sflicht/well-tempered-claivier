"""Fugue XXI, the summit ("Il congedo", the farewell): composed first.

E1-E5.2  both subjects in augmentation at once: the posthorn subject S x2 in Corno 4 (at
         Bach's own pitch, B-flat3) and the friends' theme T x2 in Amico 15, with the
         horn's head in Corno 16 and Corno 12, over a bass that walks I-vi-I6-ii7 | V ...
E5.3-E9  Bach's own subject (BWV 992/6) as the bass (Corno 2), the friends' theme on top
         (Forestiero 22), our subject entering six beats after Bach's and landing on the
         cadence (Corno 12); every other voice has its own rhythmic layer.
Harmony per beat (bass = Corno 1 / Corno 2):
 E1 Bb | Gm | Bb/D | Cm7      E2 F | Bb/F | Bb | Gm7/Bb    E3 Gm | Eb/G | Bb/F | Cm7/F
 E4 F | F | Gm7/F | Bb/F      E5 F7 | Bb/D | Bb | Eb/Bb     E6 Bb | Gm7/Bb | Dm-Bb | Bb
 E7 Gm | Gm7-Eb/G | F6/C-F/A | F   E8 Bb-Gm | Gm-C7/E | Bb/F | F7   E9 Bb
"""
from xxi import *  # noqa


def place(sc, E):
    """E = bar number of the summit's first bar."""
    e = lambda k: E + k - 1  # noqa: E731  (summit bar k -> score bar)

    # ---------------------------------------------------------------- the pillars
    sc.theme(V(4), e(1), 1, aug(S, 2), 'S x2 (B-flat3, Bach\'s pitch)', 5)
    sc.theme(V(15), e(1), 1, aug(T, 2), 'T x2', 4)
    # Bach's subject in the bass, from E5 beat 3
    sc.put(V(2), e(1), 1,
           "Bb2:4 G2:4 D3:4 Eb3:4 "                     # E1
           "F3:4 D3:4 Bb2:2 C3:2 D3:4 "                 # E2
           "G2:4 Eb3:4 D3:4 C3:4 "                      # E3
           "A2:8 D3:4 Bb2:4 "                           # E4
           "A2:4 Bb2:4")                                # E5.1-2
    sc.theme(V(2), e(5), 3, octv(BACH, -1), "Bach's subject (BWV 992/6), bass", 3)
    sc.put(V(2), e(8), 4, "C3:4 Bb2:8 R:8")             # E8.4 F7/C -> E9 Bb
    sc.put(V(1), e(1), 1,
           "Bb1:16 F1:8 D2:8 Bb1:8 D2:4 Eb2:4 F2:16 "  # E1-E4
           "F2:4 Bb1:12 Bb1:16 "                        # E5-E6
           "Bb1:8 F1:4 Eb2:4 D2:4 C2:4 F1:8 Bb1:16")   # E7-E9
    # the friends' theme on top, two beats after Bach's subject (tail turned to A for F major)
    sc.theme(V(22), e(6), 1, "R:2 Bb5:1 C6:1 D6:2 C6:1 Bb5:1 A5:2 Bb5:1 C6:1 D6:1 Eb6:1 F6:1 G6:1 "
             "G6:4 F6:2 Eb6:2 D6:3 C6:1 A5:4", 'T (top; last note A)', 2)
    # our subject six beats after Bach's: it lands on the cadence
    sc.theme(V(12), e(7), 1, S, 'S (lands on the cadence)', 2)
    # our subject two beats after Bach's, an octave higher (Corno 16): Bach and us in stretto
    sc.theme(V(16), e(6), 1, octv(S, 1).replace('F6:6 D6:2', 'F6:8'), 'S (stretto with Bach, +2 beats; last F held)', 2)
    # the answer's head (Bach's answer) high in Corno 18
    sc.theme(V(18), e(7), 3, "F5:4 R:2 F5:1 F5:1 Bb5:2 Bb5:2 Bb5:2 Bb5:2", "A head", 1)

    if LAYERS >= 1:
        free_a(sc, e)
    if LAYERS >= 2:
        free_b(sc, e)


LAYERS = 2


def free_a(sc, e):
    """E1-E5.2.  Layers: halves (Fo22), quarters (Am20), eighths (Co3), octave calls (Co16, Co9),
    Am5 with Bach's answer head."""
    sc.put(V(22), e(1), 1, "D6:8 Bb5:4 C6:4 C6:8 Bb5:4 F6:4 Bb5:8 F6:4 C6:4~ C6:8 D6:8 C6:4 D6:4")
    sc.put(V(22), e(8), 1, "D6:4 G5:4 Bb5:4 C6:4 D6:16")
    sc.put(V(20), e(1), 1, "F5:4 G5:4 F5:4 G5:4 A5:4 F5:4 F5:4 Bb5:4 D6:4 Eb6:4 Bb5:4 G5:4 A5:8 G5:4 F5:4 A5:4 F5:4")
    sc.put(V(3), e(1), 1, "D3:2 C3:2 Bb2:2 D3:2 Bb3:4 G3:2 F3:2 "
           "C4:2 A3:2 D4:2 Bb3:2 F3:2 Eb3:2 G3:2 A3:2 "
           "Bb3:2 G3:2 G3:2 F3:2 R:2 F3:2 G3:2 Eb3:2 "
           "C3:2 F3:2 A3:2 F3:2 Bb3:2 G3:2 D3:2 F3:2 "
           "Eb3:4 D3:2 F3:2")
    sc.put(V(5), e(1), 1, "D4:8")
    sc.theme(V(5), e(2), 1, "F3:4 R:2 F3:1 F3:1 Bb3:2 Bb3:2 Bb3:2 Bb3:2", "A head (Bach's answer, his pitch)", 1)
    # Corno 16: the posthorn's octave call; at E2 exactly Bach's countersubject (BWV 992/6 b.5)
    sc.theme(V(16), e(2), 1, BACH_CS, "Bach's countersubject (BWV 992/6, b.5), his pitch", 1)
    sc.put(V(16), e(3), 1, "G4:2 G5:1 G4:1 G4:4 R:2 D5:1 D4:1 G4:4 "
           "F4:2 F5:1 F4:1 C5:4 R:2 G5:1 G4:1 Bb4:4 C5:4 Bb4:4")
    # Amico 10: the Arioso's turn (BWV 992/1) as a figure, under the augmented T
    sc.put(V(10), e(1), 3, "F4:1 G4:1 F4:1 Eb4:1 C4:2 Eb4:2")
    sc.put(V(10), e(3), 1, "Bb4:1 C5:1 Bb4:1 A4:1 Bb4:4 Bb4:1 C5:1 Bb4:1 A4:1 C5:4 "
           "C5:1 Bb4:1 A4:1 Bb4:1 C5:2 A4:2 Bb4:1 A4:1 G4:1 F4:1 F4:4")


FREE_B = {
    21: ("R:8 C6:6 Bb5:2 D6:4 C6:4 Bb5:4 F5:12 D6:4 R:12 D6:4"),
    3: ("D3:2 F3:2 G3:2 F3:2 "
        "D3:2 C3:2 Bb2:2 D3:2 F3:2 D3:2 D3:2 F3:2 "
        "Bb2:2 D3:2 D3:4 F3:2 A3:2 A3:2 Bb3:2 "
        "F3:2 G3:2 Bb2:2 C3:2 D3:2 C3:2 F2:4 D3:4"),
    4: ("Bb4:8 F4:8 Bb3:8 Bb3:8 C4:8 F4:4 E4:4 D4:4 A3:4 F3:4"),
    5: ("R:8 R:2 D4:4 Bb3:2 R:8 R:2 Bb3:4 G3:2 R:8 R:2 G3:4 Bb3:2 R:8 D4:4"),
    6: ("Bb3:8 R:8 D4:8 R:16 R:8 D4:4 C4:4 R:4"),
    9: ("R:8 F4:2 F5:1 F4:1 Bb3:2 Bb4:1 Bb3:1 R:8 G4:2 G5:1 G4:1 Bb3:2 Bb4:1 Bb3:1 R:8 "
        "Bb3:2 Bb4:1 Bb3:1 C4:2 C5:1 C4:1 R:8 D4:4"),
    8: ("R:2 F4:4 Eb4:2 R:8 R:2 F4:4 D4:2 R:8 R:2 Eb4:4 D4:2 R:8 R:2 F4:4 C4:2 R:4"),
    11: ("R:8 Bb4:1 C5:1 D5:1 Eb5:1 F5:1 Eb5:1 D5:1 C5:1 R:8 G4:1 A4:1 Bb4:1 C5:1 D5:1 C5:1 Bb4:1 A4:1 R:8 "
         "F5:1 Eb5:1 D5:1 C5:1 C5:1 D5:1 E5:1 C5:1 R:8 F5:4"),
    7: ("D4:1 C4:1 Bb3:1 A3:1 Bb3:1 C4:1 D4:1 Eb4:1 R:8 F4:1 G4:1 A4:1 Bb4:1 C5:1 Bb4:1 A4:1 G4:1 R:8 "
        "A4:1 Bb4:1 C5:1 A4:1 F4:1 G4:1 A4:1 F4:1 R:8 D4:1 F4:1 Bb4:1 F4:1 F4:1 Eb4:1 C4:1 Eb4:1 F4:4"),
    13: ("F4:1 F4:1 F4:2 Eb4:2 D4:2 F4:1 F4:1 F4:2 F4:1 F4:1 F4:2 F4:1 F4:1 F4:2 F4:1 F4:1 F4:2 G4:1 G4:1 G4:2 G4:1 G4:1 G4:2 R:8 D4:1 D4:1 D4:2 G4:1 G4:1 G4:2 F4:1 F4:1 F4:2 Eb4:1 Eb4:1 Eb4:2 D4:4"),
    14: ("R:4 R:2 Eb5:2~ Eb5:2 D5:2 R:2 C5:2~ C5:2 Bb4:2 R:2 C5:2~ C5:2 Bb4:2 R:2 Bb4:2~ "
        "Bb4:2 A4:2 R:2 A4:2~ A4:2 G4:2 R:2 C5:2~ C5:2 Bb4:2 R:2 C5:2~ C5:2 Bb4:2"),
    15: ("D5:4 R:2 C5:2~ C5:2 Bb4:2 R:2 Eb5:2~ Eb5:2 D5:2 R:2 Eb5:2~ Eb5:2 D5:2 R:2 D5:2~ "
         "D5:2 C5:2 R:2 C5:2~ C5:2 Bb4:2 R:2 G4:2~ G4:2 F4:2 R:2 F4:2~ F4:4"),
    19: ("D6:4 Eb6:4 D6:2 R:14 G5:8 C6:8 R:8 F5:8 F5:4"),
    20: ("Bb5:4 G5:4 F5:4 D5:12 G4:8 A4:4 C5:4 Bb4:12 A4:4 Bb4:4"),
}
B_ORDER = [14, 20, 4, 15, 19, 3, 13, 9, 8, 11, 7, 5, 6, 21]
import os
N_B = int(os.environ.get("XXI_NB", "99"))


def free_b(sc, e):
    """E5.3-E9.1: every voice in its own layer around Bach's subject in the bass.
    lows: Co3 eighths, Co4 halves, Am5 syncopated sighs (beats 1-2), Co6 quarters (beats 3-4);
    middles: Co9 octave calls (beats 1-2) answered by Co8 eighths (beats 3-4), Fo11 sixteenths
    (beats 1-2) answered by Fo7 sixteenths (beats 3-4), Fo13 tonguing, Fo14 a suspension chain,
    Am15 halves; highs: Fo19 halves, Am20 quarters."""
    for v in B_ORDER[:N_B]:
        sc.put(V(v), e(5), 3, FREE_B[v])
