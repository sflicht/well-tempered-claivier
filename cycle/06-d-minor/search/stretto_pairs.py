"""Search (proposes only): subject or inversus as a stretto partner of the subject."""
from lab import *
res = []
first = notes(SUBJECT, 0, -7)   # subject at D4 (lower voice, tenor) from 0
for form, tok, base in (('subj', SUBJECT, 69), ('inv', INV, 74)):
  for sh in range(-6, 16):
    for off in (4, 6, 8, 10, 12, 14, 16, 18, 20, 24):
        L = notes(tok, off, sh)
        if min(p for *_, p in L) < 62: continue   # second voice above
        c, bad = cons_cost([first, L], off, 48)
        span = (48 - off) / 12
        res.append((round(c / span, 2), form, pname(base + sh, True), off, bad[:3]))
res.sort(key=lambda r: r[0])
for r in res[:25]: print(r)
