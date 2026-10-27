#!/usr/bin/env python3
"""Prelude XXI in B-flat major: "Arioso" (third edition).

The first movement of Bach's Capriccio BWV 992 is an Arioso, "Ist eine Schmeichelung der Freunde,
um denselben von seiner Reise abzuhalten" -- the friends coaxing the traveller to stay.  This
prelude is their coaxing, for one pianist, and it introduces the friends' theme T of the fugue,
which begins with the Arioso's opening turn (B-flat C D C B-flat A B-flat C, soprano and alto in
sixths, as Bach writes it) and runs up to G, the one note the posthorn of the fugue will never
have.

  b1-2    T in B-flat in the Arioso's sixths, over a walking bass.
  b3-4    its answer in F.
  b5-7    the friends' lament: the bass walks down Bach's chromatic tetrachord (Lamento,
          BWV 992/3), B-flat A A-flat G G-flat F, under sighing appoggiaturas in thirds.
  b8      the half cadence on F; from far off the left hand blows the posthorn's call.
  b9-10   T again, more urgent (the alto in sixteenths), and a deceptive cadence.
  b11-12  the farewell: T's sigh, an echo, the posthorn call once more (left hand), and the
          last chord.
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

# ---------------------------------------------------------------- b1-4  T and its answer
B.bar('T in B-flat: the Arioso turn in sixths',  # 1   Bb | Bb | F/A | Gm
      Soprano='R:2 Bb4:1 C5:1 D5:2 C5:1 Bb4:1 A4:2 Bb4:1 C5:1 D5:1 Eb5:1 F5:1 G5:1',
      Alto='R:2 D4:1 Eb4:1 F4:2 Eb4:1 D4:1 C4:2 D4:1 Eb4:1 F4:1 G4:1 A4:1 Bb4:1',
      Tenor='F3:4 F3:4 F3:4 G3:4',
      Bass='Bb2:2 F2:2 Bb2:2 D3:2 A2:2 C3:2 G2:2 Bb2:2')
B.bar('T: the sigh from G',  # 2   Eb | F7 | Bb  F7 | Bb
      Soprano='G5:4 F5:2 Eb5:2 D5:3 C5:1 Bb4:4',
      Alto='Bb4:4 A4:2 G4:2 F4:3 Eb4:1 D4:4',
      Tenor='Bb3:4 Eb4:4 D4:8',
      Bass='Eb3:2 C3:2 F3:2 A2:2 Bb2:2 A2:2 Bb2:2 D3:2')
B.bar('answer in F',  # 3   F | F | C/E | Bb/D
      Soprano='R:2 F5:1 G5:1 A5:2 G5:1 F5:1 E5:2 F5:1 G5:1 A5:1 Bb5:1 C6:1 D6:1',
      Alto='R:2 A4:1 Bb4:1 C5:2 Bb4:1 A4:1 G4:2 A4:1 Bb4:1 C5:1 D5:1 E5:1 F5:1',
      Tenor='C4:4 C4:4 C4:4 Bb3:4',
      Bass='F3:2 C3:2 A2:2 F3:2 C3:2 E3:2 D3:2 F3:2')
B.bar('the answer sighs to F',  # 4   Bb | C7 | F  C7 | F
      Soprano='D6:4 C6:2 Bb5:2 A5:3 G5:1 F5:4',
      Alto='F5:4 E5:2 D5:2 C5:3 Bb4:1 A4:4',
      Tenor='Bb3:4 G3:4 A3:4 A3:4',
      Bass='Bb2:2 F3:2 C3:2 E3:2 F3:2 A2:2 C3:2 Eb3:2')

# ---------------------------------------------------------------- b5-8  the lament
B.bar('lament: B-flat, A',  # 5   Bb | Bb | F/A | F7/A
      Soprano='Eb5:2 D5:2 F5:2 Eb5:2 D5:2 C5:2 Eb5:4',
      Alto='C5:2 Bb4:2 D5:2 Bb4:2 Bb4:2 A4:2 A4:4',
      Tenor='F4:8 F4:8',
      Bass='D3:8 A2:8')
B.bar('lament: A-flat, G',  # 6   Bbm/Ab | Fm/Ab | Eb/G | Gø7
      Soprano='Eb5:2 Db5:2 C5:2 Db5:2 Bb4:2 G4:2 Bb4:2 Ab4:2',
      Alto='Bb4:2 F4:6 G4:2 Eb4:2 F4:4',
      Tenor='F4:4 C4:4 Eb4:4 Db4:4',
      Bass='Ab2:8 G2:8')
B.bar('lament: G-flat, F',  # 7   Gb | Ebm/Gb | F | F7
      Soprano='Gb4:2 F4:2 Bb4:4 A4:2 C5:2 Eb5:4',
      Alto='Eb4:2 Db4:2 Db4:2 Eb4:2 F4:4 F4:4',
      Tenor='Bb3:4 Bb3:4 C4:4 A3:4',
      Bass='Gb2:8 F2:8')
B.bar('half cadence; the posthorn from afar',  # 8   F (posthorn call on F in the left hand)
      Soprano='F5:8 R:8',
      Alto='C5:8 R:8',
      Tenor='A4:8 R:8',
      Bass='F2:4 R:2 F2:1 F2:1 F3:2 F3:2 F3:2 F3:2')

# ---------------------------------------------------------------- b9-12  pleading and farewell
B.bar('T again, more urgent',  # 9   Bb | Bb | F/A | Gm
      Soprano='R:2 Bb4:1 C5:1 D5:2 C5:1 Bb4:1 A4:2 Bb4:1 C5:1 D5:1 Eb5:1 F5:1 G5:1',
      Alto='D4:1 F4:1 Bb3:1 F4:1 F4:1 Bb4:1 F4:1 D4:1 C4:1 Eb4:1 F4:1 Eb4:1 D4:1 Bb3:1 D4:1 G4:1',
      Tenor='R:16',
      Bass='Bb2:4 F3:4 A2:4 Bb2:4')
B.bar('deceptive cadence',  # 10   Eb | F7 | Gm  Eb | F7
      Soprano='G5:4 F5:2 Eb5:2 D5:3 C5:1 Eb5:4',
      Alto='Bb4:2 G4:2 A4:2 C5:2 Bb4:2 G4:2 A4:2 C5:2',
      Tenor='Eb4:4 C4:4 G3:4 C4:4',
      Bass='Eb3:4 F3:4 G3:4 F3:4')
B.bar('farewell: the sigh and its echo',  # 11   Bb | Eb/Bb | Bb  F7/Bb | Bb
      Soprano='D5:4 G5:2 F5:2 Eb5:3 D5:1 D5:4',
      Alto='Bb4:4 Bb4:4 A4:4 Bb4:4',
      Tenor='F4:4 Eb4:4 F4:8',
      Bass='Bb2:16')
B.bar('the last call, and the last chord',  # 12   Bb
      Soprano='D5:16',
      Alto='F4:16',
      Tenor='Bb3:16',
      Bass='Bb1:4 R:2 Bb1:1 Bb1:1 Bb2:8')


def build(path=None):
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Prelude XXI in B-flat major: Arioso (the friends coax the traveller)',
            'composer': 'Claude / Sam, after J. S. Bach (BWV 992, Arioso and Lamento)',
            'instrument': 'Keyboard (one player)',
            'key': 'Bb', 'mode': 'major', 'meter': list(METER), 'bpm': 50,
            'tempo_text': 'Adagio (Arioso)',
            'movement_number': 21, 'piece_type': 'prelude', 'edition': 'third',
            # 12 bars = 48 quarters.  The lament a little slower; the posthorn bar in time,
            # held back at its end; the farewell broadening into a long last chord.
            'tempo_map': [[16, 46], [28, 42, 'ramp'], [28, 52], [32, 48], [40, 44], [44, 36, 'ramp'],
                          [48, 30, 'ramp']]}
    voices = [('Soprano', 'S.', 'treble', 70), ('Alto', 'A.', 'treble', 58),
              ('Tenor', 'T.', 'bass', 56), ('Bass', 'B.', 'bass', 62)]

    def dynamics(b):
        return {0: 0, 1: 0, 2: 2, 3: 2, 4: -4, 5: -4, 6: -4, 7: -10, 8: 4, 9: 4, 10: -2, 11: -10}.get(b, 0)
    return W.build_score(path or HERE / 'prelude.json', meta, voices, B.bars, tags=B.tags, dynamics=dynamics)


if __name__ == '__main__':
    build()
    print('bars', len(B))
