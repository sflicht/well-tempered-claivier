"""Search: subject (rectus / inversus) placements over the repeating ground."""
from lab import *
import sys
gr = []
for k in range(-1, 3):
    gr += notes(GROUND, k * 96)
res = []
for form in ('rectus', 'inversus'):
    for shift in range(-24, 25):
        for off in range(0, 96, 2):
            s = notes(SUBJECT, off, shift)
            if form == 'inversus':
                s = invert(notes(SUBJECT, off, 0), 69)  # mirror about A4 -> D C# C B Bb A ...
                s = [(a, d, p + shift) for a, d, p in s]
            lo = min(p for *_, p in s)
            if lo < 50:   # keep above the bass ground
                continue
            c = pair_cost(s, gr)
            res.append((c['cost'], form, shift, off, c['bad_beats'], c['harsh'], c['par'], c['bpar'], pname(s[0][2], True)))
res.sort()
seen = 0
for r in res[:40]:
    print(r[0], r[1], 'start', r[8], 'offset16', r[3], f'(bar {r[3]//12+1} beat {(r[3]%12)/4+1:g})', 'bad', r[4], 'harsh', r[5], 'par', r[6], r[7])
