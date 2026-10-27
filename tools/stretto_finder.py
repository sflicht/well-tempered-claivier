#!/usr/bin/env python3
"""Search for contrapuntal combinations of hand-written lines.

Proposes; never composes.  Given a subject (and optionally a second line such
as Bach's own subject), enumerate placements of a transformed copy against the
original: time offset, transposition (chromatic or diatonic), rectus/inversus,
augmentation/diminution.  Each candidate two-voice combination is scored with
the same critic used on finished scores (parallels, unresolved dissonance,
harsh beat intervals), so a composer can see which strettos, inversions and
canons the material genuinely permits.

Examples
  stretto_finder.py --subject "C5:4 B4:2 D5:2 G4:2 Eb5:2 G4:2 F5:2" --meter 4/4 \
      --scale C:minor --max-offset 16 --top 15
  stretto_finder.py --subject "..." --against "C#4:16 B#3:16 E4:16 D#4:16" \
      --scale C#:minor --forms rectus --scales-time 1,2
  stretto_finder.py --subject "..." --chain 4 --offsets 4,8,12 --levels 0,7,-5,12
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wtclib  # noqa: E402
from critic import analyse  # noqa: E402

MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 11]  # harmonic minor for inversion mapping
TONIC = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6,
         'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def line(tokens, start16=Fraction(0)):
    """tokens -> list of (start16, dur16, pitch) (rests skipped)."""
    out, u = [], Fraction(start16)
    for tok in tokens.split():
        p, d, sp, tie = wtclib.parse_tok(tok)
        if p is not None:
            out.append((u, d, p))
        u += d
    return out


def to_voice(notes, name):
    return {'name': name, 'abbr': name, 'events': [{'t': float(s / 4), 'd': float(d / 4), 'p': int(p)} for s, d, p in notes]}


def _deg(p, scale):
    """Absolute diatonic degree, octaves counted from the tonic (scale[0])."""
    t = scale[0]
    return ((p - t) // 12) * 7 + scale.index(p % 12)


def _pitch(j, scale, ref):
    """Inverse of _deg; ref is any pitch used to fix the octave frame."""
    t = scale[0]
    return t + (j // 7) * 12 + ((scale[j % 7] - t) % 12)


def diatonic_shift(p, steps, scale):
    pc = p % 12
    if pc not in scale:
        return None
    return _pitch(_deg(p, scale) + steps, scale, p)


def transform(notes, form, time_scale, offset16, shift, scale, axis, diatonic=True):
    out = []
    t0 = notes[0][0]
    for s, d, p in notes:
        q = p
        if form == 'inversus':
            q = 2 * axis - p if not diatonic else None
            if diatonic:
                pc = p % 12
                if pc in scale and axis % 12 in scale:
                    j = 2 * _deg(axis, scale) - _deg(p, scale)
                    q = _pitch(j, scale, p)
                else:
                    q = 2 * axis - p
        if diatonic:
            q2 = diatonic_shift(q, shift, scale)
            q = q2 if q2 is not None else q + round(shift * 12 / 7)
        else:
            q = q + shift
        out.append((offset16 + (s - t0) * Fraction(time_scale), d * Fraction(time_scale), q))
    return out


DISS_W = {0: .4, 1: 3, 2: 2, 3: 0, 4: 0, 5: 1, 6: 2, 7: .3, 8: 0, 9: 0, 10: 2, 11: 3}


def roughness(a, b, meter):
    """Duration- and metre-weighted dissonance per quarter of overlap."""
    bar16 = Fraction(meter[0] * 16, meter[1])
    times = sorted({s for s, _, _ in a} | {s for s, _, _ in b} | {s + d for s, d, _ in a} | {s + d for s, d, _ in b})

    def at(line_, t):
        for s, d, p in line_:
            if s <= t < s + d:
                return p
        return None
    tot = Fraction(0)
    span = Fraction(0)
    for t0, t1 in zip(times, times[1:]):
        pa, pb = at(a, t0), at(b, t0)
        if pa is None or pb is None:
            continue
        r = t0 % bar16
        strong = 2 if r == 0 else (1.5 if r % 4 == 0 else 1)
        tot += Fraction(DISS_W[abs(pa - pb) % 12]) * (t1 - t0) * Fraction(strong)
        span += t1 - t0
    return float(tot / span * 4) if span else 99.0, float(span / 4)


def score_pair(a, b, meter):
    data = {'metadata': {'meter': list(meter), 'bpm': 80}, 'voices': []}
    hi, lo = (a, b) if sum(p for *_, p in a) / len(a) >= sum(p for *_, p in b) / len(b) else (b, a)
    data['voices'] = [to_voice(hi, 'A'), to_voice(lo, 'B')]
    R = analyse(data)
    s = R['summary']
    harsh = sum(1 for x in R['dissonance'] if x['kind'] in ('UNPREPARED+UNRESOLVED', 'UNRESOLVED (held)'))
    weak_par = s['parallels_weak']
    crossings = s['crossings']
    rough, overlap = roughness(a, b, meter)
    cost = 10 * s['parallels_error'] + 6 * harsh + 2 * weak_par + 1 * crossings + round(4 * rough)
    return cost, s['parallels_error'], harsh, weak_par, crossings, round(rough, 2), overlap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--subject', required=True)
    ap.add_argument('--against', help='a second line to place the subject against (default: the subject itself)')
    ap.add_argument('--meter', default='4/4')
    ap.add_argument('--scale', default='C:major', help='tonic:major|minor for diatonic transposition/inversion')
    ap.add_argument('--forms', default='rectus,inversus')
    ap.add_argument('--scales-time', default='1', help='comma list of time factors for the moving copy, e.g. 1,2,0.5')
    ap.add_argument('--max-offset', type=int, default=16, help='max entry distance in sixteenths')
    ap.add_argument('--offset-step', type=int, default=2)
    ap.add_argument('--steps', default=','.join(str(x) for x in range(-14, 15)),
                    help='diatonic transposition steps for the copy (7 = octave)')
    ap.add_argument('--axis', help='inversion axis pitch name, e.g. G4 (default: first note)')
    ap.add_argument('--top', type=int, default=20)
    ap.add_argument('--min-overlap', type=float, default=2.0, help='minimum overlap in quarters')
    ap.add_argument('--json')
    a = ap.parse_args()
    meter = tuple(int(x) for x in a.meter.split('/'))
    tonic, mode = a.scale.split(':')
    scale = [(TONIC[tonic] + x) % 12 for x in (MAJOR if mode == 'major' else MINOR)]
    scale = sorted(scale, key=lambda pc: (pc - TONIC[tonic]) % 12)
    subj = line(a.subject)
    base = line(a.against) if a.against else subj
    axis = wtclib.parse_tok(a.axis + ':1')[0] if a.axis else subj[0][2]
    res = []
    for form in a.forms.split(','):
        for ts in [Fraction(x) for x in a.scales_time.split(',')]:
            for off in range(0, a.max_offset + 1, a.offset_step):
                if off == 0 and not a.against and form == 'rectus' and ts == 1:
                    continue
                for st in [int(x) for x in a.steps.split(',')]:
                    cand = transform(subj, form, ts, Fraction(off), st, scale, axis)
                    cost = score_pair(base, cand, meter)
                    res.append((cost, form, float(ts), off, st))
    res.sort(key=lambda r: (r[0][0], r[3]))
    res = [r for r in res if r[0][6] >= a.min_overlap]
    print(f"{'cost':>5} {'par':>3} {'dis':>3} {'wpar':>4} {'x':>3} {'rough':>6} {'ovl':>5}  form      time  offset16  steps")
    for (cost, par, dis, wp, x, rough, ovl), form, ts, off, st in res[:a.top]:
        print(f"{cost:5d} {par:3d} {dis:3d} {wp:4d} {x:3d} {rough:6.2f} {ovl:5g}  {form:9s} {ts:4g}  {off:8d}  {st:+d}")
    if a.json:
        Path(a.json).write_text(json.dumps([{'cost': r[0][0], 'parallels': r[0][1], 'unresolved': r[0][2], 'roughness': r[0][5], 'overlap_q': r[0][6],
                                             'form': r[1], 'time': r[2], 'offset16': r[3], 'steps': r[4]} for r in res], indent=1))


if __name__ == '__main__':
    main()
