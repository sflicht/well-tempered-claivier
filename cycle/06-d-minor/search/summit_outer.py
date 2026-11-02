"""Search (proposes only): placements of the normal-speed ground in an upper voice against the augmented ground in the bass."""
from lab import *
AUG = notes(GROUND, 0, 0, 2)
res = []
for sop_off in (48, 36, 60, 24):
  for sop_sh in (31, 24, 36, 26, 29):  # A5, D5, D6, E5, G5
    SOP = notes(GROUND, sop_off, sop_sh)
    c0, _ = cons_cost([AUG, SOP], sop_off, sop_off + 96)
    res.append((round(c0, 1), sop_off, pname(50 + sop_sh, True)))
res.sort()
for r in res[:10]: print(r)
