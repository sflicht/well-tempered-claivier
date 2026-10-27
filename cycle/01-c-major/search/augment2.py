from ladder import parse, place, pair_cost, head_ok
S = parse(open('../SUBJECT.txt').readline())
AUG = [(2 * d, g) for d, g in S]
out = []
for aug_shift in (-14, -7):
    A = place(AUG, 12, 'rectus', aug_shift)
    cands = []
    for start in range(-8, 12 + 64 - 16, 2):
        for form in ('rectus', 'inversus'):
            for s in range(-6, 14):
                if not head_ok(S, form, s): continue
                B = place(S, start, form, s)
                if aug_shift == -14 and min(n[3] for n in B) < 55: continue   # upper voice stays above G3
                if aug_shift == -7 and max(n[3] for n in B) > 62: continue    # lower voice below D4
                c, w = pair_cost(A, B, True)
                cands.append((c, start, form, s))
    for c1, s1, f1, h1 in cands:
        if c1 > 20: continue
        for c2, s2, f2, h2 in cands:
            if c2 > 20 or s2 < s1 + 32 or s2 > s1 + 38: continue
            out.append((round(c1 + c2, 1), aug_shift, (s1, f1, h1, round(c1, 1)), (s2, f2, h2, round(c2, 1))))
out.sort()
for o in out[:30]:
    print(o)
