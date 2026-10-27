"""The release (bars 52-61, B major), after the arrival at c11 (bar 51).
Bars 52-53: the voices let go one after another; Fugue V's subject, transposed to B major,
sounds once more as a fanfare (T3).  Bars 53-57: Fugue I's subject in B major climbs a
two-rung ladder of canons at the octave three eighths apart (its own rung R3): Baritone II
leads, Tenor V follows; then Alto II leads, Soprano I follows, an octave higher, each
entry taking over the last note of the one before.  Bars 58-59: the mirror wedge -- the
subject's chromatic tail rises (G G# A A#) in Tenor I while the inversion's tail falls
(D# D C# C) in Alto III, both in four-fold augmentation like the cantus, over B and E
pedals: Em(maj7) - E7 - A - French sixth, closing together on one B.  Bars 60-61: the
final chord gathers all twenty-five voices."""
from xxiv import *

I_B = tr(GUESTS['FI'][0], -1, -1)        # Fugue I's subject in B major (upbeat F#4)
V_B = tr(GUESTS['V'][0], -3, -2)        # Fugue V's subject in B major (F#4 ...)
S_TAIL4 = aug("G4:2 G#4:2 A4:2 A#4:2", 4)   # the last four notes of S, x4
I_TAIL4 = aug("D#5:2 D5:2 C#5:2 C5:2", 4)   # the last four notes of I, x4


def release(sc, b0=52):
    P = sc.put
    r = lambda k: b0 + k
    # ---- the cantus's B becomes a pedal: one note, ten bars
    for k in range(9):
        P('B5', r(k), 1, "B1:16~")
    P('B5', r(9), 1, "B1:16")
    # ---- bar 52: B major; the arrival's lines let go one after another, eight keep going
    sc.theme('T3', r(0), 1, V_B, 'Fugue V guest (in B major)', 'V', semis=-3)
    P('S1', r(0), 1, "B5:16"); P('S1', r(1), 1, "C#6:4 B5:8 C#6:2 B5:2")
    P('S2', r(0), 1, "D#6:16~"); P('S2', r(1), 1, "D#6:8 E6:4 F#6:4"); P('S2', r(2), 1, "F#6:4 D#6:8 G#5:4")
    P('S2', r(3), 1, "A#5:2 G#5:6 F#5:8")
    P('S3', r(0), 1, "D#5:4")
    P('S4', r(0), 1, "B4:4")
    P('S5', r(0), 1, "B5:8")
    P('A1', r(0), 1, "D#4:8 E4:4 F#4:4"); P('A1', r(1), 1, "F#4:8 G#4:4 F#4:4"); P('A1', r(2), 1, "D#4:4")
    P('A2', r(0), 1, "F#4:12")
    P('A3', r(0), 1, "D#5:8")
    P('A4', r(0), 1, "B4:4")
    P('A5', r(0), 1, "B3:8 C#4:4 D#4:4"); P('A5', r(1), 1, "D#4:12 C#4:4")
    P('T1', r(0), 1, "B3:12")
    P('T2', r(0), 1, "F#3:4")
    P('T4', r(0), 1, "D#4:4")
    P('Br1', r(0), 1, "B3:4")
    P('Br2', r(0), 1, "F#3:16~"); P('Br2', r(1), 1, "F#3:12")
    P('Br3', r(0), 1, "D#3:4")
    P('Br4', r(0), 1, "F#3:4")
    P('Br5', r(0), 1, "B3:8")
    P('B1', r(0), 1, "D#3:8 B2:8"); P('B1', r(1), 1, "B2:8 G#2:4 A#2:4")
    P('B3', r(0), 1, "B3:4")
    # ---- bars 53-55: Fugue I, rung 1 (Br2 leads, T5 follows an octave higher, 3 eighths later)
    sc.theme('Br2', r(1), 4.5, octv(I_B, -1), 'Fugue I guest (in B major), canon leader', 'FI', semis=-13)
    sc.theme('T5', r(2), 2, I_B, 'Fugue I guest, canon at the octave (its rung R3)', 'FI', semis=-1)
    P('S4', r(2), 1, "R:8 F#5:6 E5:2"); P('S4', r(3), 1, "E5:8 D#5:4 C#5:4")
    P('B1', r(2), 1, "B2:12 G#2:4"); P('B1', r(3), 1, "F#2:4 C#3:4 D#3:4 A#2:4")
    P('Br4', r(2), 1, "D#3:12 E3:4"); P('Br4', r(3), 1, "E3:8 F#3:8")
    P('Br4', r(4), 1, "D#3:12 E3:4"); P('Br4', r(5), 1, "E3:8 D#3:8")
    # ---- bars 55-58: rung 2, an octave higher (A2 leads, S1 follows); Br2 and T5 walk down
    sc.theme('A2', r(3), 4.5, I_B, 'Fugue I guest, second rung', 'FI', semis=-1)
    sc.theme('S1', r(4), 2, octv(I_B, 1), 'Fugue I guest, canon at the octave above', 'FI', semis=11)
    P('Br2', r(4), 1, "E4:8 D#4:8"); P('Br2', r(5), 1, "C#4:10 B3:6")
    P('T5', r(4), 2, "D#5:4 C#5:4 B4:4"); P('T5', r(5), 1, "A#4:4 G#4:4 F#4:8")
    P('B1', r(4), 1, "B2:8 A2:4 G#2:4"); P('B1', r(5), 1, "A#2:4 E2:4 F#2:8")
    # ---- bars 58-59: the mirror wedge over B and E: Em(maj7) - E7 - A - French sixth
    P('T1', r(6), 1, S_TAIL4); P('A3', r(6), 1, I_TAIL4)
    P('Br2', r(6), 1, "E3:16~"); P('Br2', r(7), 1, "E3:16")
    P('A2', r(5), 4.5, "E5:2~"); P('A2', r(6), 1, "E5:16~"); P('A2', r(7), 1, "E5:16~")
    P('S1', r(6), 2, "E6:20 F#6:8~")
    P('B1', r(6), 1, "B2:8 E2:8"); P('B1', r(7), 1, "A2:8 F#2:8~")
    # ---- bars 60-61: the last chord.  Each voice arrives by step on its own beat: the wedge
    #      and the bass on 1, then two or three voices on every beat, each from a neighbour note
    P('T1', r(8), 1, "B4:32"); P('A3', r(8), 1, "B4:32"); P('Br2', r(8), 1, "D#3:32")
    P('S1', r(8), 1, "F#6:32"); P('B1', r(8), 1, "F#2:32"); P('A2', r(8), 1, "E5:4 D#5:28")
    arrive = [  # (voice, bar offset, beat of the neighbour note, neighbour, final); it resolves one beat later.
        # at every beat one line falls into the chord and one or two rise into it (contrary motion)
        ('S3', 8, 1, 'C#6', 'B5'), ('Br4', 8, 1, 'A#2', 'B2'),
        ('T3', 8, 2, 'E4', 'D#4'), ('S4', 8, 2, 'E#5', 'F#5'), ('B2', 8, 2, 'C#3', 'B2'),
        ('S2', 8, 3, 'E6', 'D#6'), ('A5', 8, 3, 'E#4', 'F#4'), ('Br5', 8, 3, 'C#3', 'D#3'),
        ('A1', 8, 4, 'C#5', 'B4'), ('T2', 8, 4, 'E3', 'F#3'), ('B3', 8, 4, 'C#2', 'D#2'),
        ('S5', 9, 1, 'E5', 'D#5'), ('T4', 9, 1, 'A#3', 'B3'), ('B4', 9, 1, 'C#2', 'B1'),
        ('A4', 9, 2, 'E4', 'D#4'), ('Br1', 9, 2, 'A#3', 'B3'), ('Br3', 9, 2, 'E#3', 'F#3'),
        ('T5', 9, 3, 'E#4', 'F#4')]
    for v, k, beat, a, f in arrive:
        left = 16 * (10 - (r(k) - b0)) - 4 * (beat - 1)      # sixteenths to the end of the piece
        P(v, r(k), beat, f"{a}:4 {f}:{left - 4}")

