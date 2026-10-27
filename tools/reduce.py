#!/usr/bin/env python3
"""Print a beat-by-beat harmonic reduction of an event score: bass, chord, top.

Usage: reduce.py score.json [--per bar|beat|half]
"""
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from critic import Score, TPQ  # noqa
from chords import name_chord, pname  # noqa
import collections

ap = argparse.ArgumentParser(); ap.add_argument('score'); ap.add_argument('--per', default='beat')
a = ap.parse_args()
S = Score(json.load(open(a.score)))
step = {'beat': S.beat, 'half': S.bar // 2, 'bar': S.bar}[a.per]
line = []
for b in range(S.nbars):
    cells = []
    for t in range(b * S.bar, (b + 1) * S.bar, step):
        w = collections.Counter(); lows = []; highs = []
        for v in S.voices:
            for n in v:
                if n['s'] < t + step and n['e'] > t:
                    w[n['p'] % 12] += min(n['e'], t + step) - max(n['s'], t)
                    lows.append(n['p']); highs.append(n['p'])
        if not w:
            cells.append('  --  '); continue
        keep = {pc for pc, x in w.items() if x >= step * 0.2}
        bass = min(lows)
        nm = name_chord(keep, bass % 12, S.flats) or name_chord({pc for pc, x in w.most_common(3)}, bass % 12, S.flats) or '?' + ''.join(str(x) for x in sorted(keep))
        cells.append(f"{nm}[{pname(bass, S.flats)}^{pname(max(highs), S.flats)}]")
    print(f"b{b+1:<3}", ' | '.join(cells))
