#!/usr/bin/env python3
"""Fugue XVIII in G-sharp minor, nineteen voices: "Vigilate" (the four night watches).

Every note is written here.  Thematic statements are explicit transforms
(wtclib.transpose / scale_rhythm) of the hand-written subject and door
subject; everything else is literal token strings placed at bar / half-note
beat positions.  No code chooses pitches.

Bar = 3/2 (24 sixteenths).  pos(bar, beat, e): beat = half-note beat 1-3,
e = extra eighths.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (3, 2)
BAR = 24
NAMES = ['S1', 'S2', 'S3', 'S4', 'S5', 'A1', 'A2', 'A3', 'A4', 'A5',
         'T1', 'T2', 'T3', 'T4', 'Br1', 'Br2', 'Br3', 'B1', 'B2']
LONG = ['Soprano I', 'Soprano II', 'Soprano III', 'Soprano IV', 'Soprano V',
        'Alto I', 'Alto II', 'Alto III', 'Alto IV', 'Alto V',
        'Tenore I', 'Tenore II', 'Tenore III', 'Tenore IV',
        'Baritono I', 'Baritono II', 'Baritono III', 'Basso I', 'Basso II']
CLEF = ['treble'] * 10 + ['treble_8'] * 4 + ['bass'] * 5

# ---------------------------------------------------------------- material
# THE SUBJECT, "night".  It keeps its shape through the four watches; each
# watch raises one note, in the order of the sharps (A, E, B, F#), so the
# subject brightens from Phrygian to Ionian.  The eighth sharp cannot be
# written in G-sharp: at dawn the score turns to A-flat major.
S_PHR = 'G#4:8 A4:8 B4:8 E5:12 D#5:4 C#5:8 B4:4 A4:4 G#4:8 F#4:8'       # I   Sero (evening)
S_AEO = 'G#4:8 A#4:8 B4:8 E5:12 D#5:4 C#5:8 B4:4 A#4:4 G#4:8 F#4:8'     # II  Media nocte
S_DOR = 'G#4:8 A#4:8 B4:8 E#5:12 D#5:4 C#5:8 B4:4 A#4:4 G#4:8 F#4:8'    # III Galli cantu
S_MIX = 'G#4:8 A#4:8 B#4:8 E#5:12 D#5:4 C#5:8 B#4:4 A#4:4 G#4:8 F#4:8'  # first light
S_ION = 'Ab4:8 Bb4:8 C5:8 F5:12 Eb5:4 Db5:8 C5:4 Bb4:4 Ab4:8 G4:8'      # IV  Mane (A-flat major)

# The answers at the fifth stay inside each watch's collection.
A_PHR = 'D#4:8 E4:8 F#4:8 B4:12 A#4:4 G#4:8 F#4:4 E4:4 D#4:8 C#4:8'     # D# Phrygian (real answer of I; tonal answer of II)
A_DOR = 'D#4:8 E#4:8 F#4:8 B4:12 A#4:4 G#4:8 F#4:4 E#4:4 D#4:8 C#4:8'   # D# Aeolian
A_ION = 'Eb4:8 F4:8 G4:8 C5:12 Bb4:4 Ab4:8 G4:4 F4:4 Eb4:8 Db4:8'       # E-flat Mixolydian

# THE DOOR, after BWV 61 no. 4, "Siehe, ich stehe vor der Tuer und klopfe an":
# three knocks, then a chromatic rise through the notes that change
# (E/E#, F#/F##), arriving on the tonic.
K = 'D#4:2 R:2 D#4:2 R:2 D#4:4 E4:4 E#4:4 F#4:4 F##4:4 G#4:8'           # 36 sixteenths
KA = 'A#3:2 R:2 A#3:2 R:2 A#3:4 B3:4 B#3:4 C#4:4 C##4:4 D#4:8'           # the door subject on the dominant's fifth
K_LOW = 'G#3:2 R:2 G#3:2 R:2 G#3:4 A3:4 A#3:4 B3:4 B#3:4 C#4:8'          # the lower door (A/A#, B/B#)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []


def pos(bar, beat=1, e=0):
    return Fr(bar - 1) * BAR + (Fr(beat) - 1) * 8 + Fr(e) * 2


def put(v, bar, beat, toks, e=0):
    VO[v].append((pos(bar, beat, e), toks))


def theme(v, bar, beat, toks, label, nbars=None, e=0):
    put(v, bar, beat, toks, e)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / BAR))
    ENTRIES.append((LONG[NAMES.index(v)], bar, (Fr(beat) - 1) * 2 + Fr(e, 2), label, n))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / BAR + 1)}: {toks[:40]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * BAR)
    if cur > total:
        raise ValueError(f'{v}: runs past the end')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)



# ================================================================ I. SERO (evening), Phrygian: b1-15
# The subject rises out of the depth (bass), the answers climb one register at a time.
# Harmony keeps the Phrygian A natural (Neapolitan colour); phrases close with A -> G# in the bass.
theme('B1', 1, 1, octv(S_PHR, -2), 'I. Sero: subject (Phrygian) in the bass')
theme('T2', 4, 1, A_PHR, 'I: answer (D# Phrygian)')
put('B1', 4, 1, 'G#2:8 E2:4 F#2:4 B2:8 G#2:8 F#2:8 C#3:8 D#3:8 B2:8 A2:8 '          # countersubject (bass)
                'G#2:8 F#2:8 E2:8 C#3:8 G#2:8 A2:8 E2:16 D#2:8')
theme('Br2', 7, 1, octv(S_PHR, -1), 'I: subject')
put('T2', 7, 1, 'D#4:6 E4:2 F#4:8 G#4:8 G#4:8 B3:8 E4:8 E4:4 D#4:4 C#4:8 B3:8')
theme('A4', 10, 1, A_PHR, 'I: answer')
put('Br2', 10, 1, 'B2:8 E2:4 F#2:4 B2:8 G#2:8 F#2:8 C#3:8 D#3:8 B2:8 A2:8')             # countersubject, now in the baritone
put('T2', 10, 1, 'B3:8 G#3:8 D#4:8 D#4:8 A#3:8 C#4:8 F#3:8 G#3:8 A3:8')
theme('S4', 13, 1, S_PHR, 'I: subject (soprano)')
put('A4', 13, 1, 'D#4:8 F#4:8 G#4:8 G#4:8 B4:8 E4:8 G#4:8 B3:8 D#4:8')
put('T2', 13, 1, 'G#3:8 C#4:8 E4:8 C#4:8 F#3:8 A3:8 G#3:8 E3:8 F#3:8')
put('Br2', 13, 1, 'B2:8 C#3:8 G#2:8 E3:8 D#3:8 E3:8 G#2:8 B2:8 F#2:8')
put('B1', 13, 1, 'G#2:8 F#2:8 E2:8 C#3:8 B2:8 A2:8 E2:16 D#2:8')


# ================================================================ II. MEDIA NOCTE, Aeolian (A#): b16-30
# The door subject (BWV 61: "Siehe, ich stehe vor der Tuer und klopfe an") is heard for the first time:
# three knocks, then the chromatic rise.  The subject enters 1.5 beats after the knocks, a third
# above the rise, so that it is displaced off the beat: its long notes become suspensions.
theme('T1', 16, 1, K, 'II. Media nocte: door subject (first time)', 2)
theme('A2', 16, 2.5, S_AEO, 'II: subject (Aeolian), entering off the beat against the door subject', 3)
put('B1', 16, 1, 'G#2:16 E#2:8 D#2:8 G#2:8 C#3:8 B2:8 F#2:16 '
                  'D#3:16 B#2:8 A#2:8 D#3:8 G#2:8 F#2:8 C#3:16')
put('Br2', 16, 1, 'D#3:16 G#2:8 R:24 F#3:8 A#2:16 F#3:16 G#3:16 F#3:8 G#3:8 C#3:8 E#3:8 G#3:8')
put('T2', 17, 2, 'D#4:8 E4:8 F#4:16 A#3:8 D#4:24 A#3:16 B3:8 C#4:16')
put('S4', 18, 1, 'F#5:16 C#5:8 D#5:4 R:12 B#4:12 A#4:12 G#4:8 A#4:8 C#5:16')
put('T1', 17, 2.5, 'R:4 R:8 B3:8 A#3:8 R:8 R:24 R:16 D#4:8 F#4:8 E#4:16')
theme('T4', 19, 1, KA, 'II: door subject on A# (with the answer)', 2)
theme('S5', 19, 2.5, octv(A_DOR, 1), 'II: answer, off the beat, over the door subject', 3)

# b22-24 episode: falling fifths, D#m7 G#m7 C#m7 F#7 Bmaj7 Emaj7 A#o7 D#7 G#m; each seventh is
# prepared and resolved (Soprano IV and Alto II hold and fall in turn); the knocks begin to travel.
put('B1', 22, 1, 'D#3:8 G#2:8 C#3:8 F#2:8 B2:8 E2:8 A#2:8 D#2:8 G#2:8')
put('S4', 22, 1, 'F#5:16 E5:16 D#5:16 C#5:16 B4:8')
put('A2', 22, 1, 'A#4:8 B4:16 A#4:16 G#4:16 F##4:8 G#4:8')
put('Br1', 23, 2, 'F#3:2 R:2 F#3:4 R:8')
put('T1', 22, 1, 'A#3:8 D#4:8 E4:8 C#4:2 R:2 C#4:2 R:2 C#4:4 R:4 B3:8 E4:8 D#4:16')
put('T2', 22, 1, 'F#3:8 R:8 G#3:8 F#3:8 D#3:8 R:8 R:8 A#3:8 G#3:8')
put('S5', 22, 2.5, 'D#5:4 R:4 F#5:2 R:2 F#5:2 R:2 F#5:4 R:12 R:8 A#4:2 R:2 A#4:2 R:2 A#4:4 R:4')

# b25-28: the door again, an octave lower in the baritone; the subject in the fifth alto
theme('Br1', 25, 1, octv(K, -1), 'II: door subject in the baritone', 2)
theme('A5', 25, 2.5, S_AEO, 'II: subject, off the beat, over the door subject', 3)
put('B1', 25, 1, 'G#2:16 C#3:8 A#2:8 G#2:8 C#3:8 B2:8 F#2:16 D#2:16')
put('Br1', 26, 3, 'G#3:8 D#3:8 A#2:16 F#3:16')
put('S4', 25, 1, 'D#5:16 C#5:8 R:8 G#5:20 F#5:12 C#5:8 D#5:16')
put('T1', 25, 1, 'B3:16 C#4:8 C#4:8 B3:8 C#4:8 D#4:8 F#3:8 C#4:8 C#4:16')
put('T2', 25, 1, 'G#3:24 D#4:16 E4:8 B3:8 C#4:8 F#3:8 R:16')
put('Br2', 25, 1, 'B2:16 R:8 R:16 E3:8 G#3:8 C#3:16 R:16')

# b28.3-30: the bass climbs the door's rise, E E# F# F## G#, and the Dorian E# (the next sharp)
# sounds at the top over the subdominant C# major; half cadence on D#.
put('B1', 28, 3, 'E2:8 E#2:8 F#2:8 F##2:8 G#2:8 C#3:8 D#3:8')
put('S4', 28, 3, 'G#5:16 F#5:8 A#5:8 G#5:8 E#5:8 F##5:8')
put('A5', 28, 3, 'B4:8 G#4:8 A#4:16 B4:8 C#5:8 A#4:8')
put('T1', 28, 3, 'B3:8 C#4:8 F#4:8 C#4:8 B3:8 G#3:8 C#4:8')
put('A2', 28, 3, 'R:8 E#4:8 D#4:8 D#4:16 E#4:8 D#4:8')

# ================================================================ III. GALLI CANTU (cockcrow), Dorian (E#): b31-44
# The subject now has E# (its leap B-E# is the shrill augmented fourth of the cockcrow); the door
# subject rises D# E# F# F## G#.  New voices enter with each statement; the texture thickens toward
# the summit.
K_DOR = 'D#4:2 R:2 D#4:2 R:2 D#4:4 E#4:4 F#4:4 F##4:4 G#4:8'
theme('T3', 31, 1, K_DOR, 'III. Galli cantu: door subject (Dorian)', 2)
theme('A3', 31, 2, S_DOR, 'III: subject (Dorian)', 3)
put('B1', 31, 1, 'G#2:16 D#3:8 G#2:8 E#2:8 C#3:8 F#2:8 D#3:8 G#2:8')
put('S4', 31, 1, 'G#5:20 F#5:4 D#5:8 G#5:16 F#5:8 D#5:16')
put('T1', 31, 1, 'B3:16 A#3:8 D#4:8 C#4:16 A#3:8 B3:16')
put('A2', 31, 1, 'B4:16 R:16 G#4:8 E#4:8 F#4:16 B4:8')
put('Br2', 31, 1, 'D#3:16 R:8 D#3:8 E#3:16 A#2:8 F#3:8 D#3:8')

# b34-36: the whole block answered a fifth higher (explicit transposition of the block's lines),
# sung by the entering voices: the answer in Soprano III over the door subject on A#.
KA_DOR = 'A#3:2 R:2 A#3:2 R:2 A#3:4 B#3:4 C#4:4 C##4:4 D#4:8'
theme('T4', 34, 1, KA_DOR, 'III: door subject on A# (Dorian)', 2)
theme('S3', 34, 2, octv(A_DOR, 1), 'III: answer (D# Aeolian)', 3)
put('B1', 34, 1, 'D#3:16 A#2:8 D#2:8 B#2:8 G#2:8 C#3:8 F#2:8 D#3:8')
put('S2', 34, 1, tr('G#5:20 F#5:4 D#5:8 G#5:16 F#5:8 D#5:16', 7, 4))
put('A1', 34, 2, 'F#4:8 E#4:8 A#4:8 G#4:16 E#4:8 F#4:16')
put('S5', 34, 1, tr('B4:16 R:16 G#4:8 E#4:8 F#4:16 B4:8', 7, 4))
put('Br1', 35, 1, 'A#3:8 B#3:16 E#3:8 C#4:8 A#3:8')

# b37-39: the episode of b22-24 transposed into the Dorian collection (A#m7 D#m7 G#m7 C#7 F#maj7
# Bmaj7 E#o7 A#7 D#m); Basso II enters with the deep bass.
put('B2', 37, 1, tr('D#3:8 G#2:8 C#3:8 F#2:8 B2:8 E2:8 A#2:8 D#2:8 G#2:8', -5, -3))
put('S2', 37, 1, tr('F#5:16 E5:16 D#5:16 C#5:16 B4:8', 7, 4))
put('S3', 37, 2, tr('B4:16 A#4:16 G#4:16 F##4:8 G#4:8', 7, 4))
put('A3', 37, 1, tr('A#3:8 D#4:8 E4:8 C#4:2 R:2 C#4:2 R:2 C#4:4 R:4 B3:8 E4:8 D#4:16', 7, 4))
put('T1', 37, 1, tr('F#3:8 R:8 G#3:8 F#3:8 D#3:8 R:8 R:8 A#3:8 G#3:8', 7, 4))
put('Br1', 38, 2, tr('F#3:2 R:2 F#3:4 R:8', 7, 4))
put('A4', 37, 2.5, tr('D#5:4 R:4 F#5:2 R:2 F#5:2 R:2 F#5:4 R:12 R:8 A#4:2 R:2 A#4:2 R:2 A#4:4 R:4', -5, -3))

# b40-42: block 1's combination returns with the parts exchanged (invertible at the octave):
# the door subject on top (Soprano IV), the subject in the tenor.
theme('S4', 40, 1, octv(K_DOR, 1), 'III: door subject on top (parts exchanged)', 2)
theme('T2', 40, 2, octv(S_DOR, -1), 'III: subject in the tenor (parts exchanged)', 3)
put('B1', 40, 1, 'G#2:16 D#3:8 G#2:8 E#2:8 C#3:8 F#2:8 D#3:8 G#2:8')
put('S3', 40, 1, 'G#5:20 F#5:4 D#5:8 G#5:16 F#5:8 D#5:16')
put('A4', 40, 1, 'B4:16 R:16 G#4:8 E#4:8 F#4:16 B4:8')
put('Br3', 40, 1, 'D#3:16 R:8 D#3:8 E#3:16 A#2:8 F#3:8 D#3:8')

# b43-44: approach.  The bass climbs B B# C# C## D# (the lower door); B#o7 C# C##o7 D# D#7 -> summit.
put('B1', 43, 1, 'B2:8 B#2:8 C#3:8 C##3:8 D#3:8 D#2:8')
put('S3', 43, 2, 'D#5:8 E#5:16 F##5:16')
put('S4', 43, 1, 'F#5:16 G#5:16 A#5:16')
put('A1', 43, 1, 'D#4:8 A#4:8 G#4:8 B4:8 A#4:8 C#5:8')
put('T2', 43, 2, 'R:8 C#4:8 E#4:8 A#3:16')
put('T4', 43, 3, 'E#3:16 R:16')
put('S2', 43, 1, 'B5:8 D#6:8 C#6:16 R:16')
put('A2', 43, 1, 'F#4:16 E#4:16 D#4:16')

# ================================================================ SUMMIT (composed first)
SUM = 45
# "Nox nocti indicat scientiam": eight entries of the Dorian subject, each a
# third above the last, two beats apart, climbing from the bass to the top.
# The two highest entries already carry the first light (B#, Mixolydian).
CHAIN = [  # (voice, bar, beat, tokens) -- modal transpositions inside the Dorian collection, written out
    ('B1', SUM + 0, 1, 'G#2:8 A#2:8 B2:8 E#3:12 D#3:4 C#3:8 B2:4 A#2:4 G#2:8 F#2:8'),     # on G#, the depth
    ('T1', SUM + 0, 3, 'B3:8 C#4:8 D#4:8 G#4:12 F#4:4 E#4:8 D#4:4 C#4:4 B3:8 A#3:8'),     # on B
    ('S2', SUM + 1, 2, 'D#5:8 E#5:8 F#5:8 B5:12 A#5:4 G#5:8 F#5:4 E#5:4 D#5:8 C#5:8'),    # on D#, high
    ('T3', SUM + 2, 1, 'F#3:8 G#3:8 A#3:8 D#4:12 C#4:4 B3:8 A#3:4 G#3:4 F#3:8 E#3:8'),    # on F#, low
    ('A1', SUM + 2, 3, 'A#4:8 B4:8 C#5:8 F#5:12 E#5:4 D#5:8 C#5:4 B4:4 A#4:8 G#4:8'),     # on A#
    ('Br2', SUM + 3, 2, 'C#3:8 D#3:8 E#3:8 A#3:12 G#3:4 F#3:8 E#3:4 D#3:4 C#3:8 B2:8'),   # on C#, low
    ('A3', SUM + 4, 1, 'E#4:8 F#4:8 G#4:8 C#5:12 B#4:4 A#4:8 G#4:4 F#4:4 E#4:8 D#4:8'),   # on E#: first light (B#)
    ('S1', SUM + 4, 3, 'G#5:8 A#5:8 B#5:8 E#6:12 D#6:4 C#6:8 B#5:4 A#5:4 G#5:8 F#5:8'),   # on G#, Mixolydian, the top
]
for v, b, bt, t in CHAIN:
    theme(v, b, bt, t, 'Summit chain: subject (Dorian) a third higher every two beats', 3)

# The door subject inside the summit (Dorian form: knocks, then E# F# F## G#)
K_DOR = 'D#4:2 R:2 D#4:2 R:2 D#4:4 E#4:4 F#4:4 F##4:4 G#4:8'
theme('A3', SUM + 0, 1, 'D#4:2 R:2 D#4:2 R:2 D#4:4 E#4:8 F#4:2 F##4:2 G#4:8', 'Door subject (knocks), Dorian, the rise hurried', 2)
theme('Br1', SUM + 2, 1, octv(K_DOR, -1), 'Door subject (knocks) in the baritone', 2)

# Phase A free lines (b45-52), added one voice at a time.
L = SUM
put('B2', L + 3, 1, 'G#2:8 A#2:8 B2:8 C#3:8 D#3:8 A#2:16 R:4 G#2:4 R:16 F#2:8 G#2:8 C#3:8 F#2:8 D#2:8')
# free lines, one voice at a time
put('T4', L, 1, 'G#3:8 C#3:8 D#3:8 G#3:8 A#3:12 G#3:4')
put('T2', L, 1, 'B3:8 C#4:8 F#3:8 R:16 E#3:8')
put('B1', L + 4, 3, 'R:8 C#3:8 R:8 A#2:8')
put('A1', L, 1, 'B4:8 A#4:8 R:8')
put('S2', L + 4, 2, 'A#5:8 R:8')
put('S5', L + 2, 1, 'R:8 G#4:2 A#4:2 G#4:2 F##4:2 R:8 R:8 A#4:2 G#4:2 F#4:2 G#4:2 R:8 G#4:2 A#4:2 B4:2 G#4:2 R:16 R:16 C#5:2 B#4:2 C#5:2 D#5:2 R:16 D#5:2 C#5:2 D#5:2 C#5:2')
put('A2', L, 1, 'R:16 D#4:2 D#4:2 D#4:4 R:8 F#4:2 F#4:2 F#4:4 R:8 R:24 R:16 D#4:2 D#4:2 D#4:4 R:8 D#4:2 D#4:2 D#4:4 R:8 R:16 E#4:2 E#4:2 E#4:4 R:8 A#3:2 A#3:2 A#3:4 R:8')
put('A3', L + 1, 2, 'R:8 E#4:8 D#4:16 R:8 G#4:8 E#4:8 R:8')
put('T1', L + 3, 3, 'F#4:8 C#4:8 R:8 C#4:16 D#4:4 B#3:4 C#4:8 C#4:20 B#3:4 C#4:8')
put('S4', L, 1, 'D#5:12 C#5:8 B4:4 B4:4 A#4:8 C#5:12 C#5:4 B4:12 F#5:4 R:4 R:24 R:8 A#4:8 R:8 R:8 D#5:8 E#5:8 C#5:16 G#4:16')
put('S1', L, 1, 'D#6:8 C#6:8 B5:8 G#5:8 F#5:8 G#5:8 D#6:8 R:16')
put('S3', L, 1, 'G#5:8 E#5:8 D#5:8 R:24 D#5:16 R:8 D#5:8 A#5:8 R:8 G#5:8 D#6:8 R:8 F#5:8 G#5:8 A#5:8 C#6:8 A#5:8 G#5:8 E#5:8')



# ================================================================ SUMMIT, phase B: "Vor der Tuer" (b52-56)
# 52.2 D#m/F#: the subject's last F# ... 52.3 D#: ... becomes F##, the leading tone (the last door note).
# Over a knocking D# pedal the door subject enters four times, two beats apart (D#4, A#3, D#4, A#4);
# a chromatic line falls against the rises; three tutti knocks; silence; then the door opens (b57).
KD = 'D#4:2 R:2 D#4:2 R:2 D#4:4 E4:4 E#4:4 F#4:4 F##4:4 G#4:8'         # = K
KNOCK3 = lambda n: f'{n}:2 R:2 {n}:2 R:2 {n}:4 R:12'                   # the last three knocks, then silence
B = SUM + 7   # bar 52
theme('A3', B + 1, 1, KD, 'Door subject 1 (stretto), on D#', 2)
theme('T1', B + 1, 3, KA, 'Door subject 2, on A#', 2)
theme('A2', B + 2, 2, KD, 'Door subject 3, on D#', 2)
theme('S5', B + 3, 1, tr(KA, 12, 7), 'Door subject 4, on A#', 2)
put('S1', B, 3, 'R:8 A#5:16 C#6:16 B#5:8 A#5:8 D#6:16 C#6:16 B#5:8 A#5:8 ' + KNOCK3('D#6'))
put('S2', B, 1, 'R:16 F##5:8 G#5:12 F##5:12 R:16 F##5:8 E#5:8 E5:8 D#5:8 F##5:8 G#5:8 F##5:8 ' + KNOCK3('A#5'))
theme('A2', B + 3, 3.5, 'F##4:4', 'resolution', 0) if False else put('A2', B + 3, 3.5, 'F##4:4')


def knk(v, bar, q, pitch, form='k3'):
    """a knock figure (from the door subject's head) placed at quarter q (0-5) of a bar"""
    f = {'k3': f'{pitch}:2 {pitch}:2 {pitch}:4', 'k2': f'{pitch}:2 R:2 {pitch}:4'}[form]
    VO[v].append((Fr(bar - 1) * BAR + Fr(q) * 4, f))


# b52: the chain's cadence C# - D#m/F# - D#; the voices gather toward the door
put('S3', B, 2, 'D#5:8 A#4:8')
put('S4', B, 2, 'D#4:16')
put('S5', B, 1, 'C#5:8 A#4:8')
put('A1', B, 1, 'E#4:8 F#4:8')
put('A2', B, 3, 'A#3:2 A#3:2 A#3:4')
put('T3', B, 2, 'F#3:8 A#3:8')
put('Br1', B, 2, 'D#3:16')
put('Br2', B, 1, 'G#3:8 A#3:8')
put('Br3', B, 3, 'D#3:8')

# the relay of knocks travels voice to voice (round the ring of players), on D# and A#, b53-55
for v, bar, q, pch, f in [
        ('Br3', 53, 0, 'D#3', 'k3'), ('S4', 53, 0, 'D#5', 'k2'), ('T3', 53, 0, 'A#3', 'k3'), ('S3', 53, 1, 'A#4', 'k3'),
        ('B1', 53, 1, 'A#2', 'k2'), ('Br2', 53, 2, 'A#3', 'k3'), ('A1', 53, 2, 'D#5', 'k3'), ('A5', 53, 2, 'F##4', 'k2'),
        ('A4', 53, 3, 'A#4', 'k2'), ('Br1', 53, 3, 'D#3', 'k3'), ('T4', 53, 4, 'A#2', 'k3'), ('S5', 53, 4, 'D#5', 'k3'),
        ('Br3', 54, 0, 'A#2', 'k3'), ('S4', 54, 0, 'A#4', 'k2'), ('T3', 54, 0, 'D#3', 'k3'), ('T2', 54, 0, 'D#4', 'k2'),
        ('S3', 54, 1, 'D#5', 'k3'), ('B1', 54, 2, 'G#2', 'k3'), ('Br2', 54, 2, 'G#3', 'k2'), ('A1', 54, 2, 'B#4', 'k3'),
        ('A4', 54, 3, 'D#5', 'k3'), ('Br1', 54, 3, 'D#3', 'k2'), ('T4', 54, 4, 'A#3', 'k3'), ('A5', 54, 4, 'A#4', 'k2'),
        ('Br3', 55, 0, 'D#3', 'k3'), ('S4', 55, 0, 'D#5', 'k2'), ('T3', 55, 0, 'A#3', 'k3'), ('S3', 55, 1, 'A#5', 'k3'),
        ('B1', 55, 1, 'A#2', 'k2'), ('T2', 55, 1, 'D#4', 'k3'), ('Br2', 55, 2, 'A#3', 'k3'), ('A4', 55, 3, 'D#4', 'k3'),
        ('Br1', 55, 3, 'A#2', 'k2'), ('T4', 55, 4, 'D#3', 'k3'), ('A5', 55, 4, 'A#3', 'k2'),
        ('Br3', 56, 0, 'D#3', 'k3'), ('S4', 56, 0, 'A#4', 'k2'), ('T2', 56, 0, 'D#4', 'k3'), ('S3', 56, 1, 'D#6', 'k3'),
        ('A3', 56, 1, 'D#4', 'k2'), ('B1', 56, 2, 'G#2', 'k3'), ('Br2', 56, 2, 'B#3', 'k2'), ('A1', 56, 2, 'G#4', 'k3'),
        ('A4', 56, 3, 'D#5', 'k3'), ('Br1', 56, 3, 'D#3', 'k2'), ('A2', 56, 3, 'A#4', 'k3'), ('T4', 56, 4, 'A#3', 'k3'),
        ('A5', 56, 4, 'D#4', 'k2'), ('T1', 56, 4, 'C#4', 'k3'),
        ]:
    knk(v, bar, q, pch, f)
for v, pch in [('S3', 'F##5'), ('S4', 'A#4'), ('A1', 'D#5'), ('A3', 'D#4'), ('A4', 'D#4'), ('A5', 'D#4'), ('A2', 'A#4'),
               ('T1', 'A#3'), ('T2', 'D#3'), ('T3', 'A#2'), ('T4', 'D#3'), ('Br1', 'A#2'), ('Br2', 'D#3'), ('Br3', 'D#2'),
               ('B1', 'D#2')]:
    put(v, B + 5, 1, KNOCK3(pch))
put('B2', B + 1, 1, 'D#2:4 R:4 D#2:4 R:4 D#2:8 D#2:4 R:4 D#2:4 R:4 D#2:8 D#2:4 R:4 D#2:4 R:4 D#2:8 D#2:4 R:4 D#2:4 R:4 D#2:8 ' + KNOCK3('D#2'))


# ================================================================ IV. MANE (morning): b58-72, A-flat major
# The eighth sharp cannot be written: the door opens and the score turns to A-flat major
# (G-sharp major sounding).  The Ionian subject comes down from the top voice to the bass,
# a fourth or fifth lower every two bars; the knocks become bells; the stars go out one by one.
DAWN = 58
theme('S1', DAWN, 1, octv(S_ION, 1), 'IV. Mane: subject in A-flat major (Ionian), at the top', 3)
theme('A3', DAWN + 2, 1, A_ION, 'IV: answer (E-flat Mixolydian)', 3)
theme('A4', DAWN + 4, 2, S_ION, 'IV: subject', 3)
theme('T3', DAWN + 6, 2, octv(A_ION, -1), 'IV: answer', 3)
theme('B1', DAWN + 8, 3, octv(S_ION, -2), 'IV: subject in the bass: the light reaches the depth', 3)
put('B1', 69, 3, 'Ab2:' + str(24 * 2 + 8))
put('B2', DAWN, 1, 'Ab2:8 G2:8 C3:8 Db3:8 Bb2:16 Ab2:8 F2:8 Eb2:8 Ab2:8 F2:16 Eb2:8 Ab2:8 G2:8 '
                   'Ab2:8 Db3:8 Bb2:16 Ab2:8 Db2:8 Eb2:8 Ab2:8 F2:16 R:8')
put('A3', DAWN + 5, 1, 'C4:8')
# the ending: V7 at 69.2 (one leading tone, in the bass subject; one seventh, in Soprano I), then the
# voices gather on A-flat major one by one, by step, through b71.
END = 71
def arrive(v, bar, beat, toks):
    put(v, bar, beat, toks)
put('B2', 68, 1, 'Ab1:8 Bb1:8 Eb2:24')   # I - ii - V(6/4-5/3) under the bass entry
arrive('B2', 69, 3, 'Ab1:' + str(24 * 2 + 8))
arrive('S1', 69, 2, 'Db6:8 C6:' + str(24 * 2 + 8))
arrive('S3', 69, 2, 'Bb5:16 Ab5:' + str(24 * 2))
arrive('S4', 69, 1, 'Eb5:' + str(24 * 3))
arrive('A1', 69, 2, 'Bb4:8 Ab4:' + str(24 * 2 + 8))
arrive('T3', 69, 2, 'Bb3:8 C4:' + str(24 * 2 + 8))
arrive('Br3', 69, 2, 'Eb3:' + str(24 * 2 + 16))
arrive('Br2', 70, 1, 'G3:4 Ab3:' + str(24 + 20))
arrive('S2', 70, 1, 'Db5:4 C5:' + str(24 + 20))
arrive('T2', 70, 3, 'Bb3:4 Ab3:' + str(24 + 4))
arrive('A3', 70, 1.5, 'F5:4 Eb5:' + str(24 + 16))
arrive('T4', 70, 2, 'C3:' + str(24 + 16))
arrive('A5', 70, 2, 'F4:4 Eb4:' + str(24 + 12))
arrive('A2', 70, 2.5, 'Bb4:4 Ab4:' + str(24 + 8))
arrive('A4', 70, 3, 'G4:4 Ab4:' + str(24 + 4))
arrive('Br1', 70, 3, 'Db4:4 C4:' + str(24 + 4))
arrive('S5', 70, 3.5, 'Bb4:4 C5:' + str(24))
put('S1', DAWN + 3, 1, 'Eb6:8 Ab5:8 Db6:8 Bb5:8 C6:8 Bb5:8 Ab5:16 Bb5:16 C6:8 Db6:8 Bb5:8 C6:16 Db6:8 '
                       'Eb6:16 Bb5:8 Ab5:16 C6:8 F6:8 Eb6:16')   # the descant climbs to F6, then Eb6 - Db6 (7th) - C6

# ---- the voices wake, one at a time (b60-69): singing lines in half notes and suspensions
put('T1', 60, 1, 'C4:8 Db4:8 Bb3:8 '      # 9-8 over the tonic at 61.1, 4-3 over the dominant at 62.1
                 'Bb3:4 Ab3:20 '
                 'Ab3:4 G3:4 C4:8 R:8 '
                 'Eb4:8 Db4:16 '
                 'Db4:8 Eb4:4 F4:4 Db4:8 '
                 'R:8 Eb4:8 F4:8 '
                 'F4:8 Eb4:8 C4:8 '
                 'Db4:8 C4:16 '
                 'C4:8 Db4:8 Eb4:56')
put('A4', 65, 2, 'Ab4:16 Db5:8 Bb4:8 Ab4:8 F4:8 Eb4:8 Ab4:16 F4:8 G4:8')   # after its entry, Alto IV sings on
put('T3', 67, 2, 'Ab3:36 G3:4')   # held Ab3: seventh over Bb1 (68.2), then 4-3 over Eb2 (68.3)
put('S4', 65, 2, 'C5:8 F5:16 G5:8 Ab5:4 F5:4 Db5:8 Eb5:8 F5:24 C5:4 Db5:4')   # a new soprano wakes
put('Br2', 65, 1, 'Eb3:8 C3:16 F3:8 R:8 C3:8')
put('A1', 67, 2, 'Ab4:8 C5:16 R:8 Eb5:8 C5:8')

def build(nbars, path=None):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XVIII in G-sharp minor, nineteen voices: Vigilate',
            'composer': 'Claude / Sam (after J. S. Bach, BWV 887 and BWV 61)',
            'instrument': 'Nineteen voices (open score, nineteen keyboards)',
            'key': 'G#', 'mode': 'minor', 'meter': list(METER), 'bpm': 112,
            'movement_number': 18, 'piece_type': 'fugue', 'edition': 'third'}
    voices = [(LONG[i], NAMES[i], CLEF[i], 62) for i, n in enumerate(NAMES)]
    return W.build_score(path or (HERE / 'fugue.json'), meta, voices, bars, entries=ENTRIES, subject=S_AEO)


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // BAR))
    build(nb)
    print('bars', nb)
