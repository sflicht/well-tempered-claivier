#!/usr/bin/env python3
"""Local pitch-only neighbourhood of a hand-written subject (rhythm fixed).

Enumerates all 1- and 2-note pitch edits (+-1, +-2 steps) that stay
melodically valid and reports the ones whose ladder improves.  It proposes
edits for the composer to judge; it never chooses the subject.
Usage: local.py P0 "TOKENS" [--top N]
"""
import itertools
import sys

from ladder import ladder, parse, to_tokens
from search import valid_melody


def score(n, p0):
    L = ladder(n, p0, keep=1)
    best = [L[d][0][0] for d in range(1, 9)]
    R = ladder(n, p0, forms=('rectus',), keep=1)
    rb = [R[d][0][0] for d in range(1, 9)]
    return sum(best) + 1.5 * max(best), best, rb


def main():
    p0 = int(sys.argv[1])
    base = parse(sys.argv[2])
    top = int(sys.argv[sys.argv.index('--top') + 1]) if '--top' in sys.argv else 25
    b0, best0, rb0 = score(base, p0)
    print(f'base {b0:.1f}', [round(x, 1) for x in best0], 'rectus', [round(x, 1) for x in rb0])
    out = []
    idx = range(len(base))
    for k in idx:
        for dk in (-2, -1, 1, 2):
            n = list(base)
            n[k] = (n[k][0], n[k][1] + dk)
            if valid_melody(n, p0):
                v, b, r = score(n, p0)
                out.append((v, sum(r), to_tokens(n), b, r))
    for k, j in itertools.combinations(idx, 2):
        for dk, dj in itertools.product((-2, -1, 1, 2), repeat=2):
            n = list(base)
            n[k] = (n[k][0], n[k][1] + dk)
            n[j] = (n[j][0], n[j][1] + dj)
            if valid_melody(n, p0):
                v, b, r = score(n, p0)
                out.append((v, sum(r), to_tokens(n), b, r))
    out.sort()
    for v, rs, t, b, r in out[:top]:
        print(f'{v:6.1f} rect{rs:6.1f}  {t}\n        ', [round(x, 1) for x in b], 'rectus', [round(x, 1) for x in r])


if __name__ == '__main__':
    main()
