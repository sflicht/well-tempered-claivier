"""Fugue XXI, section A ("I postiglioni"): the horns' exposition, bars 1-13.

Only the 3-limit voices (the horns: partials 1 2 3 4 6 8 9 12 16 18) sing here, in the keys of
their own harmonics: B-flat and F.  Four full entries two bars apart (Bach's own pitches for the
first two), then the remaining six horns stack the head of the F-horn's call half a bar apart over
a dominant pedal: the post station sounding its fanfare.  Each full entry is harmonised anew by
the voices already present.
"""
from xxi import *  # noqa


def place(sc, b0=1):
    b = lambda k: b0 + k - 1  # noqa: E731
    # 1. Corno 4: the subject at Bach's pitch (BWV 992/6 begins on B-flat3)
    sc.theme(V(4), b(1), 1, S, 'S (B-flat3, Bach\'s pitch)', 2)
    # 2. Corno 3: the answer at Bach's pitch (F3); Corno 4 against it: Bach's countersubject
    sc.theme(V(3), b(3), 1, A.replace('C5:6 A4:2', 'C5:6 Bb4:2'), 'A (F3, Bach\'s pitch; last note B-flat)', 2)
    sc.put(V(4), b(3), 2, "C5:4 R:2 D5:1 D4:1 D4:4 "                       # b3 (b.3 = Bach CS, 2nd half)
           "R:2 A4:1 G4:1 A4:1 Bb4:1 A4:1 G4:1 F4:4 Eb4:4")                  # b4 = Bach CS bar 2, then E-flat
    # 3. Corno 16: the subject an octave higher (b5); Corno 4 becomes the bass, Corno 3 the alto
    sc.theme(V(16), b(5), 1, octv(S, 1), 'S (B-flat4)', 2)
    sc.put(V(4), b(5), 1, "Bb3:4 Eb3:4 D3:4 A2:4 "                         # b5  Bb | Eb/G | Dm | F/A
           "G2:4 Eb3:4 D3:4 A2:4")                                         # b6  Gm | Eb | Bb/D | F/A
    sc.put(V(3), b(5), 2, "G4:2 F4:2 A4:2 F4:2 A4:2 C5:2 "                 # (A ends on b5 beat 1)
           "Bb4:2 G4:2 G4:4 F4:4 C5:2 A4:2")
    # 4. Corno 2: the answer in the bass (b7)
    sc.theme(V(2), b(7), 1, octv(A, -1), 'A (F2, bass)', 2)
    sc.put(V(16), b(7), 2, "C6:4 Bb5:4 G5:4 A5:4 C6:4 A5:4 G5:4")        # (S ends b7.1)
    sc.put(V(3), b(7), 1, "A4:8 D5:8 C5:12 Bb4:4")
    sc.put(V(4), b(7), 1, "F3:4 A3:4 F3:4 G3:4 C4:4 A3:4 F4:4 E4:4")
    # 5-9. The post station: five horns stack the head of the F-horn's call a beat apart (b9-11)
    FH = "F4:4 R:2 F4:1 F4:1 C5:2 C5:2 C5:2 C5:2 A4:2 F4:2 F4:2 F4:1 F4:1"   # S's head on F (partials of F)
    sc.theme(V(9), b(9), 1, FH, 'S head on F (F4)', 1)
    sc.theme(V(6), b(9), 2, octv(FH, -1), 'S head on F (F3)', 1)
    sc.theme(V(18), b(9), 3, octv(FH, 1), 'S head on F (F5)', 1)
    sc.theme(V(8), b(9), 4, FH, 'S head on F (F4)', 1)
    sc.theme(V(12), b(10), 1, octv(FH, 1), 'S head on F (F5)', 1)
    # the bass tongues an F pedal (posthorn rhythm); Corno 16 holds its high A; Corni 3 and 4 listen
    sc.put(V(2), b(9), 2, "F3:2 F3:1 F3:1 " + "F2:2 F2:1 F2:1 " * 7 + "F2:4")
    sc.put(V(16), b(9), 1, "A5:16 A5:16 A5:8")
    sc.put(V(4), b(9), 1, "F4:4")
    # 10. Corno 1, the fundamental, enters on the tonic: the subject two octaves below Bach's (b11.3)
    sc.theme(V(1), b(11), 3, octv(S, -2), 'S (B-flat1, the fundamental)', 2)
    # b11.3-13: the horns close on B-flat over the fundamental, turning at the last beat to A7
    # (the friends answer in D minor at b14)
    sc.put(V(16), b(11), 3, "D6:4 Eb6:4 C6:8 Bb5:4 Bb5:4 Bb5:4 A5:4 Bb5:4 A5:4")
    sc.put(V(12), b(11), 3, "F5:4 G5:4 A5:8 F5:4 G5:4 F5:4 C5:4 D5:4 C#5:4")
    sc.put(V(9), b(11), 3, "Bb4:4 Bb4:4 A4:4 C5:4 D5:4 Eb5:4 D5:4 F4:4 F4:4 E4:4")
    sc.put(V(6), b(11), 3, "D4:4 Bb3:4 C4:4 Eb4:4 D4:4 G3:4 Bb3:4 C4:4 Bb3:4 G3:4")
    sc.put(V(2), b(13), 4, "A2:4")
