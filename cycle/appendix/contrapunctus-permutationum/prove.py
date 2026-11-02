#!/usr/bin/env python3
"""Proof of quadruple invertible counterpoint at the octave.

Places the four hand-written lines of lines.py in all 24 vertical orderings
(by octave transposition only) in both modes, and runs tools/critic.py's
analyse() on each, plus two strict checks the critic does not make:

  beat4    a perfect fourth between the lowest sounding note and any other
           note at a quarter-beat onset (a "fourth against the bass")
  beat5    any perfect fifth/fourth between two lines at a quarter-beat onset
           (a structural fifth; it becomes beat4 in some other ordering)

usage: prove.py [--mode major|minor|both] [--detail ABCD] [--table]
"""
import argparse
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / 'tools'))
sys.path.insert(0, str(HERE))
import wtclib  # noqa: E402
from critic import analyse, Score, TPQ, print_report  # noqa: E402
import lines as L  # noqa: E402

METER = (4, 4)


def notes_of(tokens, shift=0):
    out, u = [], 0
    for tok in tokens.split():
        p, d, sp, tie = wtclib.parse_tok(tok)
        if p is not None:
            out.append((u, d, p + shift))
        u += d
    return out


def place(order, mode, gap=None):
    """order: string top->bottom e.g. 'DCBA'.  Returns {line: octave shift}
    so that each line sits above the one below it with the fewest crossings
    (ties: closest spacing)."""
    src = L.LINES[mode]
    shifts = {}
    below = None
    for name in reversed(order):
        base = notes_of(src[name])
        if below is None:
            # bottom line: put its lowest note around C3-G3
            lo = min(p for _, _, p in base)
            k = round((50 - lo) / 12)
            shifts[name] = 12 * k
        else:
            bnotes = notes_of(src[below], shifts[below])
            best = None
            for k in range(-4, 5):
                cand = notes_of(src[name], 12 * k)
                cross = 0
                for (s, d, p) in cand:
                    for (s2, d2, q) in bnotes:
                        if s < s2 + d2 and s2 < s + d and p < q:
                            cross += 1
                mean_gap = sum(p for *_, p in cand) / len(cand) - sum(q for *_, q in bnotes) / len(bnotes)
                key = (cross, mean_gap if mean_gap > 0 else 99)
                if best is None or key < best[0]:
                    best = (key, k)
            shifts[name] = 12 * best[1]
        below = name
    return shifts


def score_for(order, mode, shifts=None):
    src = L.LINES[mode]
    shifts = shifts or place(order, mode)
    voices = []
    for i, name in enumerate(order):
        toks = wtclib.transpose(src[name], shifts[name], 7 * shifts[name] // 12)
        evs = wtclib.events_for(wtclib.concat_bars(toks, METER), METER)
        voices.append({'name': f"{i + 1}:{name}", 'abbr': name, 'events': evs})
    return {'metadata': {'title': order, 'meter': list(METER), 'bpm': 84,
                         'key': 'C', 'mode': mode}, 'voices': voices}


def strict(data):
    S = Score(data)
    b4, b5 = [], []
    for t in S.onsets:
        if t % S.beat:
            continue
        snd = S.sounding(t)
        items = sorted((S.note(i, k)['p'], i, k, att) for i, (k, att) in snd.items())
        if len(items) < 2:
            continue
        bass = items[0]
        for x in range(len(items)):
            for y in range(x + 1, len(items)):
                lo, hi = items[x], items[y]
                if not (lo[3] or hi[3]):
                    continue
                c = (hi[0] - lo[0]) % 12
                if c in (5, 7):
                    rec = f"{S.loc(t)} {S.names[lo[1]]}/{S.names[hi[1]]} {'P4' if c == 5 else 'P5'}"
                    b5.append(rec)
                    if x == 0 and c == 5:
                        b4.append(rec)
    return b4, b5


def run(mode, detail=None, quiet=False):
    rows = []
    for perm in itertools.permutations('ABCD'):
        order = ''.join(perm)
        data = score_for(order, mode)
        R = analyse(data)
        s = R['summary']
        b4, b5 = strict(data)
        unres = [x for x in R['dissonance'] if x['sev'] == 'error']
        weak7 = [x for x in R['dissonance'] if x['sev'] == 'note']
        pe = [x for x in R['parallels'] if x['sev'] in ('error', 'warn')]
        pc = [x for x in R['parallels'] if x['sev'] == 'note']
        bp = [x for x in R.get('beat_parallels', []) if x['sev'] != 'doubling']
        rows.append({'order': order, 'par_err': s['parallels_error'], 'par_weak': s['parallels_weak'],
                     'beat_par': len(bp), 'tripled': s.get('pc_tripled_on_beats_pct', 0),
                     'contrary': len(pc), 'unresolved': s['dissonance_unresolved'], 'seventh_note': len(weak7),
                     'beat4': len(b4), 'beat5': len(b5), 'crossings': s['crossings'],
                     'kinds': s['dissonance_kinds'], 'unres_list': [f"{x['loc']} {x['kind']} {x['what']}" for x in unres],
                     'par_list': [f"{x['loc']} {x['voices']} {x['kind']} {x['what']}" for x in pe + pc + bp],
                     'b4_list': b4, 'b5_list': b5, 'ranges': R['ranges'],
                     'melody': s['melody']})
        if detail == order:
            print_report(R)
            print('beat4:', b4)
            print('beat5:', b5)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', default='both')
    ap.add_argument('--detail')
    ap.add_argument('--json', type=Path)
    ap.add_argument('-v', action='store_true')
    a = ap.parse_args()
    modes = ['major', 'minor'] if a.mode == 'both' else [a.mode]
    out = {}
    for m in modes:
        rows = run(m, a.detail)
        out[m] = rows
        tot = {k: sum(r[k] for r in rows) for k in ('par_err', 'par_weak', 'beat_par', 'contrary', 'unresolved', 'beat4', 'beat5', 'seventh_note')}
        print(f"== {m}: totals {tot}")
        for r in rows:
            flag = '' if not (r['par_err'] or r['unresolved'] or r['beat4'] or r['beat_par']) else '  <-- FIX'
            print(f"  {r['order']}  par_err {r['par_err']} weak {r['par_weak']} beatpar {r['beat_par']} contrary {r['contrary']} "
                  f"unres {r['unresolved']} beat4 {r['beat4']} 7th-note {r['seventh_note']} cross {r['crossings']}{flag}")
            if a.v or flag:
                for x in r['unres_list'] + r['par_list'] + r['b4_list']:
                    print('       ', x)
        b5 = sorted({x.split(' ', 1)[0] + ' ' + x.split(' ')[-1] for r in rows for x in r['b5_list']})
        if b5:
            print('  structural 4ths/5ths on beats (any pair):', b5[:20])
    if a.json:
        a.json.write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
