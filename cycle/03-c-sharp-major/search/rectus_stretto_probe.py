"""Rank rectus/rectus strettos of the subject (beat-aligned, diatonic transpositions).
Result: only at one bar's distance (up a 6th) is the subject clean against itself;
the close strettos belong to the inversus (see probe_inv2.py)."""
from lib import *
S = "G#4:2 C#5:4 C#5:2 E#5:4 E#5:2 G#5:4 R:2 G#4:4 A#4:1 B#4:1 C#5:2 D#5:2 E#5:2 F#5:4 E#5:2 C#5:4 B#4:2 C#5:4"
L = length(S); res = []
for st in range(-16, 17):
    if st == 0:
        continue
    M = dshift(S, st)
    for k in range(1, 7):
        lines = [(S, 22), (M, 22 + 6 * k)]
        ps = [p for tok, s0 in lines for _, _, p, _ in notes(tok, s0)]
        if min(ps) < 38 or max(ps) > 89:
            continue
        cost, m, R = score(lines)
        q, nb = beat_quality(lines, 24 + 6 * k, 22 + L)
        tot = 20 * m['pe'] + 8 * m['un'] + 3 * m['pw'] + 2 * m['x'] + q
        res.append((round(tot / max(1, nb), 2), k, st, m['pe'], m['un'], m['pw'], q, nb))
res.sort()
print('(penalty/beat, distance in beats, diatonic steps, par, unres, weak par, beat penalty, beats)')
for r in res[:12]:
    print(r)
