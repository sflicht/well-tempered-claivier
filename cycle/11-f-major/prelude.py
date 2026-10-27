#!/usr/bin/env python3
"""Prelude XI in F major (third edition): Invention a 2, 12/8.

After the F-major prelude of WTC I (BWV 856): two voices, 12/8, one hand running in sixteenths while
the other speaks in eighths, and the roles traded back and forth.  Its theme is the fugue subject made
to swing: the fanfare head C C F | F F A | A C becomes three groups of triplet eighths, the running tail
(D C B-flat A ...) keeps its sixteenths and now falls in groups of six.  The countersubject Q runs in
sixteenths under the head and walks in eighths under the tail; the pair is invertible at the octave
(no fifths on the eighth-note positions, which would become fourths), and is heard both ways round:
P over Q (F, d, D-flat) and Q over P (C, B-flat, F).

Plan (bars of 12/8):
  1-3     P in F (right hand) over Q; answer in C in the left hand with Q above.
  4-5     episode: the head, on the bass, climbs through C-F-B-flat-A under falling sixteenths.
  6-7     P in D minor over Q.
  7-9     episode: descending fifths d-g-C-F-B-flat, the head again in the left hand.
  10-11   P in B-flat in the left hand, Q above.
  11-12   the head in imitation, B-flat - g - d, to a half cadence on C: the right hand plays the
          subject's upbeat "C C" alone...
  13-14   ...and the theme arrives in D-FLAT major (the surprise: the flat sixth instead of F).
  14-15   B-flat minor, a diminished seventh, the dominant: back to F.
  16-17   P in F in the left hand, Q above.
  17-18   stretto: the head in the right hand and its inversion a beat later in the left; the tail to
          the cadence.
  19-21   the head tossed between the hands as an echo game; a cadence; and at the very end the right
          hand says the fugue's opening words straight -- C C | F in sixteenths, not in triplets.

Every pitch is written here (the statements of P and Q in other keys are written-out transpositions of
the two lines below, done with wtclib.transpose and pasted literally).  Playable by one pianist: right
hand = upper voice, left hand = lower voice throughout.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (12, 8)

# The theme P (the fugue subject with a triplet head) and its countersubject Q, in F.
P = ('C5:2 C5:2 F5:2 F5:2 F5:2 A5:2 A5:2 C6:4 '
     'D6:1 C6:1 Bb5:1 A5:1 Bb5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 E5:1 C5:1 D5:1 E5:1 F5:2')
Q = ('A3:1 G3:1 A3:1 Bb3:1 A3:1 F3:1 D4:1 C4:1 D4:1 E4:1 F4:1 D4:1 C4:1 Bb3:1 A3:1 Bb3:1 C4:1 A3:1 '
     'Bb3:2 D4:2 G4:2 E4:2 G4:2 Bb4:2 C5:2 Bb4:2 A4:2')

RH, LH = [], []


def sec(rh, lh):
    RH.append(rh)
    LH.append(lh)


# ---------------------------------------------------------------- b1-3: P over Q in F; Q over P in C
sec(P, Q)
sec('E5:1 D5:1 E5:1 F5:1 E5:1 C5:1 A5:1 G5:1 A5:1 B5:1 C6:1 A5:1 G5:1 F5:1 E5:1 F5:1 G5:1 E5:1 '
    'F5:2 A5:2 D6:2 B5:2 D6:2 F6:2 G6:2 F6:2 E6:2',                       # Q in C, two octaves up
    'G3:2 G3:2 C4:2 C4:2 C4:2 E4:2 E4:2 G4:4 '
    'A4:1 G4:1 F4:1 E4:1 F4:1 E4:1 D4:1 C4:1 D4:1 C4:1 B3:1 A3:1 B3:1 G3:1 A3:1 B3:1 C4:2')  # P in C
# ---------------------------------------------------------------- b4-5: episode, the head on the bass
sec('G6:1 F6:1 E6:1 F6:1 E6:1 C6:1 G6:1 F6:1 E6:1 D6:1 C6:1 Bb5:1 '
    'A5:1 G5:1 A5:1 Bb5:1 A5:1 F5:1 C6:1 Bb5:1 A5:1 G5:1 F5:1 Eb5:1 '
    'D5:1 Eb5:1 F5:1 Eb5:1 D5:1 C5:1 D5:1 F5:1 Bb5:1 A5:1 Bb5:1 F5:1 '
    'E5:1 F5:1 G5:1 F5:1 E5:1 D5:1 C#5:1 D5:1 E5:1 D5:1 C#5:1 B4:1',
    'G3:2 G3:2 C4:2 C4:2 C4:2 E4:2 F4:2 F4:2 C4:2 C4:2 C4:2 A3:2 '
    'Bb3:2 Bb3:2 F3:2 F3:2 F3:2 D3:2 E3:2 E3:2 A3:2 A3:2 G3:2 E3:2')
# ---------------------------------------------------------------- b6-7: P in D minor over Q
sec('A4:2 A4:2 D5:2 D5:2 D5:2 F5:2 F5:2 A5:4 '
    'Bb5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 E5:1 D5:1 C#5:1 B4:1 C#5:1 A4:1 B4:1 C#5:1 D5:2',
    'F3:1 E3:1 F3:1 G3:1 F3:1 D3:1 Bb3:1 A3:1 Bb3:1 C4:1 D4:1 Bb3:1 A3:1 G3:1 F3:1 G3:1 A3:1 F3:1 '
    'G3:2 Bb3:2 E4:2 C#4:2 E4:2 G4:2 A4:2 G4:2 F4:2')
# ---------------------------------------------------------------- b7-9: descending fifths to B-flat
sec('F5:1 E5:1 F5:1 G5:1 F5:1 D5:1 A5:1 G5:1 F#5:1 G5:1 A5:1 C6:1 '              # d, D7
    'Bb5:1 A5:1 G5:1 A5:1 Bb5:1 G5:1 E5:1 F5:1 G5:1 A5:1 G5:1 Bb5:1 '             # g, C7
    'A5:1 G5:1 A5:1 G5:1 A5:1 F5:1 C6:1 Bb5:1 A5:1 Bb5:1 C6:1 Eb6:1 '             # F, F7
    'D6:1 C6:1 Bb5:1 C6:1 D6:1 Bb5:1 G5:1 Bb5:1 G5:1 F5:1 G5:1 Bb5:1 '            # B-flat, E-flat
    'A5:1 Bb5:1 A5:1 G5:1 A5:1 F5:1 C6:1 Bb5:1 A5:1 G5:1 F5:1 Eb5:1',             # F, F7
    'D4:2 D4:2 A3:2 A3:2 A3:2 F#3:2 D3:2 D3:2 G3:2 G3:2 G3:2 C3:2 '
    'C3:2 C3:2 F3:2 F3:2 F3:2 A3:2 F3:2 F3:2 Bb3:2 Bb3:2 Bb3:2 Eb3:2 '
    'C3:2 C3:2 F3:2 F3:2 F3:2 A3:2')
# ---------------------------------------------------------------- b10-11: Q over P in B-flat
sec('D5:1 C5:1 D5:1 Eb5:1 D5:1 Bb4:1 G5:1 F5:1 G5:1 A5:1 Bb5:1 G5:1 F5:1 Eb5:1 D5:1 Eb5:1 F5:1 D5:1 '
    'Eb5:2 G5:2 C6:2 A5:2 C6:2 Eb6:2 F6:2 Eb6:2 D6:2',
    'F3:2 F3:2 Bb3:2 Bb3:2 Bb3:2 D4:2 D4:2 F4:4 '
    'G4:1 F4:1 Eb4:1 D4:1 Eb4:1 D4:1 C4:1 Bb3:1 C4:1 Bb3:1 A3:1 G3:1 A3:1 F3:1 G3:1 A3:1 Bb3:2')
# ---------------------------------------------------------------- b11-12: the head in imitation, to C; "C C" alone
sec('F5:2 F5:2 Bb5:2 Bb5:2 Bb5:2 D6:2 D6:2 F6:4 '
    'E6:1 D6:1 C6:1 Bb5:1 A5:1 G5:1 E5:2 G5:2 C6:2 R:2 C6:1 C6:1 R:2',
    'D3:1 C3:1 D3:1 Eb3:1 D3:1 Bb2:1 G3:1 F3:1 G3:1 A3:1 Bb3:1 G3:1 F3:1 E3:1 D3:1 E3:1 F3:1 D3:1 '
    'G2:2 C3:2 E3:2 C3:1 D3:1 E3:1 F3:1 G3:1 E3:1 C3:2 R:4')
# ---------------------------------------------------------------- b13-14: the surprise -- P over Q in D-FLAT major
sec('Ab4:2 Ab4:2 Db5:2 Db5:2 Db5:2 F5:2 F5:2 Ab5:4 '
    'Bb5:1 Ab5:1 Gb5:1 F5:1 Gb5:1 F5:1 Eb5:1 Db5:1 Eb5:1 Db5:1 C5:1 Bb4:1 C5:1 Ab4:1 Bb4:1 C5:1 Db5:2',
    'F3:1 Eb3:1 F3:1 Gb3:1 F3:1 Db3:1 Bb3:1 Ab3:1 Bb3:1 C4:1 Db4:1 Bb3:1 Ab3:1 Gb3:1 F3:1 Gb3:1 Ab3:1 F3:1 '
    'Gb3:2 Bb3:2 Eb4:2 C4:2 Eb4:2 Gb4:2 Ab4:2 Gb4:2 F4:2')
# ---------------------------------------------------------------- b14-15: b-flat minor, diminished 7th, C7
sec('F5:2 F5:2 Bb5:2 Bb5:2 Bb5:2 Db6:2 '
    'C6:1 Bb5:1 A5:1 Bb5:1 G5:1 E5:1 C5:1 D5:1 E5:1 F5:1 G5:1 Bb5:1 '
    'G5:1 F5:1 E5:1 F5:1 G5:1 E5:1 E5:1 D5:1 C5:1 Bb4:1 C5:1 Bb4:1',
    'Db4:1 C4:1 Bb3:1 C4:1 Db4:1 Bb3:1 G3:1 F3:1 E3:1 F3:1 G3:1 E3:1 '
    'C3:2 C3:2 E3:2 E3:2 E3:2 G3:2 G3:2 E3:4 C3:6')
# ---------------------------------------------------------------- b16-17: Q over P in F
sec('A4:1 G4:1 A4:1 Bb4:1 A4:1 F4:1 D5:1 C5:1 D5:1 E5:1 F5:1 D5:1 C5:1 Bb4:1 A4:1 Bb4:1 C5:1 A4:1 '
    'Bb4:2 D5:2 G5:2 E5:2 G5:2 Bb5:2 C6:2 Bb5:2 A5:2',
    'C3:2 C3:2 F3:2 F3:2 F3:2 A3:2 A3:2 C4:4 '
    'D4:1 C4:1 Bb3:1 A3:1 Bb3:1 A3:1 G3:1 F3:1 G3:1 F3:1 E3:1 D3:1 E3:1 C3:1 D3:1 E3:1 F3:2')
# ---------------------------------------------------------------- b17-18: stretto, head and its inversion; the cadence
sec('C5:2 C5:2 F5:2 F5:2 F5:2 A5:2 A5:2 C6:4 '
    'D6:1 C6:1 Bb5:1 A5:1 Bb5:1 A5:1 G5:1 F5:1 G5:1 F5:1 E5:1 D5:1 E5:1 C5:1 D5:1 E5:1 F5:2',
    'F3:1 G3:1 A3:1 Bb3:1 A3:1 F3:1 '
    'F3:2 F3:2 C3:2 C3:2 C3:2 A2:2 A2:2 F2:4 '
    'Bb2:2 G2:2 E2:2 C3:4 C2:2')
# ---------------------------------------------------------------- b19-21: the echo game, the cadence, the fugue's first words
sec('C6:2 C6:2 F6:2 R:6 F5:2 F5:2 Bb5:2 R:6 '
    'G5:2 G5:2 C6:2 E5:2 G5:2 Bb5:2 A5:6 R:6 '
    'R:2 C6:1 C6:1 F6:20',
    'F2:6 C3:2 C3:2 F3:2 Bb2:6 F3:2 F3:2 Bb2:2 '
    'C3:6 C3:2 C3:2 C2:2 F2:6 R:6 '
    'R:4 F2:20')

BARS = {'Right hand': W.concat_bars(' '.join(RH), METER), 'Left hand': W.concat_bars(' '.join(LH), METER)}

DYN = {1: 0, 4: -3, 6: 2, 7: -2, 10: 2, 11: 0, 12: -4, 13: 4, 14: 0, 16: 3, 17: 5, 19: 0, 20: -2, 21: 2}


def dyn(b):
    v = 0
    for k in sorted(DYN):
        if b + 1 >= k:
            v = DYN[k]
    return v


if __name__ == '__main__':
    nb = {len(v) for v in BARS.values()}
    assert len(nb) == 1, {k: len(v) for k, v in BARS.items()}
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Prelude XI in F major: Invention a 2',
            'composer': 'Claude / Sam (after the F-major prelude of WTC I, BWV 856)', 'instrument': 'Piano',
            'key': 'F', 'mode': 'major', 'meter': list(METER), 'bpm': 90,
            'tempo_text': 'Allegretto giocoso (dotted quarter = 60)',
            'movement_number': 11, 'piece_type': 'prelude', 'edition': 'third',
            # a breath on the lone "C C" before the D-flat surprise; a broadening into the last cadence
            # and a held last bar
            'tempo_map': [[66, 90], [72, 66, 'ramp'], [72, 90], [108, 90], [117, 70, 'ramp'],
                          [120, 74], [126, 56, 'ramp']]}
    voices = [('Right hand', 'RH', 'treble', 70), ('Left hand', 'LH', 'bass', 64)]
    W.build_score(HERE / 'prelude.json', meta, voices, BARS, dynamics=dyn, subject=P,
                  entries=[('Right hand', 1, 0, 'theme (F)', 2), ('Left hand', 2, 3, 'answer (C)', 2),
                           ('Right hand', 6, 0, 'theme (d)', 2), ('Left hand', 10, 0, 'theme (B-flat)', 2),
                           ('Right hand', 13, 0, 'theme in D-flat: the surprise', 2),
                           ('Left hand', 16, 0, 'theme (F)', 2), ('Right hand', 17, 3, 'stretto: theme', 2),
                           ('Left hand', 17, 4.5, 'stretto: head inverted', 1)])
    print('bars', len(BARS['Right hand']))
