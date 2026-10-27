"""Convergence, part A: lead-in bar (c0, the dominant) and cantus bars c1-c4.
Harmony: c0 F#7 | c1 Bm7 | c2 Bm7/D . C#o7 (ii) | c3 E#dim7 | c4 C#7/E# . F#7 | (c5 D#m)
Attack staggering: long-breath lines move on beats 1/3, suspension chains on 2/4,
upbeat figures land on 1/3, sixteenth runs relay; at no onset do two voices make
the same move between the same pitch classes (checked with hot.py)."""
from xxiv import *


def part_a(sc, b0):
    c = lambda k: b0 + k            # bar number of cantus bar c_k
    P = sc.put
    # cantus: the subject in four-fold augmentation, Contrabass, from c1 (the 25th voice)
    sc.theme('B5', c(1), 1, octv(aug(S, 4), -2), 'Subject x4 (cantus)', 'S', scale=4, semis=-24)
    # S1: climbs to the dominant seventh, then Fugue V's subject in its own key
    P('S1', c(0), 1, "C#6:4 D6:2 E6:10")
    P('S1', c(1), 1, "D6:4 R:2")
    sc.theme('S1', c(1), 2.5, octv(GUESTS['V'][0], 1), 'Fugue V guest (D major, own key)', 'V', semis=12)
    P('S1', c(3), 2.5, "C#6:2 B5:8~")
    P('S1', c(4), 1, "B5:12 A#5:4")                  # 4-3 over F#7
    # Voicing rule for c0-c4: one seventh and one leading tone per beat (F#7: A# in S2, E in S1;
    # Bm7: A only in Fugue V's subject; C#o7: one B; E#o7: one D; C#7/E#: E# only in the cantus).
    # S2 long breath: A# | B F# | F# E | E# D | C#
    P('S2', c(0), 1, "A#5:16")
    P('S2', c(1), 1, "B5:4 F#5:12~")
    P('S2', c(2), 1, "F#5:8 E5:8")
    P('S2', c(3), 1, "E#5:12 D5:4")
    P('S2', c(4), 1, "C#5:16")
    # S3: CS1 x2 ends on C#; upbeat figure into c1; upbeat figure into c4
    P('S3', c(0), 1, "C#5:8 R:2 F#4:2 F#4:2 F#4:2")
    P('S3', c(1), 1, "D5:6 C#5:2 D5:8")
    P('S3', c(2), 1, "R:8 E5:8")
    P('S3', c(3), 1, "D5:4 R:6 E#4:2 E#4:2 E#4:2")
    P('S3', c(4), 1, "C#5:6 B4:2 C#5:8")
    # S4 chain
    P('S4', c(0), 1, "R:4 C#5:8 F#5:4~")
    P('S4', c(1), 1, "F#5:4 D5:12~")
    P('S4', c(2), 1, "D5:8")
    P('S4', c(3), 1, "G#5:16~")
    P('S4', c(4), 1, "G#5:8")
    # S5: sixteenths c1-c2a
    P('S5', c(0), 3, "F#5:8~")
    P('S5', c(1), 1, "F#5:1 E5:1 D5:1 E5:1 F#5:1 G5:1 F#5:1 E5:1 D5:1 C#5:1 B4:1 C#5:1 D5:1 C#5:1 D5:1 E5:1")
    P('S5', c(2), 1, "D5:4 F#5:1 B5:1 A5:1 G5:1 F#5:1 E5:1 F#5:1 G5:1 E5:2 R:2")
    P('S5', c(3), 1, "R:4 B4:4 D5:4 E#5:4")
    P('S5', c(4), 1, "G#5:8 C#6:8")
    # A1 upbeat into c2.3, chain
    P('A1', c(0), 1, "C#5:12 R:4")
    P('A1', c(1), 1, "B4:12 A4:4~")
    P('A1', c(2), 1, "A4:2 B4:2 B4:2 B4:2 G5:6 F#5:2")   # lands G (C#o7), leans
    P('A1', c(3), 1, "E#5:8 B4:8")
    P('A1', c(4), 1, "C#5:16")
    # A2 long breath: F# | F# | F# E | G# | G#
    P('A2', c(0), 1, "R:6 F#4:10~")
    P('A2', c(1), 1, "F#4:16~")
    P('A2', c(2), 1, "F#4:12 G4:4")
    P('A2', c(3), 1, "G#4:16~")
    P('A2', c(4), 1, "G#4:8 R:8")
    # A3 chain
    P('A3', c(0), 1, "R:8 F#4:4 C#5:4~")
    P('A3', c(1), 1, "C#5:4 B4:12~")                  # 9-8
    P('A3', c(2), 1, "B4:16~")
    P('A3', c(3), 1, "B4:12 G#4:4~")
    P('A3', c(4), 1, "G#4:8")
    # A4 sixteenths c0 and c4 (the leading tone only between the beats)
    P('A4', c(0), 1, "F#4:1 G#4:1 A#4:1 G#4:1 F#4:1 E#4:1 F#4:1 G#4:1 F#4:1 A#4:1 C#5:1 A#4:1 F#4:1 G#4:1 A#4:1 B4:1")
    P('A4', c(1), 1, "R:4 D4:12~")
    P('A4', c(2), 1, "D4:8")
    P('A4', c(3), 1, "G#4:16")
    P('A4', c(4), 1, "G#4:1 F#4:1 E#4:1 F#4:1 G#4:1 A#4:1 B4:1 G#4:1 A#4:1 B4:1 C#5:1 E5:1 F#5:1 E5:1 C#5:1 A#4:1")
    # A5 sixteenths c2
    P('A5', c(0), 1, "E4:8 C#4:8")
    P('A5', c(1), 1, "F#4:8 B3:8~")
    P('A5', c(2), 1, "B3:1 C#4:1 D4:1 E4:1 F#4:1 E4:1 F#4:1 A4:1 G4:4 F#4:2 E4:2")
    P('A5', c(3), 1, "R:4 E#4:8 G#4:4")
    P('A5', c(4), 1, "G#4:8")
    # T1: an echo of the guest's tattoo
    P('T1', c(1), 1, "R:8 D4:4 D4:2 D4:1 D4:1")
    P('T1', c(2), 1, "D4:4 D4:2 D4:1 D4:1 R:8")
    P('T1', c(3), 1, "B4:4 B4:2 B4:1 B4:1 G#4:8")
    P('T1', c(4), 1, "C#4:8 F#3:8")
    # T2 upbeat figures into c1 and c3
    P('T2', c(0), 1, "F#3:8 R:2 C#4:2 C#4:2 C#4:2")
    P('T2', c(1), 1, "A4:6 G4:2 F#4:8~")               # lands A (7th of Bm7, before the guest's A)
    P('T2', c(2), 1, "F#4:8")
    P('T2', c(3), 3, "G#4:8~")
    P('T2', c(4), 1, "G#4:8 E4:8")
    # T3 long breath: C# | D | D E | E# G# | G# F#
    P('T3', c(0), 1, "C#4:16")
    P('T3', c(1), 1, "D4:16~")
    P('T3', c(2), 1, "D4:8 E4:8")
    P('T3', c(3), 1, "G#3:16~")
    P('T3', c(4), 1, "G#3:8 F#3:8")
    # T4 sixteenths c3
    P('T4', c(0), 1, "R:8 F#3:8~")
    P('T4', c(1), 1, "F#3:16~")
    P('T4', c(2), 1, "F#3:4 D4:8 C#4:4")
    P('T4', c(3), 1, "R:1 F#3:1 G#3:1 F#3:1 E#3:1 F#3:1 G#3:1 A3:1 B3:1 A3:1 G#3:1 A3:1 B3:1 C#4:1 D4:1 C#4:1")
    P('T4', c(4), 1, "R:2 C#4:10 F#3:4")
    # T5 chain
    P('T5', c(0), 1, "R:4 C#4:12~")
    P('T5', c(1), 1, "C#4:12 B3:4~")                   # 9-8, late
    P('T5', c(2), 1, "B3:8")
    P('T5', c(3), 1, "R:4 G#3:12~")
    P('T5', c(4), 1, "G#3:8")
    # Br1 upbeat figure into c2.2
    P('Br1', c(1), 1, "R:4 D3:4 F#3:4 R:2 D3:2")
    P('Br1', c(2), 1, "D3:2 D3:2 B3:6 C#4:6")
    P('Br1', c(3), 1, "R:4 B3:12")
    P('Br1', c(4), 1, "G#3:8")
    # Br2 long line
    P('Br2', c(0), 1, "C#4:4 F#3:12~")
    P('Br2', c(1), 1, "F#3:16~")
    P('Br2', c(2), 1, "F#3:8 C#4:4 B3:4~")
    P('Br2', c(3), 1, "B3:8")
    P('Br2', c(4), 4, "C#4:4")
    # Br3 walking quarters
    P('Br3', c(0), 1, "R:4 C#3:4")
    P('Br3', c(1), 1, "F#3:6 E3:2 F#3:4 D3:4")
    P('Br3', c(2), 1, "B2:4 B3:4 E3:4 C#3:4")
    P('Br3', c(3), 1, "G#3:4 B2:8")
    P('Br3', c(4), 2, "C#3:4")
    # Br4 half notes
    P('Br4', c(0), 1, "R:4 C#4:12~")
    P('Br4', c(1), 1, "C#4:4 D4:12")
    P('Br4', c(2), 1, "D3:8")
    P('Br4', c(3), 1, "R:4 G#3:12~")
    P('Br4', c(4), 1, "G#3:4")
    # Br5, B1-B4
    P('Br5', c(0), 1, "C#3:16")
    P('Br5', c(1), 1, "R:8 F#3:8~")
    P('Br5', c(2), 1, "F#3:8 R:8")
    P('Br5', c(3), 1, "R:4 G#3:12~")
    P('Br5', c(4), 1, "G#3:8 R:8")
    P('B1', c(0), 1, "C#3:16")
    P('B1', c(1), 1, "R:8 D3:8")
    P('B1', c(4), 1, "R:8 C#3:8")
    P('B2', c(0), 1, "F#2:16")
    P('B3', c(3), 1, "B2:12 R:4")
    P('B3', c(4), 1, "R:8 C#3:8")
    P('B4', c(0), 1, "R:8 F#2:8")

# The composer's harmonic plan for c0-c4 (beats relative to c0 = 0), used by nct.py.
def plan_a(off):
    B, Cs, D, Ds, E, Es, Fs, G, Gs, A, As = 11, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    rows = [(0, 4, [Fs, As, Cs, E], 'F#7'), (4, 10, [B, D, Fs, A], 'Bm7'), (10, 12, [Cs, E, G, B], 'C#o7'),
            (12, 16, [Es, Gs, B, D], 'E#dim7'), (16, 18, [Cs, Es, Gs, B], 'C#7/E#'), (18, 20, [Fs, As, Cs, E], 'F#7')]
    return [[off + a, off + b, pcs, lab] for a, b, pcs, lab in rows]
