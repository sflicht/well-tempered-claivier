from lab import *
aug = notes(GROUND, 0, 0, 2)
res = []
for offb in range(0, 9):
    for shift in range(12, 37):
        up = notes(GROUND, offb * 12, shift)
        c = pair_cost(up, aug)
        res.append((round(c['cost'] / c['beats'] * 24, 1), offb, pname(50 + shift, True), c['bad_beats'], c['harsh'], c['par'], c['bpar']))
res.sort()
for r in res[:20]:
    print(r)
