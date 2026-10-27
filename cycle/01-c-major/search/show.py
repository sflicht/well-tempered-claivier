#!/usr/bin/env python3
"""Print the stretto ladder of one subject: the best placements per distance,
with the specific problems of each.  Usage: show.py P0 "TOKENS" [--top 4] [--grid D FORM SHIFT]
"""
import sys

from ladder import ladder, parse, place, rung, name, LET

def grid(notes, p0, d, form, shift):
    A = place(notes, p0)
    B = place(notes, p0 + 2 * d, form, shift)
    t0, t1 = A[0][0], max(A[-1][1], B[-1][1])

    def row(L):
        s = ''
        for t in range(t0, t1):
            k = next((i for i, n in enumerate(L) if n[0] <= t < n[1]), None)
            if k is None:
                s += '    '
            elif L[k][0] == t:
                s += f"{name(L[k][2]):<4}"
            else:
                s += '-   '
        return s
    bars = ''.join(('|' if (t % 16 == 0) else ':' if t % 4 == 0 else ' ') + '   ' for t in range(t0, t1))
    print('   ', bars)
    print('   ', row(A))
    print('   ', row(B))


def main():
    p0 = int(sys.argv[1])
    notes = parse(sys.argv[2])
    top = 4
    if '--top' in sys.argv:
        top = int(sys.argv[sys.argv.index('--top') + 1])
    if '--grid' in sys.argv:
        i = sys.argv.index('--grid')
        d, form, sh = int(sys.argv[i + 1]), sys.argv[i + 2], int(sys.argv[i + 3])
        c, why = rung(notes, p0, d, form, sh, detail=True)
        print(f'd={d} {form} {sh:+d} cost {c:.2f}', why)
        grid(notes, p0, d, form, sh)
        return
    L = ladder(notes, p0, keep=top)
    print('subject:', sys.argv[2], ' len16 =', sum(d for d, _ in notes))
    for d in range(8, 0, -1):
        print(f'd={d} eighths:')
        for c, form, sh in L[d]:
            _, why = rung(notes, p0, d, form, sh, detail=True)
            iv = sh if form == 'rectus' else sh
            print(f'   {c:6.2f} {form:8s} {sh:+3d}  ', '; '.join(f't{t}:{w}' for t, w in why)[:150])


if __name__ == '__main__':
    main()
