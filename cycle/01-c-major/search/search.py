#!/usr/bin/env python3
"""Mutation search for a subject that strettos at every distance 8..1 eighths.

Usage: search.py [--iters N] [--restarts R] [--seed S] [--out results.json]

The objective is   sum(best rung cost) + 1.5*max(best rung cost)
                 + melodic penalty + character penalty
where 'character' encodes the brief's demands (upbeat, clear head with a leap,
a longer or syncopated note, some sixteenths, no closing tonic at the end).
The output is a ranked list of CANDIDATES for a composer to read; the final
subject is chosen and edited by hand.
"""
from __future__ import annotations

import argparse
import json
import math
import random

from ladder import ladder, melodic_penalty, parse, to_tokens, semi

SEEDS = [
    (14, "G4:2 C5:4 G4:2 A4:1 B4:1 C5:2 D5:2 E5:2 F5:3 E5:1 D5:2 C5:2 B4:2 C5:2 D5:2"),
    (14, "G4:2 C5:2 C5:1 D5:1 E5:2 C5:2 G5:4 F5:1 E5:1 D5:1 C5:1 B4:2 G4:2 A4:2 B4:2 C5:2 D5:2"),
    (2, "C4:2 D4:2 E4:2 F4:3 G4:1 F4:2 E4:2 A4:2 D4:2 G4:3 F4:1 E4:2"),
    (14, "G4:2 E5:4 D5:1 C5:1 B4:2 C5:2 G4:2 A4:2 F4:2 G4:2 E4:2 F4:1 G4:1 A4:2 B4:2 C5:2"),
    (12, "C5:2 G4:2 C5:2 D5:2 E5:4 C5:2 F5:2 E5:2 D5:1 C5:1 D5:2 G4:2 A4:1 B4:1 C5:2 D5:2"),
    (10, "G4:1 A4:1 B4:2 C5:6 D5:2 E5:2 C5:2 A4:2 F5:2 D5:2 B4:2 C5:1 D5:1 E5:2"),
]


def total_len(notes):
    return sum(d for d, _ in notes)


def valid_rhythm(notes, p0):
    durs = [d for d, _ in notes]
    if any(d not in (1, 2, 3, 4, 6) for d in durs):
        return False
    L = sum(durs)
    if not (24 <= L <= 32) or len(durs) < 12:
        return False
    t = p0
    for k, d in enumerate(durs):
        if t % 2 == 1 and d != 1:
            return False
        if d == 3 and (t % 2 == 1 or k + 1 >= len(durs) or durs[k + 1] != 1):
            return False
        if d >= 4 and t % 2 == 1:
            return False
        t += d
    if t % 2:
        return False
    if sum(1 for d in durs if d >= 4) > 3 or durs.count(6) > 1:
        return False
    if durs.count(1) < 2 or durs.count(1) > 10:
        return False
    if any(not (-3 <= g <= 12) for _, g in notes):
        return False
    return True


def valid_melody(notes, p0):
    degs = [g for _, g in notes]
    sem = [semi(g) for g in degs]
    iv = [sem[k + 1] - sem[k] for k in range(len(sem) - 1)]
    a = [abs(x) for x in iv]
    n = len(iv)
    if sum(1 for x in a if 1 <= x <= 2) < 0.5 * n:
        return False                      # mostly conjunct
    if sum(1 for x in a if x == 0) > 1:
        return False
    if sum(1 for x in a if x >= 7) > 2 or any(x > 12 for x in a):
        return False
    if any(x in (6, 10, 11) for x in a):
        return False
    for k in range(n - 1):
        if a[k] >= 5 and not (iv[k + 1] * iv[k] < 0 or a[k + 1] <= 2):
            return False                  # leaps of a 4th+ are recovered
        if a[k] >= 3 and a[k + 1] >= 3 and k + 2 < n and a[k + 2] >= 3:
            return False                  # no three leaps in a row
    rng_ = max(degs) - min(degs)
    if not (6 <= rng_ <= 10):
        return False
    if degs[0] % 7 not in (0, 4):
        return False
    t = p0
    for d, g in notes:
        if t + d > 16:
            if g % 7 not in (0, 2, 4):
                return False
            break
        t += d
    if degs[-1] % 7 == 0:
        return False
    return True


def character(notes, p0):
    pen = 0.0
    durs = [d for d, _ in notes]
    degs = [g for _, g in notes]
    sem = [semi(g) for g in degs]
    # the first note on/over the first downbeat should be a tonic triad tone
    t = p0
    for d, g in notes:
        if t + d > 16:
            if g % 7 not in (0, 2, 4):
                pen += 6
            break
        t += d
    if degs[0] % 7 not in (4, 0):
        pen += 3                      # upbeat on G or C
    head = [abs(sem[k + 1] - sem[k]) for k in range(min(5, len(sem) - 1))]
    if max(head) < 5:
        pen += 6
    if degs[-1] % 7 == 0:
        pen += 6
    if durs[-1] >= 4:
        pen += 5
    # syncopation bonus: a long note entering on an eighth off-beat
    t = p0
    sync = False
    for d, g in notes:
        if t % 4 == 2 and d >= 4:
            sync = True
        t += d
    if sync:
        pen -= 3
    run = 1
    for k in range(1, len(durs)):
        run = run + 1 if durs[k] == durs[k - 1] else 1
        if run >= 5:
            pen += 2
    rep = sum(1 for k in range(1, len(degs)) if degs[k] == degs[k - 1])
    pen += 2.5 * max(0, rep - 1)
    rng_ = max(degs) - min(degs)
    if rng_ < 6:
        pen += 3 * (6 - rng_)
    leaps = [abs(sem[k + 1] - sem[k]) for k in range(len(sem) - 1)]
    if sum(1 for x in leaps if x >= 5) > 4:
        pen += 3 * (sum(1 for x in leaps if x >= 5) - 4)
    if sum(1 for x in leaps if x >= 8) > 1:
        pen += 6
    if any(x > 12 for x in leaps):
        pen += 20
    if degs.count(max(degs)) > 2:
        pen += 3
    return pen


