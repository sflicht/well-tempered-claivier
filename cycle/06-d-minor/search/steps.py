"""Melodic profile per voice and per bar range (analysis only).
Usage: steps.py score.json [LO-HI]"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from critic import Score
from chords import pname
d = json.load(open(sys.argv[1]))
S = Score(d)
lo, hi = (1, 999)
if len(sys.argv) > 2:
    lo, hi = map(int, sys.argv[2].split('-'))
# theme spans per voice (ticks)
bq = S.bar // 3 if False else None
spans = {}
for e in d.get('subject_entries', []):
    pass
tot = st = 0
rows = []
for i, v in enumerate(S.voices):
    n = s = 0
    leaps = []
    for a, b in zip(v, v[1:]):
        if b['s'] - a['e'] > S.beat:
            continue
        bar = b['s'] // S.bar + 1
        if not (lo <= bar <= hi):
            continue
        iv = abs(b['p'] - a['p'])
        n += 1
        if 1 <= iv <= 2:
            s += 1
        else:
            leaps.append((S.loc(b['s']), pname(a['p']), pname(b['p']), iv))
    tot += n; st += s
    rows.append((S.names[i], n, s, leaps))
print(f'total {tot} intervals, {st} steps = {100*st/max(1,tot):.1f}%; need {int(0.62*tot - st) + 1} more steps for 62%')
for name, n, s, leaps in rows:
    print(f'{name:4} {n:4} {s:4} {100*s/max(1,n):5.1f}%')
if '-v' in sys.argv:
    for name, n, s, leaps in rows:
        print(name, ' '.join(f'{l}:{a}-{b}({iv})' for l, a, b, iv in leaps))
