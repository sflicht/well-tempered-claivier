"""Chains of 3-4 mutually compatible entries over the summit's dominant pedal and into the
final tonic (bars 57-66); every overlapping pair must be clean; the context is the
augmented ground (held D2 into the coda) and the soprano ground."""
from lab2 import *
import itertools
AUG = ground(49, 0, 2) + [(64*12, 48, 38)]
SOP = ground(53, 31)
def uni(a, b):
    return sum(min(s+d, s2+d2) - max(s, s2) for s, d, p in a for s2, d2, p2 in b if p == p2 and s < s2+d2 and s2 < s+d) / 4
C = {}
for form in ('rect', 'inv'):
    for sh in range(-19, 12):
        for b in range(57, 63):
            for beat in (1, 2, 3):
                s = subj(b, sh, beat) if form == 'rect' else inv(b, sh, beat)
                if s[-1][0] + s[-1][1] > 66 * 12: continue
                lo = min(p for *_, p in s); hi = max(p for *_, p in s)
                if lo < 52 or hi > 81: continue
                t = 0
                for c in (AUG, SOP):
                    r = pair_cost(s, c)
                    if r: t += r['cost'] + 10 * r['par'] + 8 * uni(s, c)
                if t <= 12:
                    C[f"{form}{pname(s[0][2], True)}@{b}.{beat}"] = (t, s, (b - 57) * 3 + beat - 1, s[0][2])
keys = sorted(C, key=lambda k: C[k][2])
ok = {}
for a, b in itertools.combinations(keys, 2):
    sa, sb = C[a][1], C[b][1]
    c = pair_cost(sa, sb)
    if c is None:
        ok[(a, b)] = ok[(b, a)] = 0.0
    else:
        v = c['cost'] + 10 * c['par'] + 4 * c['bpar'] + 8 * uni(sa, sb)
        if v <= 3.5 and abs(C[a][3] - C[b][3]) >= 3:
            ok[(a, b)] = ok[(b, a)] = v
res = []
for n in (4, 3):
    for combo in itertools.combinations(keys, n):
        ts = [C[k][2] for k in combo]
        if any(t2 - t1 < 2 or t2 - t1 > 6 for t1, t2 in zip(ts, ts[1:])): continue
        if sum(1 for k in combo if k.startswith('rect')) < 2: continue
        if all((x, y) in ok for x, y in itertools.combinations(combo, 2)):
            tot = sum(C[k][0] for k in combo) + sum(ok[(x, y)] for x, y in itertools.combinations(combo, 2))
            res.append((n, round(tot, 1), combo))
    if res: break
res.sort(key=lambda r: (-r[0], r[1]))
for r in res[:25]: print(r)
