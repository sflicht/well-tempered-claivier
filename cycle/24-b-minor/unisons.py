#!/usr/bin/env python3
"""Diagnostic (reports only): per beat, voices sounding vs distinct pitches, and every unison
group ('*' = attacked on that beat).  Usage: unisons.py score.json a-b [--quiet]"""
import json, sys, collections
sys.path.insert(0, '/home/user/well-tempered-claivier/tools')
from chords import pname
d = json.load(open(sys.argv[1])); a, b = (int(x) for x in sys.argv[2].split('-'))
quiet = '--quiet' in sys.argv
V = [(v['abbr'], sorted(v['events'], key=lambda e: e['t'])) for v in d['voices']]
tv = tp = n = 0
for t in [x for x in range((a - 1) * 4, b * 4)]:
    groups = collections.defaultdict(list)
    for nm, evs in V:
        for e in evs:
            if e['t'] <= t < e['t'] + e['d']:
                groups[e['p']].append(nm + ('*' if e['t'] == t else ''))
                break
    nv = sum(len(g) for g in groups.values()); np_ = len(groups)
    tv += nv; tp += np_; n += 1
    if not quiet:
        uni = '; '.join(f"{pname(p)} {'/'.join(g)}" for p, g in sorted(groups.items()) if len(g) > 1)
        print(f"b{t // 4 + 1}.{t % 4 + 1}  voices {nv:2d}  pitches {np_:2d}  {uni}")
print(f"bars {a}-{b}: mean voices {tv / n:.1f}, mean distinct pitches {tp / n:.1f}, ratio {tp / max(1, tv):.2f}")