B, C, Cs, D, Ds, E, F, Fs, G, Gs, A, As = 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10


def plan_release(o):
    rows = [(0, 4, [B, Ds, Fs], 'B'),
            (4, 6, [B, Ds, Fs], 'B'), (6, 7, [E, Gs, B], 'E/B'), (7, 7.5, [Fs, As, Cs, E], 'F#7/B'), (7.5, 8, [B, Ds, Fs], 'B')]
    for k in (8, 16):        # the two Fugue I rungs share one harmonisation
        rows += [(k, k + 3, [B, Ds, Fs], 'B'), (k + 3, k + 3.5, [E, Gs, B], 'E/B'), (k + 3.5, k + 4, [B, Ds, Fs], 'B'),
                 (k + 4, k + 4.5, [Fs, As, Cs, E], 'F#7/B'), (k + 4.5, k + 5, [Fs, As, Cs, E], 'F#7'),
                 (k + 5, k + 6, [Cs, E, Gs, B], 'C#m7/G#'), (k + 6, k + 7, [B, Ds, Fs], 'B/D#'), (k + 7, k + 8, [Fs, As, Cs], 'F#')]
    rows += [(24, 26, [E, G, B, Ds], 'Em(maj7)/B'), (26, 28, [E, Gs, B, D], 'E7/B'), (28, 30, [A, Cs, E], 'A/B'),
             (30, 32, [C, E, Fs, As], 'Fr6/B'), (32, 40, [B, Ds, Fs], 'B')]
    return [[o + a, o + b, pcs, lab] for a, b, pcs, lab in rows]
