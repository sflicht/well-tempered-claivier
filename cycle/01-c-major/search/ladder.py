"""Fast two-voice stretto-ladder evaluator for Fugue I (C major).

A candidate subject is (p0, notes): p0 = metric position of the first note in
sixteenths (0..15 within a 4/4 bar), notes = [(dur16, degree)], degree being a
diatonic index in the C-major collection with C4 = 0.

For every entry distance d (in eighths, 1..8) the follower is placed d eighths
after the leader, as rectus (deg + shift) or inversus (-deg + shift), and the
overlap is scored for: same-direction parallel perfect intervals (any onset),
contrary-motion perfect repeats, dissonances that are neither passing,
neighbour, suspension nor appoggiatura, raw roughness (duration x metric
weight), unisons and voice crossing.  It is stricter than tools/critic.py
(which only examines beats); finalists are re-checked with the real critic.

This module PROPOSES; it never writes a note into the score.
"""
from __future__ import annotations

MAJ = [0, 2, 4, 5, 7, 9, 11]
LET = 'CDEFGAB'


def semi(deg: int) -> int:
    return 60 + 12 * (deg // 7) + MAJ[deg % 7]


def name(deg: int) -> str:
    return f"{LET[deg % 7]}{4 + deg // 7}"


def to_tokens(notes):
    return ' '.join(f"{name(g)}:{d}" for d, g in notes)


def parse(tokstr):
    out = []
    for tok in tokstr.split():
        n, d = tok.split(':')
        L, o = n[0], int(n[-1])
        out.append((int(d), LET.index(L) + 7 * (o - 4)))
    return out


DISS = {1, 2, 5, 6, 10, 11}          # 4th counts as dissonant in two parts
PERF = {0, 7}
ROUGH = {1: 1.0, 2: .8, 5: .45, 6: .7, 10: .8, 11: 1.0}


def strength(t):
    r = t % 16
    if r == 0:
        return 3
    if r == 8:
        return 2.5
    if r % 4 == 0:
        return 2
    if r % 2 == 0:
        return 1
    return 0


def place(notes, start, form='rectus', shift=0):
    out = []
    t = start
    for d, g in notes:
        q = g + shift if form == 'rectus' else -g + shift
        out.append((t, t + d, q, semi(q)))
        t += d
    return out


def _index(line, t0, t1):
    idx = {}
    for k, (s, e, g, p) in enumerate(line):
        for t in range(max(s, t0), min(e, t1)):
            idx[t] = k
    return idx


def _step(a, b):
    return 1 <= abs(a - b) <= 2


def pair_cost(A, B, detail=False):
    """A, B: placed lines (lists of (s, e, deg, semi)).  Returns (cost, notes)."""
    t0 = max(A[0][0], B[0][0])
    t1 = min(A[-1][1], B[-1][1])
    if t1 <= t0:
        return 0.0, []
    ia, ib = _index(A, t0, t1), _index(B, t0, t1)
    upper_is_A = None
    cost = 0.0
    why = []
    prev = None
    for t in range(t0, t1):
        ka, kb = ia.get(t), ib.get(t)
        if ka is None or kb is None:
            prev = None
            continue
        na, nb = A[ka], B[kb]
        pa, pb = na[3], nb[3]
        ic = abs(pa - pb) % 12
        st = strength(t)
        # roughness / crossing / unison on every sixteenth slice
        if ic in DISS:
            cost += ROUGH[ic] * (1.4 if st >= 2 else (1.0 if st == 1 else .6)) * .8
        if pa == pb:
            cost += 1.0
        side = pa > pb
        if upper_is_A is None and pa != pb:
            upper_is_A = side
        elif pa != pb and side != upper_is_A:
            cost += 1.5
            if detail:
                why.append((t, 'cross'))
        att_a, att_b = na[0] == t, nb[0] == t
        if not (att_a or att_b):
            continue
        # parallels
        if prev is not None:
            ppa, ppb, pt = prev
            if pa != ppa and pb != ppb:
                pic = abs(ppa - ppb) % 12
                if pic in PERF and ic == pic:
                    same = (pa - ppa) * (pb - ppb) > 0
                    if same:
                        c = 60 if (t % 2 == 0 and pt % 2 == 0) else 30
                        cost += c
                        if detail:
                            why.append((t, f'parallel {"8" if ic == 0 else "5"}'))
                    else:
                        cost += 6
                        if detail:
                            why.append((t, 'contrary perfect'))
        prev = (pa, pb, t)
        if ic not in DISS:
            continue
        # dissonance treatment
        lines = ((A, ka, att_a), (B, kb, att_b))

        def nbrs(L, k):
            pv = L[k - 1] if k > 0 and L[k - 1][1] == L[k][0] else None
            nx = L[k + 1] if k + 1 < len(L) and L[k + 1][0] == L[k][1] else None
            return pv, nx

        def passing(L, k):
            pv, nx = nbrs(L, k)
            return pv is not None and nx is not None and _step(pv[3], L[k][3]) and _step(L[k][3], nx[3])

        def leaves_by_step(L, k):
            _, nx = nbrs(L, k)
            return nx is not None and _step(L[k][3], nx[3])

        c = 0.0
        if att_a and att_b:
            if passing(A, ka) or passing(B, kb):
                c = 4 if st >= 2 else 1
            elif leaves_by_step(A, ka) or leaves_by_step(B, kb):
                c = 9 if st >= 2 else 5
            else:
                c = 30
        else:
            (X, kx, _), (Y, ky, _) = (lines[0], lines[1]) if att_a else (lines[1], lines[0])
            # X attacked now, Y held
            ny = Y[ky]
            _, ynext = nbrs(Y, ky)
            susp = ynext is not None and (ynext[3] - ny[3]) in (-1, -2) and ynext[0] - t <= 8
            if passing(X, kx):
                c = 3 if st >= 2 else 0.5
            elif susp and st >= 1:
                c = 0.5
            elif leaves_by_step(X, kx):
                c = 8 if st >= 2 else 4
            elif ynext is not None and _step(ny[3], ynext[3]) and ynext[0] - t <= 4:
                c = 6  # held note moves away by step soon (retardation-like)
            else:
                c = 30
        cost += c
        if detail and c >= 4:
            why.append((t, f'diss ic{ic} c{c}'))
    return cost, why


def rung(notes, p0, d, form, shift, detail=False):
    A = place(notes, p0)
    B = place(notes, p0 + 2 * d, form, shift)
    return pair_cost(A, B, detail)


SHIFTS = list(range(-11, 12))


def head_ok(notes, form, s):
    """False if the shift turns the head's first interval into a tritone."""
    a, b = notes[0][1], notes[1][1]
    if form == 'rectus':
        x, y = a + s, b + s
    else:
        x, y = s - a, s - b
    return abs(semi(x) - semi(y)) != 6


def ladder(notes, p0, dists=range(1, 9), forms=('rectus', 'inversus'), shifts=SHIFTS, keep=3):
    """For each distance, the best `keep` (cost, form, shift) placements."""
    res = {}
    for d in dists:
        cands = []
        for form in forms:
            for s in shifts:
                if form == 'rectus' and s == 0:
                    continue
                if not head_ok(notes, form, s):
                    continue
                c, _ = rung(notes, p0, d, form, s)
                # mild preference for useful intervals (8ve, 5th, 4th) in rectus
                cands.append((round(c, 2), form, s))
        cands.sort()
        res[d] = cands[:keep]
    return res


def melodic_penalty(notes, p0):
    pen = 0.0
    why = []
    degs = [g for _, g in notes]
    sem = [semi(g) for g in degs]
    rng = max(degs) - min(degs)
    if rng > 10:
        pen += 4 * (rng - 10)
        why.append('range')
    for k in range(1, len(sem)):
        iv = sem[k] - sem[k - 1]
        a = abs(iv)
        if a == 6:
            pen += 8
            why.append('tritone')
        if a in (10, 11) or a > 12:
            pen += 8
            why.append('7th/compound')
        if a >= 5 and k + 1 < len(sem):
            iv2 = sem[k + 1] - sem[k]
            if iv2 * iv > 0 and abs(iv2) > 2:
                pen += 3
                why.append('leap continue')
            if iv2 * iv > 0 and abs(iv2) <= 2 and a >= 7:
                pen += 1.5
        if iv == 0:
            pen += 0.5
    # avoid more than 5 notes moving the same direction stepwise? (runs are fine)
    return pen, why
