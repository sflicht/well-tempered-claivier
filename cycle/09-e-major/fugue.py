#!/usr/bin/env python3
"""Fugue IX in E major, ten voices: "Ricercar a 10 in circulo" (draft scaffold)."""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (2, 2)
NAMES = ['S1', 'A1', 'T1', 'Bar1', 'B1', 'S2', 'A2', 'T2', 'Bar2', 'B2']
SC = [4, 6, 8, 9, 11, 1, 3]          # E major from the tonic

S = 'B4:8 E5:16 D#5:8 C#5:4 B4:4 A4:4 G#4:4 A4:8 B4:8'
F = 'E4:16 F#4:8 A4:8 G#4:8 F#4:8 E4:8'   # BWV 878 / Fischer


def dshift(toks, steps):
    out = []
    for t in toks.split():
        p, d, sp, tie = W.parse_tok(t)
        if p is None:
            out.append(t)
            continue
        pc = p % 12
        deg = ((p - 4) // 12) * 7 + SC.index(pc)
        nd = deg + steps
        q = 4 + (nd // 7) * 12 + ((SC[nd % 7] - 4) % 12)
        nl = 'CDEFGAB'[('CDEFGAB'.index(sp[0].upper()) + steps) % 7]
        out.append(f"{W.name_of(q, nl)}:{t.rsplit(':', 1)[1]}")
    return ' '.join(out)


I = W.invert_diatonic(S, 'B4', SC)
VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, q):
    return Fr(bar - 1) * 16 + (Fr(q) - 1) * 4


def put(v, bar, q, toks):
    VO[v].append((pos(bar, q), toks))


def theme(v, bar, q, toks, label, nbars=None):
    put(v, bar, q, toks)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / 16))
    ENTRIES.append((v, bar, (Fr(q) - 1), label, n))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / 16 + 1)}: {toks[:40]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * 16)
    if cur > total:
        raise ValueError(f'{v}: runs past the end')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# ---- exposition entries
theme('S1', 1, 1, S, 'S on B')
theme('A1', 3, 1, dshift(I, -3), 'I on F#')
theme('T1', 5, 1, dshift(I, -6), 'I on C#')
theme('Bar1', 7, 1, dshift(I, -11), 'I on E')
theme('B1', 9, 1, dshift(I, -14), 'I on B')
theme('S2', 11, 1, dshift(S, 3), 'S on E')
theme('A2', 13, 1, dshift(S, -6), 'S on C#')
theme('T2', 15, 1, dshift(S, -10), 'S on F#')
theme('Bar2', 17, 1, dshift(S, -7), 'S on B')

# ---- FIRST TUTTI (b19-25): ten voices over the ancestor in augmentation
theme('S1', 19, 1, 'B4:16 C#5:8 E5:8 D#5:8 C#5:8 B4:8', "BWV 878 answer at normal speed (Bach's answer form)", 4)
put('S1', 22, 3, 'D#5:8 E5:16 F#5:8 B4:8 E5:16')
theme('T1', 19, 1, 'E4:8 A4:16 G#4:8', 'S head on E', 2)
put('T1', 21, 1, 'A4:16 R:16 G#4:16 R:16 E4:16')
put('B1', 19, 1, 'B2:8 R:8')
theme('B1', 20, 1, 'F#3:8 B3:16 A3:8', 'S head on F#', 2)
put('B1', 22, 1, 'B3:8 R:8 R:8 B2:24 G#2:16')
put('S2', 19, 1, 'E5:8 D#5:8 F#5:8 G#5:8 C#6:24 B5:16 G#5:8 B5:32')
put('A2', 19, 1, 'B3:16 E4:16')
theme('A2', 21, 3, 'C#4:8 F#4:16 E4:8', 'S head on C#', 2)
put('A2', 23, 3, 'E4:8 R:16 B3:16')
put('T2', 19, 1, 'G#3:8 R:8')
theme('T2', 22, 3, 'F#3:8 B3:16 A3:8', 'S head on F#', 2)
put('T2', 24, 3, 'A3:8 G#3:16')
put('Bar2', 21, 1, 'F#3:16')
theme('Bar2', 23, 1, 'B2:8 E3:16 D#3:8', 'S head on B', 2)
put('Bar2', 25, 1, 'E3:16')
put('A1', 19, 1, 'G#4:8 F#4:16 E4:8 C#4:8 E4:8 D#4:8 R:8 R:8')
theme('A1', 23, 3, 'B4:8 F#4:16 G#4:8', 'I head on B', 2)
put('A1', 25, 3, 'G#4:8')
put('Bar1', 19, 3, 'A2:8 C#3:8 B2:8 R:16 F#3:8 R:8 R:16 R:16 B2:16')
theme('B2', 19, 1, W.transpose(W.scale_rhythm(F, 2), -24, -14), 'BWV 878 subject (Fischer/Bach) in augmentation x2', 7)


def build(nbars):
    bars = {n: assemble(n, nbars) for n in NAMES}
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue IX in E major, ten voices',
            'key': 'E', 'mode': 'major', 'meter': list(METER), 'bpm': 84}
    voices = [(n, n, 'treble', 64) for n in NAMES]
    ents = [(v, b, o, l, n) for v, b, o, l, n in ENTRIES]
    return W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ents, subject='B4:8 E5:16 D#5:8 C#5:4 B4:4 A4:4 G#4:4 A4:8 B4:8')


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    build(nb)
    print('bars', nb)
