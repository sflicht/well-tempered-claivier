"""Subject against its own augmentation (coda).  The augmentation (x2) is the
leader; the normal-speed subject enters at every even offset, rectus/inversus,
any diatonic shift.  Prints best placements per offset window."""
from ladder import parse, place, pair_cost, head_ok
S = parse(open('../SUBJECT.txt').readline())
AUG = [(2 * d, g) for d, g in S]
res = []
for aug_form in ('rectus',):
  for aug_shift in (-14, -7):
    A = place(AUG, 12, aug_form, aug_shift)           # quarter upbeat at bar pos 12
    for start in range(12, 12 + 64 - 20, 2):
        for form in ('rectus', 'inversus'):
            for s in range(-4, 12):
                if form == 'rectus' and s in (aug_shift,):
                    continue
                if not head_ok(S, form, s):
                    continue
                B = place(S, start, form, s)
                c, w = pair_cost(A, B, True)
                res.append((round(c, 1), start, form, s, aug_shift, w))
res.sort(key=lambda r: r[0])
seen = set()
for r in res:
    if len(seen) > 40: break
    k = (r[1], r[2])
    if k in seen: continue
    seen.add(k)
    print(f'{r[0]:6.1f} start={r[1]:3d} (bar {1 + r[1] // 16} pos {r[1] % 16:2d}) {r[2]:8s} {r[3]:+d}  aug {r[4]}', r[5][:5])
