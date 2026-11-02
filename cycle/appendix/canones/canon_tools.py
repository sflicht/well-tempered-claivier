"""Shared helpers for the two appendix canons (derivation, verification, reports).

Nothing here chooses notes.  The functions apply named, explicit canonic
transformations (retrograde, inversion, rhythmic scaling) to lines written by
hand, check the result, and print what a composer needs to judge it.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'tools'))

import wtclib as W  # noqa: E402
from critic import analyse  # noqa: E402
from chords import pname  # noqa: E402

C_MAJOR = [0, 2, 4, 5, 7, 9, 11]


def flatten(bars):
    """Bar strings -> one token string with ties merged into single notes."""
    out = []
    pend = None  # [name, dur]
    for bar in bars:
        for tok in bar.split():
            name, d = tok.rsplit(':', 1)
            tie = d.endswith('~')
            d = Fraction(d.rstrip('~'))
            if pend is not None:
                if pend[0] != name:
                    raise ValueError(f'tie from {pend[0]} into {name}')
                pend[1] += d
            else:
                pend = [name, d]
            if not tie:
                out.append(f'{pend[0]}:{pend[1]}')
                pend = None
    if pend is not None:
        raise ValueError('dangling tie at end')
    return ' '.join(out)


def rinv(stream, axis='D4', scale=C_MAJOR):
    """Retrograde inversion of a flattened token stream (the table-canon rule)."""
    return W.retrograde(W.invert_diatonic(stream, axis, scale))


def notes(stream):
    """[(onset, dur, midi or None, name)] in sixteenths."""
    t = Fraction(0)
    res = []
    for tok in stream.split():
        p, d, sp, tie = W.parse_tok(tok)
        res.append((t, d, p, tok.rsplit(':', 1)[0]))
        t += d
    return res


def length(stream):
    return sum(W.parse_tok(t)[1] for t in stream.split())


def check_rotation(v1_stream, v2_stream, axis_midi=62):
    """Verify that the two-voice score equals itself turned through 180 degrees:
    every note (t, d, p) of either voice appears in the other voice at
    (T - t - d, d, 2*axis - p).  Returns a list of mismatches (empty = proof)."""
    a, b = notes(v1_stream), notes(v2_stream)
    T = length(v1_stream)
    if T != length(v2_stream):
        return [f'lengths differ {T} vs {length(v2_stream)}']
    bad = []
    for src, dst, nm in ((a, b, 'v1->v2'), (b, a, 'v2->v1')):
        index = {(t, d): p for t, d, p, _ in dst}
        for t, d, p, name in src:
            key = (T - t - d, d)
            if key not in index:
                bad.append(f'{nm}: no partner for {name} at {t}')
                continue
            q = index[key]
            exp = None if p is None else 2 * axis_midi - p
            if q != exp:
                bad.append(f'{nm}: {name} at {t} expects {exp}, found {q}')
    return bad


def short_report(data, show=('parallels', 'dissonance', 'melody'), limit=40):
    R = analyse(data)
    print('summary:', R['summary'])
    print('ranges:', R['ranges'])
    n = 0
    if 'parallels' in show:
        for x in R['parallels']:
            if x['sev'] in ('error', 'warn', 'doubling'):
                print(f"  PAR [{x['sev']}] {x['loc']} {x['voices']} {x['kind']}: {x['what']}")
    if 'parallels' in show:
        for x in R.get('beat_parallels', []):
            print(f"  BPAR {x['loc']} {x['voices']} {x['kind']}: {x['what']}")
    if 'dissonance' in show:
        for x in R['dissonance']:
            if x['sev'] != 'ok' and n < limit:
                print(f"  DIS [{x['sev']}] {x['loc']} {x['kind']}: {x['what']}")
                n += 1
    if 'melody' in show:
        for x in R['melody']:
            if x['sev'] == 'warn':
                print(f"  MEL {x['loc']} {x['kind']}: {x['what']}")
    return R


IV_NAMES = {0: 'P1', 1: 'm2', 2: 'M2', 3: 'm3', 4: 'M3', 5: 'P4', 6: 'TT', 7: 'P5', 8: 'm6', 9: 'M6', 10: 'm7', 11: 'M7'}


def dyad_grid(v1_stream, v2_stream, units_per_bar, step=4, bars=None):
    """Print, per beat, the two sounding pitches and their interval class."""
    A, B = notes(v1_stream), notes(v2_stream)

    def at(ns, t):
        for o, d, p, nm in ns:
            if o <= t < o + d:
                return p, nm, o == t
        return None, '-', False
    T = length(v1_stream)
    nb = int(T // units_per_bar)
    for b in range(nb):
        if bars and not (bars[0] <= b + 1 <= bars[1]):
            continue
        cells = []
        t = Fraction(b * units_per_bar)
        while t < (b + 1) * units_per_bar:
            p, n1, a1 = at(A, t)
            q, n2, a2 = at(B, t)
            iv = IV_NAMES[abs(p - q) % 12] if p is not None and q is not None else '..'
            cells.append(f"{n1.replace(':', '')}{'*' if a1 else ' '}/{n2}{'*' if a2 else ' '} {iv}")
            t += step
        print(f'b{b + 1:<3}', ' | '.join(f'{c:<18}' for c in cells))


def sixteenth_rule(v1_stream, v2_stream, beat=4, bars=None, units_per_bar=12):
    """Table-canon dissonance rule.  Under rotation a sixteenth at position k of
    a beat moves to position 3-k, so only positions 1 and 2 may carry
    dissonance.  Report every beat whose position 0 or 3 is dissonant (P4
    against the lower voice counts as dissonant in two parts)."""
    A, B = notes(v1_stream), notes(v2_stream)

    def at(ns, t):
        for o, d, p, nm in ns:
            if o <= t < o + d:
                return p, nm
        return None, '-'
    T = length(v1_stream)
    out = []
    t = Fraction(0)
    while t < T:
        b = int(t // units_per_bar) + 1
        if not bars or bars[0] <= b <= bars[1]:
            for pos in (0, 3):
                p, n1 = at(A, t + pos)
                q, n2 = at(B, t + pos)
                if p is None or q is None:
                    continue
                iv = abs(p - q) % 12
                if iv in (1, 2, 5, 6, 10, 11):
                    out.append(f'b{b}.{(t % units_per_bar) / beat + 1} pos{pos}: {n1}/{n2} {IV_NAMES[iv]}')
        t += beat
    return out
