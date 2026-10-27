#!/usr/bin/env python3
"""Build the score and report critic findings around given links/bars.

usage: check.py [L3 L12 ... | 20-28 | all]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / 'tools'))
sys.path.insert(0, str(HERE))
from critic import analyse, Score  # noqa: E402
import source  # noqa: E402


def fourths(data, lo, hi):
    """4th against the bass at quarter-beat onsets (the strict check)."""
    S = Score(data)
    out = []
    for t in S.onsets:
        if t % S.beat or not (lo <= t // S.bar + 1 <= hi):
            continue
        items = sorted((S.note(i, k)['p'], i, att) for i, (k, att) in S.sounding(t).items())
        if len(items) < 2:
            continue
        b = items[0]
        for p, i, att in items[1:]:
            if (p - b[0]) % 12 == 5 and (att or b[2]):
                out.append(f"{S.loc(t)} {S.names[b[1]]}/{S.names[i]}")
    return out


def report(data, lo, hi, tag=''):
    R = analyse(data, (lo, hi))
    bad = []
    for x in R['parallels']:
        if x['sev'] in ('error', 'warn'):
            bad.append(f"PAR[{x['sev']}] {x['loc']} {x['voices']} {x['kind']} {x['what']}")
    for x in R['beat_parallels']:
        bad.append(f"BEATPAR {x['loc']} {x['voices']} {x['kind']} {x['what']}")
    for x in R['dissonance']:
        if x['sev'] == 'error':
            bad.append(f"DIS {x['loc']} {x['kind']} {x['what']}")
        elif x['sev'] == 'note':
            bad.append(f"  7th {x['loc']} {x['what']}")
    for x in R['melody']:
        if x['sev'] == 'warn':
            bad.append(f"  MEL {x['loc']} {x['kind']} {x['what']}")
    for x in R['direct']:
        bad.append(f"  DIRECT {x['loc']} {x['what']}")
    low = [l for l in R['sonority']['low_register_examples'] if lo <= int(l[1:].split('.')[0]) <= hi]
    if low:
        bad.append(f"  LOW {low}")
    f4 = fourths(data, lo, hi)
    if f4:
        bad.append(f"  4TH-vs-bass {f4}")
    print(f"[{tag} bars {lo}-{hi}] " + ('clean' if not bad else ''))
    for b in bad:
        print('   ', b)


if __name__ == '__main__':
    data, tags, rows = source.build()
    args = sys.argv[1:] or ['all']
    for a in args:
        if a == 'all':
            report(data, 1, len(tags), 'all')
        elif a.startswith('L'):
            k = int(a[1:])
            idx = [i for i, t in enumerate(tags) if t == f'L{k}']
            if not idx:
                print(a, 'no such link')
                continue
            report(data, idx[0], idx[-1] + 2, a)
        elif a == 'coda':
            idx = [i for i, t in enumerate(tags) if t == 'coda']
            report(data, idx[0] - 1, idx[-1] + 1, a)
        else:
            lo, hi = map(int, a.split('-'))
            report(data, lo, hi, a)
