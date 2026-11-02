#!/usr/bin/env python3
"""Texture metrics for XXIV, computed the same way as diagnosis/inspect_actual_texture.py
(slices between consecutive onsets/offsets), plus the critic's moving-voice count.

Usage: texture.py score.json [--window a-b (quarter beats)] [--bars a-b]
Reports: mean sounding parts, mean distinct pitches and pitch classes per slice,
pitch-class histogram, fraction of time with >=4 / >=5 pitch classes, attacks off the
quarter grid, within-part step/octave transitions, longest note, and the critic's
mean moving voices per bar over the window.
"""
import argparse, collections, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from critic import analyse  # noqa: E402


def clip(e, a, b):
    s = max(a, e['t']); z = min(b, e['t'] + e['d'])
    return None if z <= s else {'t': s, 'd': z - s, 'p': e['p']}


def stats(d, a, b):
    voices = d['voices']
    ee = [[f for e in v['events'] if (f := clip(e, a, b))] for v in voices]
    bounds = sorted({a, b} | {e['t'] for v in ee for e in v} | {e['t'] + e['d'] for v in ee for e in v})
    S = collections.Counter(); pcs_hist = collections.Counter(); parts_hist = collections.Counter()
    for x, y in zip(bounds, bounds[1:]):
        t = (x + y) / 2; dt = y - x
        ps = [e['p'] for v in ee for e in v if e['t'] <= t < e['t'] + e['d']]
        S['parts'] += len(ps) * dt; S['pitches'] += len(set(ps)) * dt
        npc = len({p % 12 for p in ps}); S['pcs'] += npc * dt; pcs_hist[npc] += dt
        parts_hist[len(ps)] += dt
        if npc >= 4: S['ge4'] += dt
        if npc >= 5: S['ge5'] += dt
    attacks = [e for v in voices for e in v['events'] if a <= e['t'] < b]
    frac = sum(abs(e['t'] - round(e['t'])) > 1e-7 for e in attacks)
    steps = octs = trans = 0
    for v in voices:
        evs = [e for e in v['events'] if a <= e['t'] < b]
        for p, q in zip(evs, evs[1:]):
            if abs(p['t'] + p['d'] - q['t']) < 1e-7:
                trans += 1; iv = abs(q['p'] - p['p'])
                steps += 1 <= iv <= 2; octs += iv == 12
    L = b - a
    longest = max(((e['d'], e['t'], i) for i, v in enumerate(ee) for e in v), default=(0, 0, 0))
    return {'quarter_beats': [a, b], 'mean_sounding_parts': round(S['parts'] / L, 2),
            'mean_distinct_pitches': round(S['pitches'] / L, 2), 'mean_distinct_pitch_classes': round(S['pcs'] / L, 2),
            'min_pitch_classes': min(k for k in pcs_hist if pcs_hist[k] > 0) if pcs_hist else 0,
            'share_ge4_pcs': round(S['ge4'] / L, 3), 'share_ge5_pcs': round(S['ge5'] / L, 3),
            'pcs_histogram_beats': {k: round(v, 2) for k, v in sorted(pcs_hist.items())},
            'note_attacks': len(attacks), 'off_quarter_attacks': frac,
            'transitions': trans, 'stepwise_transitions': steps, 'octave_transitions': octs,
            'longest_note_beats': longest[0], 'longest_note_at_beat': longest[1],
            'longest_note_voice': voices[longest[2]].get('name') if attacks else None}


def moving(d, bar_lo, bar_hi):
    R = analyse(d)
    rows = [r for r in R['texture'] if bar_lo <= r['bar'] <= bar_hi]
    return round(sum(r['moving'] for r in rows) / max(1, len(rows)), 2), [r['moving'] for r in rows], R


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('score'); ap.add_argument('--bars')
    a = ap.parse_args()
    d = json.load(open(a.score))
    m = d['metadata']['meter']; bq = m[0] * 4 / m[1]
    lo, hi = (int(x) for x in a.bars.split('-')) if a.bars else (1, int(max(e['t'] + e['d'] for v in d['voices'] for e in v['events']) // bq + 1))
    st = stats(d, (lo - 1) * bq, hi * bq)
    mv, rows, R = moving(d, lo, hi)
    st['mean_moving_voices_per_bar'] = mv; st['moving_per_bar'] = rows
    print(json.dumps(st, indent=1))
