import sys
from realize import statement, placed, head_ok, tokens
from ladder import pair_cost
keys = sys.argv[1].split(',') if len(sys.argv) > 1 else ['C','G','a','e','F','d']
for d8 in range(8, 0, -1):
    print(f'=== d={d8} eighths')
    for key in keys:
        L = statement(key, 'rectus', 0, 0)
        if not head_ok(L): continue
        res = []
        for form in ('rectus', 'inversus'):
            for s in range(-11, 12):
                if form == 'rectus' and s == 0: continue
                F = statement(key, form, s, 0)
                if not head_ok(F): continue
                c, w = pair_cost(placed(L, 14), placed(F, 14 + 2 * d8), True)
                res.append((round(c, 1), form, s, F[0][1], w))
        res.sort(key=lambda r: r[0])
        print(f'  {key:2s}', '  '.join(f'{c}:{f[:3]}{s:+d}({n})' for c, f, s, n, w in res[:4]))
