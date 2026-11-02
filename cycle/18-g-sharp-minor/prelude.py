#!/usr/bin/env python3
"""Prelude XVIII in G-sharp minor: "Der Waechter" (the watchman).  One player.

Three layers: the fugue's subject sung in the right hand (Phrygian at evening, then once more with
the A-sharp of the second watch), a knocking middle voice (the knock figure of the fugue's door
subject: knock, knock, KNOCK, one figure per bar), and a walking bass.  At "midnight" (b11-12) the
middle voice plays the whole door subject; over a dominant pedal (b13-14) a fourth voice adds the
leading tone.  The prelude ends on an open fifth with three knocks that nobody answers: the third
(and the morning) are left to the fugue.

Every note is written here as a literal token string.  Bar = 4/4 (16 sixteenths).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)


def kn(x, y):
    """the watchman's knock: x, x, then y (a quarter) on the third beat"""
    return f'{x}:2 R:2 {x}:2 R:2 {y}:4 R:4'


# ---------------------------------------------------------------- I. evening: the subject (Phrygian) above, b1-5
S = ('G#4:8 A4:8 B4:8 E5:12 D#5:4 C#5:8 B4:4 A4:4 G#4:8 F#4:8 G#4:8 ')
K = (kn('D#4', 'E4') + ' ' + kn('F#4', 'G#4') + ' ' + 'C#4:2 R:2 D#4:2 R:2 E4:4 R:4 ' + kn('B3', 'E4') + ' '
     + kn('C#4', 'B3') + ' ')
B = ('G#2:8 C#3:8 D#3:8 C#3:8 A2:4 B2:4 C#3:8 E3:8 C#3:8 A2:8 G#2:8 ')   # A -> G#: the Phrygian close
T = 'R:80 '

# ---------------------------------------------------------------- II. the answer in the bass (on D#), b6-10
S += 'A#4:8 G#4:8 A#4:8 D#5:8 D#5:4 C#5:4 B4:8 A#4:4 G#4:4 F#4:8 G#4:8 A#4:8 '
K += (kn('F#4', 'E4') + ' ' + kn('C#4', 'D#4') + ' ' + kn('F#4', 'B3') + ' ' + kn('C#4', 'D#4') + ' '
      + kn('G#3', 'F##3') + ' ')
B += 'D#3:8 E3:8 F#3:8 B3:12 A#3:4 G#3:8 F#3:4 E3:4 D#3:8 C#3:4 E3:4 D#3:8 '   # the answer, then E -> D#
T += 'R:80 '

# ---------------------------------------------------------------- III. midnight: the door subject in the middle, b11-14
S += 'B4:8 D#5:4 C#5:12 A#4:4 B4:4 '
K += 'D#4:2 R:2 D#4:2 R:2 D#4:4 E4:4 E#4:4 F#4:4 F##4:4 G#4:8 '
B += 'G#2:8 B2:4 C#3:8 A#2:4 D#3:4 G#2:4 '
T += 'G#3:8 R:24 '
# dominant pedal: the 6/4 sighs over D#, the knocks go on
S += 'B4:4 A#4:4 A#4:8 C#5:8 B4:4 A#4:4 '
K += 'F##4:4 R:8 ' + kn('D#4', 'D#4') + ' '
B += 'D#2:32 '
T += 'R:8 F##3:16 G#3:4 F##3:4 '

# ---------------------------------------------------------------- IV. the subject again, with the A# of the next watch, b15-20
S += 'G#4:8 A#4:8 B4:8 E5:12 D#5:4 C#5:8 B4:4 A#4:4 G#4:8 F#4:8 G#4:24'
K += (kn('D#4', 'F#4') + ' ' + kn('G#4', 'E4') + ' ' + kn('E4', 'F#4') + ' ' + kn('F#4', 'E4') + ' '
      + kn('D#4', 'B3') + ' ' + kn('D#4', 'D#4'))
B += 'G#2:8 F#2:8 E2:8 C#3:16 F#2:8 B2:4 F#2:4 C#3:8 D#3:8 G#2:24'
T += 'G#3:8 R:88'


def build(path=None):
    bars = {n: W.concat_bars(s, METER) for n, s in
            [('Right hand (song)', S), ('Right hand (knocks)', K), ('Left hand (tenor)', T), ('Left hand (bass)', B)]}
    nb = len(bars['Right hand (song)'])
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Prelude XVIII in G-sharp minor: Der Waechter (the watchman)',
            'composer': 'Claude / Sam (after J. S. Bach, BWV 61 no. 4)',
            'instrument': 'Keyboard (one player)', 'key': 'G#', 'mode': 'minor', 'meter': list(METER),
            'bpm': 66, 'tempo_text': 'Lento, sempre piano: the knocks detached',
            'tempo_map': [[(nb - 2) * 4, 66], [nb * 4, 46, 'ramp']],
            'movement_number': 18, 'piece_type': 'prelude', 'edition': 'third'}
    voices = [('Right hand (song)', 'S', 'treble', 70), ('Right hand (knocks)', 'K', 'treble', 54),
              ('Left hand (tenor)', 'T', 'bass', 56), ('Left hand (bass)', 'B', 'bass', 62)]
    entries = [('Right hand (song)', 1, 0, 'Subject (Phrygian), as in the fugue', 5),
               ('Left hand (bass)', 6, 0, 'Answer in the bass', 5),
               ('Right hand (knocks)', 11, 0, 'Door subject (BWV 61: "Siehe, ich stehe vor der Tuer")', 2),
               ('Right hand (song)', 15, 0, 'Subject (Aeolian: the second watch)', 5)]
    return W.build_score(path or (HERE / 'prelude.json'), meta, voices, bars, entries=entries,
                         subject='G#4:8 A4:8 B4:8 E5:12 D#5:4 C#5:8 B4:4 A4:4 G#4:8 F#4:8')


if __name__ == '__main__':
    for n, s in [('S', S), ('K', K), ('T', T), ('B', B)]:
        print(n, sum(W.parse_tok(t)[1] for t in s.split()) / 16)
    build()
