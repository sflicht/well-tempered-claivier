#!/usr/bin/env python3
"""Performance tuning for Prelude IX: adaptive 5-limit just intonation (the comma pump),
then Bach-Lehman for the coda.

Tuning is performance, not composition: this script never changes a written note.  It reads
prelude.json (built by prelude.py) and the harmonic analysis stored in it
(metadata['harmony'], written by hand in prelude.py as CYCLE_HARMONY / CODA_HARMONY), and adds a
'cents' field (offset from equal temperament) to every note.  Render the result with
`render_music.py --temperament equal`, so that only these cents apply.  It also writes
prelude-tempered.json (the same notes without cents) for comparison renders in a keyboard
temperament.

THE RULES (in this order)
1. Every chord is tuned pure: from its root, major third 5/4 (386.3 c), minor third 6/5 (315.6 c),
   fifth 3/2 (702.0 c); the seventh of a minor-seventh chord 9/5 (1017.6 c, a pure minor third above
   the fifth); the seventh of a dominant-seventh chord 16/9 (996.1 c) unless it is prepared.
2. Common tones keep their pitch.  When the chord changes, every pitch class that belongs to both
   chords is a pivot: the new chord's root is placed so that the pivot (as root, third or fifth of
   the new chord) keeps exactly the pitch it had.  A prepared seventh (a pitch class sounding in the
   previous chord) keeps its pitch too.  If several pivots disagree, the script says so (it never
   happens in this piece).  In the music the pivots are literally held or repeated (S, A, T and B
   tie G#, C#, E, F#, A and B across the barlines of the antecedent), so the rule "any tone held or
   repeated across a chord change keeps its pitch" is the musical reality, not a convention.
3. With no common tone (IV -> V), the root moves by the pure interval of the root progression
   (a whole tone 9/8, a fifth 3/2, ...).
4. Non-chord tones (passing, neighbour, appoggiatura) take the 5-limit interval above the root of
   the chord they sound against (9/8, 4/3, 5/3, 15/8, 16/15 ...).  A note that repeats the previous
   note of its voice without a gap keeps that note's pitch (rule 2 again).  A note held across a
   chord change is a single event and keeps its pitch by construction.
5. The first chord's E is placed at Bach-Lehman's E (-1.96 c), so the opening tonic and the final
   tempered tonic are the same pitch.  From metadata['tuning']['just_until_q'] on (the coda), every
   note takes the Bach-Lehman offset of its pitch class, computed from
   tools/render_music.py temperament_offsets('bach-lehman').
6. The musette drone (voice 'Drone') is a fixed-pitch instrument: it always takes the Bach-Lehman
   offset, so it stays at the opening pitch while the rest of the consort sinks away from it.  Its
   growing mismatch with the tonic is the point, so it is left out of the purity check.

WHY IT DRIFTS
I -> vi keeps E and G#, so C# lands a pure major sixth above E (5/3).  vi -> ii7 keeps C# (and E, the
seventh), so F# lands a pure fifth below C# = 10/9 above E, the 'grave' second.  ii7 -> V7 keeps F#
and A, so B is a pure fourth above that F#: 40/27, a syntonic comma (81/80, 21.5 c) below the 3/2
fifth.  V -> I keeps B, so the new tonic is a comma flat.  The consequent (I - IV - I6/4 - V7 - I)
closes without drift, so each cycle of the theme sinks by exactly one comma.

Usage: python3 tune_prelude.py            (tunes prelude.json in place, prints the drift report)
"""
from __future__ import annotations

import copy
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import render_music as rm  # noqa: E402


def c(ratio):
    return 1200.0 * math.log2(ratio)


SYNTONIC = c(81 / 80)
# chord-tone templates: interval in semitones above the root -> just ratio
TEMPLATES = {'': {0: 1, 4: 5 / 4, 7: 3 / 2},
             'm': {0: 1, 3: 6 / 5, 7: 3 / 2},
             '7': {0: 1, 4: 5 / 4, 7: 3 / 2, 10: 16 / 9},
             'm7': {0: 1, 3: 6 / 5, 7: 3 / 2, 10: 9 / 5}}
SEVENTH = {'7': 10, 'm7': 10}
# 5-limit intervals for non-chord tones and for root motion without a common tone
FIVE_LIMIT = {0: 1, 1: 16 / 15, 2: 9 / 8, 3: 6 / 5, 4: 5 / 4, 5: 4 / 3, 6: 45 / 32, 7: 3 / 2, 8: 8 / 5,
              9: 5 / 3, 10: 16 / 9, 11: 15 / 8}
