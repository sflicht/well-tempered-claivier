"""Search/inspection lab for Fugue VI a 4 (writes no notes)."""
from __future__ import annotations
import sys
from fractions import Fraction
from pathlib import Path
ROOT = Path('/home/user/well-tempered-claivier')
sys.path.insert(0, str(ROOT / 'tools'))
import wtclib  # noqa
from critic import analyse  # noqa
from chords import pname  # noqa

SUBJECT = 'A4:8 Bb4:4 B4:4 C5:2 C#5:2 D5:6 C#5:2 E5:4 D5:12 A5:4'
GROUND = 'D3:16 C#3:8 C3:8 B2:4 Bb2:4 A2:12 Bb2:4 G2:8 A2:24 D2:8'
INV = 'D5:8 C#5:4 C5:4 B4:2 Bb4:2 A4:6 Bb4:2 G4:4 A4:12 D4:4'


def notes(tokens, start16=0, shift=0, scale=1):
    out, u = [], Fraction(start16)
    for tok in tokens.split():
        p, d, sp, tie = wtclib.parse_tok(tok)
        d = d * Fraction(scale)
        if p is not None:
            out.append((u, d, p + shift))
        u += d
    return out


def at(nl, t):
    for s, d, p in nl:
        if s <= t < s + d:
            return p, s == t
    return None


def cons_cost(lines, lo, hi, step=2):
    """Beat-weighted dissonance cost over all pairs; bass = lowest sounding.
    Returns (cost, list of bad spots)."""
    cost = 0.0
    bad = []
    t = lo
    while t < hi:
        snd = [(at(nl, t), k) for k, nl in enumerate(lines)]
        snd = [(r[0], r[1], k) for r, k in snd if r is not None]
        if len(snd) >= 2:
            w = 3 if t % 12 == 0 else (2 if t % 4 == 0 else 0.7)
            ps = sorted(snd)
            bass = ps[0][0]
            for i in range(len(ps)):
                for j in range(i + 1, len(ps)):
                    a, b = ps[i], ps[j]
                    if not (a[1] or b[1]):
                        continue
                    ic = (b[0] - a[0]) % 12
                    c = 0
                    if ic in (1, 11):
                        c = 3
                    elif ic in (2, 10):
                        c = 1.5
                    elif ic == 6:
                        c = 0.8
                    elif ic == 5 and a[0] == bass:
                        c = 1.0
                    if b[0] - a[0] <= 0:
                        c += 0.5
                    if c:
                        cost += c * w
                        if c * w >= 3:
                            bad.append((loc(t), pname(a[0], True), pname(b[0], True)))
        t += step
    return cost, bad


def loc(t):
    t = Fraction(t)
    return f"b{int(t // 12) + 1}.{float((t % 12) / 4 + 1):g}"


def data_of(lines, meter=(3, 4), bpm=76):
    vs = []
    for k, nl in enumerate(lines):
        vs.append({'name': f'V{k+1}', 'abbr': f'V{k+1}',
                   'events': [{'t': float(s / 4), 'd': float(d / 4), 'p': int(p)} for s, d, p in sorted(nl)]})
    return {'metadata': {'meter': list(meter), 'bpm': bpm, 'key': 'D', 'mode': 'minor'}, 'voices': vs}


def grid(lines, start16, end16, step=4):
    t = start16
    while t < end16:
        row = []
        for nl in lines:
            r = at(nl, t)
            row.append('  .  ' if r is None else (pname(r[0], True) + ('*' if r[1] else ' ')).ljust(5))
        print(f"{loc(t):<8}", ' '.join(row))
        t += step
