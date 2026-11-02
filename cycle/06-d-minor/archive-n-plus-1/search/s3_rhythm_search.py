"""Search the shared rhythm of subject and ground (ground = subject inverted, x2).

Pitches are fixed by the concept (Crucifixus lament ground D C# C B Bb A Bb G A D;
subject = its inversion A Bb B C C# D C# E D A).  Only the durations vary.  Each
candidate is scored for how well the subject (at the tonic-key levels) and its
answer sit over the repeating ground.  Output: ranked rhythms for a human choice.
"""
import itertools, numpy as np, json, sys
SUBJ_P = [69, 70, 71, 72, 73, 74, 73, 76, 74, 81]           # A4 Bb B C C# D C# E D A5
GR_P = [50, 49, 48, 47, 46, 45, 46, 43, 45, 38]             # D3 C# C B Bb A Bb G A D2
COST = np.array([0, 4, 1.5, 0, 0, 0.6, 0.6, 0, 0, 0, 1.5, 4])   # by interval class (upper-lower)
def metric_w(t):  # t in sixteenths within 3/4 bar
    r = t % 12
    return 3 if r == 0 else (2 if r % 4 == 0 else (1 if r % 2 == 0 else .5))
W = np.array([metric_w(t) for t in range(96)])

def arr(pitches, durs, scale=1):
    p, a = [], []
    for x, d in zip(pitches, durs):
        n = int(d * scale)
        p += [x] * n
        a += [1] + [0] * (n - 1)
    return np.array(p), np.array(a)

def place_cost(sp, sa, gp, ga, off, shift):
    L = len(sp)
    idx = (off + np.arange(L)) % len(gp)
    u = sp + shift
    l = gp[idx]
    att = (sa | ga[idx]).astype(bool)
    ic = (u - l) % 12
    w = W[idx % 96]
    c = (COST[ic] * w * att).sum()
    # crossing below the ground is not allowed
    if (u <= l).any():
        c += 50
    # parallel perfect intervals between consecutive attack points where both move
    pts = np.nonzero(att)[0]
    for i in range(1, len(pts)):
        t0, t1 = pts[i - 1], pts[i]
        if u[t0] != u[t1] and l[t0] != l[t1] and ic[t0] in (0, 7) and ic[t0] == ic[t1]:
            c += 8
    return c / L * 12   # per bar

vals = [2, 4, 6, 8, 12]
res = []
count = 0
for durs in itertools.product(vals, repeat=9):
    s = sum(durs)
    if s > 46 or s < 36:
        continue
    last = 48 - s
    if last > 12:
        continue
    D = list(durs) + [last]
    if D[0] < 4:
        continue
    # note starts must keep long notes on beats (no note >=6 starting off the beat)
    t, ok = 0, True
    for d in D:
        if d >= 6 and t % 4 != 0:
            ok = False; break
        t += d
    if not ok or len(set(D)) < 3:
        continue
    count += 1
    sp, sa = arr(SUBJ_P, D)
    gp, ga = arr(GR_P, D, 2)
    best = {}
    for name, shift in (('A', 0), ('A8', 12), ('D', 5), ('E', 7), ('E-', -5), ('D-', -7)):
        for off in range(0, 96, 12):
            best[(name, off)] = place_cost(sp, sa, gp, ga, off, shift)
    # inversus (descending = ground diminished) at D5 and A4 levels
    ip = 2 * 69 - sp  # mirror about A4: A G# G F# F E F D E A3 (+ shift)
    inv = {}
    for name, shift in (('iA', 12), ('iD', 17), ('iD8', 5)):
        for off in range(0, 96, 12):
            inv[(name, off)] = place_cost(ip, sa, gp, ga, off, shift)
    # exposition: subject (A) and answer (D or E) four bars apart
    expo = min(min(best[('A', o)], best[('A8', o)]) + min(best[(n, (o + 48) % 96)] for n in ('D', 'E', 'E-', 'D-'))
               for o in range(0, 96, 12))
    expo_any = min(min(best[('A', o)], best[('A8', o)]) for o in range(0, 96, 12)) + \
        min(best[(n, o)] for n in ('D', 'E', 'E-', 'D-') for o in range(0, 96, 12))
    ib = min(inv.values())
    res.append((round(expo + 0.5 * ib, 2), round(expo, 2), round(expo_any, 2), round(ib, 2), D))
res.sort()
print('candidates', count)
for r in res[:40]:
    print(r)
json.dump(res[:400], open('/tmp/claude-0/-home-user-well-tempered-claivier/9e003b56-0315-515e-a129-a5b629d0f3cb/scratchpad/rhythms.json', 'w'))
