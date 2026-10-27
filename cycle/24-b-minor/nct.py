#!/usr/bin/env python3
"""Plan-aware non-chord-tone check.  The score's 'harmonic_plan' lists
[start_beat, end_beat, [pitch classes], label]: the composer's intended harmony.
Every sounding note whose pitch class is outside the planned chord at a quarter-beat
point (or at its own attack) is classified as suspension/retardation, passing, neighbour,
appoggiatura, escape tone, anticipation, or UNRESOLVED.

Usage: nct.py score.json [--bars a-b] [--list]"""
import argparse, collections, json, sys
sys.path.insert(0, '/home/user/well-tempered-claivier/tools')
from chords import pname


def chord_at(plan, t):
    for a, b, pcs, lab in plan:
        if a <= t + 1e-9 < b:
            return set(pcs), lab
    return None, None


def classify(evs, k, t, plan):
    n = evs[k]
    prev = evs[k - 1] if k > 0 and n['t'] - (evs[k - 1]['t'] + evs[k - 1]['d']) <= 1.0 + 1e-9 else None
    nxt = evs[k + 1] if k + 1 < len(evs) and evs[k + 1]['t'] - (n['t'] + n['d']) <= 1.0 + 1e-9 else None
    p = n['p']
    step = lambda a, b: 1 <= abs(a - b) <= 2
    def ok_next():
        if not nxt:
            return False
        c, _ = chord_at(plan, nxt['t'])
        return c is not None and (nxt['p'] % 12 in c or True)
    if n['t'] < t - 1e-9:                      # held into a new harmony
        if nxt and step(p, nxt['p']) and nxt['t'] <= t + 3.0 + 1e-9:
            return 'suspension' if nxt['p'] < p else 'retardation'
        if nxt and nxt['p'] == p:
            return 'held-anticipation'
        return 'UNRESOLVED held'
    if nxt and nxt['p'] == p:
        c, _ = chord_at(plan, nxt['t'])
        if c and p % 12 in c:
            return 'anticipation'
    c2, _ = chord_at(plan, n['t'] + n['d'] - 0.01)
    if c2 and p % 12 in c2 and n['t'] + n['d'] - t > 0.5:
        return 'anticipation (held into the next harmony)'
    if prev and nxt and step(prev['p'], p) and step(p, nxt['p']):
        return 'passing' if (p - prev['p']) * (nxt['p'] - p) > 0 else 'neighbour'
    if nxt and step(p, nxt['p']):
        return 'appoggiatura'
    if prev and step(prev['p'], p) and nxt and n['d'] <= 0.5 + 1e-9 and (nxt['p'] - p) * (p - prev['p']) < 0:
        return 'escape'
    if n['d'] <= 0.25 + 1e-9 and ((prev and step(prev['p'], p)) or (nxt and step(p, nxt['p']))):
        return 'passing (16th)'
    return 'UNRESOLVED'


def guest_spans(d):
    spans = []
    for th in d.get('themes', []):
        if th['key'] in ('FI', 'II', 'IV', 'V', 'VIII'):
            spans.append((th['voice'], th['t']))
    return spans


def run(d, lo=None, hi=None):
    plan = d.get('harmonic_plan', [])
    out = []
    gs = guest_spans(d)
    for v in d['voices']:
        evs = sorted(v['events'], key=lambda e: e['t'])
        for k, n in enumerate(evs):
            pts = sorted({n['t']} | {float(x) for x in range(int(n['t']) + 1, int(n['t'] + n['d'] - 1e-9) + 1)})
            pts = [x for x in pts if x < n['t'] + n['d'] - 1e-9]
            seen = set()
            for t in pts:
                c, lab = chord_at(plan, t)
                if c is None or n['p'] % 12 in c or lab in seen:
                    continue
                seen.add(lab)
                bar = int(t // 4) + 1
                if lo and not (lo <= bar <= hi):
                    continue
                kind = classify(evs, k, t, plan)
                if kind.startswith('UNRES') and any(gv == v['abbr'] and gt <= n['t'] < gt + 8 for gv, gt in gs):
                    kind = 'quoted guest note (free)'
                out.append({'voice': v['abbr'], 'bar': bar, 'beat': t % 4 + 1, 'pitch': pname(n['p']),
                            'chord': lab, 'kind': kind})
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('score'); ap.add_argument('--bars'); ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    d = json.load(open(a.score))
    lo, hi = (int(x) for x in a.bars.split('-')) if a.bars else (None, None)
    res = run(d, lo, hi)
    print('NCT kinds:', dict(collections.Counter(r['kind'] for r in res)))
    for r in res:
        if a.list or r['kind'].startswith('UNRES'):
            print(f"  b{r['bar']}.{r['beat']:g} {r['voice']} {r['pitch']} over {r['chord']}: {r['kind']}")
