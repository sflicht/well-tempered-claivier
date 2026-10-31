"""Summit stretto chain, second pass: harmonic fit (s14 regions), pairwise counterpoint
cost, unison collisions and the fixed context (augmented ground, soprano ground, the
Tenor II answer tail).  Summit bar 1 = fugue bar 49."""
import sys
from lab2 import *
from s14_harmfit import fit, beat_notes
AUG = ground(1, 0, 2); SOP = ground(5, 31)
TAIL = [(s - 48 * 12, d, p) for s, d, p in subj(47, -17) if s >= 48 * 12]   # answer tail, summit bars 1-2
CTX = [AUG, SOP, TAIL]
def unisons(a, b):
    n = 0
    for s, d, p in a:
        for s2, d2, p2 in b:
            if p == p2 and s < s2 + d2 and s2 < s + d:
                n += min(s + d, s2 + d2) - max(s, s2)
    return n / 4
cands = []
for form in ('rect', 'inv'):
    for shift in range(-19, 13):
        for b in range(1, 13):
            for beat in (1, 2, 3):
                s = subj(b, shift, beat) if form == 'rect' else inv(b, shift, beat)
                if s[-1][0] + s[-1][1] > 16 * 12:
                    continue
                lo = min(p for *_, p in s); hi = max(p for *_, p in s)
                if lo < 52 or hi > 79:
                    continue
                f, _ = fit([s])
                if f / len(beat_notes(s)) * 10 > 2.6:
                    continue
                cc = 0
                for c in CTX:
                    r = pair_cost(s, c)
                    if r:
                        cc += r['cost'] + 10 * r['par']
                    cc += 8 * unisons(s, c)
                cands.append(((b - 1) * 3 + beat - 1, form, s[0][2], s, cc))
print('cands', len(cands))
cache = {}
def pc(i, j):
    k = (min(i, j), max(i, j))
    if k not in cache:
        a, b = cands[i][3], cands[j][3]
        c = pair_cost(a, b)
        v = 0 if c is None else c['cost'] + 10 * c['par'] + 4 * c['bpar']
        cache[k] = v + 8 * unisons(a, b)
    return cache[k]
beam = [((), 0.0)]
for step in range(7):
    nb = []
    for chain, sc in beam:
        last_t = cands[chain[-1]][0] if chain else -1
        for j, c in enumerate(cands):
            t = c[0]
            if chain and not (last_t + 2 <= t <= last_t + 6):
                continue
            if not chain and t > 5:
                continue
            active = [i for i in chain if cands[i][0] + 12 > t]
            if len(active) >= 4:
                continue
            add = c[4] + sum(pc(i, j) for i in active)
            f, _ = fit([cands[i][3] for i in chain] + [c[3]])
            nb.append((chain + (j,), sc + add, f))
    nb.sort(key=lambda r: (r[1] + r[2]) / len(r[0]))
    beam = [(c, s) for c, s, f in nb[:300]]
    for c, s, f in nb[:4]:
        print(step + 1, round(s, 1), round(f, 1), [(cands[i][1], pname(cands[i][2], True), cands[i][0] // 3 + 49, cands[i][0] % 3 + 1, round(cands[i][4], 1)) for i in c])
