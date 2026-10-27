#!/usr/bin/env python3
"""Search aid for the canon per tempora.

The composer fixes the rhythm of M, the Westminster chime that opens it, the
vocabulary of everything after it (Westminster 'changes', i.e. the chime's
own 4-note cells, rectus or inverted, sung in running eighths) and any anchor
notes (e.g. the cadence).  The search only chooses, cell by cell, WHICH change
on WHICH degree, so that the four-speed canon passes the same dissonance and
parallel rules as tools/critic.py.  It prints ranked candidates; the composer
chooses and edits by hand in tempo_canon.py.  It writes nothing.

    python3 tempo_search.py [--beam 300] [--show 6]
"""
import argparse
import bisect
import itertools
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from chords import chord_candidates  # noqa: E402

E_MAJOR = [0, 2, 4, 5, 7, 9, 11]
BASE = 64  # degree 0 = E4 (M is notated in the alto's register)


def deg2midi(d):
    return BASE + E_MAJOR[d % 7] + 12 * (d // 7)


SHAPES = {'c1': [0, -1, -2, -5], 'c2': [0, 2, 1, -3], 'c3': [0, 1, 2, 0],
          'c4': [0, -2, -1, -5], 'c5': [0, 4, 5, 3]}
SHAPES.update({k + 'i': [-x for x in v] for k, v in list(SHAPES.items())})
SHAPES.update({'up': [0, 1, 2, 3], 'dn': [0, -1, -2, -3]})
PENALTY = {'up': 1, 'dn': 1}
# Shorter cells: heads and tails of the changes, plus plain intervals.
SHAPES3 = {}
for k, v in list(SHAPES.items()):
    SHAPES3[k + 'h'] = v[:3]
    SHAPES3[k + 't'] = [x - v[1] for x in v[1:]]
SHAPES2 = {f'i{n}': [0, n] for n in (-7, -4, -3, -2, -1, 1, 2, 3, 4, 7)}
SHAPES1 = {'n': [0]}
VOCAB = {4: SHAPES, 3: SHAPES3, 2: SHAPES2, 1: SHAPES1}

RATIOS = [4, 3, 2, 1]                    # bass, tenor, alto, soprano
OCT = {4: -24, 3: -12, 2: 0, 1: 12}
SEVENTHS = {'7', 'o7', 'ø7', 'm7', 'maj7', '7(no5)', 'm(no5)7'}

E4, Fs4, Gs4, B3 = 64, 66, 68, 59
CHIME = [(E4, 2), (Gs4, 2), (Fs4, 2), (B3, 6), (E4, 2), (Fs4, 2), (Gs4, 2), (E4, 6),
         (Gs4, 2), (E4, 2), (Fs4, 2), (B3, 6), (B3, 2), (Fs4, 2), (Gs4, 2), (E4, 6)]


def dissonant(lo, hi, lo_is_bass):
    c = abs(hi - lo) % 12
    return c in (1, 2, 6, 10, 11) or (c == 5 and lo_is_bass)


class Problem:
    def __init__(self, rhythm, final=E4):
        self.rhythm = rhythm                      # list of cells, each a list of durations
        self.ncells = len(rhythm)
        self.n0 = len(CHIME)
        self.cstart = list(itertools.accumulate([self.n0] + [len(c) for c in rhythm]))
        self.durs = [d for _, d in CHIME] + [d for c in rhythm for d in c]
        self.N = len(self.durs) + 1                     # + final note (no duration)
        self.final = final
        self.starts = list(itertools.accumulate([0] + self.durs))
        self.L = sum(self.durs)
        self.T = max(RATIOS) * self.L
        self.events = []
        for t in range(0, self.T, 4):
            cur = []
            for r in RATIOS:
                s = self.T - r * self.L
                if t < s:
                    continue
                x = Fraction(t - s, r)
                k = bisect.bisect_right(self.starts, x) - 1
                cur.append((r, k, self.starts[k] * r + s == t))
            if len(cur) >= 2 and any(a for _, _, a in cur):
                self.events.append((t, cur))
        self.ready = {}
        for e in self.events:
            last = max(self.cell(min(k + 1, self.N - 1)) for _, k, _ in e[1])
            self.ready.setdefault(last, []).append(e)
        self.pairs = {}
        for i in range(1, len(self.events)):
            c0, c1 = self.events[i - 1][1], self.events[i][1]
            last = max(self.cell(k) for _, k, _ in c0 + c1)
            self.pairs.setdefault(last, []).append((c0, c1))

    def cell(self, k):
        if k < self.n0 or k >= self.cstart[-1]:
            return -1          # chime and final note are fixed
        return bisect.bisect_right(self.cstart, k) - 1

    def p(self, notes, k, r):
        return notes[k] + OCT[r]

    def cost_events(self, notes, evs):
        bad = soft = 0
        for t, cur in evs:
            items = sorted((self.p(notes, k, r), r, k, a) for r, k, a in cur)
            pcs = {x[0] % 12 for x in items}
            cands = chord_candidates(pcs, items[0][0] % 12)
            seventh = bool(cands) and cands[0][1] in SEVENTHS
            for x in range(len(items)):
                for y in range(x + 1, len(items)):
                    lo, rlo, klo, alo = items[x]
                    hi, rhi, khi, ahi = items[y]
                    if not dissonant(lo, hi, x == 0):
                        continue
                    if not (alo or ahi):
                        continue
                    if cands and (seventh or abs(hi - lo) % 12 in (5, 6)):
                        soft += 1
                        continue
                    nlo = notes[klo + 1] + OCT[rlo] if klo + 1 < self.N else None
                    nhi = notes[khi + 1] + OCT[rhi] if khi + 1 < self.N else None
                    step = lambda a, b: b is not None and 1 <= abs(b - a) <= 2
                    if alo != ahi:
                        held_next, held = (nhi, hi) if alo else (nlo, lo)
                        new_next, new = (nlo, lo) if alo else (nhi, hi)
                        ok = step(held, held_next) or step(new, new_next)
                    else:
                        ok = step(lo, nlo) or step(hi, nhi)
                    if ok:
                        soft += 1
                    else:
                        bad += 1
        return 10 * bad + soft

    def cost_par(self, notes, pairs):
        c = 0
        for c0, c1 in pairs:
            d0 = {r: self.p(notes, k, r) for r, k, a in c0}
            d1 = {r: self.p(notes, k, r) for r, k, a in c1}
            for ra, rb in itertools.combinations(sorted(set(d0) & set(d1)), 2):
                a0, b0, a1, b1 = d0[ra], d0[rb], d1[ra], d1[rb]
                if a0 == a1 or b0 == b1:
                    continue
                i0, i1 = (a0 - b0) % 12, (a1 - b1) % 12
                if i0 == i1 and i0 in (0, 7) and (a1 - a0) * (b1 - b0) > 0:
                    c += 10
        return c


def search(rhythm, plan, beam=300, show=6, lo=-4, hi=8, start_deg=0, seed=None):
    """plan[ci] = set of pitch classes allowed for the cell's first note (chord
    tones of the composer's harmonic plan), optionally ('end', degrees)."""
    P = Problem(rhythm)
    n_free = P.cstart[-1] - P.n0
    notes0 = [p for p, _ in CHIME] + [None] * n_free + [P.final]
    base = P.cost_events(notes0, P.ready.get(-1, [])) + P.cost_par(notes0, P.pairs.get(-1, []))
    states = [(base, notes0, [], start_deg)]
    for ci in range(P.ncells):
        n = len(rhythm[ci])
        want = plan.get(ci, {})
        nxt = []
        for cost, notes, ch, lastd in states:
            if seed and ci < len(seed):
                options = [(seed[ci][0], VOCAB[n][seed[ci][0]], [seed[ci][1]])]
            else:
                options = [(nm, shp, range(lo, hi + 1)) for nm, shp in VOCAB[n].items()]
            for name, shp, degs in options:
                for d0 in degs:
                    ds = [d0 + x for x in shp]
                    if min(ds) < lo or max(ds) > hi:
                        continue
                    if 'end' in want and ds[-1] not in want['end']:
                        continue
                    step = abs(d0 - lastd)
                    if step > 4 or step == 0:
                        continue
                    nn = list(notes)
                    for j, d in enumerate(ds):
                        nn[P.cstart[ci] + j] = deg2midi(d)
                    c = cost + PENALTY.get(name, 0) + (step > 2) + 2 * (step > 3)
                    if 'pcs' in want and deg2midi(d0) % 12 not in want['pcs']:
                        c += 4
                    if ch and ch[-1][0] == name:
                        c += 1
                    c += P.cost_events(nn, P.ready.get(ci, [])) + P.cost_par(nn, P.pairs.get(ci, []))
                    nxt.append((c, nn, ch + [(name, d0)], ds[-1]))
        nxt.sort(key=lambda s: s[0])
        seen, states = set(), []
        for st in nxt:
            key = tuple(st[2][-3:])
            if key in seen:
                continue
            seen.add(key)
            states.append(st)
            if len(states) >= beam:
                break
    out = sorted(((c, nt, ch) for c, nt, ch, _ in states), key=lambda s: s[0])
    return P, out[:show]


def describe(notes, P):
    names = {0: 'E', 2: 'F#', 4: 'G#', 5: 'A', 7: 'B', 9: 'C#', 11: 'D#'}
    from chords import pname
    toks = []
    for k in range(P.n0, P.cstart[-1]):
        toks.append(f'{pname(notes[k])}:{P.durs[k]}')
    return ' '.join(toks)


# Composer's rhythm for M after the chime (sixteenths; one list per cell)
RHYTHM = [[2, 2, 2, 2], [2, 2, 2, 2], [4, 2, 2],          # M3  I -> vi
          [2, 2, 2, 2], [2, 2, 4], [2, 2, 2, 2],          # M4  IV -> ii -> V
          [4, 2, 2], [2, 2, 2, 2], [4, 4],                # M5  V
          [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 4],          # M6  V7
          [4, 2, 2], [2, 2, 2, 2], [4, 4],                # M7  I
          [2, 2, 2, 2], [4, 2, 2], [2, 2, 2, 2]]          # M8  I (V) I -> final E
I, VI, IV, II, V, V7 = {4, 8, 11}, {1, 4, 8}, {9, 1, 4}, {6, 9, 1}, {11, 3, 6}, {11, 3, 6, 9}
PLAN = {0: {'pcs': I}, 1: {'pcs': I}, 2: {'pcs': VI}, 3: {'pcs': IV}, 4: {'pcs': II}, 5: {'pcs': V},
        6: {'pcs': V}, 7: {'pcs': V}, 8: {'pcs': V}, 9: {'pcs': V7}, 10: {'pcs': V7}, 11: {'pcs': V7},
        12: {'pcs': I}, 13: {'pcs': I}, 14: {'pcs': IV}, 15: {'pcs': I}, 16: {'pcs': V},
        17: {'pcs': I, 'end': [-3, 4, -1, 6]}}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--beam', type=int, default=300)
    ap.add_argument('--show', type=int, default=6)
    a = ap.parse_args()
    P, best = search(RHYTHM, PLAN, a.beam, a.show)
    for cost, notes, ch in best:
        print(cost, ' '.join(f'{n}@{d}' for n, d in ch))
        print('   ', describe(notes, P))
