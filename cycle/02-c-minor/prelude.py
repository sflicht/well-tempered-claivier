#!/usr/bin/env python3
"""Prelude II in C minor: "losing the beat".  Third edition, Pair II.

Continuous sixteenths whose grouping changes; every note is written literally
below, one call per bar (no voicing search, no generated figuration).

  A   1-5   groups of 4 on the beat, LH in steady eighths.  The accented first
            note of each group is the fugue subject in augmentation
            (C - B D | G Eb G F | Eb D C D Eb - D C | B C - G); rising bass
            C-D-Eb-F-G (i, V4/3, i6, vii4/3-iv, V).
  B   6-11  groups of 3 against a steady LH quarter-note beat.  From 8.1 (one
            sixteenth after the barline) the accents spell the fugue subject in
            its E-flat form at dotted-eighth speed:
            Eb D F Bb G Bb Ab | G F Eb F G F Eb D Eb Bb.  Harmony accelerates into
  12        E-flat, downbeat regained (groups of 4).
  C   13-18 groups of 5, rising waves within an octave; the LH now strikes with
            the groups, so the beat dissolves.  Chromatic bass Db-C-Db-E-F-Db-Ab
            (Eb7/Db, Ab/C, Bbm/Db, C7/E, Fm, Db, D-half-dim/Ab, German sixth).
  D   19-22 dominant pedal; groups 3+5+3+3+5+5 / 3+5+3+3+5+5 / 3+3+5+5; the waves
            climb from G5 to A-flat 6 while the harmony over the pedal speeds up.
  23-24     the beat breaks: a written-out Presto (32nds on the diminished
            seventh) and an Adagio in which the subject's head C-B-D-G is heard
            alone in quarter notes (after BWV 847's Presto/Adagio).
  E   25-29 the downbeat regained (groups of 4, both hands): i | iv6 N6 | i6/4 V7 |
            VI (deceptive) | iv6 N6 i6/4 V7 in quarters.
  F   30-32 tonic pedal: i, iv6/4, vii7, i; the last note C5 is the fugue's first.
Velocity accents are applied to the first note of every group (see GROUPS).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import Bars, build_score  # noqa: E402

METER = (4, 4)
B = Bars(['upper', 'lower'], METER)

B.bar('A: groups of 4; the subject, augmented, in the accents',  # 1
      upper='C5:1 G4:1 Eb4:1 G4:1 C5:1 G4:1 Ab4:1 G4:1 B4:1 G4:1 F4:1 G4:1 D5:1 B4:1 G4:1 B4:1',
      lower='C3:2 G3:2 Eb3:2 G3:2 G2:2 D3:2 G2:2 D3:2')
B.bar('',  # 2
      upper='G4:1 Eb4:1 C4:1 Eb4:1 Eb5:1 C5:1 G4:1 C5:1 G4:1 F4:1 D4:1 F4:1 F5:1 D5:1 B4:1 D5:1',
      lower='C3:2 G3:2 C3:2 G3:2 D3:2 G3:2 D3:2 G3:2')
B.bar('',  # 3
      upper='Eb5:1 G4:1 D5:1 G4:1 C5:1 G4:1 D5:1 G4:1 Eb5:1 G4:1 C5:1 G4:1 D5:1 Ab4:1 C5:1 Ab4:1',
      lower='Eb3:2 C4:2 Eb3:2 C4:2 Eb3:2 C4:2 F3:2 Ab3:2')
B.bar('',  # 4
      upper='B4:1 F4:1 Ab4:1 F4:1 C5:1 F4:1 Ab4:1 F4:1 C5:1 Bb4:1 Ab4:1 F4:1 G4:1 B4:1 D5:1 F5:1',
      lower='F3:2 C4:2 F3:2 C4:2 F3:2 C4:2 G2:2 D3:2')
B.bar('',  # 5
      upper='Eb5:1 D5:1 B4:1 D5:1 C5:1 B4:1 G4:1 B4:1 Ab4:1 G4:1 F4:1 G4:1 F4:1 D4:1 B3:1 D4:1',
      lower='G2:2 D3:2 F3:2 D3:2 G2:2 D3:2 F3:2 B2:2')
B.bar('B: groups of 3 against the beat',  # 6
      upper='G4:1 Eb4:1 C4:1 Ab4:1 Eb4:1 C4:1 G4:1 Eb4:1 C4:1 Ab4:1 Eb4:1 C4:1 C5:1 Ab4:1 Eb4:1 Eb5:1',
      lower='C3:4 Eb3:4 Ab2:4 C3:4')
B.bar('',  # 7
      upper='Ab4:1 C5:1 F5:1 C5:1 Ab4:1 Eb5:1 C5:1 Ab4:1 D5:1 Bb4:1 F4:1 F5:1 D5:1 Bb4:1 Ab5:1 F5:1',
      lower='F2:4 Ab2:4 Bb2:4 D3:4')
B.bar('accents: the fugue subject (E-flat), off the beat',  # 8
      upper='G5:1 Eb5:1 Bb4:1 G4:1 D5:1 Bb4:1 F4:1 F5:1 Bb4:1 G4:1 Bb4:1 G4:1 Eb4:1 G5:1 Eb5:1 Bb4:1',
      lower='Eb3:4 D3:4 Eb3:4 G2:4')
B.bar('',  # 9
      upper='Bb4:1 F4:1 D4:1 Ab5:1 Bb4:1 G4:1 G5:1 Eb5:1 C5:1 F5:1 C5:1 Ab4:1 Eb5:1 Bb4:1 G4:1 F5:1',
      lower='Bb2:4 Eb3:4 Ab2:4 G2:4')
B.bar('',  # 10
      upper='C5:1 Eb5:1 G5:1 Eb5:1 Bb4:1 F5:1 D5:1 Bb4:1 Eb5:1 Bb4:1 G4:1 D5:1 Bb4:1 G4:1 Eb5:1 Bb4:1',
      lower='C3:4 D3:4 Eb3:4 G2:4')
B.bar('',  # 11
      upper='G4:1 Bb4:1 G4:1 Eb4:1 C5:1 G4:1 Eb4:1 Eb5:1 C5:1 Ab4:1 F5:1 C5:1 Ab4:1 Ab5:1 F5:1 D5:1',
      lower='Eb3:4 C3:4 Ab2:4 Bb2:4')
B.bar('E-flat: downbeat regained',  # 12
      upper='G5:1 Eb5:1 Bb4:1 Eb5:1 Ab5:1 Eb5:1 C5:1 Eb5:1 G5:1 Eb5:1 Bb4:1 G4:1 Db5:1 Bb4:1 G4:1 Bb4:1',
      lower='Eb3:2 Bb3:2 C3:2 Ab3:2 G2:2 Bb2:2 Db3:2 G3:2')
B.bar('C: groups of 5; the beat dissolves',  # 13
      upper='G4:1 Ab4:1 Bb4:1 Db5:1 Eb5:1 Bb4:1 C5:1 Db5:1 Eb5:1 G5:1 Eb4:1 F4:1 G4:1 Bb4:1 Db5:1 G4:1',
      lower='Db3:5 Db4:5 Db3:5 Db4:1')
B.bar('',  # 14
      upper='Ab4:1 C5:1 Eb5:1 Ab5:1 C5:1 Db5:1 Eb5:1 Ab5:1 C6:1 Ab4:1 Bb4:1 C5:1 Eb5:1 Ab5:1 Ab4:1 Bb4:1',
      lower='C3:4 C4:5 C3:5 C4:2')
B.bar('',  # 15
      upper='Db5:1 F5:1 Bb5:1 F4:1 G4:1 Bb4:1 Db5:1 F5:1 E4:1 G4:1 Bb4:1 C5:1 E5:1 G4:1 Bb4:1 C5:1',
      lower='Db3:3 Db4:5 E3:5 E2:3')
B.bar('',  # 16
      upper='F5:1 Ab5:1 C5:1 Db5:1 F5:1 Ab5:1 C6:1 F4:1 G4:1 Ab4:1 C5:1 F5:1 Ab4:1 Bb4:1 C5:1 F5:1',
      lower='F2:2 F3:5 F2:5 F3:4')
B.bar('',  # 17
      upper='Ab5:1 C5:1 Eb5:1 F5:1 Ab5:1 C6:1 F4:1 G4:1 Ab4:1 Db5:1 F5:1 Ab4:1 Bb4:1 Db5:1 F5:1 Ab5:1',
      lower='F2:1 F3:5 F2:2 Db3:3 Db2:5')
B.bar('German sixth',  # 18
      upper='F4:1 Ab4:1 C5:1 D5:1 F5:1 Ab4:1 C5:1 D5:1 Eb5:1 F#5:1 C5:1 Eb5:1 F#5:1 Ab5:1 C6:1 Eb5:1',
      lower='Ab2:5 Ab3:3 Ab2:2 Ab3:5 Ab2:1')
B.bar('D: dominant pedal; groups 3+5+3+3+5+5',  # 19
      upper='G4:1 C5:1 Eb5:1 G4:1 C5:1 D5:1 Eb5:1 G5:1 B4:1 D5:1 F5:1 D5:1 F5:1 G5:1 F4:1 B4:1',
      lower='G2:3 G1:5 G2:3 G1:3 G2:2~')
B.bar('',  # 20
      upper='C5:1 F5:1 Ab5:1 C5:1 Eb5:1 F5:1 Ab5:1 C6:1 C5:1 Eb5:1 F#5:1 Eb5:1 F#5:1 A5:1 C6:1 Eb6:1',
      lower='G2:3 G1:5 G2:3 G1:5')
B.bar('',  # 21
      upper='C5:1 Eb5:1 G5:1 Eb5:1 F5:1 B5:1 D5:1 F5:1 Ab5:1 C6:1 F6:1 C5:1 Eb5:1 F#5:1 A5:1 C6:1',
      lower='G2:3 G1:3 G2:5 G1:5')
B.bar('',  # 22
      upper='B4:1 D5:1 F5:1 D5:1 F5:1 Ab5:1 F5:1 Ab5:1 B5:1 D6:1 F6:1 Ab5:1 B5:1 D6:1 F6:1 Ab6:1',
      lower='G2:3 G1:3 G2:5 G1:5')
B.bar('Presto (written out in 32nds)',  # 23
      upper='Ab6:0.5 F6:0.5 D6:0.5 B5:0.5 Ab5:0.5 F5:0.5 D5:0.5 B4:0.5 Ab4:0.5 F4:0.5 D4:0.5 B3:0.5 D4:0.5 F4:0.5 Ab4:0.5 B4:0.5 D5:0.5 F5:0.5 Ab5:0.5 B5:0.5 D6:0.5 F6:0.5 Ab6:0.5 F6:0.5 D6:0.5 B5:0.5 Ab5:0.5 F5:0.5 D5:0.5 B4:0.5 Ab4:0.5 G4:0.5',
      lower='G1:16')
B.bar("Adagio: the subject's head, unaccompanied",  # 24
      upper='C5:4 B4:4 D5:4 G4:4',
      lower='Ab2:4 G2:4 F2:4 G2:4')
B.bar('E: the downbeat regained',  # 25
      upper='Eb5:1 C6:1 B5:1 C6:1 G5:1 C6:1 B5:1 C6:1 Eb5:1 C6:1 B5:1 C6:1 G5:1 C6:1 B5:1 C6:1',
      lower='C3:2 C4:2 C3:2 C4:2 C3:2 C4:2 C3:2 C4:2')
B.bar('',  # 26
      upper='C5:1 Ab5:1 G5:1 Ab5:1 F5:1 Ab5:1 G5:1 Ab5:1 Ab5:1 Db6:1 C6:1 Db6:1 F5:1 Db6:1 C6:1 Db6:1',
      lower='Ab2:2 Ab3:2 Ab2:2 Ab3:2 F2:2 F3:2 F2:2 F3:2')
B.bar('',  # 27
      upper='Eb5:1 C6:1 B5:1 C6:1 G5:1 C6:1 B5:1 C6:1 D5:1 B5:1 A5:1 B5:1 F5:1 B5:1 A5:1 B5:1',
      lower='G2:2 G3:2 G2:2 G3:2 G2:2 G3:2 G2:2 G3:2')
B.bar('deceptive cadence',  # 28
      upper='Eb5:1 C6:1 Bb5:1 C6:1 Ab5:1 C6:1 Bb5:1 C6:1 Eb5:1 C6:1 Bb5:1 C6:1 Ab5:1 C6:1 Bb5:1 C6:1',
      lower='Ab2:2 Ab3:2 Ab2:2 Ab3:2 Ab2:2 Ab3:2 Ab2:2 Ab3:2')
B.bar('',  # 29
      upper='C5:1 Ab5:1 G5:1 Ab5:1 Db5:1 Ab5:1 F5:1 Ab5:1 Eb5:1 C6:1 B5:1 C6:1 D5:1 B5:1 F5:1 B5:1',
      lower='Ab2:2 Ab3:2 F2:2 F3:2 G2:2 G3:2 G2:2 G3:2')
B.bar('F: tonic pedal',  # 30
      upper='Eb5:1 C5:1 G4:1 C5:1 Eb5:1 C5:1 G4:1 C5:1 F5:1 C5:1 Ab4:1 C5:1 F5:1 C5:1 Ab4:1 C5:1',
      lower='C2:2 C3:2 C2:2 C3:2 C2:2 C3:2 C2:2 C3:2')
B.bar('',  # 31
      upper='Ab5:1 F5:1 D5:1 B4:1 Ab5:1 F5:1 D5:1 B4:1 G5:1 Eb5:1 C5:1 G4:1 Eb5:1 C5:1 G4:1 Eb4:1',
      lower='C2:2 C3:2 C2:2 C3:2 C2:2 C3:2 C2:2 C3:2')
B.bar('to the fugue',  # 32
      upper='C4:1 Eb4:1 G4:1 C5:13',
      lower='C2:16')


# Group starts (sixteenths within each bar) used for the accents.
def group_starts(bar):
    if bar <= 5 or bar == 12 or bar >= 25:
        return {0, 4, 8, 12}
    if 6 <= bar <= 11:                      # threes from 6.1
        return {u for u in range(16) if (16 * (bar - 6) + u) % 3 == 0}
    if 13 <= bar <= 18:                     # fives from 13.1
        return {u for u in range(16) if (16 * (bar - 13) + u) % 5 == 0}
    if 19 <= bar <= 22:                     # 3+5+3+3+5+5, 3+5+3+3+5+5, 3+3+5+5
        seq, s, starts = [3, 5, 3, 3, 5, 5, 3, 5, 3, 3, 5, 5, 3, 3, 5, 5], 0, set()
        for g in seq:
            starts.add(s)
            s += g
        return {x - 16 * (bar - 19) for x in starts if 16 * (bar - 19) <= x < 16 * (bar - 18)}
    if bar == 23:
        return {0, 4, 8, 12}
    return set()


LEVEL = {1: 0, 6: 2, 12: 5, 13: 3, 16: 6, 19: 6, 20: 9, 21: 12, 22: 15, 23: 16, 24: -8,
         25: 16, 26: 12, 28: 8, 29: 10, 30: 4, 32: 0}


def level(bar):
    v = 0
    for k in sorted(LEVEL):
        if k <= bar:
            v = LEVEL[k]
    return v


MARKS = [(1, 'Andante: groups of four'), (6, 'groups of three against the beat'),
         (8, 'the subject in the accents'), (12, 'E-flat: downbeat regained'),
         (13, 'groups of five'), (19, 'dominant pedal'), (23, 'Presto'), (24, 'Adagio'),
         (25, 'a tempo: the downbeat regained'), (28, 'deceptive cadence'), (30, 'tonic pedal')]


def main():
    assert len(B) == 32, len(B)
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'II. Prelude in C minor - losing the beat',
        'number': 2, 'movement_number': 2, 'piece_type': 'prelude',
        'key': 'C', 'mode': 'minor', 'meter': list(METER), 'bpm': 63, 'tempo_map': [[92, 40], [96, 63], [122, 63], [128, 46, 'ramp']],
        'tempo_text': 'Andante; the accents follow the groups',
        'composer': 'Original composition (Claude) for Sam',
        'instrument': 'Keyboard',
        'score_tagline': 'The Well-Tempered clAIvier - third edition',
        'markers': [{'t': float((b - 1) * 4), 'label': txt} for b, txt in MARKS],
    }
    out = HERE / 'prelude.json'
    build_score(out, meta, [('upper', 'RH', 'treble', 70), ('lower', 'LH', 'bass', 62)], B.bars,
                accents=False, tags=B.tags)
    data = json.loads(out.read_text())
    # phrase level plus accents on group starts (velocity shaping only)
    for v in data['voices']:
        boost = 8 if v['name'] == 'upper' else 4
        for e in v['events']:
            bar = e['bar']
            u = round((e['t'] - (bar - 1) * 4) * 4, 3)
            vel = e['v'] + level(bar)
            if u == int(u) and int(u) in group_starts(bar):
                vel += boost
            e['v'] = max(24, min(118, int(vel)))
    out.write_text(json.dumps(data, indent=1))
    print(f"wrote {out}: {len(B)} bars")


if __name__ == '__main__':
    main()
