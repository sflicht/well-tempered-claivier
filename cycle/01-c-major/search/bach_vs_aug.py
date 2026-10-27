import ladder
ladder.RES = 2
from ladder import parse, place, pair_cost
S = parse(open('../SUBJECT.txt').readline())
AUG = [(4 * d, g) for d, g in S]          # augmentation in 32nds
B = [(4, 0), (4, 1), (4, 2), (6, 3), (1, 4), (1, 3), (4, 2), (4, 5), (4, 1), (6, 4), (2, 5), (2, 4), (2, 3), (2, 2), (2, 3), (2, 2)]
A = place(AUG, 24, 'rectus', -14)          # aug starts at coda pos 12 (sixteenths) = 24 32nds
res = []
for start16 in range(2, 64, 2):            # Bach line start, keep Bach's metric habit: start on an 8th
    for sh in range(0, 15):
        for n in (10, 12, 16):
            Bl = place([(d, g + sh) for d, g in B[:n]], 2 * start16)
            c, w = pair_cost(A, Bl, True)
            res.append((round(c, 1), start16, sh, n, [(t / 2, x) for t, x in w][:4]))
res.sort(key=lambda r: (r[0] - r[3]))
for r in res[:15]:
    print(r)
