"""Summit search judged by the critic in 3-voice context (soprano ground, entry, augmented bass)."""
from lab2 import *
AUG = ground(1, 0, 2); SOP = ground(5, 31)
res = []
for form in ('rect', 'inv'):
    for shift in range(-19, 13):
        for b in range(2, 13):
            for beat in (1, 2, 3):
                s = subj(b, shift, beat) if form == 'rect' else inv(b, shift, beat)
                lo = min(p for *_, p in s); hi = max(p for *_, p in s)
                if lo <= 52 or hi >= 80:
                    continue
                t0 = s[0][0]; t1 = s[-1][0] + s[-1][1]
                clip = lambda L: [(a, d, p) for a, d, p in L if a < t1 and a + d > t0]
                R = analyse(data_of([clip(SOP), s, clip(AUG)]))
                sm = R['summary']
                un = sm['dissonance_unresolved']
                # dissonances the critic accepts but that sit on downbeats between entry and bass
                cost = 10 * sm['parallels_error'] + 6 * un + 3 * sm['beat_parallels'] + 2 * sm['parallels_weak']
                res.append((cost, form, pname(s[0][2], True), b, beat, sm['dissonance_kinds']))
res.sort(key=lambda r: r[0])
for r in res[:50]:
    print(r)
