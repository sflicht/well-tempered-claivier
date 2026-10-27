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
    sc.put(V(2), e(8), 4, "A2:4 Bb2:8 R:8")             # E8.4 F7/A -> E9 Bb
    sc.put(V(1), e(1), 1,
           "Bb1:16 F1:8 Bb1:8 Bb1:8 D2:4 Eb2:4 F2:16 "  # E1-E4
           "F2:4 Bb1:12 Bb1:16 "                        # E5-E6
           "G1:8 F1:8 Bb1:4 C2:4 F1:8 Bb1:16")          # E7-E9
    # the friends' theme on top, two beats after Bach's subject (tail turned to A for F major)
    sc.theme(V(22), e(6), 1, "R:2 Bb5:1 C6:1 D6:2 C6:1 Bb5:1 A5:2 Bb5:1 C6:1 D6:1 Eb6:1 F6:1 G6:1 "
             "G6:4 F6:2 Eb6:2 D6:3 C6:1 A5:4", 'T (top; last note A)', 2)
    # our subject six beats after Bach's: it lands on the cadence
    sc.theme(V(12), e(7), 1, S, 'S (lands on the cadence)', 2)

    if LAYERS >= 1:
        free_a(sc, e)


LAYERS = 1


def free_a(sc, e):
    """E1-E5.2.  Layers: halves (Fo22), quarters (Am20, Fo19/Fo14 syncopated), eighths (Co3,
    Co16, Co9 octave calls), Am5 with Bach's answer head."""
    sc.put(V(22), e(1), 1, "D6:8 Bb5:4 C6:4 C6:8 Bb5:4 F6:4 D6:4 Eb6:4 F6:4 C6:4~ C6:8 D6:8 C6:4 Bb5:4")
    sc.put(V(22), e(8), 1, "Bb5:4 Bb5:4 Bb5:4 A5:4 Bb5:16")
    sc.put(V(20), e(1), 1, "F5:4 G5:4 F5:4 G5:4 A5:4 F5:4 F5:4 Bb5:4 Bb5:8 Bb5:4 G5:4 A5:8 G5:4 F5:4 A5:4 F5:4")
    sc.put(V(3), e(1), 1, "D3:2 C3:2 Bb2:2 D3:2 F3:2 G3:2 G3:2 F3:2 A3:2 G3:2 F3:2 Eb3:2 D3:2 Eb3:2 F3:2 G3:2 "
           "Bb2:2 D3:2 G3:2 F3:2 F3:4 Eb3:2 G3:2 C3:2 F3:2 A3:2 F3:2 G3:2 F3:2 D3:2 F3:2 C3:2 Eb3:2 D3:2 F3:2")
    sc.put(V(5), e(1), 1, "D4:8 D4:4 C4:4")
    sc.theme(V(5), e(2), 1, "F3:4 R:2 F3:1 F3:1 Bb3:2 Bb3:2 Bb3:2 Bb3:2", "A head (Bach's answer)", 1)
    # the posthorn's head in Corno 16 (E1.3), then octave calls
    sc.theme(V(16), e(1), 3, "Bb4:4 R:2 Bb4:1 Bb4:1 F5:2 F5:2 F5:2 F5:2 D5:2 Bb4:2 Bb4:2 Bb4:1 Bb4:1",
             'S head', 2)
    sc.put(V(16), e(3), 1, "G4:2 G5:1 G4:1 Bb4:2 Bb5:1 Bb4:1 F4:2 F5:1 F4:1 Eb5:2 C5:2 "
           "C5:2 F5:1 C5:1 A4:2 C5:2 D5:2 Bb4:2 F5:2 D5:2 "
           "C5:4 D5:4")
    # Bach's countersubject figure (the octave leaps) in Corno 9
    sc.put(V(9), e(1), 1, "D4:2 D5:1 D4:1 D4:4 R:2 F5:1 F4:1 G4:4 "
           "C4:2 C5:1 C4:1 D4:4 R:2 F5:1 F4:1 F4:4 "
           "D4:2 D5:1 D4:1 Eb4:4 R:2 D5:1 D4:1 Eb4:4 "
           "C4:2 C5:1 C4:1 C4:4 R:2 D5:1 D4:1 D4:4 "
           "Eb4:4 D4:4")
