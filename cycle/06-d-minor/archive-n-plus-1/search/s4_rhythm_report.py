"""Detailed report for one candidate rhythm: expo placements, inversus, strettos, summit."""
import sys, numpy as np
sys.argv += []
from s3_rhythm_search import arr, place_cost, SUBJ_P, GR_P, W, COST
D = [int(x) for x in sys.argv[1].split(',')]
sp, sa = arr(SUBJ_P, D)
gp, ga = arr(GR_P, D, 2)
print('rhythm', D)
names = {0: 'A4', 12: 'A5', 5: 'D5', -7: 'D4', 7: 'E5', -5: 'E4', 3: 'C5', -4: 'F4', 8: 'F5', -2: 'G4', 10: 'G5', 1: 'Bb4'}
print('subject (asc) over ground, cost per bar at bar offsets 1..8:')
for sh, nm in names.items():
    print(f'  {nm:4s}', ' '.join(f'{place_cost(sp, sa, gp, ga, o, sh):5.2f}' for o in range(0, 96, 12)))
ip = 2 * 69 - sp
print('inversus (desc) over ground:')
for sh, nm in ((12, 'A4'), (17, 'D5'), (5, 'D4'), (24, 'A5'), (20, 'F5'), (8, 'F4'), (15, 'C5'), (19, 'E5'), (7, 'E4')):
    print(f'  {nm:4s}', ' '.join(f'{place_cost(ip, sa, gp, ga, o, sh):5.2f}' for o in range(0, 96, 12)))

# strettos: subject vs subject at offsets (eighths), transposition; cost of overlap
def pair(u, ua, l, la, off):
    # u starts at off, l at 0; overlap only
    n = min(len(u) + off, len(l))
    if n - off < 8:
        return None
    uu, uua = u[:n - off], ua[:n - off]
    ll, lla = l[off:n], la[off:n]
    att = (uua | lla).astype(bool)
    ic = (uu - ll) % 12
    w = W[(off + np.arange(n - off)) % 96]
    c = (COST[ic] * w * att).sum()
    if (uu <= ll).any():
        c += 50
    pts = np.nonzero(att)[0]
    for i in range(1, len(pts)):
        t0, t1 = pts[i - 1], pts[i]
        if uu[t0] != uu[t1] and ll[t0] != ll[t1] and ic[t0] in (0, 7) and ic[t0] == ic[t1]:
            c += 8
    return c / (n - off) * 12
print('stretto: follower above leader (rows: interval of follower vs leader in semitones; cols: offset in quarters 1..8)')
res = []
for form, F in (('rect', sp), ('inv', ip - 24)):
    for sh in range(-24, 25):
        for off in range(4, 36, 4):
            for upper in (0, 1):
                f = F + sh
                if upper:
                    c = pair(f, sa, sp, sa, off)   # follower above
                else:
                    # follower below leader: compute with roles swapped in pitch
                    n = min(len(f) + off, len(sp))
                    c = pair(sp[off:], sa[off:], f, sa, 0) if False else None
                    if n - off >= 8:
                        uu, uua = sp[off:n], sa[off:n]
                        ll, lla = f[:n - off], sa[:n - off]
                        att = (uua | lla).astype(bool)
                        ic = (uu - ll) % 12
                        w = W[(off + np.arange(n - off)) % 96]
                        c = (COST[ic] * w * att).sum() + (50 if (uu <= ll).any() else 0)
                        pts = np.nonzero(att)[0]
                        for i in range(1, len(pts)):
                            t0, t1 = pts[i - 1], pts[i]
                            if uu[t0] != uu[t1] and ll[t0] != ll[t1] and ic[t0] in (0, 7) and ic[t0] == ic[t1]:
                                c += 8
                        c = c / (n - off) * 12
                if c is not None:
                    res.append((round(c, 2), form, sh, off // 4, 'above' if upper else 'below'))
res.sort()
for r in res[:24]:
    print('  ', r)
# summit: ground (normal) vs augmented ground (x2) at bar offsets and transpositions
ap, aa = arr(GR_P, D, 4)  # 192 slots
out = []
for sh in range(12, 36):
    for ob in range(0, 9):
        u = np.full(192, -1); ua = np.zeros(192, int)
        u[ob * 12: ob * 12 + 96] = gp + sh
        ua[ob * 12: ob * 12 + 96] = ga
        m = u >= 0
        att = ((ua | aa) * m).astype(bool)
        ic = (u - ap) % 12
        w = np.array([W[t % 96] for t in range(192)])
        c = (COST[ic] * w * att).sum()
        out.append((round(c / 8, 2), ob, sh))
out.sort()
print('summit (ground over its augmentation, 8 bars):', out[:8])
