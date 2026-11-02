"""Search (proposes only): subject or inversus as a stretto partner of the subject."""
from lab import *
res = []
SU = notes(SUBJECT, 0, -12)    # subject at A3 (tenor), from 0
for form, tok, base in (('inv', INV, 74), ('subj', SUBJECT, 69)):
  for sh in range(-14, 12):
    for off in list(range(-24, 0, 2)) + list(range(2, 26, 2)):
        L = notes(tok, off, sh)
        if form == 'subj' and sh == -12: continue
        lo = max(0, off); hi = min(48, off + 48)
        c, bad = cons_cost([SU, L], lo, hi)
        span = (hi - lo) / 12
        if span < 2: continue
        res.append((round(c / span, 2), form, pname(base + sh, True), off, bad[:3]))
res.sort(key=lambda r: r[0])
for r in res[:40]: print(r)
