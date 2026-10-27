from lab import *
aug = notes(GROUND, 0, 0, 2)
for half, off in (('first', 0), ('second', 96)):
    res = []
    for shift in range(12, 37):
        up = notes(GROUND, off, shift)
        c = pair_cost(up, aug)
        res.append((c['cost'], shift, c))
    res.sort(key=lambda r: r[0])
    print(half, [(r[0], pname(50 + r[1], True), r[2]['bad_beats'], r[2]['harsh']) for r in res[:8]])
