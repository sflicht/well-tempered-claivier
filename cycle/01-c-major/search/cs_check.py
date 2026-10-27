import sys
from ladder import parse, place, pair_cost, name
S = parse(open('../SUBJECT.txt').readline())
def check(cs_tokens, cs_start=2, verbose=True):
    cs = parse(cs_tokens)
    A1 = place(S, 14); B1 = place(cs, cs_start)                 # CS below (as written)
    A2 = place([(d, g - 7) for d, g in S], 14)                   # subject down an octave
    B2 = place([(d, g + 7) for d, g in cs], cs_start)            # CS up an octave -> above
    c1, w1 = pair_cost(A1, B1, True); c2, w2 = pair_cost(A2, B2, True)
    if verbose:
        print(f'below {c1:5.1f} {w1}\nabove {c2:5.1f} {w2}')
    return c1, c2
if __name__ == '__main__':
    check(sys.argv[1])
