"""Beam search for a stretto chain of inner entries at the summit (harmonic fit +
pairwise counterpoint cost between overlapping entries)."""
import sys
from lab2 import *
from s14_harmfit import fit, beat_notes
AUG = ground(1, 0, 2); SOP = ground(5, 31)
cands = []
FORMS = sys.argv[1].split(",") if len(sys.argv) > 1 else ["rect", "inv"]
for form in FORMS:
    for shift in range(-19, 13):
        for b in range(1, 13):
            for beat in (1, 2, 3):
                s = subj(b, shift, beat) if form == 'rect' else inv(b, shift, beat)
                if s[-1][0] + s[-1][1] > 16 * 12:
                    continue
                lo = min(p for *_, p in s); hi = max(p for *_, p in s)
                if lo <= 52 or hi >= 80:
                    continue
                f, _ = fit([s])
                if f / len(beat_notes(s)) * 10 <= 2.6:
                    cands.append(((b - 1) * 3 + beat - 1, form, s[0][2], s))
print('cands', len(cands))
pc_cache = {}
def pc(i, j):
    k = (min(i, j), max(i, j))
    if k not in pc_cache:
        a, b = cands[i][3], cands[j][3]
        c = pair_cost(a, b)
        if c is None:
            pc_cache[k] = 0
        else:
            # unisons/near collisions: penalise mean distance < 4 semitones
            pc_cache[k] = c['cost'] + 10 * c['par'] + 4 * c['bpar']
    return pc_cache[k]
beam = [((), 0.0)]
best_full = []
for step in range(7):
    nb = []
    for chain, sc in beam:
        last_t = cands[chain[-1]][0] if chain else -1
        for j, c in enumerate(cands):
            t = c[0]
            if chain and not (last_t + 2 <= t <= last_t + 7):
                continue
            if not chain and t > 4:
                continue
            # register: at most 5 simultaneous entries; avoid same start pitch twice in overlap
            ok = True
            add = 0
            for i in chain:
                if cands[i][0] + 12 > t:   # overlapping (entry lasts 12 beats)
                    if abs(cands[i][2] - c[2]) < 3:
                        ok = False; break
                    add += pc(i, j)
            if not ok:
                continue
            ents = [cands[i][3] for i in chain] + [c[3]]
            f, _ = fit(ents)
            nb.append((chain + (j,), f + add))
    nb.sort(key=lambda r: r[1] / len(r[0]))
    beam = nb[:400]
    for chain, sc in beam[:3]:
        print(step + 1, round(sc, 1), [(cands[i][1], pname(cands[i][2], True), cands[i][0] // 3 + 1, cands[i][0] % 3 + 1) for i in chain])
