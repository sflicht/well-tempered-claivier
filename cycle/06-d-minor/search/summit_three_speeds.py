"""Search (proposes only): normal-speed ground + inversus (double speed) against the augmented ground."""
from lab import *
AUG = notes(GROUND, 0, 0, 2)
norms = []
for off in range(0, 100, 4):
    for sh in range(7, 36):
        N = notes(GROUND, off, sh)
        c, _ = cons_cost([AUG, N], off, off + 96)
        norms.append((c, off, sh, N))
norms.sort(key=lambda r: r[0])
print('best normal placements:')
for c, off, sh, N in norms[:15]:
    print(round(c, 1), loc(off), pname(50 + sh, True))
res = []
for c0, off, sh, N in norms[:15]:
    if c0 > 20: continue
    for ish in range(-26, 8):
        for ioff in range(off, off + 96 - 24, 2):
            L = notes(INV, ioff, ish)
            ps = [p for *_, p in L]
            # keep inv between bass and normal ground roughly
            if min(ps) < 52 or max(ps) > 84: continue
            c, bad = cons_cost([AUG, N, L], ioff, ioff + 48)
            ov = (min(ioff + 48, off + 96) - ioff) / 12
            res.append((round(c / 4, 1), loc(off), pname(50 + sh, True), loc(ioff), pname(74 + ish, True), ov, bad[:3]))
res.sort(key=lambda r: r[0])
for r in res[:40]: print(r)
