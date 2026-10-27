"""Convergence, part A: lead-in bar (c0, the dominant) and cantus bars c1-c4.
Harmony: c0 F#7 | c1 Bm7 | c2 Bm7/D . C#o7 (ii) | c3 E#dim7 | c4 C#7/E# . F#7 | (c5 D#m)
Attack staggering: long-breath lines move on beats 1/3, suspension chains on 2/4,
upbeat figures land on 1/3, sixteenth runs relay; at no onset may two voices make
the same move between the same pitch classes."""
from xxiv import *


def part_a(sc, b0):
    c = lambda k: b0 + k            # bar number of cantus bar c_k
    P = sc.put
    # ---- cantus: the subject in four-fold augmentation, Contrabass, from c1 (the 25th voice)
    sc.theme('B5', c(1), 1, octv(aug(S, 4), -2), 'Subject x4 (cantus)', 'S', scale=4, semis=-24)
    # ---- S1: climbs to the dominant seventh, then Fugue V's subject in its own key
    P('S1', c(0), 1, "C#6:4 D6:2 E6:10")
    P('S1', c(1), 1, "D6:4 R:2")
    sc.theme('S1', c(1), 2.5, octv(GUESTS['V'][0], 1), 'Fugue V guest (D major, own key)', 'V', semis=12)
    P('S1', c(3), 2.5, "C#6:2 B5:8~")
    P('S1', c(4), 1, "B5:12 A#5:4")                 # 4-3 over F#7
    # ---- S2 long breath: A# B | F# | F# E | E# | E# F#   (rises chromatically E E# F#)
    P('S2', c(0), 1, "C#6:8 A#5:8")
    P('S2', c(1), 1, "B5:4 F#5:12")
    P('S2', c(2), 1, "F#5:8 E5:8")
    P('S2', c(3), 1, "E#5:16")
    P('S2', c(4), 1, "E#5:8 F#5:8")
    # ---- S3 upbeat figure into c1; chain; upbeat figure into c4
    P('S3', c(0), 3.5, "F#4:2 F#4:2 F#4:2")
    P('S3', c(1), 1, "D5:6 C#5:2 B4:8")
    P('S3', c(2), 1, "R:4 F#5:8 E5:2 D5:2~")         # F# over C#o7 -> E, passing D
    P('S3', c(3), 1, "D5:8 R:2 E#4:2 E#4:2 E#4:2")
    P('S3', c(4), 1, "C#5:6 B4:2 A#4:8")             # lands C# (C#7), leans to B, A#
    # ---- S4 chain
    P('S4', c(0), 1, "R:4 C#5:8 E5:4~")
    P('S4', c(1), 1, "E5:4 D5:8 A5:4~")              # 4-3
    P('S4', c(2), 1, "A5:12 G5:4")                   # A over C#o7 -> G
    P('S4', c(3), 1, "G#5:8 B5:4 G#5:4~")
    P('S4', c(4), 1, "G#5:12 F#5:4")                 # 9-8 over F#7
    # ---- S5 sixteenths in c1, then a quarter-note line
    P('S5', c(0), 1, "A#4:8 B4:4 C#5:4")
    P('S5', c(1), 1, "D5:1 C#5:1 B4:1 C#5:1 D5:1 E5:1 F#5:1 E5:1 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:1 F#5:1")
    P('S5', c(2), 1, "F#5:4 D5:4 C#5:4 B4:4")
    P('S5', c(3), 1, "B4:4 D5:4 C#5:4 B4:4")
    P('S5', c(4), 1, "C#5:4 E#5:4 E5:4 C#5:4")
    # ---- A1 upbeat into c2.3, chain
    P('A1', c(0), 1, "C#5:12 R:4")
    P('A1', c(1), 1, "B4:12 A4:4~")
    P("A1", c(2), 1, "A4:2 B4:2 B4:2 B4:2 G5:6 F#5:2")   # lands G (C#o7), leans
    P('A1', c(3), 1, "E#5:4 D5:4 B4:8~")
    P('A1', c(4), 1, "B4:12 A#4:4")
    # ---- A2 long breath: A# | A | A G | G# | G# F#
    P('A2', c(0), 1, "G#4:4 A#4:12")
    P('A2', c(1), 1, "A4:16")
    P('A2', c(2), 1, "A4:8 G4:8")
    P('A2', c(3), 1, "G#4:16")
    P('A2', c(4), 1, "G#4:8 F#4:8")
    # ---- A3 chain
    P('A3', c(0), 1, "R:8 F#4:4 C#5:4~")
    P('A3', c(1), 1, "C#5:4 B4:12~")                 # 9-8
    P('A3', c(2), 1, "B4:4 A4:4 B4:4 C#5:4~")
    P('A3', c(3), 1, "C#5:4 B4:8 D5:4~")             # C# over E#dim7 -> B
    P('A3', c(4), 1, "D5:4 C#5:12")                  # D over C#7: 9-8
    # ---- A4 sixteenths c0 and c4
    P('A4', c(0), 1, "F#4:1 E#4:1 F#4:1 G#4:1 A#4:1 G#4:1 A#4:1 B4:1 C#5:1 B4:1 A#4:1 G#4:1 A#4:2 R:2")
    P('A4', c(1), 1, "R:4 F#4:8 E4:4")
    P('A4', c(2), 1, "D4:8 C#4:4 E4:4")
    P('A4', c(3), 1, "D4:8 G#4:8")
    P('A4', c(4), 1, "G#4:1 F#4:1 E#4:1 F#4:1 G#4:1 A#4:1 B4:1 G#4:1 A#4:1 B4:1 C#5:1 B4:1 A#4:1 G#4:1 F#4:1 E4:1")
    # ---- A5 sixteenths c2
    P('A5', c(0), 1, "E4:8 C#4:8")
    P('A5', c(1), 1, "D4:8 F#4:8")
    P('A5', c(2), 1, "F#4:1 E4:1 D4:1 E4:1 F#4:1 G4:1 A4:1 F#4:1 G4:1 E4:1 C#4:1 D4:1 E4:1 G4:1 B4:1 G4:1")
    P('A5', c(3), 1, "G#4:8 E#4:8")
    P('A5', c(4), 1, "E#4:8 E4:8")
    # ---- T1: echo of the guest's tattoo, answering it a fifth below
    P('T1', c(1), 1, "R:8 F#4:4 F#4:2 F#4:1 F#4:1")
    P('T1', c(2), 1, "A4:4 A4:2 A4:1 A4:1 G4:4 E4:4")
    P('T1', c(3), 1, "D4:4 D4:2 D4:1 D4:1 E#4:4 G#4:4")
    P('T1', c(4), 1, "G#4:8 C#4:4 E4:4")
    # ---- T2 upbeat figures into c1 and c3
    P('T2', c(0), 1, "F#3:8 R:2 C#4:2 C#4:2 C#4:2")
    P('T2', c(1), 1, "A4:6 G4:2 F#4:8")              # lands A (7th of Bm7)
    P('T2', c(2), 1, "F#4:8 R:2 E4:2 E4:2 E4:2")
    P('T2', c(3), 1, "C#5:6 B4:2 B4:8~")             # C# leans to B over E#dim7
    P('T2', c(4), 1, "B4:8 A#4:8")
    # ---- T3 long breath: C# | D | D E | D | E# E
    P('T3', c(0), 1, "C#4:16")
    P('T3', c(1), 1, "D4:16")
    P('T3', c(2), 1, "D4:8 E4:8")
    P('T3', c(3), 1, "D4:16")
    P('T3', c(4), 1, "E#4:8 E4:8")
    # ---- T4 sixteenths c3
    P('T4', c(0), 1, "A#3:8 C#4:8")
    P('T4', c(1), 1, "B3:8 A3:8")
    P('T4', c(2), 1, "B3:8 G3:8")
    P('T4', c(3), 1, "G#3:1 A3:1 B3:1 C#4:1 D4:1 C#4:1 B3:1 D4:1 E#4:1 D4:1 C#4:1 B3:1 C#4:1 B3:1 A#3:1 G#3:1")
    P('T4', c(4), 1, "E#3:8 C#3:8")
    # ---- T5 chain
    P('T5', c(0), 1, "R:4 C#4:8 A#3:4~")
    P('T5', c(1), 1, "A#3:4 B3:8 F#3:4~")            # retardation A# -> B
    P('T5', c(2), 1, "F#3:8 E3:4 A3:4~")
    P('T5', c(3), 1, "A3:4 G#3:12~")                 # A over E#dim7 -> G#
    P('T5', c(4), 1, "G#3:12 F#3:4")
    # ---- Br1 upbeat into c2, c4.3
    P('Br1', c(1), 1, "R:4 D3:4 F#3:4 R:2 A3:2")
    P('Br1', c(2), 1, "A3:2 A3:2 F#4:6 E4:2 E4:4")
    P('Br1', c(3), 1, "D4:8 B3:2 R:2 D3:2 D3:2")
    P('Br1', c(4), 1, "D3:2 B3:6 A#3:8")
    # ---- Br2 long breath: A# | B | B C# | B | B A#
    P('Br2', c(0), 1, "A#3:16")
    P('Br2', c(1), 1, "B3:16")
    P('Br2', c(2), 1, "B3:8 C#4:8")
    P('Br2', c(3), 1, "B3:16")
    P('Br2', c(4), 1, "B3:8 A#3:8")
    # ---- Br3 walking quarters
    P('Br3', c(0), 1, "C#3:4 E3:4 F#3:4 E3:4")
    P('Br3', c(1), 1, "D3:4 E3:4 F#3:4 A3:4")
    P('Br3', c(2), 1, "F#3:4 E3:2 D3:2 E3:4 G3:4")
    P('Br3', c(3), 1, "G#3:4 F#3:2 E#3:2 D3:4 B2:4")
    P('Br3', c(4), 1, "C#3:4 E#3:4 F#3:4 E3:4")
    # ---- Br4 half notes
    P('Br4', c(0), 1, "E3:16")
    P('Br4', c(1), 1, "D3:16")
    P('Br4', c(2), 1, "F#3:8 E3:8")
    P('Br4', c(3), 1, "E#3:16")
    P('Br4', c(4), 1, "E#3:8 C#3:8")
    # ---- Br5, B1-B4
    P('Br5', c(0), 1, "A#2:8 C#3:8")
    P('Br5', c(1), 1, "F#3:8 A3:8")
    P('Br5', c(2), 1, "A3:8 G3:8")
    P('Br5', c(3), 1, "G#3:8 D3:8")
    P('Br5', c(4), 1, "C#3:8 C#3:8")
    P('B1', c(0), 1, "C#3:8 R:2 F#2:2 F#2:2 F#2:2")
    P('B1', c(1), 1, "D3:6 C#3:2 B2:4 D3:4")
    P('B1', c(2), 1, "F#3:8 E3:8")
    P('B1', c(3), 1, "R:10 G#2:2 G#2:2 G#2:2")
    P('B1', c(4), 1, "E#3:6 D#3:2 C#3:8")
    P('B2', c(0), 1, "F#2:16")
    P('B3', c(3), 1, "D3:8 G#2:8")
    P('B3', c(4), 1, "G#2:8 A#2:8")
    P('B4', c(0), 1, "R:8 F#2:4 E2:4")
