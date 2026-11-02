"""Search (proposes only): subject/inversus placements over one statement of the ground."""
from lab import *
G = notes(GROUND, 0) + notes(GROUND, 96)   # two statements (second one an octave up in tenor is different; ok for first look)
res = []
for form, tok, base in (('subj', SUBJECT, 69), ('inv', INV, 74)):
    for sh in range(-14, 14):
        for off in range(0, 52, 4):
            L = notes(tok, off, sh)
            ps = [p for *_, p in L]
            if min(ps) < 55: continue
            c, bad = cons_cost([notes(GROUND, 0), L], off, min(off + 48, 96))
            res.append((round(c, 1), form, pname(base + sh, True), loc(off), bad[:3]))
res.sort(key=lambda r: r[0])
for r in res[:30]: print(r)
