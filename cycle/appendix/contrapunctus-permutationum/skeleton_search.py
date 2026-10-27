#!/usr/bin/env python3
"""Proposal tool (does not compose): beat-level skeletons for quadruple
invertible counterpoint over the B-A-C-H cantus.

Pitch-class search.  On every quarter beat the four lines must form a
fifth-free sonority (no P4/P5 between ANY pair, because every pair is
inverted somewhere in the 24 orderings); dissonant pairs must be prepared or
stepwise and resolve down by step; no consecutive unisons/octaves between
moving lines.  Prints the best-scoring skeletons so the composer can choose,
reject or rewrite them.  Octaves, passing notes and the real melodic shapes
are written by hand afterwards.

usage: skeleton_search.py [--pattern P1] [--top 30] [--minor]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from chords import chord_candidates, name_chord  # noqa: E402

NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
A_MAJ = [10, 10, 9, 9, 0, 0, 11, 11]
A_ATT = [1, 0, 1, 0, 1, 0, 1, 0]
# B rhythm patterns: per beat 'R' rest, 'a' attack, 'h' held from previous beat
PATTERNS = {
    'P1': 'Rahaaaha',   # R q h q | q h q
    'P2': 'Raaahaha',   # R q q h~|~ h q   (tie over barline)
    'P3': 'Rahahaha',   # 4th species
}


def ic(a, b):
    d = (a - b) % 12
    return min(d, 12 - d)


def dissonant(a, b):
    return ic(a, b) in (1, 2, 6)


def tertian(pcs):
    pcs = set(pcs)
    if len(pcs) == 1:
        return True
    if len(pcs) == 2:
        return True
    return bool(chord_candidates(pcs))


def search(pattern, diat, chroma, top, a_line):
    pat = PATTERNS[pattern]
    dom = sorted(set(diat) | set(chroma))
    results = []

    def step_down(x, y):
        return (x - y) % 12 in (1, 2)

    def step(x, y):
        return ic(x, y) in (1, 2)

    def check_beat(t, bt, ct, dt):
        snd = [a_line[t], ct, dt] + ([bt] if bt is not None else [])
        for i in range(len(snd)):
            for j in range(i + 1, len(snd)):
                if ic(snd[i], snd[j]) == 5:
                    return False
        return tertian(snd)

    best = []

    def rec(t, B, C, D, score):
        if t == 8:
            best.append((score, list(B), list(C), list(D)))
            return
        mode = pat[t]
        bopts = [None] if mode == 'R' else ([B[-1]] if mode == 'h' else dom)
        for bt in bopts:
            if mode == 'a' and B and B[-1] is not None:
                prevb = B[-1]
                # B: after a held (suspension) beat, must step down; else step or small leap
                if pat[t - 1] == 'h':
                    if not step_down(prevb, bt):
                        continue
                elif ic(prevb, bt) == 0 or ic(prevb, bt) > 5:
                    continue
            for ct in dom:
                if C and (ct == C[-1]):
                    continue
                for dt in dom:
                    if not check_beat(t, bt, ct, dt):
                        continue
                    s = score
                    # parallel octaves/unisons between moving voices
                    if t > 0:
                        prev = {'A': a_line[t - 1], 'B': B[-1], 'C': C[-1], 'D': D[-1]}
                        cur = {'A': a_line[t], 'B': bt, 'C': ct, 'D': dt}
                        moving = {k for k in cur if cur[k] is not None and prev[k] is not None and cur[k] != prev[k]}
                        bad = False
                        ks = sorted(moving)
                        for x in range(len(ks)):
                            for y in range(x + 1, len(ks)):
                                p, q = ks[x], ks[y]
                                if ic(prev[p], prev[q]) == 0 and ic(cur[p], cur[q]) == 0:
                                    bad = True
                        if bad:
                            continue
                        # dissonance treatment of beat t-1, now that t is known
                        pv = [(k, prev[k]) for k in prev if prev[k] is not None]
                        ok = True
                        for x in range(len(pv)):
                            for y in range(x + 1, len(pv)):
                                (k1, p1), (k2, p2) = pv[x], pv[y]
                                if not dissonant(p1, p2):
                                    continue
                                res = False
                                for k, p, other in ((k1, p1, p2), (k2, p2, p1)):
                                    nxt = cur[k]
                                    held_before = (k == 'B' and pat[t - 1] == 'h') or (k == 'A' and not A_ATT[t - 1])
                                    if k == 'A' and nxt == p:
                                        continue
                                    if nxt is not None and (step_down(p, nxt) or (ic(p, other) == 6 and step(p, nxt))):
                                        res = True
                                if not res:
                                    ok = False
                        if not ok:
                            continue
                        # scoring
                        if pat[t - 1] == 'h' and B[-1] is not None and \
                                any(dissonant(B[-1], v) for k, v in pv if k != 'B'):
                            s += 3  # real suspension on the held beat
                        if C[-1] is not None and D[-1] is not None:
                            dc = (ct - C[-1] + 6) % 12 - 6
                            dd = (dt - D[-1] + 6) % 12 - 6
                            if dc * dd < 0:
                                s += 0.6
                        if dt == D[-1]:
                            s -= 1.2
                    snd = {a_line[t], ct, dt} | ({bt} if bt is not None else set())
                    s += 0.8 * (len(snd) - 2)
                    if ct == dt:
                        s -= 1.0
                    if bt is not None and bt == a_line[t]:
                        s -= 1.0
                    for v in (bt, ct, dt):
                        if v is not None and v not in diat:
                            s -= 0.7
                    rec(t + 1, B + [bt], C + [ct], D + [dt], s)

    rec(0, [], [], [], 0.0)
    best.sort(key=lambda r: -r[0])
    return best[:top], len(best)


def show(r, a_line, pattern):
    score, B, C, D = r
    pat = PATTERNS[pattern]
    nm = lambda v: '.' if v is None else NAMES[v]
    rows = []
    for t in range(8):
        snd = {a_line[t], C[t], D[t]} | ({B[t]} if B[t] is not None else set())
        bass = None
        rows.append(f"{nm(a_line[t]):>2}{nm(B[t]) + ('~' if pat[t] == 'h' else ''):>4}{nm(C[t]):>4}{nm(D[t]):>4} "
                    f"[{name_chord(snd) or '-'}]")
    print(f"score {score:.1f}")
    print('   ' + ' | '.join(rows))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--pattern', default='P1')
    ap.add_argument('--top', type=int, default=25)
    ap.add_argument('--chroma', default='10,6')
    a = ap.parse_args()
    diat = [0, 2, 4, 5, 7, 9, 11]
    chroma = [int(x) for x in a.chroma.split(',')] if a.chroma else []
    res, n = search(a.pattern, diat, chroma, a.top, A_MAJ)
    print(f"{n} skeletons; best {len(res)}  (columns per beat: A B C D [chord])")
    for r in res:
        show(r, A_MAJ, a.pattern)
