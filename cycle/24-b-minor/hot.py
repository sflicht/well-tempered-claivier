#!/usr/bin/env python3
"""List, per onset, voices that move together between the same pitch classes (octave-parallel risk)
or into/out of fifths together.  Usage: hot.py score.json a-b"""
import json, sys, collections
sys.path.insert(0, '/home/user/well-tempered-claivier/tools')
from chords import pname
d = json.load(open(sys.argv[1])); a, b = (int(x) for x in sys.argv[2].split('-'))
V = [(v['abbr'], sorted(v['events'], key=lambda e: e['t'])) for v in d['voices']]
times = sorted({e['t'] for _, evs in V for e in evs if (a - 1) * 4 <= e['t'] < b * 4})
def at(evs, t):
    for k, e in enumerate(evs):
        if e['t'] <= t < e['t'] + e['d']:
            return k
for t in times:
    moves = collections.defaultdict(list)
    for nm, evs in V:
        k = at(evs, t)
        if k is None or evs[k]['t'] != t or k == 0:
            continue
        p0 = evs[k - 1]; p1 = evs[k]
        if p1['t'] - (p0['t'] + p0['d']) > 1 or p0['p'] == p1['p']:
            continue
        moves[(p0['p'] % 12, p1['p'] % 12)].append(f"{nm}:{pname(p0['p'])}>{pname(p1['p'])}")
    bad = {k: v for k, v in moves.items() if len(v) > 1}
    if bad:
        bar = int(t // 4) + 1; beat = t % 4 + 1
        print(f"b{bar}.{beat:g}", '; '.join(' & '.join(v) for v in bad.values()))
