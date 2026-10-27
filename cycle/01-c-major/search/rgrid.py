import sys
from realize import statement, placed, tokens
from ladder import pair_cost
def grid(key, d8, fform, fshift, lead_oct=0, foct=0, lead_shift=0):
    L = statement(key, 'rectus', lead_shift, lead_oct); F = statement(key, fform, fshift, foct)
    A = placed(L, 14); B = placed(F, 14 + 2 * d8)
    c, w = pair_cost(A, B, True)
    print(f'{key} d={d8} {fform}{fshift:+d}: cost {c:.1f}', w)
    print('  L:', tokens(L)); print('  F:', tokens(F))
    t0, t1 = 14, max(A[-1][1], B[-1][1])
    names = lambda st: [nm for d, nm, m in st]
    def row(P, st):
        s = ''
        for t in range(t0, t1):
            k = next((i for i, n in enumerate(P) if n[0] <= t < n[1]), None)
            s += ('    ' if k is None else (f'{st[k][1]:<4}' if P[k][0] == t else '-   '))
        return s
    print('   ' + ''.join(('|' if t % 16 == 0 else ':' if t % 4 == 0 else ' ') + '   ' for t in range(t0, t1)))
    print('   ' + row(A, L)); print('   ' + row(B, F))
if __name__ == '__main__':
    a = sys.argv[1:]
    grid(a[0], int(a[1]), a[2], int(a[3]), int(a[4]) if len(a) > 4 else 0, int(a[5]) if len(a) > 5 else 0)
