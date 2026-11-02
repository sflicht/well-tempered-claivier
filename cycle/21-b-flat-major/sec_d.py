"""Fugue XXI, the climb ("La posta"), bars 36-41: from the friends' lament to the summit.

b36     the friends' lament, compressed to one bar: the bass walks down Bach's chromatic
        tetrachord (Lamento, BWV 992/3: ... E-flat D D-flat C) to the dominant of the dominant.
b37-38  the post station on the dominant: the fundamental returns (Corno 1, F1) under the bass's
        posthorn tonguing, and five horns stack the head of the subject on F a beat apart;
        Forestiero 22, the last stranger, enters with the octave call of Bach's Aria di
        postiglione on F (BWV 992/5, second half).
b39     Forestiero 11 sings the run of Bach's Aria with an alphorn's fa: where Bach writes E-flat,
        the 11th partial (E, 49 cents flat) -- the note between E-flat and E that no keyboard has.
b40-41  over B-flat/F (the cadential six-four) the strangers fire the subject's rocket (partials
        6 8 10 12) in stretto a beat apart, then the dominant seventh: the summit begins at b42.
"""
from xxi import *  # noqa

FH = "F4:4 R:2 F4:1 F4:1 C5:2 C5:2 C5:2 C5:2 A4:2 F4:2 F4:2 F4:1 F4:1"   # S's head on F
ELEVEN = -48.68   # partial 11 against the tempered E


def place(sc, b0=36):
    b = lambda k: b0 + k - 1  # noqa: E731
    # ---- b36: lament.  Eb | Bb/D | Bbm/Db | C7  ->  F
    sc.put(V(2), b(1), 1, "Eb3:4 D3:4 Db3:4 C3:4")
    sc.put(V(14), b(1), 1, "G5:4 F5:4 F5:4 E5:4 F5:4")             # the crack A-flat resolves to G
    sc.put(V(21), b(1), 1, "Bb5:12 G5:4 A5:16")
    sc.put(V(11), b(1), 1, "Eb4:4 F4:4 F4:4 C4:4 C4:4")
    sc.put(V(4), b(1), 1, "G3:4 Bb3:4 Bb3:4 C4:4 A3:4")
    sc.put(V(10), b(1), 3, "Db5:4 Bb4:4 A4:4")                     # the friends' minor sigh
    # ---- b37-38: the post station on F
    sc.put(V(1), b(2), 1, "F1:32")
    sc.put(V(2), b(2), 1, "F2:2 F2:1 F2:1 F2:12 F2:2 F2:1 F2:1 F2:12")
    sc.theme(V(3), b(2), 1, octv(FH, -1), 'S head on F (F3)', 1)
    sc.theme(V(6), b(2), 2, FH, 'S head on F (F4)', 1)
    sc.theme(V(12), b(2), 3, octv(FH, 1), 'S head on F (F5)', 1)
    sc.theme(V(9), b(2), 4, FH, 'S head on F (F4)', 1)
    sc.theme(V(18), b(3), 1, octv(FH, 1), 'S head on F (F5)', 1)
    sc.put(V(22), b(3), 1, "R:4 R:2 F6:1 F5:1 F5:4 R:2 F6:1 F5:1")     # Bach's Aria call, on F
    # ---- b39: the Aria's run with the alphorn fa (partial 11), over the pedal
    sc.put(V(1), b(4), 1, "F1:40")
    sc.put(V(2), b(4), 1, "F2:4 R:4 F2:2 F2:1 F2:1 F2:4 F2:16 F2:2 F2:1 F2:1 F2:4 F2:2 F2:1 F2:1 F2:4")
    # Aria di postiglione (BWV 992/5, b.1); E-flat sung as the 11th partial
    sc.put(V(11), b(4), 1, "Bb4:1 C5:1 D5:1 E5:1 F5:2 G5:2 F5:1 G5:1 F5:1 E5:1 D5:3 C5:1")
    for beat in (1.75, 3.75):
        sc.tune(V(11), b(4), beat, ELEVEN)
    sc.put(V(5), b(4), 1, "D4:8 C4:8 D4:12 F4:4 F4:16")
    # ---- b40: the Aria's octave call (Forestiero 11), the strangers' rockets, the friends' Arioso
    sc.put(V(11), b(5), 1, "Bb4:2 Bb5:1 Bb4:1 Bb4:2 Bb5:1 Bb4:1 Bb4:2 Bb5:1 Bb4:1 C5:2 C6:1 C5:1")
    sc.put(V(7), b(5), 1, "F3:1 Bb3:1 D4:1 F4:1 F4:12")
    sc.put(V(13), b(5), 2, "F4:1 Bb4:1 D5:1 F5:1 F5:8")
    sc.put(V(14), b(5), 3, "F4:1 Bb4:1 D5:1 F5:1 F5:4 A4:4")
    sc.put(V(19), b(5), 4, "F5:1 Bb5:1 D6:1 F6:1 F6:8")
    sc.put(V(20), b(5), 2, "R:2 Bb5:1 C6:1 D6:2 C6:1 Bb5:1 A5:2 Bb5:1 C6:1 C6:8 A5:8")
    sc.put(V(15), b(5), 2, "R:2 D5:1 Eb5:1 F5:2 Eb5:1 D5:1 C5:2 D5:1 Eb5:1 Eb5:8 F5:8")
    # ---- b41: the dominant seventh; rockets in F
    sc.put(V(17), b(6), 1, "C5:1 F5:1 A5:1 C6:1 C6:12")
    sc.put(V(21), b(6), 2, "C5:1 F5:1 A5:1 C6:1 C6:8")
    sc.put(V(22), b(5), 1, "D6:8 F6:8 C6:8 Eb6:8")
    sc.put(V(4), b(6), 1, "C4:16")
    sc.put(V(3), b(6), 1, "F3:12 C3:4")
