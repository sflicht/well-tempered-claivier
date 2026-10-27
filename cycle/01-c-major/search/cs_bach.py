"""BWV 846's subject in Bach's own rhythm (32nd grid) against our subject."""
import ladder
ladder.RES = 2
from ladder import parse, place, pair_cost
from fractions import Fraction
S = parse(open('../SUBJECT.txt').readline())
S2 = [(2 * d, g) for d, g in S]
# Bach: C D E F. g f E A D G. a g f e f e  (durations in 32nds)
B = [(4, 0), (4, 1), (4, 2), (6, 3), (1, 4), (1, 3), (4, 2), (4, 5), (4, 1), (6, 4), (2, 5), (2, 4), (2, 3), (2, 2), (2, 3), (2, 2)]
res = []
for n in (10, 12, 16):
    for off in range(-32, 9, 2):          # 32nds, CS start relative to subject start
        for oct_ in (-14, -7):
            A1 = place(S2, 28); B1 = place([(d, g + oct_) for d, g in B[:n]], 28 + off)
            c1, w1 = pair_cost(A1, B1, True)
            A2 = place([(d, g - 7) for d, g in S2], 28); B2 = place([(d, g + oct_ + 14) for d, g in B[:n]], 28 + off)
            c2, w2 = pair_cost(A2, B2, True)
            ov = min(A1[-1][1], B1[-1][1]) - max(A1[0][0], B1[0][0])
            res.append((round(c1 + c2, 1), round(c1, 1), round(c2, 1), n, off / 2, oct_, ov / 2, w1[:3], w2[:3]))
res.sort()
for r in res[:20]:
    print(r)
