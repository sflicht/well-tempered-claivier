"""Small analysis lab for Pair VI (search and inspection only; it writes no notes).

Lines are hand-written token strings (wtclib format).  Helpers place them in
time, transpose them chromatically (exact intervals, so the chromatic ground
and subject stay themselves), and score combinations with tools/critic.py.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
import wtclib  # noqa: E402
from critic import analyse  # noqa: E402
from chords import pname  # noqa: E402

# The two themes, as composed (see NOTES.md).  Units: sixteenths.
SUBJECT = 'A4:8 Bb4:4 B4:6 C5:2 C#5:4 D5:6 C#5:2 E5:4 D5:8 A5:4'
GROUND = 'D3:16 C#3:8 C3:12 B2:4 Bb2:8 A2:12 Bb2:4 G2:8 A2:16 D2:8'


def notes(tokens, start16=0, shift=0, scale=1):
    """tokens -> [(start16, dur16, pitch)], rests skipped."""
    out, u = [], Fraction(start16)
    for tok in tokens.split():
        p, d, sp, tie = wtclib.parse_tok(tok)
        d = d * Fraction(scale)
        if p is not None:
            out.append((u, d, p + shift))
        u += d
    return out


def invert(nl, axis):
    return [(s, d, 2 * axis - p) for s, d, p in nl]


def data_of(lines, meter=(3, 4), bpm=63):
    vs = []
    for k, nl in enumerate(lines):
        vs.append({'name': f'V{k+1}', 'abbr': f'V{k+1}',
                   'events': [{'t': float(s / 4), 'd': float(d / 4), 'p': int(p)} for s, d, p in sorted(nl)]})
    return {'metadata': {'meter': list(meter), 'bpm': bpm, 'key': 'D', 'mode': 'minor'}, 'voices': vs}


def pair_cost(a, b, meter=(3, 4)):
    """Critic-based cost of two lines sounding together (only where both sound)."""
    lo = max(min(s for s, _, _ in a), min(s for s, _, _ in b))
    hi = min(max(s + d for s, d, _ in a), max(s + d for s, d, _ in b))
    if hi <= lo:
        return None
    def clip(nl):
        out = []
        for s, d, p in nl:
            e = s + d
            s2, e2 = max(s, lo), min(e, hi)
            if e2 > s2:
                out.append((s2, e2 - s2, p))
        return out
    A, B = clip(a), clip(b)
    hiL, loL = (A, B) if sum(p for *_, p in A) / len(A) >= sum(p for *_, p in B) / len(B) else (B, A)
    R = analyse(data_of([hiL, loL], meter))
    s = R['summary']
    harsh = sum(1 for x in R['dissonance'] if x['sev'] == 'error')
    # consonance of the two lines on every beat (perfect 4th counts as dissonant against a lower line)
    beat = 4
    t = (lo // beat) * beat
    bad = 0
    nbeats = 0
    def at(nl, t):
        for s, d, p in nl:
            if s <= t < s + d:
                return p
        return None
    while t < hi:
        x, y = at(hiL, t), at(loL, t)
        if x is not None and y is not None:
            nbeats += 1
            iv = (x - y) % 12
            if iv in (1, 2, 10, 11):
                bad += 1
            elif iv == 5:
                bad += 0.5
            elif iv == 6:
                bad += 0.3
        t += beat
    cost = 10 * s['parallels_error'] + 4 * s['beat_parallels'] + 6 * harsh + 2 * s['parallels_weak'] + 3 * bad
    return {'cost': round(cost, 1), 'par': s['parallels_error'], 'bpar': s['beat_parallels'], 'harsh': harsh,
            'bad_beats': bad, 'beats': nbeats}


def grid(lines, start16, end16, step=4, names=None):
    """Print the sounding pitches of every line at each step (default: beat)."""
    def at(nl, t):
        for s, d, p in nl:
            if s <= t < s + d:
                return p, s == t
        return None
    t = start16
    while t < end16:
        row = []
        for nl in lines:
            r = at(nl, t)
            row.append('  .  ' if r is None else (pname(r[0], True) + ('*' if r[1] else ' ')).ljust(5))
        bar = int(t // 12) + 1
        beat = (t % 12) / 4 + 1
        print(f"b{bar:<3}{beat:<5g}", ' '.join(row))
        t += step
