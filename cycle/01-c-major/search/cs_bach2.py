import ladder
ladder.RES = 2
from ladder import parse, place, pair_cost
S = parse(open('../SUBJECT.txt').readline())
S2 = [(2 * d, g) for d, g in S]
B = [(4, 0), (4, 1), (4, 2), (6, 3), (1, 4), (1, 3), (4, 2), (4, 5), (4, 1), (6, 4), (2, 5), (2, 4), (2, 3), (2, 2), (2, 3), (2, 2)]
for subj16 in (6, 14, 22, 30):
    for n in (10, 12, 14, 16):
        for oct_ in (-14, -7):
            A1 = place(S2, 2 * subj16); B1 = place([(d, g + oct_) for d, g in B[:n]], 4)
            c1, w1 = pair_cost(A1, B1, True)
            A2 = place([(d, g - 7) for d, g in S2], 2 * subj16); B2 = place([(d, g + oct_ + 14) for d, g in B[:n]], 4)
            c2, w2 = pair_cost(A2, B2, True)
            ov = (min(A1[-1][1], B1[-1][1]) - max(A1[0][0], B1[0][0])) / 2
            print(f'subj@{subj16:2d} n={n} oct={oct_}: below {c1:5.1f} above {c2:5.1f} overlap16={ov}', [(t/2, w) for t, w in w1][:4], [(t/2, w) for t, w in w2][:3])
