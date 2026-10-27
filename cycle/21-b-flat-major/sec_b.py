"""Fugue XXI, section B ("Schmeichelung der Freunde"): the friends' exposition, bars 14-21.

The four 5-limit voices (partials 5 10 15 20: D and A) enter with the friends' theme T in
D minor and its answer in A minor, two bars apart, each entering voice taking over from the one
before a falling, sighing countersubject.  The horns keep their places: the bass walks, the
inner horns hold and sigh, and Corno 4 (the first postilion) taps his impatient call on A.
Harmony of T in D minor: Dm | Dm | A/C# | Dm || Bb | A7 | Dm | Dm.
"""
from xxi import *  # noqa


def place(sc, b0=14):
    b = lambda k: b0 + k - 1  # noqa: E731
    sc.theme(V(10), b(1), 1, T_DM, 'T (D minor, D5)', 2)
    sc.theme(V(15), b(3), 1, T_AM, 'T answer (A minor, A4)', 2)
    sc.theme(V(5), b(5), 1, octv(T_DM, -1), 'T (D minor, D4)', 2)
    sc.theme(V(20), b(7), 1, octv(T_AM, 1), 'T answer (A minor, A5)', 2)
    # the bass (Corno 2): i iv6? V6 i | VI V7 i V7/V ... one harmony per beat
    sc.put(V(2), b(1), 1, "D3:4 Bb2:4 A2:4 D3:4 G2:4 A2:4 D3:4 B2:4 "       # B1-2  (T in D minor)
           "A2:4 F2:4 E2:4 A2:4 D3:4 E3:4 A2:4 C#3:4 "                      # B3-4  (answer in A minor)
           "D3:4 Bb2:4 A2:4 D3:4 G2:4 A2:4 D3:4 B2:4 "                      # B5-6  (T in D minor, tenor)
           "A2:4 C3:4 B2:4 A2:4 D3:4 E3:4 A2:4 F2:4")                       # B7-8  (answer, top) -> F7
    # the friends' countersubject: sighs (appoggiaturas resolving down) after each T
    sc.put(V(10), b(3), 1, "E5:4 F5:2 E5:2 D5:2 E5:2 C5:4 D5:4 B4:2 G#4:2 C5:2 A4:2 G4:4")
    sc.put(V(15), b(5), 1, "A4:4 Bb4:2 A4:2 E4:2 C#4:2 D4:4 F4:4 E4:2 C#4:2 D4:2 F4:2 E4:4")
    sc.put(V(5), b(7), 1, "C4:4 E4:4 B3:2 G#3:2 A3:4 A3:4 G#3:4 A3:2 C4:2 Eb4:4")
    # horns: Corno 16 a slow descant; Corno 9 the tonguing of the impatient postilion; Corno 6 inner
    sc.put(V(16), b(1), 1, "A4:4 Bb4:4 A4:4 A4:4 Bb4:4 A4:4 A4:4 G#4:4 A5:4 A5:4 G#5:4 A5:4 A5:4 G#5:4 A5:4 G5:4 "
           "F5:4 F5:4 E5:4 F5:4 G5:4 G5:4 F5:4 E5:4 E5:4 C5:4 B4:4 C5:4 D5:4 E5:4 C5:4 C5:4")
