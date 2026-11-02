#!/usr/bin/env python3
"""Prelude VIII in E-flat minor (third edition), 12/8.

Rebuilt on the texture of the first-draft "Night loom" prelude that Sam liked
(editions/complete-cycle/baseline/scores/08-prelude-eflat-minor.json, and its
second-edition melody revision): a slow cantabile over a continuous inner
eighth-note figure and a bass.  Kept from that draft: the separation of time
scales, the inner figure's opening shape (Eb F Gb Bb Eb Gb, draft b1), the
falling-and-returning arc (second edition b1-2: Bb Ab Gb, Gb embellished,
reaching Ab and returning) and the held upper note across a change of harmony
(draft b10-11).  Kept from the French-overture v1: the G-flat arrival (v1 b8),
the circle of secondary dominants (v1 b9-12), the deceptive i6/4-V7-VI-iv
approach (v1 b13-14) and the half-cadence attacca with a tirade (v1 b15-16).

New: the melody IS the fugue subject in retrograde inversion
(Eb F D Cb Bb Ab Gb Ab Eb) -- its segment Bb Ab Gb Ab is the draft's arc --
and in bars 14-17 the bass sings that melody while the soprano sings it in
G-flat major a tenth (plus octaves) above.  The fugue's bass returns the same
line in bars 45-47 under Bach's own subject.  The last bar's bass is the
subject's head, E-flat B-flat C-flat B-flat, leading attacca into the fugue.

Every pitch is written here.  The inner figure is written as six-note
half-bar groups of eighths (the helper only appends the eighth-note value).
Playable by one pianist: right hand = melody (+ figure where marked by
register), left hand = bass (+ figure in bars 14-17).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (12, 8)


def f(*halves):
    """Inner figure: each argument is six pitch names (one half bar of eighths)."""
    return ' '.join(f'{p}:2' for h in halves for p in h.split())


B = W.Bars(['Melody', 'Figure', 'Bass'], METER)
# ---------------------------------------------------------------- phrase 1: the retrograde inversion, e-flat (b1-4)
B.bar('1 i | V', Melody='Eb5:12 F5:6 D5:6',
      Figure=f('Eb4 F4 Gb4 Bb4 Eb4 Gb4', 'D4 F4 Ab4 F4 D4 F4'), Bass='Eb2:12 Bb1:12')
B.bar('2 VI | iv (9-8 in the melody)', Melody='Cb5:12 Bb4:6 Ab4:6',
      Figure=f('Cb4 Eb4 Gb4 Eb4 Cb4 Eb4', 'Ab3 Cb4 Eb4 Cb4 Ab3 Cb4'), Bass='Cb2:12 Ab1:12')
B.bar('3 i6 | i: the falling-and-returning arc', Melody='Gb4:2 F4:2 Gb4:2 Ab4:6 Gb4:12',
      Figure=f('Gb3 Bb3 Eb4 Bb3 Gb3 Bb3', 'Eb3 Gb3 Bb3 Gb3 Eb3 Gb3'), Bass='Gb2:12 Eb2:12')
B.bar('4 iv | i', Melody='Ab4:12 Eb5:12',
      Figure=f('Cb4 Eb4 Ab3 Eb4 Cb4 Eb4', 'Gb4 Bb4 Gb4 Bb4 Eb4 Bb4'), Bass='Ab1:12 Gb2:12')
# ---------------------------------------------------------------- phrase 2: the same line in G-flat major (b5-8)
B.bar('5 III | V7/III', Melody='Gb5:12 Ab5:6 F5:6',
      Figure=f('Gb4 Bb4 Db5 Bb4 Gb4 Bb4', 'F4 Ab4 Cb5 Ab4 F4 Ab4'), Bass='Gb2:12 Db2:12')
B.bar('6 IV | V7', Melody='Eb5:12 Db5:6 Cb5:6',
      Figure=f('Cb4 Eb4 Gb4 Eb4 Cb4 Eb4', 'F4 Ab4 Db4 Ab4 F4 Ab4'), Bass='Cb2:12 Db2:12')
B.bar('7 I6 | vi', Melody='Bb4:2 Ab4:2 Bb4:2 Cb5:6 Bb4:12',
      Figure=f('Bb3 Db4 Gb4 Db4 Bb3 Db4', 'Bb3 Eb4 Gb4 Eb4 Bb3 Eb4'), Bass='Bb1:12 Eb2:12')
B.bar('8 V7 | I: the G-flat arrival', Melody='Cb5:12 Gb5:12',
      Figure=f('F4 Ab4 Db4 F4 Ab4 F4', 'Gb4 Bb4 Db5 Bb4 Gb4 Db5'), Bass='Db2:12 Gb2:12')
# ---------------------------------------------------------------- phrase 3: circle of fifths, held notes become 7ths (b9-13)
B.bar('9 Cb | ab', Melody='Gb5:12 F5:6 Eb5:6',
      Figure=f('Eb4 Gb4 Cb5 Gb4 Eb4 Gb4', 'Ab4 Cb5 Eb4 Cb5 Ab4 Eb4'), Bass='Cb2:12 Ab1:12')
B.bar('10 F7/A | bb: E-flat held as the 7th', Melody='Eb5:12 Db5:12',
      Figure=f('F4 A4 C5 A4 F4 A4', 'Db4 F4 Bb4 F4 Db4 F4'), Bass='A1:12 Bb1:12')
B.bar('11 Eb7/G | ab: D-flat held as the 7th', Melody='Db5:12 Cb5:12',
      Figure=f('Eb4 G4 Bb4 G4 Eb4 G4', 'Cb4 Eb4 Ab4 Eb4 Cb4 Eb4'), Bass='G1:12 Ab1:12')
B.bar('12 VI | ii-half-dim7', Melody='Cb5:6 Bb4:6 Ab4:12',
      Figure=f('Eb4 Gb4 Eb4 Cb4 Eb4 Gb4', 'F3 Ab3 Cb4 Ab3 F3 Ab3'), Bass='Cb2:12 F2:12')
B.bar('13 V7 | V: half cadence', Melody='Ab4:12 Bb4:6 D5:6',
      Figure=f('Bb3 D4 F4 D4 Bb3 D4', 'F3 Bb3 D4 Bb3 F3 Bb3'), Bass='Bb1:12 D2:12')
# ---------------------------------------------------------------- phrase 4: the bass sings the line; the soprano sings it in G-flat (b14-17)
B.bar('14 i | ii-dim | V6 (bass = retrograde inversion)', Melody='Gb5:12 Ab5:6 F5:6',
      Figure=f('Gb3 Bb3 Eb4 Bb3 Gb3 Bb3', 'Ab3 Cb4 Ab3 Bb3 D4 Bb3'), Bass='Eb3:12 F3:6 D3:6')
B.bar('15 VI | i6/4 | iv', Melody='Eb5:12 Db5:6 Cb5:6',
      Figure=f('Gb3 Cb4 Eb4 Cb4 Gb3 Cb4', 'Gb3 Bb3 Db4 Ab3 Cb4 Eb4'), Bass='Cb3:12 Bb2:6 Ab2:6')
B.bar('16 i6 | iv | i6', Melody='Bb4:2 Ab4:2 Bb4:2 Cb5:6 Bb4:12',
      Figure=f('Bb3 Eb4 Bb3 Ab3 Cb4 Eb4', 'Eb4 Gb3 Bb3 Gb3 Eb4 Gb3'), Bass='Gb2:2 F2:2 Gb2:2 Ab2:6 Gb2:12')
B.bar('17 iv | i', Melody='Cb5:12 Gb5:12',
      Figure=f('Cb4 Eb4 Ab3 Eb4 Cb4 Ab3', 'Gb3 Bb3 Eb4 Gb4 Eb4 Bb3'), Bass='Ab2:12 Eb3:12')
# ---------------------------------------------------------------- phrase 5: i6/4 - V7 - deceptive VI - iv - V, tirade, attacca (b18-21)
B.bar('18 i6/4 | V7', Melody='Gb5:12 F5:12',
      Figure=f('Eb4 Gb4 Bb4 Gb4 Eb4 Gb4', 'D4 F4 Ab4 F4 D4 F4'), Bass='Bb2:12 Bb1:12')
B.bar('19 VI (deceptive) | iv', Melody='Eb5:6 Gb5:6 Cb5:12',
      Figure=f('Cb4 Eb4 Gb4 Eb4 Gb4 Eb4', 'Cb4 Eb4 Ab4 Eb4 Cb4 Eb4'), Bass='Cb2:12 Ab1:12')
B.bar('20 V | V7(b9): rising tirade to the ninth, the high point C-flat6', Melody='D5:6 F5:6 D5:1 Eb5:1 F5:1 Gb5:1 Ab5:1 Bb5:1 Cb6:6',
      Figure=f('Bb3 D4 F4 D4 F4 D4', 'Bb3 D4 F4 D4 Bb3 Ab3'), Bass='Bb1:12 Bb2:12')
# (Nov 2026) the figure starts an octave lower, E-flat3 (was E-flat4), and rises unbroken to A-flat4:
# the downbeat is struck E-flat2 E-flat3 | B-flat5, one hand each, instead of three registers at once.
B.bar('21 bass = the fugue subject head Eb Bb Cb Bb; half cadence, attacca', Melody='Bb5:6 Ab5:6 Gb5:6 D5:6',
      Figure=f('Eb3 Gb3 Bb3 D4 F4 Ab4', 'Eb4 Gb4 Eb4 F4 D4 F4'), Bass='Eb2:6 Bb2:6 Cb3:6 Bb2:6')

DYN = {1: -4, 5: 0, 8: 4, 9: 0, 13: -2, 14: 2, 17: 4, 18: 6, 19: 2, 20: 6, 21: 4}


def dyn(b):
    v = 0
    for k in sorted(DYN):
        if b + 1 >= k:
            v = DYN[k]
    return v


if __name__ == '__main__':
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Prelude VIII in E-flat minor',
            'composer': 'Claude / Sam (after the first-draft "Night loom" prelude)', 'instrument': 'Piano',
            'key': 'Eb', 'mode': 'minor', 'meter': list(METER), 'bpm': 90, 'tempo_text': 'Andante sostenuto, attacca',
            'movement_number': 8, 'piece_type': 'prelude', 'edition': 'third',
            'tempo_map': [[114, 90], [126, 64, 'ramp']]}            # broadening into the half cadence (attacca)
    voices = [('Melody', 'M.', 'treble', 70), ('Figure', 'F.', 'treble', 54), ('Bass', 'B.', 'bass', 62)]
    data = W.build_score(HERE / 'prelude.json', meta, voices, B.bars, dynamics=dyn, tags=B.tags,
                         subject='Eb5:12 F5:6 D5:6 Cb5:12 Bb4:6 Ab4:6 Gb4:6 Ab4:6 Gb4:12 Ab4:12 Eb5:12')
    # balance pass (second review, P2): in b14-17 the bass sings the retrograde inversion in tenths
    # under the soprano, so the bass comes forward (+8) and the melody steps back (-4)
    for voice in data['voices']:
        d = {'Bass': 8, 'Melody': -4}.get(voice['name'], 0)
        for e in voice['events']:
            if d and 13 * 6 <= float(e['t']) < 17 * 6:
                e['v'] = max(24, min(118, int(e['v']) + d))
    (HERE / 'prelude.json').write_text(json.dumps(data, indent=1))
    print('bars', len(B))
