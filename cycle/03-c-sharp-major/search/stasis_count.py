"""Second review's stasis metric: beats whose sounding pitch classes all belong to a
C# triad, a G# triad or G#7.  Usage: stasis_count.py score.json"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from critic import Score
S = Score(json.load(open(sys.argv[1])))
SETS = [{1, 5, 8}, {8, 0, 3}, {8, 0, 3, 6}]
flags = []
for t in range(0, S.end, S.beat):
    pcs = {S.note(i, k)['p'] % 12 for i, (k, _) in S.sounding(t).items()}
    if pcs:
        flags.append((t, any(pcs <= x for x in SETS)))
n = sum(f for _, f in flags)
print(f'{n} of {len(flags)} beats bare I/V ({100 * n / len(flags):.0f}%)')
runs, cur = [], []
for t, f in flags:
    if f:
        cur.append(t)
    else:
        if len(cur) >= 5:
            runs.append((S.loc(cur[0]), len(cur)))
        cur = []
print('runs of >=5 bare beats:', runs)
