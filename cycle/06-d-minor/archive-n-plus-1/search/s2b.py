from lab import *
import sys
gr = []
for k in range(-1, 3):
    gr += notes(GROUND, k * 96)
want = sys.argv[1:]  # starting pitch-class names for rectus
for shift in range(-24, 25):
    s0 = notes(SUBJECT, 0, shift)
    nm = pname(s0[0][2], True)
    if nm[:-1] not in want or s0[0][2] < 57:
        continue
    out = []
    for off in range(0, 96, 4):
        s = notes(SUBJECT, off, shift)
        c = pair_cost(s, gr)
        out.append((c['cost'], off // 12 + 1, (off % 12) / 4 + 1, c['bad_beats'], c['harsh'], c['par'], c['bpar']))
    out.sort()
    print(nm, out[:8])
