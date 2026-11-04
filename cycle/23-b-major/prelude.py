#!/usr/bin/env python3
"""Prelude XXIII in B major (one keyboard player): *A Ground upon Ut re mi fa sol la*.

An English virginalist's set of divisions on a ground, the kind of piece Byrd and Bull wrote on
the hexachord (Byrd's "Ut re mi fa sol la", FVB no. CI; Bull's no. LI, the model of the fugue).
The ground is the hexachord itself in minims, up and down: B C# D# E F# G# | G# F# E D# C# B,
six bars, harmonised I - V4/3 | I6 - IV | V - vi | IV6 - V7 | ii6/5 - I6 | V4/3 - I.
Four statements, each a new division:
  1 (b1-6)    the plainsong: treble in minims with a few crotchets, a mean voice, the ground below
  2 (b7-12)   quaver divisions in the treble (broken chords, as on the virginals)
  3 (b13-18)  the ground moves to the treble; the bass divides in quavers; the mean in sixths;
              the falling half is reharmonised over a falling bass, IV - iii | ii - I | V7 - I
  4 (b19-24)  semiquaver runs in the treble over the ground, as in Bull's fastest variations,
              with the mean in minims between them
then a two-bar close (IV - V7 - I) that leaves the B-major chord for the fugue's first breve.

Every note is written below as a literal bar string (the ground is written out each time).

Build:  python3 cycle/23-b-major/prelude.py   -> prelude.json
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
GROUND = ['B2:8 C#3:8', 'D#3:8 E3:8', 'F#3:8 G#3:8~', 'G#3:8 F#3:8', 'E3:8 D#3:8', 'C#3:8 B2:8']

T, M, B = [], [], []          # treble, mean, bass: one string per bar

# 1. the plainsong (b1-6)
T += ['F#5:8 E5:8', 'D#5:4 C#5:4 B4:8', 'A#4:8 B4:8', 'B4:4 E5:4 C#5:8', 'C#5:4 B4:4 D#5:8', 'E5:4 C#5:4 D#5:8']
M += ['B3:8 A#3:8', 'B3:8 G#3:8', 'C#4:8 B3:8', 'E4:8 E4:8', 'G#4:8 F#4:8', 'F#4:8 F#4:8']
B += GROUND

# 2. quaver divisions (b7-12)
T += ['D#5:2 F#5:2 B5:2 F#5:2 E5:2 C#5:2 A#4:2 C#5:2',
      'B4:2 D#5:2 F#5:2 D#5:2 G#5:2 E5:2 B4:2 C#5:2',
      'A#4:2 C#5:2 F#5:2 C#5:2 B4:2 D#5:2 G#5:2 D#5:2',
      'E5:2 B4:2 G#4:2 B4:2 A#4:2 C#5:2 E5:2 C#5:2',
      'C#5:2 E5:2 G#5:2 E5:2 F#5:2 D#5:2 B4:2 D#5:2',
      'E5:2 C#5:2 A#4:2 C#5:2 D#5:4 B4:4']
M += ['B3:8 E4:8', 'D#4:8 G#3:8', 'C#4:8 G#3:8', 'B3:8 E4:8', 'E4:8 B3:8', 'A#3:8 B3:8']
B += GROUND

# 3. the ground in the treble, the bass divides (b13-18)
T += ['B4:8 C#5:8', 'D#5:8 E5:8', 'F#5:8 G#5:8~', 'G#5:8 F#5:8', 'E5:8 D#5:8', 'C#5:8 B4:8']
M += ['F#4:8 E4:8', 'F#4:8 G#4:8', 'A#4:8 B4:8', 'B4:8 A#4:8', 'G#4:8 F#4:8', 'E4:8 D#4:8']
B += ['B2:2 D#3:2 F#3:2 D#3:2 A#2:2 C#3:2 F#3:2 C#3:2',
      'B2:2 F#3:2 D#3:2 B2:2 G#2:2 B2:2 E3:2 B2:2',
      'F#2:2 A#2:2 C#3:2 A#2:2 G#2:2 B2:2 D#3:2 B2:2',
      'E2:2 G#2:2 B2:2 G#2:2 D#2:2 F#2:2 A#2:2 F#2:2',      # IV - iii: the ground's F# over D# (was V7)
      'C#3:2 E3:2 G#3:2 E3:2 B2:2 D#3:2 F#3:2 D#3:2',
      'F#2:2 C#3:2 E3:2 D#3:2 B2:4 F#2:4']

# 4. semiquaver runs over the ground (b19-24)
T += ['B4:1 C#5:1 D#5:1 E5:1 F#5:1 G#5:1 F#5:1 E5:1 E5:1 D#5:1 C#5:1 D#5:1 A#4:1 B4:1 C#5:1 A#4:1',
      'B4:1 C#5:1 D#5:1 B4:1 F#5:1 E5:1 D#5:1 C#5:1 B4:1 C#5:1 D#5:1 E5:1 G#5:1 F#5:1 E5:1 D#5:1',
      'C#5:1 D#5:1 E5:1 C#5:1 A#4:1 B4:1 C#5:1 A#4:1 B4:1 C#5:1 D#5:1 B4:1 G#4:1 A#4:1 B4:1 G#4:1',
      'E5:1 F#5:1 G#5:1 E5:1 B4:1 C#5:1 D#5:1 B4:1 A#4:1 B4:1 C#5:1 D#5:1 E5:1 D#5:1 C#5:1 A#4:1',
      'B4:1 C#5:1 E5:1 G#5:1 B5:1 G#5:1 E5:1 C#5:1 D#5:1 E5:1 F#5:1 D#5:1 B4:1 C#5:1 D#5:1 B4:1',
      'A#4:1 C#5:1 E5:1 C#5:1 F#5:1 E5:1 C#5:1 A#4:1 B4:1 D#5:1 F#5:1 D#5:1 B4:4']
M += ['D#4:8 E4:8', 'D#4:8 G#3:8', 'C#4:8 B3:8', 'B3:8 C#4:8', 'G#3:8 B3:8', 'C#4:8 D#4:8']
# (the mean returns in minims under the runs, a third layer between the ground and the semiquavers;
#  it was silent here until the self-critique pass of Nov 2026)
B += GROUND

# close (b25-26): IV - V7 | I
T += ['G#5:8 F#5:4 E5:4', 'D#5:16']
M += ['B4:8 A#4:4 C#5:4', 'B4:16']
B += ['E3:8 F#3:8', 'B2:16']

BARS = {'Treble': T, 'Mean': M, 'Bass': B}


def build(path=None):
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Prelude XXIII in B major: A Ground upon Ut re mi fa sol la',
            'composer': 'Claude / Sam, after the English virginalists (Byrd, Bull)',
            'instrument': 'Piano (one player)',
            'key': 'B', 'mode': 'major', 'meter': list(METER), 'bpm': 72,
            'tempo_text': 'Moderato, like a pavan; the divisions in time',
            'movement_number': 23, 'piece_type': 'prelude', 'edition': 'third',
            # 26 bars of 4 quarters = 104 quarters; a breath before the close, which broadens
            'tempo_map': [[0, 72], [92, 72], [96, 66, 'ramp'], [96, 64], [104, 48, 'ramp']]}
    voices = [('Treble', 'Tr', 'treble', 70), ('Mean', 'Mn', 'treble', 56), ('Bass', 'Bs', 'bass', 62)]

    def dynamics(b):
        return [-6, -6, -5, -4, -4, -4, -2, -2, -1, 0, 0, -1, 0, 1, 2, 2, 1, 0,
                2, 3, 4, 5, 5, 4, 2, 0][b] if b < 26 else 0
    return W.build_score(path or HERE / 'prelude.json', meta, voices, BARS)


if __name__ == '__main__':
    for k, v in BARS.items():
        for i, b in enumerate(v):
            tot = sum(W.parse_tok(t)[1] for t in b.split())
            if tot != 16:
                raise SystemExit(f'{k} bar {i + 1}: {tot}')
    build()
    print('bars', len(T))