PCS = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
LEHMAN = rm.temperament_offsets('bach-lehman')     # cents from ET, pitch classes C..B, A = 0


def dev(i, ratio):
    """Deviation from equal temperament (cents) of a just interval spanning i semitones."""
    return c(ratio) - 100.0 * i


def parse_chord(sym):
    root = PCS[sym[0]]
    k = 1
    while k < len(sym) and sym[k] in '#b':
        root += 1 if sym[k] == '#' else -1
        k += 1
    return root % 12, sym[k:]


def tune_chords(chart, t_end_just):
    """Return a list of segments: (t0, t1, root_pc, quality, root_offset, {pc: offset}, how)."""
    segs = []
    prev = None
    for idx, (t0, sym) in enumerate(chart):
        t1 = chart[idx + 1][0] if idx + 1 < len(chart) else float('inf')
        if t0 >= t_end_just:
            break
        r, q = parse_chord(sym)
        tmpl = TEMPLATES[q]
        cons = {i: ratio for i, ratio in tmpl.items() if i != SEVENTH.get(q)}
        if prev is None:
            R, how = LEHMAN[r], 'anchor: root at its Bach-Lehman pitch'
        else:
            _, _, pr, pq, pR, poff, _ = prev
            cands = []
            for i, ratio in cons.items():
                pc = (r + i) % 12
                if pc in poff:
                    cands.append((poff[pc] - dev(i, ratio), NAMES[pc]))
            if cands:
                spread = max(x for x, _ in cands) - min(x for x, _ in cands)
                if spread > 0.01:
                    print(f'  ! conflicting pivots at t={t0}: {cands}')
                R, how = cands[0][0], 'pivot ' + ', '.join(n for _, n in cands)
            elif q in SEVENTH and (r + SEVENTH[q]) % 12 in poff:
                i = SEVENTH[q]
                R, how = poff[(r + i) % 12] - dev(i, tmpl[i]), 'pivot: prepared seventh'
            else:
                step = (r - pr) % 12
                R, how = pR + dev(step, FIVE_LIMIT[step]), f'no common tone: root moves by {FIVE_LIMIT[step]}'
        off = {}
        for i, ratio in tmpl.items():
            pc = (r + i) % 12
            off[pc] = R + dev(i, ratio)
        if q in SEVENTH and prev is not None:          # a prepared seventh keeps its pitch
            pc7 = (r + SEVENTH[q]) % 12
            if pc7 in prev[5]:
                off[pc7] = prev[5][pc7]
        seg = (t0, t1, r, q, R, off, how)
        segs.append(seg)
        prev = seg
    return segs


def tune(data):
    meta = data['metadata']
    chart = [(float(t), ch) for t, ch in meta['harmony']]
    t_just = float(meta['tuning']['just_until_q'])
    segs = tune_chords(chart, t_just)

    def seg_at(t):
        for s in segs:
            if s[0] <= t < s[1]:
                return s
        return None

    stats = {'chord_tones': 0, 'non_chord_tones': 0, 'kept_by_repetition': 0, 'repetition_conflicts': 0,
             'tempered': 0}
    for v in data['voices']:
        prev = None
        for e in sorted(v['events'], key=lambda e: e['t']):
            t, p = float(e['t']), int(e['p'])
            pc = p % 12
            if v['name'] == 'Drone':
                e['cents'] = round(LEHMAN[pc], 3)
                stats['drone'] = stats.get('drone', 0) + 1
                continue
            if t >= t_just:
                e['cents'] = round(LEHMAN[pc], 3)
                stats['tempered'] += 1
                prev = e
                continue
            s = seg_at(t)
            t0, t1, r, q, R, off, _ = s
            if pc in off:
                val = off[pc]
                stats['chord_tones'] += 1
            else:
                i = (pc - r) % 12
                ratio = FIVE_LIMIT[i] if not (i == 10 and q.startswith('m')) else 9 / 5
                val = R + dev(i, ratio)
                stats['non_chord_tones'] += 1
            if prev is not None and int(prev['p']) == p and abs(float(prev['t']) + float(prev['d']) - t) < 1e-9 \
                    and 'cents' in prev:
                if abs(prev['cents'] - val) > 0.01:
                    stats['repetition_conflicts'] += 1
                val = prev['cents']
                stats['kept_by_repetition'] += 1
            e['cents'] = round(val, 3)
            prev = e
    return segs, stats


JUST = [0, c(16 / 15), c(9 / 8), c(6 / 5), c(5 / 4), c(4 / 3), c(45 / 32), c(3 / 2), c(8 / 5), c(5 / 3), c(9 / 5), c(15 / 8)]


