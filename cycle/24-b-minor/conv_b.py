"""Convergence, part B: cantus bars c5-c8.
The expected cadence (F#7 -> Bm) is deflected to D# minor: the cantus's D# is the tonic
of Fugue VIII (E-flat minor), whose subject enters at its own pitch, quietly, at the top of
a thinned texture.  Its last note, D#, becomes the leading tone of E minor; E minor turns
to C major (the Neapolitan), where Fugue II's subject (C minor, its own pitch) enters at
the top; the cantus falls C -> B under it (B augmented: Fugue II's E-flat is the D#).
Harmony: c5 D#m . B/D# . G#m/D# | c6 A#7/D# . D#m . D#dim7 . Em | c7 C | c8 B+ (B D# G)"""
from xxiv import *


def part_b(sc, b0):
    c = lambda k: b0 + k
    P = sc.put
    # ---- Fugue VIII's subject, own key (E-flat minor = D# minor), Soprano IV
    viii = octv(GUESTS['VIII'][0], 1)                 # Eb5 Bb5 Cb6 Bb5 Ab5 Gb5 F5 D5 Eb5
    sc.theme('S4', c(5), 1, viii + '~', 'Fugue VIII guest (E-flat minor, own key)', 'VIII', semis=12)
    P('S4', c(6), 3, "Eb5:2 E5:2 D5:4")               # its D# held, resolved up into E minor
    P('S4', c(7), 1, "C5:16~")
    P('S4', c(8), 1, "C5:4 B4:12")                    # C over B: 9-8
    # ---- Fugue II's subject, own key (C minor), Soprano I, from c7.3
    sc.theme('S1', c(7), 3, octv(GUESTS['II'][0], 1), 'Fugue II guest (C minor, own key)', 'II', semis=12)
    # ---- S2: returns on E minor and hands the C6 to Fugue II
    P('S2', c(6), 3, "B5:8")
    P('S2', c(7), 1, "C6:8")
    # ---- S3: E held over the B-augmented chord, resolving to D#
    P('S3', c(5), 1, "A#4:8 F#4:4 G#4:4~")
    P('S3', c(6), 1, "G#4:4 F#4:2 F#4:2 G4:8")
    P('S3', c(7), 1, "R:4 E5:12~")
    P('S3', c(8), 1, "E5:4 D#5:12")
    # ---- A1: the G that stays (with a neighbour)
    P('A1', c(6), 4, "B4:4")
    P('A1', c(7), 1, "R:4 G4:12")
    P('A1', c(8), 1, "G4:16")
    # ---- A3
    P('A3', c(5), 1, "C#5:8 B4:8")
    P('A3', c(6), 1, "B4:2 A#4:4 R:10")
    # ---- A4: sixteenths from c7.3 under Fugue II
    P('A4', c(7), 3, "C5:1 B4:1 C5:1 D5:1 E5:1 D5:1 C5:1 G4:1")
    P('A4', c(8), 1, "B4:1 G4:1 B4:1 D#5:1 B4:1 D#5:1 E5:1 D#5:1 G4:1 B4:1 D#5:1 E5:1 D#5:1 B4:1 A4:1 G4:1")
    # ---- A5
    P('A5', c(5), 3, "R:4 B3:4")
    P('A5', c(6), 1, "R:8 B3:4 E4:4")
    P('A5', c(7), 1, "E4:16")
    P('A5', c(8), 1, "R:16")
    # ---- T1: chromatic inner line A# B C## . C B | C
    P('T1', c(5), 1, "A#3:12 B3:4")
    P('T1', c(6), 1, "C##4:4 R:2 C4:2 B3:8")
    P('T1', c(7), 1, "R:4 C4:8 R:4")
    # ---- T2: D# . G# | A# A G | G (neighbour) | G
    P('T2', c(5), 1, "D#4:12 G#3:4")
    P('T2', c(6), 1, "A#3:4 A#3:2 A3:2 G3:8")
    P('T2', c(7), 1, "G3:8 A3:4 G3:4")
    P('T2', c(8), 1, "G3:16")
    # ---- T3: back on E minor
    P('T3', c(6), 4, "E4:4")
    P('T3', c(7), 1, "E4:16")
    P('T3', c(8), 1, "D#4:8 R:8")
    # ---- T4: F#3 . . | E# F# . E | E | D#
    P('T4', c(5), 1, "F#3:12 R:4")
    P('T4', c(6), 1, "R:4 F#3:4 B3:8")
    P('T4', c(7), 1, "E3:16")
    P('T4', c(8), 1, "R:8 B3:8")
    # ---- T5: upbeat figure into c7
    P('T5', c(6), 3, "R:2 G3:2 G3:2 G3:2")
    P('T5', c(7), 1, "E4:6 F4:2 E4:8")
    # ---- baritones and basses: quiet in c5-c6, rebuilding from c6.3
    P('Br1', c(6), 4, "E4:4")
    P('Br1', c(7), 1, "E4:4 G4:4 C5? ".replace('C5? ', 'C4:8'))
    P('Br2', c(5), 3, "B3:4 R:4")
    P('Br2', c(7), 1, "R:4 C4:4 E4? ".replace('E4? ', 'G3:4') + " E3:4")
    P('Br2', c(8), 1, "G3:4 D#3:4 G3:4 B3:4")
    P('Br3', c(6), 4, "B2:4")
    P('Br3', c(7), 1, "E3:8 G3:8")
    P('Br3', c(8), 1, "R:16")
    P('Br4', c(6), 3, "G3:8")
    P('Br4', c(7), 1, "G3:8 E3:4 C3:4")
    P('B1', c(7), 1, "R:8 G3:8")
    P('B1', c(8), 1, "R:8 D#3:8")
    P('B3', c(7), 1, "R:4 E3:12")
    P('B3', c(8), 1, "R:16")


def plan_b(off):
    B, C, Cs, D, Ds, E, Es, Fs, G, Gs, A, As, Css = 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2
    rows = [(0, 2, [Ds, Fs, As], 'D#m'), (2, 3, [B, Ds, Fs], 'B/D#'), (3, 4, [Gs, B, Ds, Fs], 'G#m/D#'),
            (4, 5, [As, Css, Es, Gs], 'A#7/D#'), (5, 5.5, [Ds, Fs, As], 'D#m'), (5.5, 6, [Ds, Fs, A, C], 'D#dim7'),
            (6, 8, [E, G, B], 'Em'), (8, 12, [C, E, G], 'C'), (12, 16, [B, Ds, G], 'B+')]
    return [[off + a, off + b, pcs, lab] for a, b, pcs, lab in rows]
