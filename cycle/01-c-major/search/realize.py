"""Key-aware realisation of subject statements (degree space -> spelled tokens).

Degrees are diatonic steps above the key's tonic in octave 4 (tonic4 = 0).
The subject (C major, tonic C) has degrees G4=-3? No: degrees are measured from
C4 = 0, so the subject's G4 = 4, C5 = 7, ...  A statement in key K keeps those
degree numbers relative to K's tonic (so 'rectus +0 in G' starts on D5).

rectus  shift s: degree d -> d + s
inversus shift s: degree d -> s - d
Pitches take the key signature's accidentals; minor keys are natural minor
(leading tones are added by hand in the score where the line wants them).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ladder import parse, pair_cost  # noqa: E402

LET = 'CDEFGAB'
NAT = [0, 2, 4, 5, 7, 9, 11]
SIG = {  # key -> {letter: alter}
    'C': {}, 'a': {}, 'G': {'F': 1}, 'e': {'F': 1}, 'D': {'F': 1, 'C': 1}, 'b': {'F': 1, 'C': 1},
    'F': {'B': -1}, 'd': {'B': -1}, 'Bb': {'B': -1, 'E': -1}, 'g': {'B': -1, 'E': -1},
}
TONIC = {'C': 'C', 'a': 'A', 'G': 'G', 'e': 'E', 'D': 'D', 'b': 'B', 'F': 'F', 'd': 'D', 'Bb': 'B', 'g': 'G'}
SUBJ = parse(open(Path(__file__).resolve().parent.parent / 'SUBJECT.txt').readline())


def deg_to_tok(deg, key, octave_shift=0):
    t = LET.index(TONIC[key])
    if key == 'Bb':
        pass
    absl = t + deg + 7 * (4 + octave_shift)     # absolute letter index
    L = LET[absl % 7]
    octv = absl // 7
    alt = SIG[key].get(L, 0)
    midi = 12 * (octv + 1) + NAT[LET.index(L)] + alt
    name = L + ('#' * alt if alt > 0 else 'b' * (-alt)) + str(octv)
    return name, midi


def statement(key, form='rectus', shift=0, octave=0, notes=SUBJ):
    out = []
    for d, g in notes:
        q = g + shift if form == 'rectus' else shift - g
        nm, midi = deg_to_tok(q, key, octave)
        out.append((d, nm, midi))
    return out


def tokens(st):
    return ' '.join(f'{nm}:{d}' for d, nm, _ in st)


def placed(st, start):
    out, t = [], start
    for d, nm, midi in st:
        out.append((t, t + d, 0, midi))
        t += d
    return out


def head_ok(st):
    return abs(st[0][2] - st[1][2]) != 6


def rung_cost(key, d8, lead_oct, fform, fshift, foct, detail=False, lead_shift=0):
    L = statement(key, 'rectus', lead_shift, lead_oct)
    F = statement(key, fform, fshift, foct)
    A = placed(L, 14)
    B = placed(F, 14 + 2 * d8)
    c, w = pair_cost(A, B, True)
    return c, w, L, F
