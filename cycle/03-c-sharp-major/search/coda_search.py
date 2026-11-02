"""Search offsets k (eighths) and mirror axes for the CS-over-S pair against
its own diatonic mirror.  Reports critic-based cost for the 4-voice overlap."""
import sys
from lib import *
from coda_eval import S

CS = sys.argv[1]
cs_start = int(sys.argv[2]) if len(sys.argv) > 2 else 2
res = []
for ax in ['E#2', 'E#3', 'E#4', 'E#5', 'E#6']:
    try:
        Sm, CSm = mirror(S, ax), mirror(CS, ax)
    except ValueError:
        continue
    for k in range(-24, 25, 2):
        base = 22 + max(0, -k)
        lines = [(CS, base + cs_start), (S, base), (Sm, base + k), (CSm, base + cs_start + k)]
        lo = base + max(0, k)
        hi = base + min(length(S), length(S)) + min(0, k) + 0
        cost, m, R = score(lines, window=(lo, hi))
        # register sanity: lowest note >= C#2, highest <= G#6
        ps = [p for tok, st in lines for _, _, p, _ in notes(tok, st)]
        if min(ps) < 37 or max(ps) > 92:
            continue
        res.append((cost, k, ax, m))
res.sort(key=lambda r: r[0])
for r in res[:20]:
    print(r)
