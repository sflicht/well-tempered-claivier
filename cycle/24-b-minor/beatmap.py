#!/usr/bin/env python3
"""Diagnostic: for each beat, the sounding pitches low->high with their voices ('*' attacked).
Usage: beatmap.py score.json a-b"""
import json, sys, collections
sys.path.insert(0, '/home/user/well-tempered-claivier/tools')
from chords import pname
d = json.load(open(sys.argv[1])); a, b = (int(x) for x in sys.argv[2].split('-'))
V = [(v['abbr'], sorted(v['events'], key=lambda e: e['t'])) for v in d['voices']]
for t in range((a - 1) * 4, b * 4):
    g = collections.defaultdict(list)
    for nm, evs in V:
        for e in evs:
            if e['t'] <= t < e['t'] + e['d']:
                g[e['p']].append(nm + ('*' if e['t'] == t else ''))
                break
    print(f"b{t//4+1}.{t%4+1} [{sum(map(len,g.values()))}/{len(g)}] " + '  '.join(f"{pname(p)}:{'/'.join(v)}" for p, v in sorted(g.items())))
