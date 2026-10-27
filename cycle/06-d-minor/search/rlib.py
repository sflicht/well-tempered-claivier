"""Fast numpy evaluator for subject/ground rhythm candidates (search only)."""
import numpy as np
SUBJ_P = [69, 70, 71, 72, 73, 74, 73, 76, 74, 81]           # A4 Bb B C C# D C# E D A5
GR_P = [50, 49, 48, 47, 46, 45, 46, 43, 45, 38]             # D3 C# C B Bb A Bb G A D2
COST = np.array([0, 4, 1.5, 0, 0, 0.6, 0.6, 0, 0, 0, 1.5, 4.0])   # interval class upper-lower
def metric_w(t):
    r = t % 12
    return 3 if r == 0 else (2 if r % 4 == 0 else (1 if r % 2 == 0 else .5))
W = np.array([metric_w(t) for t in range(400)])

def line(pitches, durs, start=0, scale=1, length=None):
    """pitch array (-1 = silent) and attack array on a sixteenth grid."""
    n = length or int(start + sum(durs) * scale)
    p = np.full(n, -1); a = np.zeros(n, int)
    t = int(start)
    for x, d in zip(pitches, durs):
        k = int(d * scale)
        p[t:t + k] = x; a[t] = 1
        t += k
    return p, a

def cyc(p, a, reps):
    return np.tile(p, reps), np.tile(a, reps)

def cost(up, ua, lp, la, t0=0):
    """Cost per bar of two aligned arrays (upper, lower) where both sound."""
    m = (up >= 0) & (lp >= 0)
    if m.sum() < 8:
        return None
    att = ((ua | la) & m).astype(bool)
    ic = (up - lp) % 12
    w = W[(t0 + np.arange(len(up))) % 12 + 0]
    c = (COST[ic] * w * att).sum()
    c += 50 * ((up <= lp) & m).sum() / 4
    pts = np.nonzero(att)[0]
    for i in range(1, len(pts)):
        x, y = pts[i - 1], pts[i]
        if up[x] != up[y] and lp[x] != lp[y] and ic[x] in (0, 7) and ic[x] == ic[y]:
            c += 8
    return c / m.sum() * 12
