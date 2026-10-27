"""Summit search: subject (rectus/inversus) placements against the augmented ground
(bass, from summit bar 1) and the ground at the dominant in the soprano (from bar 5).
Bars are numbered from the start of the summit."""
import sys
from lab2 import *
AUG = ground(1, 0, 2)            # D3.. augmented, 16 bars
SOP = ground(5, 31)              # A5 G#5 ... A4, bars 5-12
res = []
for form in ('rect', 'inv'):
    for shift in range(-19, 13):
        for b in range(1, 14):
            for beat in (1, 2, 3):
                s = subj(b, shift, beat) if form == 'rect' else inv(b, shift, beat)
                lo = min(p for *_, p in s); hi = max(p for *_, p in s)
                if lo <= 50 or hi >= 81:        # strictly between bass and soprano register
                    continue
                c1 = pair_cost(s, AUG)
                c2 = pair_cost(s, SOP)
                c = c1['cost'] + (c2['cost'] if c2 else 0)
                bad = c1['bad_beats'] + (c2['bad_beats'] if c2 else 0)
                res.append((round(c, 1), form, pname(s[0][2], True), b, beat, bad, c1['par'] + (c2['par'] if c2 else 0)))
res.sort()
for r in res[:60]:
    print(r)
