import sys
from lib import *
S = "G#4:2 C#5:4 C#5:2 E#5:4 E#5:2 G#5:4 R:2 G#4:4 A#4:1 B#4:1 C#5:2 D#5:2 E#5:2 F#5:4 E#5:2 C#5:4 B#4:2 C#5:4"
L = length(S)
res = []
for j in range(-10, 18):
    axn = dname(j)
    try:
        M = mirror(S, axn)
    except ValueError:
        continue
    for k in range(1, 9):              # inversus enters k beats after rectus (and vice versa)
        for lead in ('rect', 'inv'):
            a0, b0 = (0, 6 * k) if lead == 'rect' else (6 * k, 0)
            ov = L - 6 * k
            if ov < 18:
                continue
            lines = [(S, a0 + 22), (M, b0 + 22)]
            ps = [p for tok, st in lines for _, _, p, _ in notes(tok, st)]
            if min(ps) < 38 or max(ps) > 89:
                continue
            cost, m, R = score(lines)
            lo, hi = max(a0, b0) + 24, min(a0, b0) + 22 + L
            q, nb = beat_quality(lines, lo, hi)
            tot = 20 * m['pe'] + 8 * m['un'] + 3 * m['pw'] + 2 * m['x'] + q
            res.append((round(tot / max(1, nb), 2), tot, k, lead, axn, m['pe'], m['un'], m['pw'], m['x'], q, nb))
res.sort()
seen = set()
for r in res[:40]:
    print(r)
