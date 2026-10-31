"""Search (proposes only): subject placements against the ground plus the inversus at A4 (station I)."""
from lab import *
GR = notes(GROUND, 0)
IV = notes(INV, 24, -5)   # A4 at b3
print(cons_cost([GR, IV], 24, 72))
res = []
for sh in range(-24, 14):
    for off in range(36, 100, 2):
        L = notes(SUBJECT, off, sh)
        c, bad = cons_cost([GR, IV, L], off, min(off + 48, 96))
        span = (min(off + 48, 96) - off) / 12
        if span < 2.5: continue
        res.append((round(c / span, 2), pname(69 + sh, True), loc(off), span, bad[:3]))
res.sort(key=lambda r: r[0])
for r in res[:30]: print(r)
