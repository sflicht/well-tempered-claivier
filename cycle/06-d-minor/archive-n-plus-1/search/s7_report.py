"""Per-offset tables for one rhythm (subject and inversus over the ground; summit)."""
import sys, numpy as np
from rlib import *
from lab import pname
D = [int(x) for x in sys.argv[1].split(',')]
sp, sa = line(SUBJ_P, D, 0, 1, 48)
gp, ga = line(GR_P, D, 0, 2, 96)
G3p, G3a = cyc(gp, ga, 3)
def tok(p, d, sc=1):
    return ' '.join(f'{pname(x, True)}:{int(y*sc)}' for x, y in zip(p, d))
print('subject:', tok(SUBJ_P, D))
print('ground :', tok(GR_P, D, 2))
def row(p, sh):
    out = []
    for ob in range(8):
        o = 96 + ob * 12
        ab = cost(p + sh, sa, G3p[o:o + 48], G3a[o:o + 48])
        be = cost(G3p[o:o + 48] + 36, G3a[o:o + 48], p + sh - 12, sa)
        out.append(f'{ab:4.1f}/{be:4.1f}')
    return ' '.join(out)
print('levels (above/below ground) at ground bars 1..8')
for nm, sh in (('A', 0), ('D', 5), ('E', 7), ('C', 3), ('F', 8), ('G', 10), ('Bb', 1), ('B', 2)):
    print(f' subj {nm:3s}', row(sp, sh))
ip = 2 * 69 - sp
for nm, sh in (('A', 12), ('D', 17), ('E', 19), ('C', 15), ('F', 20), ('G', 22), ('Bb', 13)):
    print(f' inv  {nm:3s}', row(ip, sh))
ap, aa = line(GR_P, D, 0, 4, 192)
out = []
for sh in range(12, 36):
    for ob in range(0, 9):
        u = np.full(192, -1); ua = np.zeros(192, int)
        u[ob * 12: ob * 12 + 96] = gp + sh; ua[ob * 12: ob * 12 + 96] = ga
        c = cost(u, ua, ap, aa)
        out.append((round(c, 2), 'bar', ob + 1, pname(50 + sh, True)))
out.sort()
print('summit:', out[:8])
