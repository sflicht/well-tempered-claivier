#!/usr/bin/env python3
"""Proposal tool (does not compose): beat-level skeletons for quadruple
invertible counterpoint over the B-A-C-H cantus.

Pitch-class dynamic programme.  On every quarter beat the four lines must
form a fifth-free sonority (no P4/P5 between ANY pair, because every pair is
inverted somewhere in the 24 orderings); dissonant pairs must resolve by a
step down (or a tritone by step either way) in one of the two lines; no
consecutive unisons/octaves between moving lines.  It prints the best
skeletons so the composer can choose, reject or rewrite them.  Octaves,
passing notes and the real melodic shapes are written by hand afterwards.

usage: skeleton_search.py [--pattern P1] [--top 30] [--fix B=.,G,G,F,.,.,.,.]
"""
import argparse
import heapq
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from chords import chord_candidates, name_chord  # noqa: E402

NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
PC = {n: i for i, n in enumerate(NAMES)}
PC.update({'Db': 1, 'D#': 3, 'Gb': 6, 'Ab': 8, 'A#': 10})
CANTUS = {'major': [10, 10, 9, 9, 0, 0, 11, 11], 'minor': [10, 10, 9, 9, 0, 0, 11, 11]}
A_ATT = [1, 0, 1, 0, 1, 0, 1, 0]
PATTERNS = {
    'P1': 'Rahaaaha',   # R q h q | q h q
    'P2': 'Raaahaha',   # R q q h~|~q h q   (tie over barline)
    'P3': 'Rahahaha',   # 4th species
    'P4': 'Rahaahaa',
}


def ic(a, b):
    d = (a - b) % 12
    return min(d, 12 - d)


def dissonant(a, b):
    return ic(a, b) in (1, 2, 6)


def step_down(x, y):
    return (x - y) % 12 in (1, 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pattern', default='P1')
    ap.add_argument('--top', type=int, default=25)
    ap.add_argument('--mode', default='major')
    ap.add_argument('--scale', default='0,2,4,5,7,9,11')
    ap.add_argument('--chroma', default='10,6')
    ap.add_argument('--fix', action='append', default=[], help='e.g. B=.,G,G,F,.,.,.,.')
    ap.add_argument('--k', type=int, default=6)
    a = ap.parse_args()
    A = CANTUS[a.mode]
    pat = PATTERNS[a.pattern]
    diat = [int(x) for x in a.scale.split(',')]
    chroma = [int(x) for x in a.chroma.split(',')] if a.chroma else []
    dom = sorted(set(diat) | set(chroma))
    fixed = {'B': [None] * 8, 'C': [None] * 8, 'D': [None] * 8}
    for f in a.fix:
        k, v = f.split('=')
        for t, x in enumerate(v.split(',')):
            if x not in ('.', ''):
                fixed[k][t] = PC[x]

    def beat_states(t):
        bopts = [None] if pat[t] == 'R' else dom
        out = []
        for b, c, d in itertools.product(bopts, dom, dom):
            if fixed['B'][t] is not None and b != fixed['B'][t]:
                continue
            if fixed['C'][t] is not None and c != fixed['C'][t]:
                continue
            if fixed['D'][t] is not None and d != fixed['D'][t]:
                continue
            snd = [A[t], c, d] + ([b] if b is not None else [])
            if any(ic(x, y) == 5 for x, y in itertools.combinations(snd, 2)):
                continue
            s = set(snd)
            if len(s) >= 3 and not chord_candidates(s):
                continue
            sc = 0.9 * (len(s) - 2)
            if c == d:
                sc -= 1.0
            if b is not None and b == A[t]:
                sc -= 1.0
            for v in (b, c, d):
                if v is not None and v not in diat:
                    sc -= 0.7
            out.append(((b, c, d), sc))
        return out

    def trans(t, prev, cur):
        """score of moving from beat t-1 state prev to beat t state cur, or None."""
        pb, pc_, pd = prev
        b, c, d = cur
        if pat[t] == 'h' and b != pb:
            return None
        if pat[t] == 'a' and pb is not None:
            if pat[t - 1] == 'h':
                if not step_down(pb, b):
                    return None
            elif ic(pb, b) == 0 or ic(pb, b) > 5:
                return None
        if c == pc_:
            return None
        P = {'A': A[t - 1], 'B': pb, 'C': pc_, 'D': pd}
        Q = {'A': A[t], 'B': b, 'C': c, 'D': d}
        mov = [k for k in Q if Q[k] is not None and P[k] is not None and Q[k] != P[k]]
        for x, y in itertools.combinations(mov, 2):
            if ic(P[x], P[y]) == 0 and ic(Q[x], Q[y]) == 0:
                return None
        pv = [(k, P[k]) for k in P if P[k] is not None]
        for (k1, p1), (k2, p2) in itertools.combinations(pv, 2):
            if not dissonant(p1, p2):
                continue
            res = False
            for k, p, o in ((k1, p1, p2), (k2, p2, p1)):
                n = Q[k]
                if n is None or n == p:
                    continue
                if step_down(p, n) or (ic(p, o) == 6 and ic(p, n) in (1, 2)):
                    res = True
            if not res:
                return None
        s = 0.0
        if pat[t - 1] == 'h' and pb is not None and any(dissonant(pb, v) for k, v in pv if k != 'B'):
            s += 3.0
        dc = (c - pc_ + 6) % 12 - 6
        dd = (d - pd + 6) % 12 - 6
        if dc * dd < 0:
            s += 0.6
        if d == pd:
            s -= 1.2
        if abs(dc) > 4:
            s -= 0.3
        return s

    states = [beat_states(t) for t in range(8)]
    # k-best DP
    layer = {st: [(sc, (st,))] for st, sc in states[0]}
    for t in range(1, 8):
        new = {}
        for st, sc in states[t]:
            cands = []
            for pst, paths in layer.items():
                tr = trans(t, pst, st)
                if tr is None:
                    continue
                for psc, path in paths:
                    cands.append((psc + tr + sc, path + (st,)))
            if cands:
                new[st] = heapq.nlargest(a.k, cands, key=lambda x: x[0])
        layer = new
        print(f"beat {t + 1}: {len(layer)} live states", file=sys.stderr)
    allp = [p for paths in layer.values() for p in paths]
    allp.sort(key=lambda x: -x[0])
    nm = lambda v: '.' if v is None else NAMES[v]
    print(f"{len(allp)} complete skeletons kept; top {a.top}.  A B C D [chord] per beat")
    for sc, path in allp[:a.top]:
        cells = []
        for t, (b, c, d) in enumerate(path):
            snd = {A[t], c, d} | ({b} if b is not None else set())
            cells.append(f"{nm(A[t])} {nm(b) + ('~' if pat[t] == 'h' else '')} {nm(c)} {nm(d)} [{name_chord(snd) or '-'}]")
        print(f"{sc:5.1f}  " + ' | '.join(cells))


if __name__ == '__main__':
    main()
