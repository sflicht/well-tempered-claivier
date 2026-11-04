"""Fugue XXI, section B ("Schmeichelung der Freunde"): the friends' exposition, bars 14-21.

The four 5-limit voices (partials 5 10 15 20: D and A) enter with the friends' theme T in
D minor and its answer in A minor, two bars apart, each entering voice taking over from the one
before a falling, sighing countersubject.  The horns keep their places: the bass walks, the
inner horns hold and sigh, and Corno 4 (the first postilion) taps his impatient call on A.
Harmony of T in D minor: Dm | Dm | A/C# | Dm || Bb | A7 | Dm | Dm.
The fourth friend (Amico 20, b20-21) does not answer in A minor: it coaxes the traveller in
his own key, F major (the horns' third partial), and its climb ends on D6, its own partial;
Corno 3 sounds its partial F3 under the F chords, and F7 leads to B-flat (section C).
Harmony of T in F: F/A | F | C7 | F || Dm | C7/E | F | F7.  (Nov 2026)
"""
from xxi import *  # noqa


def place(sc, b0=14):
    b = lambda k: b0 + k - 1  # noqa: E731
    sc.theme(V(10), b(1), 1, T_DM, 'T (D minor, D5)', 2)
    sc.theme(V(15), b(3), 1, T_AM, 'T answer (A minor, A4)', 2)
    sc.theme(V(5), b(5), 1, octv(T_DM, -1), 'T (D minor, D4)', 2)
    sc.theme(V(20), b(7), 1, tr(T, 7, 4), 'T (F major, F5): the friends turn to the horns\' key', 2)
    # the bass (Corno 2): i iv6? V6 i | VI V7 i V7/V ... one harmony per beat
    sc.put(V(2), b(1), 1, "D3:4 Bb2:4 A2:4 D3:4 G2:4 A2:4 D3:4 B2:4 "       # B1-2  (T in D minor)
           "A2:4 F2:4 E2:4 A2:4 D3:4 E3:4 A2:4 C#3:4 "                      # B3-4  (answer in A minor)
           "D3:4 Bb2:4 A2:4 D3:4 G2:4 A2:4 D3:4 B2:4 "                      # B5-6  (T in D minor, tenor)
           "A2:4 F2:4 C3:4 F2:4 D3:4 E3:4 F3:4 F2:4")                       # B7-8  (T in F, top) -> F7
    # the friends' countersubject: sighs (appoggiaturas resolving down) after each T
    sc.put(V(10), b(3), 1, "E5:4 F5:2 E5:2 D5:2 E5:2 C5:4 D5:4 B4:2 G#4:2 C5:2 A4:2 G4:4")
    sc.put(V(15), b(5), 1, "A4:4 Bb4:2 A4:2 E4:2 C#4:2 D4:4 F4:4 E4:2 C#4:2 D4:4 E4:4")
    sc.put(V(5), b(7), 1, "C4:4 A3:4 G3:2 Bb3:2 A3:4 F3:4 G3:4 A3:2 C4:2 Eb4:4")
    # horns: Corno 16 an alto line; Corni 6 and 3 a quiet chorale; Corno 9 joins when the theme goes low
    sc.put(V(16), b(1), 1, "F4:8 A4:8 Bb4:4 G4:4 A4:4 G#4:4 C5:4 A4:4 B4:4 A4:4 A4:4 G#4:4 A4:4 E5:4 "
           "F5:4 F5:4 G5:4 F5:4 G5:4 E5:4 F5:4 E5:4")
    sc.put(V(3), b(1), 1, "F3:4 D3:4 E3:4 D3:4 G3:4 E3:4 F3:4 E3:4 A3:8 E3:8 F3:4 R:4 E3:4 A3:4 "
           "F3:4 D3:4 R:8 R:16 F3:8 R:4 F3:8 R:12")
    sc.put(V(9), b(5), 1, "D5:8 A4:8 D5:4 C#5:4 A4:4 G#4:4 A4:4 C5:12 A4:4 G4:4 F4:4 C5:4")
    # Corno 4, the impatient postilion, taps his call between the friends' phrases
    sc.put(V(4), b(2), 3, "A3:2 A3:1 A3:1")
    sc.put(V(4), b(4), 3, "A3:2 A3:1 A3:1 A3:4")
    sc.put(V(4), b(6), 3, "A3:2 A3:1 A3:1")
    sc.put(V(4), b(8), 3, "C4:2 C4:1 C4:1 C4:4")
