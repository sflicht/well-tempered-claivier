"""Harmonic-fit search for the summit's inner entries.

The augmented ground (bass) and the soprano ground (dominant level, bars 5-12)
fix a chord progression; each region lists the chords the two grounds allow.
An entry is scored by its notes that sound on beats but belong to none of the
chosen chord (weighted by length; short stepwise passing notes cost little).
Several entries are checked together so they agree on one chord per region."""
import itertools, sys
from lab2 import *
P = lambda *x: frozenset(x)
Dm, D7, Bb, Gm, Dm7 = P(2, 5, 9), P(2, 6, 9, 0), P(10, 2, 5), P(7, 10, 2), P(2, 5, 9, 0)
A, A7, Am = P(9, 1, 4), P(9, 1, 4, 7), P(9, 0, 4)
REG = [  # (beat0, beat1 exclusive, options)  beats counted from summit bar 1 beat 1
    (0, 3, [Dm, Bb, D7, Gm, Dm7]), (3, 6, [Dm, Bb, D7, Gm, Dm7]), (6, 8, [Dm, Bb, D7, Gm, Dm7]),
    (8, 10, [A, A7, P(1, 4, 7, 10)]), (10, 12, [A, A7, P(1, 4, 7, 10)]),
    (12, 16, [Am, P(5, 9, 0), D7, P(9, 0, 4, 7), Dm7]),
    (16, 18, [P(4, 8, 11), P(4, 8, 11, 2), P(8, 11, 2, 5)]),
    (18, 20, [Gm, P(4, 7, 10, 2), P(0, 4, 7, 10), P(7, 10, 2, 5)]),
    (20, 21, [P(2, 6, 9), D7, P(6, 9, 0, 3)]),
    (21, 22, [Dm, P(5, 9, 0), Dm7]),
    (22, 25, [A, Am, A7]),
    (25, 26, [Dm, P(5, 9, 0), Dm7]),
    (26, 28, [Bb, Gm, P(10, 2, 5, 9), P(7, 10, 2, 5)]),
    (28, 32, [P(4, 7, 10), P(0, 4, 7), A7, P(4, 7, 11), P(0, 4, 7, 10), P(4, 7, 10, 2)]),
    (32, 34, [A, A7]), (34, 36, [A, A7, Dm, P(9, 2, 4)]),
    (36, 38, [A, A7, Dm, P(4, 8, 11, 2), P(1, 4, 7, 10)]), (38, 40, [A, A7, Dm, P(4, 8, 11, 2), P(1, 4, 7, 10)]),
    (40, 42, [A, A7, Dm, P(4, 8, 11, 2), P(1, 4, 7, 10)]), (42, 44, [A, A7, P(9, 2, 4)]),
    (44, 48, [Dm, P(2, 6, 9)]),
]
def beat_notes(L):
    """[(beat_index, pc, weight)] for notes sounding on each beat (held notes too)."""
    out = []
    for s, d, p in L:
        b0 = int(-(-s // 4)); b1 = int((s + d - 1) // 4)
        for b in range(b0, b1 + 1):
            if b * 4 < s + d:
                w = min(d / 4, 2.0) * (1.5 if b % 3 == 0 else 1.0)
                if b * 4 != s:
                    w *= 0.8   # held into the beat (suspension-like)
                out.append((b, p % 12, float(w)))
    return out
def fit(entries):
    """Total misfit with the best common chord choice per region."""
    bn = [beat_notes(L) for L in entries]
    tot, choice = 0.0, []
    for b0, b1, opts in REG:
        best = None
        for o in opts:
            c = sum(w for notes in bn for b, pc, w in notes if b0 <= b < b1 and pc not in o)
            if best is None or c < best[0]:
                best = (c, o)
        tot += best[0]; choice.append(best[1])
    return tot, choice
if __name__ == '__main__':
    cands = []
    for form in ('rect', 'inv'):
        for shift in range(-19, 13):
            for b in range(1, 14):
                for beat in (1, 2, 3):
                    s = subj(b, shift, beat) if form == 'rect' else inv(b, shift, beat)
                    if s[-1][0] + s[-1][1] > 16 * 12:
                        continue
                    lo = min(p for *_, p in s); hi = max(p for *_, p in s)
                    if lo <= 52 or hi >= 80:
                        continue
                    f, _ = fit([s])
                    n = len(beat_notes(s))
                    cands.append((round(f / n * 10, 2), form, pname(s[0][2], True), b, beat))
    cands.sort()
    for c in cands[:70]:
        print(c)
