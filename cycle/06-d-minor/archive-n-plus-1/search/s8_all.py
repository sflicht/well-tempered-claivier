import itertools, json, sys
from s6_rhythm_search3 import ok_rhythm, evaluate
vals = [2, 4, 6, 8, 12]
out = []
for durs in itertools.product(vals, repeat=9):
    s = sum(durs)
    if s > 46 or s < 38:
        continue
    D = list(durs) + [48 - s]
    if D[-1] > 12 or not ok_rhythm(D):
        continue
    e = evaluate(D)
    out.append((D, {k: float(v) for k, v in e.items()}))
json.dump(out, open(sys.argv[1], 'w'))
