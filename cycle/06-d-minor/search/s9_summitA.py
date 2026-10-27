import json, numpy as np
from rlib import *
out = json.load(open('/tmp/claude-0/-home-user-well-tempered-claivier/9e003b56-0315-515e-a129-a5b629d0f3cb/scratchpad/all.json'))
rows = []
for D, e in out:
    gp, ga = line(GR_P, D, 0, 2, 96)
    ap, aa = line(GR_P, D, 0, 4, 192)
    best = (99, None)
    for sh in (19, 31, 24, 12):   # A or D levels
        for ob in range(0, 9):
            u = np.full(192, -1); ua = np.zeros(192, int)
            u[ob * 12: ob * 12 + 96] = gp + sh; ua[ob * 12: ob * 12 + 96] = ga
            c = cost(u, ua, ap, aa)
            if c < best[0]:
                best = (c, (sh, ob + 1))
    if best[0] <= 0.5:
        rows.append((round(e['A'] + e['ans'] + 0.5 * e['inv'] + 0.5 * e['st1'] + 0.3 * e['st2'], 2), D, round(best[0], 2), best[1], {k: round(v, 2) for k, v in e.items()}))
rows.sort(key=lambda r: r[0])
print(len(rows))
for r in rows[:25]:
    print(r)
