#!/usr/bin/env python3
"""Independent checks on the built scores (reads only the JSON files).

I.  table-canon.json: the two-voice score equals itself turned through 180
    degrees: every note (t, d, p) of either voice has a partner in the other
    voice at (T - t - d, d, 124 - p), where 124 = 2 x D4 (the mirror axis).
II. tempo-canon.json: each voice is M with durations x r (r = 4, 3, 2, 1) and
    pitches moved by whole octaves; every voice attacks its last note at the
    same instant and all end together.

    python3 verify_canones.py
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def events(v):
    return sorted((Fraction(str(e['t'])), Fraction(str(e['d'])), int(e['p'])) for e in v['events'])


def check_table():
    data = json.loads((HERE / 'table-canon.json').read_text())
    a, b = (events(v) for v in data['voices'])
    T = max(t + d for t, d, p in a + b)
    rot = lambda evs: sorted((T - t - d, d, 124 - p) for t, d, p in evs)
    ok_ab = rot(a) == b
    ok_ba = rot(b) == a
    # the whole score rotated: voices swap, time reverses, pitch mirrors
    score = {('dux', e) for e in a} | {('comes', e) for e in b}
    rotated = {('comes', e) for e in rot(a)} | {('dux', e) for e in rot(b)}
    print(f'I.  table canon: {len(a)} + {len(b)} notes, T = {T} quarters')
    print(f'    rot(dux) == comes: {ok_ab};  rot(comes) == dux: {ok_ba};  score == rotated score: {score == rotated}')
    # fixed point of the rotation: the centre
    mid = T / 2
    centre = [(t, d, p) for t, d, p in a if t < mid < t + d]
    print(f'    note(s) spanning the centre (t = {mid}): dux {centre}, comes '
          f'{[(t, d, p) for t, d, p in b if t < mid < t + d]}  (62 = D4, the axis)')
    return ok_ab and ok_ba and score == rotated


def check_tempo():
    data = json.loads((HERE / 'tempo-canon.json').read_text())
    m = data['canon']['melody'].split()
    import re
    NAT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    def midi(name):
        L, acc, o = re.fullmatch(r'([A-G])(#*|b*)(-?\d)', name).groups()
        return 12 * (int(o) + 1) + NAT[L] + acc.count('#') - acc.count('b')
    mp = [midi(t.split(':')[0]) for t in m]
    md = [Fraction(t.split(':')[1]) / 4 for t in m]          # quarters
    ratio = {'S': 1, 'A': 2, 'T': 3, 'B': 4}
    ok = True
    last_onsets, ends = set(), set()
    print('II. tempo canon:')
    for v in data['voices']:
        ev = events(v)
        r = ratio[v['abbr']]
        ps = [p for _, _, p in ev]
        shift = ps[0] - mp[0]
        same_pitch = shift % 12 == 0 and all(p - q == shift for p, q in zip(ps, mp)) and len(ps) == len(mp)
        durs = [d for _, d, _ in ev]
        same_rhythm = all(d == r * q for d, q in zip(durs[:-1], md[:-1]))
        contiguous = all(ev[i][0] + ev[i][1] == ev[i + 1][0] for i in range(len(ev) - 1))
        last_onsets.add(ev[-1][0])
        ends.add(ev[-1][0] + ev[-1][1])
        print(f'    {v["abbr"]}: x{r}, octave shift {shift:+d}, enters at {ev[0][0]} q, pitches==M: {same_pitch}, '
              f'durations==M x{r}: {same_rhythm}, no gaps: {contiguous}')
        ok &= same_pitch and same_rhythm and contiguous
    print(f'    last-note attacks: {sorted(last_onsets)}; ends: {sorted(ends)}  -> convergence: {len(last_onsets) == 1 and len(ends) == 1}')
    return ok and len(last_onsets) == 1 and len(ends) == 1


if __name__ == '__main__':
    good = check_table() & check_tempo()
    print('ALL CHECKS PASSED' if good else 'CHECK FAILED')
    sys.exit(0 if good else 1)
