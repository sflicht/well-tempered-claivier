"""Derivation and checking for the canon per tempora.

One melody M (token string, sixteenth units, as sung by the fastest voice).
Voice k sings M with every duration multiplied by RATIO[k] (an explicit
wtclib.scale_rhythm), transposed by octaves, and starts late enough that its
last note is attacked at the same instant as everyone else's: the punctum
convergentiae.  That last note is a fermata of equal length in all voices
and is outside the proportional scheme.
"""
from __future__ import annotations

import collections
from fractions import Fraction

from canon_tools import W, notes, length, IV_NAMES
from critic import analyse
from chords import name_chord, pname

METER = (6, 4)
BAR = 24  # sixteenths per 6/4 bar


def split_last(m):
    toks = m.split()
    return ' '.join(toks[:-1]), toks[-1]


def derive(m, voices, fermata=24):
    """voices: [(name, abbr, clef, ratio, semitones, letters)] slowest first.
    Returns ({name: bar strings}, total_units_before_fermata, {name: stream})."""
    body, last = split_last(m)
    L = length(body)
    rmax = max(v[3] for v in voices)
    T = rmax * L
    if T % BAR:
        raise ValueError(f'convergence at {T} is not on a barline (L={L})')
    out, streams = {}, {}
    for name, abbr, clef, r, semis, letters in voices:
        start = T - r * L
        scaled = W.scale_rhythm(body, r)                    # augmentation by r
        moved = W.transpose(scaled, semis, letters)         # octave placement
        lastname = W.transpose(last.rsplit(':', 1)[0] + ':1', semis, letters).rsplit(':', 1)[0]
        stream = (f'R:{start} ' if start else '') + moved + f' {lastname}:{fermata}'
        streams[name] = stream
        out[name] = W.concat_bars(stream, METER)
    return out, T, streams


def sonorities(streams, T, step=4):
    """Pitch content every `step` sixteenths: list of (t, [(voice, midi, attacked)])."""
    ns = {k: notes(s) for k, s in streams.items()}
    res = []
    t = Fraction(0)
    while t <= T:
        cur = []
        for k, lst in ns.items():
            for o, d, p, nm in lst:
                if o <= t < o + d and p is not None:
                    cur.append((k, p, o == t))
        res.append((t, cur))
        t += step
    return res


def chord_grid(streams, T, names, step=4, bars=None):
    for t, cur in sonorities(streams, T, step):
        b = int(t // BAR) + 1
        if bars and not (bars[0] <= b <= bars[1]):
            continue
        if t % BAR == 0:
            print()
            print(f'b{b:<3}', end='')
        ps = sorted(p for _, p, _ in cur)
        if not ps:
            print(' | --', end='')
            continue
        nm = name_chord({p % 12 for p in ps}, ps[0] % 12) or '?'
        bymv = {k: (p, a) for k, p, a in cur}
        cell = ' '.join((pname(bymv[n][0]) + ('*' if bymv[n][1] else '')) if n in bymv else '.' for n in names)
        print(f' | {cell} [{nm}]', end='')
    print()


def report(data, limit=60):
    R = analyse(data)
    print('summary:', R['summary'])
    print('ranges:', R['ranges'])
    for x in R['parallels']:
        if x['sev'] in ('error', 'warn', 'doubling'):
            print(f"  PAR [{x['sev']}] {x['loc']} {x['voices']} {x['kind']}: {x['what']}")
    for x in R.get('beat_parallels', []):
        print(f"  BPAR {x['loc']} {x['voices']} {x['kind']}: {x['what']}")
    n = 0
    for x in R['dissonance']:
        if x['sev'] != 'ok' and n < limit:
            print(f"  DIS [{x['sev']}] {x['loc']} {x['kind']}: {x['what']}")
            n += 1
    for x in R['melody']:
        if x['sev'] == 'warn':
            print(f"  MEL {x['loc']} {x['kind']}: {x['what']}")
    return R


def partner_map(durs, ratios, strong_every=4):
    """durs: durations of M's notes before the final note (sixteenths).
    For every beat (multiple of strong_every) at which some voice attacks,
    record which note index each voice is sounding.  Returns
    {i: Counter(j: weight)} with weight 2 at dotted-half beats, 1 otherwise."""
    L = sum(durs)
    rmax = max(ratios)
    T = rmax * L
    starts = []
    acc = 0
    for d in durs:
        starts.append(acc)
        acc += d
    import bisect

    def idx(r, t):
        s = T - r * L
        if t < s:
            return None
        x = Fraction(t - s, r)
        k = bisect.bisect_right(starts, x) - 1
        return k
    pm = collections.defaultdict(collections.Counter)
    for t in range(0, T, strong_every):
        cur = [(r, idx(r, t)) for r in ratios]
        cur = [(r, k) for r, k in cur if k is not None]
        w = 2 if t % 12 == 0 else 1
        for a in range(len(cur)):
            for b in range(len(cur)):
                if a != b:
                    pm[cur[a][1]][cur[b][1]] += w
    return pm