def purity(data, segs):
    """Largest deviation from a pure interval between two chord tones sounding together in a chord."""
    worst = 0.0
    where = None
    notes = [(float(e['t']), float(e['t']) + float(e['d']), int(e['p']), e['cents'])
             for v in data['voices'] if v['name'] != 'Drone' for e in v['events']]
    for t0, t1, r, q, R, off, how in segs:
        triad = {(r + i) % 12 for i in TEMPLATES[q] if i != SEVENTH.get(q)}
        times = sorted({t0} | {n[0] for n in notes if t0 <= n[0] < t1})
        for t in times:
            snd = [n for n in notes if n[0] <= t < n[1] and n[2] % 12 in triad]
            for a in snd:
                for b in snd:
                    if b[2] <= a[2]:
                        continue
                    iv = (100 * (b[2] - a[2]) + b[3] - a[3]) % 1200
                    d = min(abs(iv - j) for j in (0, JUST[3], JUST[4], JUST[5], JUST[7], JUST[8], JUST[9], 1200))
                    if d > worst:
                        worst, where = d, (t, NAMES[a[2] % 12], NAMES[b[2] % 12])
    return worst, where


def report(segs, data):
    e_offsets = [(s[0], s[5][4]) for s in segs if s[2] == 4]
    first = e_offsets[0][1]
    print('Cumulative drift of the tonic E (cents relative to the opening E; syntonic comma = %.2f c)' % SYNTONIC)
    print('  %-26s %-10s %-10s %s' % ('cycle', 'starts', 'ends', 'drift in this cycle'))
    rows = []
    for k in range(4):
        start = [o for t, o in e_offsets if abs(t - 48 * k) < 1e-6][0]
        end = [o for t, o in e_offsets if abs(t - (48 * k + 42)) < 1e-6][0]
        rows.append((k + 1, start - first, end - first, end - start))
        print('  %-26s %+8.2f   %+8.2f   %+8.2f' % (f'{k + 1} (bars {8 * k + 1}-{8 * k + 8})', start - first, end - first, end - start))
    coda = LEHMAN[4] - (first)
    print('  %-26s %+8.2f   (Bach-Lehman E = %+.2f c from ET; the opening E was placed there)' % ('coda (bars 33-36)', coda, LEHMAN[4]))
    print('  the correction at bar 33: the tonic jumps up by %.2f c' % (LEHMAN[4] - (first + rows[-1][2])))
    e2 = 440.0 * 2 ** ((40 - 69) / 12) * 2 ** (LEHMAN[4] / 1200)      # the drone, E2 at its Bach-Lehman pitch
    print('  the drone (E2, fixed at %+.2f c) against the tonic at each cycle start: beat rate on its octave partial' % LEHMAN[4])
    for k, a, b, d in rows:
        print('    cycle %d: tonic %+7.2f c from the drone, E3 beats against the drone at %.1f Hz' % (
            k, a, abs(2 * e2 * (2 ** (a / 1200) - 1))))
    return rows


def main():
    path = HERE / 'prelude.json'
    data = json.loads(path.read_text())
    for v in data['voices']:
        for e in v['events']:
            e.pop('cents', None)
    tempered = copy.deepcopy(data)
    segs, stats = tune(data)
    print('Chord-by-chord tuning (root offset from equal temperament, and why):')
    for t0, t1, r, q, R, off, how in segs:
        bar = int(t0 // 6) + 1
        beat = (t0 % 6) / 1.5 + 1
        print(f'  b{bar}.{beat:g}  {NAMES[r] + q:6s} root {R:+8.2f} c   {how}')
    rows = report(segs, data)
    worst, where = purity(data, segs)
    print(f'Purity check: largest deviation of a root/third/fifth interval from just = {worst:.3f} c', where or '')
    print('Notes:', stats)
    data['metadata']['tuning_report'] = {
        'method': 'adaptive 5-limit just intonation with common tones kept (tune_prelude.py), Bach-Lehman coda',
        'drift_by_cycle': [{'cycle': k, 'tonic_start_c': round(a, 2), 'tonic_end_c': round(b, 2), 'drift_c': round(d, 2)}
                           for k, a, b, d in rows],
        'purity_max_dev_c': round(worst, 3), 'notes': stats}
    path.write_text(json.dumps(data, indent=1))
    tempered['metadata']['subtitle'] += ' (tempered comparison: same notes, no cents)'
    tempered['metadata'].pop('tuning', None)
    (HERE / 'prelude-tempered.json').write_text(json.dumps(tempered, indent=1))
    print('wrote prelude.json (with cents) and prelude-tempered.json (no cents)')


if __name__ == '__main__':
    main()
