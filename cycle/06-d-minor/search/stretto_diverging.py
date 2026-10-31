"""Search (proposes only): subject or inversus as a stretto partner of the subject."""
from lab import *
res = []
for fsh in range(-7, 6):        # first: subject in alto/soprano
    first = notes(SUBJECT, 0, fsh)
    for sh in range(-24, 0):
        for off in (6, 8, 10, 12, 14, 16, 18, 20, 24):
            L = notes(INV, off, sh)
            if max(p for *_, p in L) > min(p for *_, p in first) + 2: continue
            c, bad = cons_cost([first, L], off, 48)
            span = (48 - off) / 12
            res.append((round(c / span, 2), pname(69 + fsh, True), 'inv', pname(74 + sh, True), off, bad[:3]))
res.sort(key=lambda r: r[0])
for r in res[:25]: print(r)
