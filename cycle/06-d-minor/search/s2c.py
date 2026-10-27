from lab import *
import sys
DESC = 'D5:8 C#5:4 C5:6 B4:2 Bb4:4 A4:6 Bb4:2 G4:4 A4:8 D4:4'
ASC = SUBJECT
gr = []
for k in range(-1, 3):
    gr += notes(GROUND, k * 96)
step = int(sys.argv[1]) if len(sys.argv) > 1 else 12
for name, S in (('DESC', DESC), ('ASC', ASC)):
    res = []
    for shift in range(-12, 12):
        for off in range(0, 96, step):
            s = notes(S, off, shift)
            c = pair_cost(s, gr)
            res.append((c['cost'], pname(s[0][2], True), off // 12 + 1, (off % 12) / 4 + 1, c['bad_beats'], c['harsh'], c['par'], c['bpar']))
    res.sort()
    print(name)
    for r in res[:14]:
        print('  ', r)
