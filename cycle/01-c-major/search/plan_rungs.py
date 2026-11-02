from realize import statement, placed, head_ok
from ladder import pair_cost
PLAN = [(8, 'G'), (7, 'e'), (6, 'a'), (5, 'd'), (4, 'F'), (3, 'C'), (2, 'G'), (1, 'C')]
for d8, key in PLAN:
    L = statement(key, 'rectus', 0, 0)
    above, below = [], []
    for form in ('rectus', 'inversus'):
        for s in range(-14, 15):
            if form == 'rectus' and s == 0: continue
            F = statement(key, form, s, 0)
            if not head_ok(F): continue
            c, w = pair_cost(placed(L, 14), placed(F, 14 + 2 * d8), True)
            mean_l = sum(x[2] for x in L) / len(L); mean_f = sum(x[2] for x in F) / len(F)
            gap = mean_f - mean_l
            if abs(gap) > 26 or abs(gap) < 3: continue
            (above if gap > 0 else below).append((round(c, 1), form[:3], s, F[0][1], len(w)))
    above.sort(); below.sort()
    print(f'd={d8} {key}  lead {L[0][1]}')
    print('   follower above:', above[:4])
    print('   follower below:', below[:4])
