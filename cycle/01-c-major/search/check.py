#!/usr/bin/env python3
"""Run the strict two-voice evaluator (ladder.pair_cost, 32nd grid) over the
built score and list every flagged spot with its bar location.
Usage: check.py ../fugue.json [--min 4]"""
import json, sys
import ladder
ladder.RES = 2
from ladder import pair_cost
data = json.load(open(sys.argv[1]))
mn = float(sys.argv[sys.argv.index('--min') + 1]) if '--min' in sys.argv else 4
def line(v):
    return [(round(e['t'] * 8), round((e['t'] + e['d']) * 8), 0, e['p']) for e in v['events']]
A, B = line(data['voices'][0]), line(data['voices'][1])
c, why = pair_cost(A, B, True)
print(f'total cost {c:.1f}')
NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
for t, w in sorted(why):
    if w.startswith('diss'):
        cc = float(w.split('c')[-1])
        if cc < mn:
            continue
    six = t / 2
    print(f'  b{int(six // 16) + 1}.{(six % 16) / 4 + 1:g}  {w}')
