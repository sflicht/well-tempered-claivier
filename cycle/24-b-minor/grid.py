#!/usr/bin/env python3
"""Print a voice x eighth (or sixteenth) grid of a bar range: pitch at attack, '-' when held, '.' rest."""
import json, sys
sys.path.insert(0, '/home/user/well-tempered-claivier/tools')
from chords import pname
d = json.load(open(sys.argv[1])); a, b = (int(x) for x in sys.argv[2].split('-'))
step = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
for v in d['voices']:
    cells = []
    t = (a - 1) * 4.0
    while t < b * 4.0 - 1e-9:
        cell = '.'
        for e in v['events']:
            if e['t'] <= t + 1e-9 < e['t'] + e['d']:
                cell = pname(e['p']) if abs(e['t'] - t) < 1e-9 else ('~' if e['t'] < t else '.')
                break
            if t < e['t'] < t + step - 1e-9:
                cell = pname(e['p']) + '*'
        cells.append(f'{cell:5s}')
        if abs((t + step) % 4) < 1e-9:
            cells.append('|')
        t += step
    print(f"{v['abbr']:4s}", ''.join(cells))
