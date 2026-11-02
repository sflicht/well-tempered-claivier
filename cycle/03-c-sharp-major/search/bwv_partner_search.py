"""Which of our lines can sound against the head of BWV 848 (gigue re-barring)?
Candidates: rectus at every diatonic level, tonal/real inversus and CS* at several
axes, CS; offsets of -3..+4 beats.  Best: the inversus around E#4 entering a beat
and a half before Bach's head (used in bars 28-30, displaced onto beat 2)."""
from lib import *
BWV = "G#5:4 A#5:2 G#5:2 F#5:2 G#5:2 E#6:4 C#6:2 G#5:4 F#5:1 E#5:1 F#5:4 D#6:2"
S = "G#4:2 C#5:4 C#5:2 E#5:4 E#5:2 G#5:4 R:2 G#4:4 A#4:1 B#4:1 C#5:2 D#5:2 E#5:2 F#5:4 E#5:2 C#5:4 B#4:2 C#5:4"
CS = "E#5:4 F#5:2 G#5:6 E#6:4 D#6:2 G#5:6 E#6:2 D#6:2 C#6:2 A#5:4 G#5:2 E#5:4 D#5:2 E#5:4"
cands = {}
for j in range(-14, 1):
    cands[f'rect {dname(j)}'] = (dshift(S, j), 0)
for ax in ['E#2', 'E#3', 'E#4', 'D#2', 'D#3', 'D#4', 'B#2', 'B#3', 'B#4', 'G#2', 'G#3', 'G#4', 'A#2', 'A#3', 'A#4']:
    try:
        cands[f'inv/{ax}'] = (mirror(S, ax), 0)
        cands[f'CS*/{ax}'] = (mirror(CS, ax), 2)
    except ValueError:
        pass
for j in (-14, -7):
    cands[f'CS {dname(j)}'] = (dshift(CS, j), 2)
res = []
B0 = 12
for name, (M, pk) in cands.items():
    for k in range(-3, 5):
        t0 = 24 + 6 * k - 2 + pk
        if t0 < 0:
            continue
        lines = [(BWV, B0), (M, t0)]
        mn = notes(M, t0); bn = notes(BWV, B0)
        if min(p for _, _, p, _ in mn) < 38 or max(p for _, _, p, _ in mn) >= min(p for _, _, p, _ in bn) - 2:
            continue
        lo = max(B0, t0 + 2); hi = min(B0 + length(BWV), t0 + length(M))
        if hi - lo < 24:
            continue
        cost, m, R = score(lines)
        q, nb = beat_quality(lines, lo, hi)
        tot = 20 * m['pe'] + 8 * m['un'] + 3 * m['pw'] + 2 * m['x'] + q
        res.append((round(tot / max(1, nb), 2), name, k, m['pe'], m['un'], m['pw'], q, nb))
res.sort(key=lambda r: r[0])
for r in res[:12]:
    print(r)
