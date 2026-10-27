from lab import *
aug = notes(GROUND, 0, 0, 2)
res = []
for shift in range(12, 37):
    for off in range(-96, 96, 12):
        up = []
        for k in (-2, -1, 0, 1, 2):
            up += notes(GROUND, off + k * 96, shift)
        up = [(s, d, p) for s, d, p in up if s + d > 0 and s < 192]
        c = pair_cost(up, aug)
        if c:
            res.append((c['cost'], shift, off, c))
res.sort(key=lambda r: r[0])
for r in res[:16]:
    print(r[0], 'shift', r[1], pname(50 + r[1], True), 'offset bars', r[2] / 12, r[3])
