"""Search helpers for Fugue III (C-sharp major gigue).

Proposes placements of hand-written lines; never writes notes itself.
Lines are wtclib token strings in sixteenths.  Transformations are the
explicit ones a composer uses: diatonic transposition, diatonic mirror
around an axis note, time shift.  Scoring calls tools/critic.py analyse().
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
import wtclib  # noqa: E402
from critic import analyse  # noqa: E402

BAR = 24
CSHARP = [1, 3, 5, 6, 8, 10, 0]          # C# major, from the tonic
GSHARP = [8, 10, 0, 1, 3, 5, 7]          # G# major
LET = 'CDEFGAB'


def notes(tok, start=0):
    """token string -> [(start16, dur16, pitch, letter)] ; rests skipped; ties merged."""
    out, u = [], Fraction(start)
    pend = None
    for t in tok.split():
        p, d, sp, tie = wtclib.parse_tok(t)
        if p is not None:
            if pend is not None and pend[2] == p and pend[0] + pend[1] == u:
                pend = (pend[0], pend[1] + d, p, pend[3])
            else:
                if pend is not None:
                    out.append(pend)
                pend = (u, d, p, sp[0].upper())
            if not tie:
                out.append(pend)
                pend = None
        u += d
    if pend is not None:
        out.append(pend)
    return out


def length(tok):
    return sum(wtclib.parse_tok(t)[1] for t in tok.split())


def deg(p, scale=CSHARP):
    t = scale[0]
    pc = p % 12
    if pc not in scale:
        return None
    return ((p - t) // 12) * 7 + scale.index(pc)


def pitch_of(j, scale=CSHARP):
    t = scale[0]
    return t + (j // 7) * 12 + ((scale[j % 7] - t) % 12)


def name(p, letter):
    return wtclib.name_of(p, letter)


def dshift(tok, steps, scale=CSHARP):
    """Diatonic transposition of a token string by `steps` scale degrees."""
    out = []
    for t in tok.split():
        p, d, sp, tie = wtclib.parse_tok(t)
        dur = t.rsplit(':', 1)[1]
        if p is None:
            out.append(t)
            continue
        j = deg(p, scale)
        L = LET[(LET.index(sp[0].upper()) + steps) % 7]
        if j is None:  # chromatic note: move by the same letter distance, keep alteration pattern
            q = p + round(steps * 12 / 7)
        else:
            q = pitch_of(j + steps, scale)
        out.append(f"{name(q, L)}:{dur}")
    return ' '.join(out)


def mirror(tok, axis, scale=CSHARP):
    return wtclib.invert_diatonic(tok, axis, scale)


def shift_time(tok, units):
    """Prepend a rest (units>0)."""
    if units == 0:
        return tok
    return f"R:{units} " + tok


def data_for(lines, meter=(12, 8), bpm=150, names=None):
    """lines: list of (token string, start16).  Voices ordered by mean pitch, high first."""
    vs = []
    for k, (tok, st) in enumerate(lines):
        ns = notes(tok, st)
        if not ns:
            continue
        mean = sum(p for _, _, p, _ in ns) / len(ns)
        vs.append((mean, k, ns))
    vs.sort(key=lambda x: -x[0])
    voices = []
    for mean, k, ns in vs:
        nm = names[k] if names else f'V{k}'
        voices.append({'name': nm, 'abbr': nm, 'events': [
            {'t': float(s / 4), 'd': float(d / 4), 'p': int(p)} for s, d, p, _ in ns]})
    return {'metadata': {'meter': list(meter), 'bpm': bpm, 'key': 'C#', 'mode': 'major'}, 'voices': voices}


def score(lines, window=None, names=None, verbose=False):
    data = data_for(lines, names=names)
    R = analyse(data)
    s = R['summary']
    if window:
        lo, hi = window
        keep = lambda x: lo <= x['t'] / 48 * 4 < hi  # ticks->sixteenths
        par = [x for x in R['parallels'] if keep(x)]
        dis = [x for x in R['dissonance'] if keep(x)]
        bp = [x for x in R['beat_parallels'] if keep(x)]
    else:
        par, dis, bp = R['parallels'], R['dissonance'], R['beat_parallels']
    pe = sum(1 for x in par if x['sev'] == 'error')
    pw = sum(1 for x in par if x['sev'] in ('warn', 'doubling'))
    un = sum(1 for x in dis if x['sev'] == 'error')
    bpar = len(bp)
    cost = 20 * pe + 8 * un + 5 * bpar + 3 * pw + 2 * s['crossings'] + 2 * s['low_register_seconds'] \
        + (100 - s['tertian_fit_pct']) / 10
    if verbose:
        for x in par:
            if x['sev'] != 'note':
                print('   par', x['loc'], x['voices'], x['kind'], x['what'])
        for x in bp:
            print('   bpar', x['loc'], x['voices'], x['kind'], x['what'])
        for x in dis:
            if x['sev'] != 'ok':
                print('   dis', x['loc'], x['kind'], x['what'])
        if R['crossing']:
            print('   cross', [(x['loc'], x['what']) for x in R['crossing']])
        print('   harmony', ' '.join(str(h) for h in R['harmony']['labels']))
    return round(cost, 1), {'pe': pe, 'pw': pw, 'un': un, 'bp': bpar, 'x': s['crossings'],
                            'low': s['low_register_seconds'], 'fit': s['tertian_fit_pct']}, R


C4DEG = 35  # degree index of C#4 in C# major


def dname(j, scale=CSHARP):
    """Name of C#-major degree j (0 = C#4)."""
    q = pitch_of(C4DEG + j, scale)
    return name(q, 'CDEFGAB'[(j + (0 if scale is CSHARP else 4)) % 7])


PC = ['C', 'C#', 'D', 'D#', 'E', 'E#', 'F#', 'G', 'G#', 'A', 'A#', 'B#']
IV = {0: 'P8', 1: 'm2', 2: 'M2', 3: 'm3', 4: 'M3', 5: 'P4', 6: 'TT', 7: 'P5', 8: 'm6', 9: 'M6', 10: 'm7', 11: 'M7'}


def at(ns, t):
    for s, d, p, L in ns:
        if s <= t < s + d:
            return (p, s == t)
    return None


def grid(lines, start=0, end=None, step=2, labels=None):
    """Print the lines on an eighth-note grid with the interval of every voice to the lowest."""
    nss = [notes(tok, st) for tok, st in lines]
    if end is None:
        end = max(s + d for ns in nss for s, d, p, L in ns)
    rows = []
    for t in range(int(start), int(end), step):
        cells = []
        sound = []
        for ns in nss:
            x = at(ns, t)
            if x:
                p, att = x
                cells.append(f"{PC[p % 12]}{p // 12 - 1}{'' if att else '~'}".ljust(5))
                sound.append(p)
            else:
                cells.append('.    ')
        lo = min(sound) if sound else None
        ivs = ' '.join(IV[(p - lo) % 12] for p in sound if p != lo) if lo is not None else ''
        bar, u = divmod(t, BAR)
        mark = '|' if u == 0 else (':' if u % 6 == 0 else ' ')
        rows.append(f"{mark}{bar + 1:>3}.{u:<2} " + ' '.join(cells) + '  ' + ivs)
    print('\n'.join(rows))
