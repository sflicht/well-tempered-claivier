#!/usr/bin/env python3
"""Prelude XIII in F-sharp major: Aria (sarabande) over the Goldberg ground.

The bass is the ground of the fugue - the eight notes of BWV 988's ground in F-sharp major (F# E#
D# C# A# B C# F#), one to a 3/4 bar - stated twice.  Over it a sarabande aria in the manner of the
Goldberg Aria: the weight on the second beat, long appoggiaturas, written-out turns, mordents and a
cadential trill; the second half is a "double" that keeps the same frame and fills it in with
running figures.  The melody is new: it does not follow the Aria's line (Bach's opens on the tonic
with a mordent and climbs stepwise; this one opens on the third and leaps to the octave), and the
inner voice is a plain second part, not the Aria's.

Three voices; playable by one pianist: right hand = aria + alto (never more than an octave apart),
left hand = the ground.

Every pitch is written here as a literal token string.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (3, 4)
B = W.Bars(['Aria', 'Alto', 'Fundamentum'], METER)

# ------------------------------------------------------------------------------- first half: the aria
B.bar('I: the third, then the octave with a turn',
      Aria='A#4:4 F#5:6 G#5:1 F#5:1/2 E#5:1/2', Alto='F#4:4 C#5:4 A#4:4', Fundamentum='F#2:8 C#3:4')
B.bar('V6: appoggiatura on the downbeat; G-sharp on the second beat',
      Aria='F#5:2 E#5:2 G#5:6 F#5:1 E#5:1', Alto='C#5:4 B4:4 G#4:4', Fundamentum='E#2:8 C#2:4')
B.bar('vi: the peak of the first phrase',
      Aria='D#5:4 A#5:6 G#5:1 F#5:1', Alto='F#4:4 A#4:8', Fundamentum='D#2:8 F#2:4')
B.bar('V: half close',
      Aria='G#5:3 F#5:1 E#5:4 D#5:2 C#5:2', Alto='C#5:4 B4:4 G#4:4', Fundamentum='C#2:8 B1:4')
B.bar('I6',
      Aria='A#4:3 B4:1 C#5:4 F#5:4', Alto='F#4:4 A#4:8', Fundamentum='A#1:8 C#2:4')
B.bar('IV / ii6: B on the second beat',
      Aria='F#5:2 G#5:2 B5:6 A#5:1 G#5:1', Alto='D#5:4 F#5:4 D#5:4', Fundamentum='B1:8 D#2:4')
B.bar('V7: the cadential trill from above',
      Aria='C#6:4 A#5:2 G#5:2 A#5:1/2 G#5:1/2 A#5:1/2 G#5:1/2 F#5:1 G#5:1',
      Alto='E#5:4 C#5:4 B4:4', Fundamentum='C#2:8 C#3:4')
B.bar('I, and the upbeat to the double',
      Aria='F#5:6 C#5:2 D#5:2 E#5:2', Alto='A#4:6 R:6', Fundamentum='F#2:8 F#3:4')

# ------------------------------------------------------------------------------- second half: double
B.bar('I (double)',
      Aria='F#5:1 G#5:1 A#5:2 F#5:2 C#6:4 A#5:1 F#5:1', Alto='C#5:4 A#4:8', Fundamentum='F#2:4 A#2:4 C#3:4')
B.bar('V6',
      Aria='G#5:2 E#5:1 F#5:1 G#5:4 B5:2 A#5:2', Alto='G#4:4 C#5:4 B4:4', Fundamentum='E#2:4 G#2:4 E#2:4')
B.bar('vi',
      Aria='F#5:1 E#5:1 D#5:1 E#5:1 F#5:4 A#5:2 F#5:2', Alto='A#4:4 D#5:4 C#5:4', Fundamentum='D#2:4 A#2:4 F#2:4')
B.bar('V',
      Aria='E#5:2 G#5:2 C#6:4 B5:1 A#5:1 G#5:1 F#5:1', Alto='C#5:4 E#5:4 C#5:4', Fundamentum='C#2:4 G#2:4 E#2:4')
B.bar('I6',
      Aria='F#5:1 E#5:1 F#5:1 G#5:1 A#5:4 C#6:2 A#5:2', Alto='C#5:4 F#5:4 E#5:2 F#5:2', Fundamentum='A#1:4 C#2:4 F#2:4')
B.bar('IV / ii6',
      Aria='B5:2 G#5:2 D#6:4 C#6:1 B5:1 A#5:1 G#5:1', Alto='F#5:4 B4:4 D#5:4', Fundamentum='B1:4 F#2:4 D#2:4')
B.bar('V7: the trill again, longer',
      Aria='A#5:2 C#6:2 B5:1/2 C#6:1/2 B5:1/2 A#5:1/2 G#5:2 A#5:1/2 G#5:1/2 A#5:1/2 G#5:1/2 A#5:1/2 G#5:1/2 F#5:1/2 G#5:1/2',
      Alto='E#5:4 G#5:2 F#5:2 E#5:4', Fundamentum='C#2:4 E#2:4 C#2:4')
B.bar('I: close',
      Aria='F#5:12', Alto='A#4:12', Fundamentum='F#2:12')


def build():
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Prelude XIII in F-sharp major: Aria',
            'composer': 'Claude / Sam (ground: J. S. Bach, BWV 988)',
            'instrument': 'Keyboard (one player)', 'key': 'F#', 'mode': 'major', 'meter': list(METER),
            'bpm': 52, 'tempo_text': 'Aria: Sarabande, cantabile',
            # a breath at the half-way cadence and a broadening into the last trill
            'tempo_map': [[21, 52], [24, 46, 'ramp'], [24, 54], [39, 54], [48, 40, 'ramp']],
            'movement_number': 13, 'piece_type': 'prelude', 'edition': 'third'}
    voices = [('Aria', 'Ar', 'treble', 72), ('Alto', 'A', 'treble', 56), ('Fundamentum', 'Fun', 'bass', 62)]
    dyn = {1: 0, 5: 2, 7: 3, 8: 0, 9: 2, 12: 3, 14: 5, 15: 3, 16: 0}

    def dynamics(b):
        v = 0
        for k in sorted(dyn):
            if b + 1 >= k:
                v = dyn[k]
        return v
    return W.build_score(HERE / 'prelude.json', meta, voices, B.bars, tags=B.tags, dynamics=dynamics)


if __name__ == '__main__':
    build()
    print('bars', len(B))
