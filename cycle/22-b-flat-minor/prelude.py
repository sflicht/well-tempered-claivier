#!/usr/bin/env python3
"""Prelude XXII in B-flat minor: Tombeau (third edition).

A lamentation for one pianist, after Froberger's Tombeau for M. Blancheroche ("se joue fort
lentement a la discretion sans observer aucune mesure") and Louis Couperin's unmeasured
preludes.  It is notated in measure; the freedom is in the tempo map (every bar has its own
pace, the cadences and the chord of the tomb are held back, Froberger's falling scale is
fast) and in the written-out arpeggiation (style brise): chords gather note by note.

  b1      a low B-flat tolls; the tonic chord gathers from the bass up (as the voices of the
          fugue will gather).
  b2-5    the head of BWV 867 (B-flat, F, a rest, the leap of a ninth to G-flat) and the
          fugue's subject, slowly, ending B-A-C-H; its B-natural sounds over F in the fugue's
          axis chord (B-natural D F A-flat), which opens onto the dominant.
  b6-8    the lament: the bass walks down the chromatic tetrachord B-flat A A-flat G G-flat F
          (i V6/5 v6 IV6 iv6 V7) under sighing appoggiaturas.
  b9-12   consolation in D-flat (the key of the fugue's second section), then back.
  b13-15  the climb: the tonic arpeggio in both hands, VI, iv, V7, and the axis chord
          broken upwards, fortissimo.
  b16     Froberger's fall: a scale tumbling two octaves down over the dominant.
  b17-20  V7 - i; the tonic chord comes apart from the top down (bar 1 backwards), a last
          low B-flat, and a lone B-flat4 -- the note the fugue begins (and ends) with.
Every note is written here by hand.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
B = W.Bars(['Soprano', 'Alto', 'Tenor', 'Bass'], METER)

# ---------------------------------------------------------------- b1-5  the toll, the subject
B.bar('the toll; the chord gathers (style brise)',  # 1   i
      Soprano='R:8 F4:4 Bb4:4',
      Alto='R:5 Db4:11',
      Tenor='R:2 F2:14',
      Bass='Bb1:16')
B.bar('BWV 867: B-flat, F, a rest, the ninth',  # 2   i
      Soprano='Bb4:8 F4:4 R:2 Gb5:2~',
      Alto='Db4:12 R:4',
      Tenor='F2:8 Bb2:8',
      Bass='Bb1:16')
B.bar('',  # 3   iv6 | V7(b9)
      Soprano='Gb5:4 F5:4 Eb5:4 Db5:4',
      Alto='Bb4:8 A4:8',
      Tenor='Bb2:8 C3:8',
      Bass='Gb2:8 F2:8')
B.bar('',  # 4   V | i6/4 | V | V7 over the dominant
      Soprano='C5:4 Bb4:4 A4:4 C5:4',
      Alto='A4:4 F4:4 F4:4 Eb4:4',
      Tenor='C3:4 Db3:4 C3:4 A2:4',
      Bass='F2:16')
B.bar('B-A-C-H: the H in the axis chord, opening onto the dominant',  # 5   ct-dim7 | V7
      Soprano='B4:8 C5:8',
      Alto='D4:8 Eb4:8',
      Tenor='Ab2:8 A2:8',
      Bass='F2:16')

# ---------------------------------------------------------------- b6-8  the lament
B.bar('lament: B-flat, A',  # 6   i | V6/5
      Soprano='Db5:8 C5:8',
      Alto='Db4:8 Eb4:8',
      Tenor='F3:16',
      Bass='Bb2:8 A2:8')
B.bar('A-flat, G',  # 7   v6 | IV6
      Soprano='Db5:4 C5:8 Bb4:4',
      Alto='F4:8 Eb4:8',
      Tenor='C3:8 Bb2:8',
      Bass='Ab2:8 G2:8')
B.bar('G-flat, F',  # 8   iv6 | V7 (4-3)
      Soprano='Cb5:4 Bb4:8 A4:4',
      Alto='Eb4:16',
      Tenor='Bb2:8 C3:8',
      Bass='Gb2:8 F2:8')

# ---------------------------------------------------------------- b9-12  consolation
B.bar('consolation: D-flat',  # 9   I | IV6/4
      Soprano='Ab4:6 Bb4:2 Db5:6 C5:2',
      Alto='F4:8 Gb4:8',
      Tenor='F2:8 Bb2:8',
      Bass='Db2:16')
B.bar('',  # 10  IV | V7(4-3)
      Soprano='Bb4:8 Db5:4 C5:4',
      Alto='Gb4:8 Eb4:8',
      Tenor='Bb2:8 C3:8',
      Bass='Gb2:8 Ab2:8')
B.bar('',  # 11  I | vi (= i of B-flat minor)
      Soprano='Db5:8 F5:6 Eb5:2',
      Alto='F4:16',
      Tenor='Ab2:8 Db3:8',
      Bass='Db2:8 Bb1:8')
B.bar('',  # 12  iv6 | V7
      Soprano='Gb5:6 F5:2 Eb5:8',
      Alto='Bb4:8 A4:8',
      Tenor='Bb2:8 C3:8',
      Bass='Gb2:8 F2:8')

# ---------------------------------------------------------------- b13-16  the climb, the tomb, the fall
B.bar('the climb',  # 13  i
      Soprano='Bb4:4 Db5:4 F5:4 Bb5:4',
      Alto='F4:4 Bb4:4 Db5:4 F5:4',
      Tenor='Bb2:16',
      Bass='Bb1:16')
B.bar('',  # 14  VI | iv6 | V
      Soprano='Db6:6 C6:2 Bb5:4 A5:4',
      Alto='Gb5:12 Eb5:4',
      Tenor='Bb2:12 C3:4',
      Bass='Gb2:12 F2:4')
B.bar('the tomb: the axis chord, broken upwards',  # 15  B-natural D F A-flat over F
      Soprano='R:3 Ab5:13',
      Alto='R:2 D5:14',
      Tenor='R:1 B2:15',
      Bass='F2:16')
B.bar("Froberger's fall",  # 16  V
      Soprano='A5:4 G5:1 F5:1 E5:1 D5:1 C5:1 Bb4:1 A4:1 G4:1 F4:1 E4:1 D4:1 C4:1',
      Alto='C5:4 R:12',
      Tenor='C3:16',
      Bass='F2:16')

# ---------------------------------------------------------------- b17-20  the end, the beginning
B.bar('',  # 17  V7(b9)
      Soprano='Eb5:6 Db5:2 C5:8',
      Alto='A4:8 F4:4 Eb4:4',
      Tenor='C3:8 A2:8',
      Bass='F2:16')
B.bar('the chord comes apart from the top (bar 1 backwards)',  # 18  i
      Soprano='Bb4:4 F4:4 R:8',
      Alto='Db4:11 R:5',
      Tenor='F2:14 R:2',
      Bass='Bb1:16')
B.bar('',  # 19
      Bass='Bb1:16')
B.bar('ma fin est mon commencement',  # 20
      Soprano='Bb4:16')

# 20 bars = 80 quarters.  A free tempo map: slow toll and gathering, the subject a little
# more flowing, every cadence held back, the consolation moving, the climb pressing on, the
# tomb chord very broad, the fall quick and slowing, the end slower and slower.
TEMPO = [[0, 34], [8, 46, 'ramp'], [16, 48], [18, 30, 'ramp'], [20, 30],
         [20, 44], [30, 42], [32, 32, 'ramp'],
         [32, 52], [44, 50], [48, 38, 'ramp'],
         [48, 52], [54, 58, 'ramp'], [56, 46, 'ramp'],
         [56, 26], [60, 24],
         [60, 80], [62, 64, 'ramp'], [64, 40, 'ramp'],
         [64, 40], [68, 34, 'ramp'], [72, 30, 'ramp'], [76, 26, 'ramp'], [80, 20, 'ramp']]


def build(path=None):
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Prelude XXII in B-flat minor: Tombeau',
            'composer': 'Claude / Sam, after Froberger and L. Couperin (subject after J. S. Bach, BWV 867)',
            'instrument': 'Keyboard (one player)',
            'key': 'Bb', 'mode': 'minor', 'meter': list(METER), 'bpm': 44,
            'tempo_text': 'Fort lentement, a la discretion (the tempo map is free)',
            'movement_number': 22, 'piece_type': 'prelude', 'edition': 'third',
            'tempo_map': TEMPO,
            'markers': [{'t': float((b - 1) * 4), 'label': txt} for b, txt in
                        [(1, 'Tombeau'), (6, 'lament'), (9, 'consolation'), (13, 'the climb'),
                         (15, 'the tomb'), (16, 'the fall'), (18, 'the end')]]}
    voices = [('Soprano', 'S.', 'treble', 66), ('Alto', 'A.', 'treble', 56),
              ('Tenor', 'T.', 'bass', 54), ('Bass', 'B.', 'bass', 60)]

    def dynamics(b):
        return {0: -6, 1: -2, 2: 0, 3: 0, 4: 2, 5: -2, 6: -2, 7: -4, 8: -6, 9: -6, 10: -4, 11: -2,
                12: 4, 13: 8, 14: 14, 15: 6, 16: -2, 17: -6, 18: -8, 19: -10}.get(b, 0)
    return W.build_score(path or HERE / 'prelude.json', meta, voices, B.bars, tags=B.tags, dynamics=dynamics)


if __name__ == '__main__':
    assert len(B) == 20, len(B)
    build()
    print('bars', len(B))
