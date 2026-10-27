"""Evaluate the 'reflection' coda: CS over S (rectus, as in Part 1) with the
diatonic mirror of both around an axis (as in Part 2), offset by k eighths."""
import sys
from lib import *

S = "G#4:2 C#5:4 C#5:2 E#5:4 E#5:2 G#5:4 R:2 G#4:4 A#4:1 B#4:1 C#5:2 D#5:2 E#5:2 F#5:4 E#5:2 C#5:4 B#4:2 C#5:4"


def overlay(S, CS, axis='E#4', k=0, cs_start=2, show=True, s_start=0):
    """S starts (upbeat) at s_start+22; CS at s_start+22+cs_start. Mirror pair delayed by k sixteenths."""
    Sm, CSm = mirror(S, axis), mirror(CS, axis)
    base = 22 + s_start
    lines = [(CS, base + cs_start), (S, base), (Sm, base + k), (CSm, base + cs_start + k)]
    cost, m, R = score(lines, names=['CS', 'S', 'S*', 'CS*'], verbose=show)
    if show:
        print('cost', cost, m)
        grid(lines, start=base - 2 if base >= 2 else 0)
    return cost, m


if __name__ == '__main__':
    CS = sys.argv[1]
    k = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    cs_start = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    print('S  ', S)
    print('S* ', mirror(S, 'E#4'))
    print('CS ', CS)
    print('CS*', mirror(CS, 'E#4'))
    print('--- 2-part S/CS:')
    c, m, R = score([(CS, 24 + cs_start - 2 + 22 - 22 + 0), (S, 22)], verbose=True)
    print(c, m)
    print('--- coda overlay:')
    overlay(S, CS, k=k, cs_start=cs_start)
