#!/usr/bin/env python3
"""Checks for XXIV: theme verification against each theme's own prototype, critic summary,
and located problems (optionally restricted to a bar range).

Usage: check.py score.json [--bars a-b] [--quiet]
"""
import argparse, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa
from critic import analyse  # noqa
import xxiv  # noqa


def proto(key):
    if key in ('S', 'I', 'CS1', 'U', 'R'):
        return getattr(xxiv, key)
    return xxiv.GUESTS[key][0]


def proto_notes(key):
    """(pitch, quarters) of a theme prototype, rests dropped, tied notes merged."""
    out, tie = [], False
    for tok in proto(key).split():
        p, dd, sp, t = W.parse_tok(tok)
        if p is None:
            tie = False
            continue
        if tie and out and out[-1][0] == p:
            out[-1] = (p, out[-1][1] + dd)
        else:
            out.append((p, dd))
        tie = t
    return [(p, float(dd / 4)) for p, dd in out]


def verify_themes(d):
    out = []
    for th in d.get('themes', []):
        v = xxiv.NAMES.index(th['voice'])
        evs = sorted(d['voices'][v]['events'], key=lambda e: e['t'])
        k0 = next((k for k, e in enumerate(evs) if e['t'] <= th['t'] + 1e-9 < e['t'] + e['d']), None)
        if k0 is None:
            out.append({'voice': th['voice'], 'beat': th['t'], 'label': th['label'], 'exact': False, 'why': 'no note'})
            continue
        want = [(p + th['semis'], dd * th['scale']) for p, dd in proto_notes(th['key'])]
        if th.get('inverted'):
            ax = want[0][0]; want = [(2 * ax - p, dd) for p, dd in want]
        got = [(e['p'], e['d']) for e in evs[k0:k0 + len(want)]]
        pm = sum(1 for a, b in zip(got, want) if a[0] == b[0])
        # the first note may begin earlier (tied in from the previous phrase); the last may be held longer
        dm = sum(1 for k, (a, b) in enumerate(zip(got, want))
                 if abs(a[1] - b[1]) < 1e-9 or (k == len(want) - 1 and a[1] > b[1])
                 or (k == 0 and evs[k0]['t'] <= th['t'] + 1e-9 and evs[k0]['t'] + evs[k0]['d'] >= th['t'] + b[1] - 1e-9))
        out.append({'voice': th['voice'], 'beat': th['t'], 'label': th['label'], 'pitches': f'{pm}/{len(want)}',
                    'durations': f'{dm}/{len(want)}', 'exact': pm == len(want) and dm == len(want)})
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('score'); ap.add_argument('--bars'); ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    d = json.load(open(a.score))
    bars = tuple(int(x) for x in a.bars.split('-')) if a.bars else None
    R = analyse(d, bars)
    print('summary:', json.dumps(R['summary']))
    th = verify_themes(d)
    bad = [x for x in th if not x['exact']]
    print(f'themes: {len(th)} declared, {len(th) - len(bad)} exact')
    for x in bad:
        print('   NOT EXACT', x)
    if not a.quiet:
        for x in R['parallels']:
            if x['sev'] in ('error', 'warn', 'doubling'):
                print(f"   PAR [{x['sev']}] {x['loc']} {x['voices']} {x['kind']}: {x['what']}")
        for x in R['beat_parallels']:
            print(f"   BEATPAR {x['loc']} {x['voices']} {x['kind']}: {x['what']}")
        for x in R['dissonance']:
            if x['sev'] != 'ok':
                print(f"   DISS [{x['sev']}] {x['loc']} {x['kind']}: {x['what']}")
        for x in R['melody']:
            if x['sev'] == 'warn':
                print(f"   MEL {x['loc']} {x['kind']}: {x['what']}")
        if R['sonority']['low_register_examples']:
            print('   LOW', R['sonority']['low_register_examples'])
        print('   moving/bar:', ' '.join(str(r['moving']) for r in R['texture']))
