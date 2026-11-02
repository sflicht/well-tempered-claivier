import sys, numpy as np
from rlib import *
from lab import pname
D = [int(x) for x in sys.argv[1].split(',')]
sh, ob = int(sys.argv[2]), int(sys.argv[3])
gp, ga = line(GR_P, D, 0, 2, 96)
ap, aa = line(GR_P, D, 0, 4, 192)
u = np.full(192, -1); ua = np.zeros(192, int)
u[(ob - 1) * 12:(ob - 1) * 12 + 96] = gp + sh; ua[(ob - 1) * 12:(ob - 1) * 12 + 96] = ga
for b in range(16):
    cells = []
    for k in range(3):
        t = b * 12 + k * 4
        cells.append(f"{pname(u[t], True) if u[t] >= 0 else '.':>4}{'*' if ua[t] else ' '}/{pname(ap[t], True):<4}{'*' if aa[t] else ' '}")
    print(f'b{b+1:<3}', '  '.join(cells))