def objective(notes, p0, detail=False):
    L = ladder(notes, p0, keep=1)
    best = [L[d][0][0] for d in range(1, 9)]
    mel, _ = melodic_penalty(notes, p0)
    ch = character(notes, p0)
    val = sum(best) + 1.5 * max(best) + mel + ch
    if detail:
        return val, L, mel, ch
    return val


def mutate(notes, rng):
    n = list(notes)
    op = rng.random()
    k = rng.randrange(len(n))
    d, g = n[k]
    if op < .40:
        n[k] = (d, g + rng.choice((-2, -1, 1, 2)))
    elif op < .52 and k + 1 < len(n):
        s = rng.choice((-1, 1))
        n[k] = (d, g + s)
        n[k + 1] = (n[k + 1][0], n[k + 1][1] + s)
    elif op < .62 and d >= 2 and d % 2 == 0:
        h = d // 2
        n[k:k + 1] = [(h, g), (h, g + rng.choice((-1, 1, -2, 2)))]
    elif op < .72 and k + 1 < len(n) and n[k][0] == n[k + 1][0] and n[k][0] in (1, 2):
        n[k:k + 2] = [(2 * d, g)]
    elif op < .80 and k + 1 < len(n) and n[k][0] == 2 and n[k + 1][0] == 2:
        n[k], n[k + 1] = (3, g), (1, n[k + 1][1])
    elif op < .86 and k + 1 < len(n) and (n[k][0], n[k + 1][0]) == (3, 1):
        n[k], n[k + 1] = (2, g), (2, n[k + 1][1])
    elif op < .92:
        # transpose a segment
        j = rng.randrange(k, len(n))
        s = rng.choice((-1, 1))
        for i in range(k, j + 1):
            n[i] = (n[i][0], n[i][1] + s)
    elif op < .94 and k + 2 < len(n) and n[k][0] == 2 and n[k + 1][0] == 2 and n[k + 2][0] == 2:
        n[k:k + 3] = [(2, g), (4, n[k + 1][1])]
    elif op < .96 and len(n) > 8:
        del n[k]
        if k < len(n):
            n[k] = (n[k][0] + d, n[k][1])
        else:
            n[-1] = (n[-1][0] + d, n[-1][1])
    else:
        n.insert(k + 1, (2, g + rng.choice((-1, 1))))
    return n


def anneal(p0, notes, iters, rng, T0=6.0):
    cur = list(notes)
    tries = 0
    while not (valid_rhythm(cur, p0) and valid_melody(cur, p0)):
        cur = mutate(cur, rng) if tries % 200 else list(notes)
        tries += 1
        if tries > 200000:
            raise RuntimeError('cannot repair seed')
    cv = objective(cur, p0)
    best, bv = cur, cv
    for i in range(iters):
        T = T0 * (1 - i / iters) + .05
        cand = mutate(cur, rng)
        if not valid_rhythm(cand, p0) or not valid_melody(cand, p0):
            continue
        v = objective(cand, p0)
        if v <= cv or rng.random() < math.exp((cv - v) / T):
            cur, cv = cand, v
            if v < bv:
                best, bv = cand, v
    return bv, best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--iters', type=int, default=3000)
    ap.add_argument('--restarts', type=int, default=12)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--out', default='results.json')
    a = ap.parse_args()
    rng = random.Random(a.seed)
    found = {}
    for r in range(a.restarts):
        p0, s = SEEDS[r % len(SEEDS)]
        notes = parse(s)
        bv, best = anneal(p0, notes, a.iters, rng)
        key = (p0, to_tokens(best))
        found[key] = bv
        print(f"{bv:7.2f}  p0={p0:2d}  {to_tokens(best)}", flush=True)
    res = sorted(((v, p0, t) for (p0, t), v in found.items()))
    out = []
    for v, p0, t in res:
        val, L, mel, ch = objective(parse(t), p0, detail=True)
        out.append({'value': v, 'p0': p0, 'subject': t, 'melodic': mel, 'character': ch,
                    'ladder': {d: L[d][0] for d in L}})
    try:
        old = json.load(open(a.out))
    except Exception:
        old = []
    allr = {(o['p0'], o['subject']): o for o in old + out}
    json.dump(sorted(allr.values(), key=lambda o: o['value']), open(a.out, 'w'), indent=1)


if __name__ == '__main__':
    main()
