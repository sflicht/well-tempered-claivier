import ladder
from ladder import parse, place, pair_cost, head_ok
S = parse(open('../SUBJECT.txt').readline())
AUG = [(2 * d, g) for d, g in S]
A = place(AUG, 12, 'rectus', -14)       # augmentation G2.. from coda pos 12 to 76
res = []
for start in range(30, 62, 2):
    for form in ('rectus', 'inversus'):
        for s in range(-4, 16):
            if not head_ok(S, form, s): continue
            B = place(S, start, form, s)
            if min(n[3] for n in B) < 57 or max(n[3] for n in B) > 86: continue
            c, w = pair_cost(A, B, True)
            res.append((round(c, 1), start, form, s, B[0][2], w[:4]))
res.sort()
from ladder import name
for r in res[:20]:
    print(r[0], 'start', r[1], f'(bar+{r[1]//16} pos {r[1]%16})', r[2], r[3], 'first', name(r[4]), r[5])
