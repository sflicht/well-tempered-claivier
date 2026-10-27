"""Convergence, part C: cantus bars c9-c11 (G G# A A# B) and the arrival, c12-c13.
Fugue II's subject closes (B C G over the cantus's G); Fugue IV's subject, transposed to
B minor, enters at the top (c9.4) and peaks on G6 over the diminished seventh A#dim7;
its A# leans onto the arrival an eighth after the cantus reaches B.  At the arrival the
held and landing lines resolve one after another across the first two beats.
Harmony: c9 C/G . E7/G# | c10 A7 . A#dim7 | c11 B | c12 E/B . F#7/B | c13 B"""
from xxiv import *


def part_c(sc, b0, close=True):
    c = lambda k: b0 + k
    P = sc.put
    # ---- Fugue IV's subject, B minor (-2), Soprano I, re-barred to start on beat 4
    sc.theme('S1', c(9), 4, tr(octv(GUESTS['IV'][0], 2), -2, -1) + '~', 'Fugue IV guest (in B minor)', 'IV', semis=22)
    P('S1', c(11), 2, "B5:12")
    # ---- cantus continues after its last B: a cadence underneath
    # ---- S2: B | C# . . . | (C#) D#
    P('S2', c(9), 3, "B5:8")
    P('S2', c(10), 1, "C#6:16~")
    P('S2', c(11), 1, "C#6:4 D#6:12")
    # ---- S3: E . F# | E G | (G) F#
    P('S3', c(9), 1, "E5:12 F#5:4")
    P('S3', c(10), 1, "E5:16~")
    P('S3', c(11), 1, "E5:4 D#5:12")
    # ---- S4: C B | C# . | (C#) B
    P('S4', c(9), 1, "C5:8 B4:4 C#5:4~")
    P('S4', c(10), 1, "C#5:16~")
    P('S4', c(11), 1, "C#5:2 B4:14")
    # ---- S5: upbeat figures into c10 and c11 (the knocking quickens)
    P('S5', c(9), 3, "R:2 D5:2 D5:2 D5:2")
    P('S5', c(10), 1, "B5:6 A5:2 R:2 E5:2 E5:2 E5:2")
    P('S5', c(11), 1, "C#6:6 B5:2 B5:8")
    # ---- A1: G . | E D | C# . | (C#) D#
    P('A1', c(9), 1, "G4:8 E4:4 D4:4")
    P('A1', c(10), 1, "E4:16~")
    P('A1', c(11), 1, "E4:8 D#4:8")
    # ---- A2: chain, from c9.3
    P('A2', c(9), 3, "G#4:8~")
    P('A2', c(10), 1, "G#4:4 A4:4 E4:4 G4:4~")       # G#->A over A7; G enters as the only 7th of A#o7
    P('A2', c(11), 1, "G4:8 F#4:8")                  # G over B: 6-5 into F#
    # ---- A3: C D | (D) C# . | (C#) D#
    P('A3', c(9), 1, "C5:8 D5:8~")
    P('A3', c(10), 1, "D5:4 C#5:12~")
    P('A3', c(11), 1, "C#5:8 D#5:8")
    # ---- A4: sixteenths to the arrival
    P('A4', c(9), 1, "G4:1 C5:1 E5:1 C5:1 G4:1 A4:1 B4:1 A4:1 E5:1 D5:1 B4:1 G#4:1 B4:1 D5:1 E5:1 B4:1")
    P('A4', c(10), 1, "G4:1 A4:1 C#5:1 E5:1 C#5:1 A4:1 B4:1 C#5:1 E5:1 C#5:1 A#4:1 C#5:1 E5:1 F#5:1 G5:1 E5:1")
    P('A4', c(11), 1, "F#5:12 B4:4")
    # ---- A5: enters on A7
    P('A5', c(10), 1, "C#4:12 A#3:4~")
    P('A5', c(11), 1, "A#3:8 B3:8")
    # ---- T1: the descending wedge against the rising cantus: E D C# . B
    P('T1', c(9), 1, "E4:8 D4:8")
    P('T1', c(10), 1, "C#4:16")
    P('T1', c(11), 1, "B3:16")
    # ---- T2
    P('T2', c(9), 1, "G3:8 R:8")
    P('T2', c(10), 1, "R:8 E3:8~")
    P('T2', c(11), 1, "E3:4 F#3:12")
    # ---- T3: upbeat figure into c11
    P('T3', c(10), 3, "R:2 C#4:2 C#4:2 C#4:2")
    P('T3', c(11), 1, "A#4:12 B4:4")
    # ---- T4: sixteenths in c10
    P('T4', c(9), 1, "R:4 E4:12~")
    P('T4', c(10), 1, "E4:1 D4:1 C#4:1 A3:1 B3:1 C#4:1 E4:1 C#4:1 A#3:1 B3:1 C#4:1 E4:1 C#4:1 B3:1 A#3:1 C#4:1")
    P('T4', c(11), 1, "E4:12 D#4:4")
    # ---- T5: upbeat figure into c11
    P('T5', c(9), 3, "R:8")
    P('T5', c(10), 1, "E4:8 R:2 A#3:2 A#3:2 A#3:2")
    P('T5', c(11), 1, "F#4:16")
    # ---- baritones and basses: fewer low voices in c9-c10 (the cantus is the bass);
    #      the resting ones re-enter on the arrival (c11)
    P('Br1', c(9), 4, "B3:4")
    P('Br1', c(10), 1, "R:4 E4:8 R:4")
    P('Br1', c(11), 2, "B3:12")
    P('Br2', c(9), 1, "E4:4 G3:4 D4:8")
    P('Br2', c(10), 1, "A3:4 C#4:8 A#3:4")
    P('Br2', c(11), 1, "F#3:16")
    P('Br3', c(11), 1, "D#3:16")
    P('Br4', c(11), 3, "F#3:8")
    P('Br5', c(9), 1, "G3:8 B3:8")
    P('Br5', c(10), 1, "B3:4 A3:4 C#4:8~")
    P('Br5', c(11), 1, "C#4:10 B3:6")
    P('B1', c(9), 1, "R:4 C3:8 D3:4~")
    P('B1', c(10), 1, "D3:8 C#3:8")
    P('B1', c(11), 1, "D#3:16")
    P('B2', c(10), 3, "E3:8")
    P('B2', c(11), 1, "R:16")
    P('B3', c(11), 3, "B3:8")
    P('B5', c(11), 1, "B2:16")                       # the cantus's A# resolves with the arrival

    if not close:
        return
    # ---- the close (standalone excerpt only; in the fugue the release follows):
    #      most lines hold the arrival, three make a plagal inflection, the cantus drops to B1
    hold = {'S3': 'D#5', 'S4': 'B4', 'S5': 'B5', 'A1': 'D#4', 'A3': 'D#5', 'A4': 'B4', 'A5': 'B3',
            'T1': 'B3', 'T3': 'B4', 'T4': 'D#4', 'T5': 'F#4', 'Br1': 'B3', 'Br2': 'F#3', 'Br3': 'D#3',
            'Br4': 'F#3', 'Br5': 'B3', 'B1': 'D#3', 'B3': 'B3', 'T2': 'F#3'}
    for v, p in hold.items():
        P(v, c(12), 1, f"{p}:16")
        P(v, c(13), 1, f"{p}:8 R:8")
    P('S1', c(12), 1, "B5:8 C#6:4 D#6:4")
    P('S1', c(13), 1, "D#6:16")
    P('S2', c(12), 1, "D#6:8 E6:8")
    P('S2', c(13), 1, "D#6:12 R:4")
    P('A2', c(12), 1, "F#4:8 G#4:8")
    P('A2', c(13), 1, "F#4:12 R:4")
    P('B5', c(12), 1, "B1:16")
    P('B5', c(13), 1, "B1:8 R:8")


def plan_c(off):
    B, C, Cs, D, Ds, E, F, Fs, G, Gs, A, As = 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    rows = [(0, 2, [C, E, G], 'C/G'), (2, 4, [E, Gs, B, D], 'E7/G#'), (4, 6, [A, Cs, E, G], 'A7'),
            (6, 8, [As, Cs, E, G], 'A#dim7'), (8, 12, [B, Ds, Fs], 'B'), (12, 16, [B, Ds, Fs, E, Gs], 'B (E/B inflection)'),
            (16, 20, [B, Ds, Fs], 'B')]
    return [[off + a, off + b, pcs, lab] for a, b, pcs, lab in rows]
