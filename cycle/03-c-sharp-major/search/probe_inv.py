import sys
from lib import *
S = sys.argv[1] if len(sys.argv) > 1 else "G#4:2 C#5:4 C#5:2 E#5:4 E#5:2 G#5:4 R:2 C#6:4 B#5:1 A#5:1 G#5:2 F#5:2 E#5:2 D#5:4 E#5:2 C#5:4 B#4:2 C#5:4"
L = length(S)
res = []
for j in range(-10, 18):
    axn = dname(j)
    M = mirror(S, axn)
    for k in range(-8, 9):
        if k == 0 and j == 9:
            continue
        a0, b0 = 0, 6 * k
        base = min(a0, b0)
        ov = min(a0 + L, b0 + L) - max(a0, b0)
        if ov < 18:
            continue
        lines = [(S, a0 - base + 22), (M, b0 - base + 22)]
        cost, m, R = score(lines)
        res.append((cost, k, axn, m, int(ov)))
res.sort(key=lambda r: (r[0], -r[4]))
for r in res[:40]:
    print(r)
