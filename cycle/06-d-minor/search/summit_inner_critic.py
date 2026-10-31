"""Summit inner entries: bass aug (b41-56), soprano ground A5 (b45-52, last note up),
then candidates: alto subject (levels/starts) and tenor inversus (levels/starts); critic-based."""
from lab import *
import itertools
B0 = 40 * 12  # bar 41 (summit) start in units
AUG = notes(GROUND, B0, 0, 2)
SOPt = 'A5:16 G#5:8 G5:8 F#5:4 F5:4 E5:12 F5:4 D5:8 E5:24 A5:8'
SOP = notes(SOPt, B0 + 48, 0)
def crit(lines, lo, hi):
    def clip(nl):
        return [(s, d, p) for s, d, p in nl if s < hi and s + d > lo]
    d = data_of([clip(l) for l in lines])
    R = analyse(d)
    s = R['summary']
    unres = sum(1 for x in R['dissonance'] if x['sev'] == 'error')
    return s['parallels_error'], s['beat_parallels'], unres, R
alto_c = []
for sh in range(-9, 4):            # subject levels around E4..
    for start in range(B0 + 72, B0 + 120, 4):
        L = notes(SUBJECT, start, sh)
        ps = [p for *_, p in L]
        if min(ps) < 60 or max(ps) > 77: continue
        pe, bp, un, R = crit([SOP, L, AUG], start, start + 48)
        c, bad = cons_cost([SOP, L, AUG], start, start + 48)
        alto_c.append((pe * 10 + bp * 3 + un * 5 + c / 6, pe, bp, un, round(c, 1), pname(69 + sh, True), loc(start - B0 + 12 * 40), start, sh))
alto_c.sort()
for r in alto_c[:15]: print(r[:7])
print('--- pairs with tenor inversus')
pairs = []
for a in alto_c[:12]:
    A = notes(SUBJECT, a[7], a[8])
    for sh in range(-14, 0):
        for start in range(B0 + 60, B0 + 132, 4):
            T = notes(INV, start, sh)
            ps = [p for *_, p in T]
            if min(ps) < 50 or max(ps) > 69: continue
            lo = min(a[7], start); hi = max(a[7], start) + 48
            pe, bp, un, R = crit([SOP, A, T, AUG], lo, hi)
            c, bad = cons_cost([SOP, A, T, AUG], lo, hi)
            cross = sum(1 for x in R['crossing'])
            # overlap of all four (alto subj, tenor inv, soprano ground until B0+144)
            ov = (min(a[7] + 48, start + 48, B0 + 144) - max(a[7], start, B0 + 48)) / 12
            pairs.append((round(pe * 10 + bp * 3 + un * 5 + cross * 2 + c / 8, 2), pe, bp, un, cross, round(c, 1),
                          'A', a[5], a[6], 'T inv', pname(74 + sh, True), loc(start - B0 + 12 * 40), 'ov4', ov))
pairs.sort()
for r in pairs[:25]: print(r)
