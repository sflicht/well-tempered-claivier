#!/usr/bin/env python3
"""Fugue IX in E major, four voices: "Ricercar in circulo".  (DRAFT IN PROGRESS)"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (2, 2)
NAMES = ['S', 'A', 'T', 'B']
LONG = ['Soprano', 'Alto', 'Tenor', 'Bass']
CLEF = ['treble', 'treble', 'treble_8', 'bass']
SC = [4, 6, 8, 9, 11, 1, 3]          # E major from the tonic

SUBJ = 'B4:8 E5:12 D#5:4 C#5:4 B4:4 A4:4 G#4:2 F#4:2 G#4:4 A4:4 B4:8'
ANSW = 'E4:8 B4:12 A#4:4 G#4:4 F#4:4 E4:4 D#4:2 C#4:2 D#4:4 E4:4 F#4:8'
GUEST = 'E4:16 F#4:8 A4:8 G#4:8 F#4:8 E4:4'          # BWV 878 subject (Fischer / Bach)
GUEST_ANS = 'B3:16 C#4:8 E4:8 D#4:8 C#4:8 B3:4'      # Bach's answer form

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


# ======================================================================
# I. ACCUMULATION: the subject travels round the ring, clockwise
# ======================================================================
theme('A', 1, 1, SUBJ, 'Subject (E), alto, front left: alone, as Spem begins')
put('A', 4, 3, 'G#4:4 E4:4 D#4:4 E4:4 F#4:8 B4:8 G#4:4 F#4:8 B4:8 A#4:4')          # countersubject
theme('T', 4, 3, 'E3:8 B3:12 A#3:4 G#3:4 F#3:4 E3:4 D#3:2 C#3:2 D#3:4 E3:4 F#3:8',
      'Answer (B), tenor, front right')
theme('B', 8, 1, 'B2:8 E3:12 D#3:4 C#3:4 B2:4 A2:4 G#2:2 F#2:2 G#2:4 A2:4 B2:8',
      'Subject (E), bass, back right')
put('T', 8, 1, 'B3:4 A3:4 G#3:4 A3:4 B3:8 E4:8 C#4:4 B3:8 E4:8 D#4:4')             # countersubject


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'IX. Fugue in E major (a 4): Ricercar in circulo',
            'composer': 'Claude / Sam (guest subject: J. S. Bach, BWV 878, after J. C. F. Fischer)',
            'instrument': 'Keyboard - four voices',
            'key': 'E', 'mode': 'major', 'meter': list(METER), 'bpm': 100, 'tempo_text': 'Alla breve, con moto',
            'movement_number': 9, 'number': 9, 'piece_type': 'fugue', 'voice_order': 'high_to_low'}
    voices = [(LONG[i], NAMES[i], CLEF[i], 66) for i in range(len(NAMES))]
    ents = [(LONG[NAMES.index(v)], b, o, l, n) for v, b, o, l, n in ENTRIES]
    return W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ents, subject=SUBJ)


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    build(nb)
    print('bars', nb)
