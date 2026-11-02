"""Where can BWV 846's pitch sequence C D E F G F E A D G (F E) sit against the
subject, so that it is ALSO good inverted at the octave (CS above the answer)?"""
from ladder import parse, place, pair_cost, semi
S = parse("G4:2 C5:3 D5:1 E5:2 C5:2 G5:4 F5:1 E5:1 D5:1 C5:1 D5:2 G4:2 A4:1 B4:1 C5:1 B4:1 E5:2 F5:2 G5:2")
P = [0, 1, 2, 3, 4, 3, 2, 5, 1, 4, 3, 2]   # C D E F G F E A D G F E (degrees from C)
RH = {
 'even8':  [2,2,2,2,2,2,2,2,2,2,2,2],
 'recon':  [2,2,2,2,1,1,2,2,2,3,1,2],
 'dotF':   [2,2,2,3,1,2,2,2,2,3,1,2],
 'lombG':  [2,2,2,2,1,1,2,2,2,2,1,1],
 'longF':  [2,2,2,4,1,1,2,2,2,2,2,2],
}
res = []
for rn, rh in RH.items():
    for n in (10, 12):
        cs = [(d, g) for d, g in zip(rh[:n], P[:n])]
        for off in range(-14, 7):       # CS start relative to subject start (subject at 14)
            for octv in (-14, -7):      # CS degree base (C3 = -7, C2 = -14)
                B = place([(d, g + octv) for d, g in cs], 14 + off)
                A = place(S, 14)
                c1, w1 = pair_cost(A, B, True)
                # inverted at the octave: subject an octave lower, CS above it
                A2 = place([(d, g - 7) for d, g in S], 14)
                for up in (0, 7):
                    B2 = place([(d, g + up) for d, g in cs], 14 + off)
                    if max(n[3] for n in B2) > 84: continue
                    c2, w2 = pair_cost(A2, B2, True)
                    res.append((c1 + c2, c1, c2, rn, n, off, (octv, up), w1, w2))
                continue
                res.append((c1 + c2, c1, c2, rn, n, off, octv, w1, w2))
res.sort(key=lambda r: r[0])
for r in res[:25]:
    print(f'{r[0]:6.1f} below{r[1]:6.1f} above{r[2]:6.1f}  {r[3]:6s} n={r[4]} off={r[5]:+d} oct={r[6]}', r[7][:4], r[8][:4])
