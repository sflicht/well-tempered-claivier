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
put('B2', L + 3, 1, 'G#2:8 A#2:8 B2:8 C#3:8 D#3:8 A#2:16 B#2:8 R:16 F#2:8 G#2:8 C#3:8')


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
