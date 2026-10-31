"""Second rhythm search: subject may start after a rest (u), ground = subject inverted x2.
Scores: subject/answer over the ground (both orientations), inversus over ground,
static D at the ground's joint.  Prints a ranked list for a human choice."""
import itertools, json, sys
import numpy as np
from rlib import *
vals = [2, 4, 6, 8, 12]
LEVELS = {'A': 0, 'D': 5, 'E': 7, 'D-': -7, 'E-': -5}
res = []
for u in (0, 2, 4, 8):
    for durs in itertools.product(vals, repeat=9):
        s = u + sum(durs)
        if s > 46 or s < 38:
            continue
        D = list(durs)
        t, ok = u, True
        for d in D:
            if d >= 6 and t % 4 != 0:
                ok = False; break
            t += d
        if not ok or len(set(D)) < 3:
            continue
        last = 48 - s           # last note fills to the next subject-cycle start
        if last > 12:
            continue
        joint_D = (last + D[0]) / 2   # beats of the ground's D at the joint (ground x2 -> /4*2)
        Dfull = D + [last]
        sp, sa = line(SUBJ_P, Dfull, u, 1, 48)
        gp, ga = line(GR_P, Dfull, 2 * u, 2, 96)
        # the ground's initial rest is the previous statement's final D, sustained
        gp[:2 * u] = GR_P[-1]
        G3p, G3a = cyc(gp, ga, 3)
        best = {}
        for nm, sh in LEVELS.items():
            for ob in range(8):
                o = 96 + ob * 12
                seg_g, seg_ga = G3p[o:o + 48], G3a[o:o + 48]
                ab = cost(sp + sh, sa, seg_g, seg_ga, 0)
                # below: subject two octaves lower, ground two octaves higher
                be = cost(seg_g + 24, seg_ga, sp + sh - 12, sa, 0)
                best[(nm, ob)] = 0.6 * ab + 0.4 * be
        ip = 2 * 69 - sp; ip[sp < 0] = -1
        inv = []
        for sh in (12, 17, 5):
            for ob in range(8):
                o = 96 + ob * 12
                ab = cost(ip + sh, sa, G3p[o:o + 48], G3a[o:o + 48])
                be = cost(G3p[o:o + 48] + 36, G3a[o:o + 48], ip + sh - 12, sa)
                inv.append(0.6 * ab + 0.4 * be)
        expo = min(min(best[('A', ob)] for _ in [0]) + min(best[(n, (ob + 4) % 8)] for n in ('D', 'E', 'D-', 'E-'))
                   for ob in range(8))
        ib = min(inv)
        score = expo + 0.5 * ib + 0.4 * max(0, joint_D - 4)
        res.append((round(score, 2), round(expo, 2), round(ib, 2), joint_D, u, Dfull))
res.sort(key=lambda r: r[0])
for r in res[:50]:
    print(r)
json.dump(res[:1000], open(sys.argv[1], 'w'))
