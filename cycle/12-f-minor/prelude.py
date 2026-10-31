#!/usr/bin/env python3
"""Prelude XII in F minor, "The name, three times" -- literal source.

A short chorale prelude for one pianist, three voices: a new chorale-like melody
in the soprano (crotchets), a slow inner voice, and a walking quaver bass that
turns into a pulsing tonic pedal, after the manner of an Orgelbuechlein chorale
(Bach's "Ich ruf zu dir", BWV 639, is also in F minor; nothing of it is quoted).
The first edition of The Art of Fugue (1751) closed the unfinished last fugue
with a chorale; here the chorale comes first.

The melody is built from two crosses:
  - C Db C B: the first four notes of Bach's WTC I F-minor fugue subject (BWV 857,
    cycle/reference/bach-subjects.md), the Book I fugue in this key (bars 1, 13);
  - B-flat A C B-natural: the name, at its own pitch (soprano b2-3, bass b9-10
    in half notes under a quieter texture, soprano again b14 over the tonic
    pedal).
Each cross resolves to C.  The bass walks in quavers, stops to sing the name in
half notes (b9-10), and becomes a repeated-quaver tonic pedal for the last
phrase (b13-14).

4/4, crotchet = 54, 16 bars, about 1:17.  Every note is written below.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import Bars, build_score  # noqa: E402

B = Bars(['soprano', 'alto', 'bass'], (4, 4))
#            soprano (melody)               inner voice                 bass (walking quavers)
B.bar('i iv V viio7/V: the cross of BWV 857',  # 1
      soprano='C5:4 Db5:4 C5:4 B4:4',
      alto='Ab4:4 Bb4:4 G4:4 Ab4:4',
      bass='F2:2 C3:2 Bb2:2 F2:2 C3:2 E3:2 D3:2 F3:2')
B.bar('V6 V7 | the name: V7 V7/iv',  # 2
      soprano='C5:8 Bb4:4 A4:4',
      alto='G4:8 E4:4 F4:4',
      bass='E3:2 C3:2 G2:2 Bb2:2 C3:2 E3:2 Eb3:2 C3:2')
B.bar('VI7 viio6/5 of V | V V4/2',  # 3
      soprano='C5:4 B4:4 C5:8',
      alto='F4:8 E4:8',
      bass='Db3:2 F3:2 D3:2 Ab2:2 C3:2 G2:2 Bb2:2 G2:2')
B.bar('i6 iio6/5 i6/4 V',  # 4
      soprano='Ab4:4 G4:4 F4:4 E4:4',
      alto='F4:8 C4:4 Bb3:4',
      bass='Ab2:2 C3:2 Bb2:2 Db3:2 C3:2 F3:2 C3:2 C2:2')
B.bar('i | VI iv',  # 5
      soprano='F4:8 Ab4:4 Bb4:4',
      alto='Ab3:4 C4:4 F4:4 Db4:4',
      bass='F2:2 C3:2 Ab2:2 C3:2 Db3:2 F3:2 Bb2:2 Db3:2')
B.bar('III VI6 VII V6/5 of III',  # 6
      soprano='C5:4 Db5:4 Eb5:4 Db5:4',
      alto='Eb4:4 F4:4 G4:4 Bb4:4',
      bass='Ab2:2 C3:2 F2:2 Ab2:2 Eb3:2 G3:2 G2:2 Eb2:2')
B.bar('III iv6/5 i V6',  # 7
      soprano='C5:4 Bb4:4 Ab4:4 G4:4',
      alto='Ab4:4 F4:4 F4:4 C4:4',
      bass='Ab2:2 C3:2 Db3:2 Bb2:2 F2:2 Ab2:2 E2:2 C3:2')
B.bar('iv7 | V (half cadence)',  # 8
      soprano='Ab4:8 G4:8',
      alto='F4:8 E4:8',
      bass='Bb2:2 Db3:2 F2:2 Ab2:2 C3:2 E3:2 G3:2 C3:2')
B.bar('the name in the bass: iv | V6/iv V6/5 of iv',  # 9
      soprano='Bb4:4 Db5:4 C5:4 Eb5:4',
      alto='F4:16',
      bass='Bb2:8 A2:8')
B.bar('V7(b9) | viio7/V',  # 10
      soprano='Db5:4 C5:4 D5:4 Ab4:4',
      alto='E4:4 E4:4 F4:4 F4:4',
      bass='C3:8 B2:8')
B.bar('V | V6/5',  # 11
      soprano='G4:8 Bb4:8',
      alto='E4:8 C4:8',
      bass='C3:8 E2:8')
B.bar('i iio6/5 i6/4 V7',  # 12
      soprano='Ab4:4 G4:4 F4:4 E4:4',
      alto='C4:4 Db4:4 C4:4 Bb3:4',
      bass='F2:2 Ab2:2 Bb2:2 G2:2 C3:2 Ab2:2 C3:2 C2:2')
B.bar('tonic pedal: the cross again (i iv6/4 i viio7/V)',  # 13
      soprano='C5:4 Db5:4 C5:4 B4:4',
      alto='Ab3:4 Bb3:4 Ab3:8',
      bass='F2:2 F2:2 F2:2 F2:2 F2:2 F2:2 F2:2 F2:2')
B.bar('the name once more (iv6/4 I iio4/3 viio7/V)',  # 14
      soprano='Bb4:4 A4:4 C5:4 B4:4',
      alto='Db4:4 C4:4 D4:8',
      bass='F2:2 F2:2 F2:2 F2:2 F2:2 F2:2 F2:2 F2:2')
B.bar('i i6 V V: the last cadence',  # 15
      soprano='C5:4 Ab4:4 G4:4 E4:4',
      alto='C4:16',
      bass='F2:2 F3:2 Ab2:2 F2:2 C3:2 G2:2 C3:2 C2:2')
B.bar('i',  # 16
      soprano='F4:16',
      alto='Ab3:16',
      bass='F2:16')

DYN = [-6, -4, -4, -6, -6, -2, 0, -3, 2, 3, 0, -2, -5, -3, -4, -7]


def build(out=HERE / 'prelude.json'):
    meta = {
        'title': 'The Well-Tempered clAIvier', 'subtitle': 'XII. Prelude in F minor',
        'composer': 'Claude / composed for Sam', 'instrument': 'Piano (three voices)',
        'key': 'F', 'mode': 'minor', 'meter': [4, 4], 'bpm': 54,
        'tempo_text': 'Adagio, come un corale', 'character': 'The name, three times',
        'movement_number': 12, 'piece_type': 'prelude', 'edition': 'third',
        # breath at the half cadence (b8), the name in the bass a little broader, broadening to the end
        'tempo_map': [[26, 54], [32, 46, 'ramp'], [32, 50], [44, 50], [48, 54], [58, 54], [64, 40, 'ramp']],
        'markers': [{'t': 0.0, 'label': 'The cross of BWV 857'}, {'t': 4.0, 'label': 'B-A-C-H (soprano)'},
                    {'t': 32.0, 'label': 'B-A-C-H (bass)'}, {'t': 48.0, 'label': 'Tonic pedal'}],
    }
    voices = [('Soprano', 'S', 'treble', 66), ('Alto', 'A', 'treble', 52), ('Bass', 'B', 'bass', 58)]
    bars = {'Soprano': B.bars['soprano'], 'Alto': B.bars['alto'], 'Bass': B.bars['bass']}

    def dynamics(b):
        return DYN[b]
    # the name in the bass (b9-10) sung out over a quieter texture
    data = build_score(out, meta, voices, bars, dynamics=dynamics, tags=B.tags)
    for v in data['voices']:
        if v['name'] == 'Bass':
            for e in v['events']:
                if 9 <= e['bar'] <= 10:
                    e['v'] = min(118, e['v'] + 10)
    Path(out).write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    build()
    print('bars', len(B))
