"""Evaluate hand-written alternative fragments for one voice segment in the convergence test.
Score = 10*parallel errors + 3*beat parallels + 2*weak parallels + 4*plan-unresolved NCTs + same-move dups
(within a bar window).  The candidates are written by the composer; this only ranks them."""
import json, sys, collections
from fractions import Fraction as Fr
sys.path.insert(0, '.'); sys.path.insert(0, '/home/user/well-tempered-claivier/tools')
from xxiv import *
from critic import analyse
import nct as NCT
from conv_a import part_a, plan_a
from conv_b import part_b, plan_b
from conv_c import part_c, plan_c

NB = 14


def build(sc):
    bars = sc.bars(NB)
    voices = [{'name': n, 'abbr': n, 'events': W.events_for(bars[n], METER)} for n, _, _ in VOICES]
    return {'metadata': {'meter': [4, 4], 'bpm': 60, 'key': 'B', 'mode': 'minor'}, 'voices': voices,
            'harmonic_plan': plan_a(0) + plan_b(20) + plan_c(36),
            'themes': [{'voice': v, 't': float(t / 4), 'label': l, 'key': k, 'scale': s, 'semis': se, 'inverted': inv}
                       for v, t, l, k, s, se, inv in sc.entries]}


def dups(d, lo, hi):
    V = [(v['abbr'], sorted(v['events'], key=lambda e: e['t'])) for v in d['voices']]
    times = sorted({e['t'] for _, evs in V for e in evs if (lo - 1) * 4 <= e['t'] < hi * 4})
    n = 0
    for t in times:
        moves = collections.Counter()
        for nm, evs in V:
            for k, e in enumerate(evs):
                if e['t'] == t and k > 0 and e['t'] - (evs[k-1]['t'] + evs[k-1]['d']) <= 1 and evs[k-1]['p'] != e['p']:
                    moves[(evs[k-1]['p'] % 12, e['p'] % 12, (e['p'] > evs[k-1]['p']))] += 1
        n += sum(c - 1 for c in moves.values() if c > 1)
    return n


def score(d, lo, hi):
    R = analyse(d, (lo, hi))
    pe = sum(1 for x in R['parallels'] if x['sev'] in ('error', 'doubling'))
    pw = sum(1 for x in R['parallels'] if x['sev'] == 'warn')
    bp = len(R['beat_parallels'])
    un = sum(1 for r in NCT.run(d, lo, hi) if r['kind'].startswith('UNRES'))
    du = dups(d, lo, hi)
    return 10 * pe + 3 * bp + 2 * pw + 4 * un + du, (pe, bp, pw, un, du)


def base():
    sc = Score(1); part_a(sc, 1); part_b(sc, 1); part_c(sc, 1)
    return sc


def try_alts(voice, bar, beat, alts, lo, hi):
    out = []
    for a in alts:
        sc = base()
        pos = sc.pos(bar, beat)
        segs = [s for s in sc.segs[voice] if s[0] != pos]
        if len(segs) == len(sc.segs[voice]):
            raise KeyError(f'no segment for {voice} at {bar}.{beat}')
        sc.segs[voice] = segs + [(pos, ' '.join(a.split()))]
        try:
            d = build(sc)
        except ValueError as e:
            out.append((999, str(e), a)); continue
        sco, parts = score(d, lo, hi)
        out.append((sco, parts, a))
    for sco, parts, a in sorted(out, key=lambda x: x[0]):
        print(f'{sco:5} {parts}  {a}')


if __name__ == '__main__':
    sc = base(); d = build(sc)
    lo, hi = (int(x) for x in sys.argv[1].split('-'))
    print('current', score(d, lo, hi))
