#!/usr/bin/env python3
"""Prelude XVI in G minor: "Fantasia" (third edition).

A short stylus-phantasticus fantasia for organ (two manual hands, alto and tenor in the left hand, and
pedal), before the chorale fantasia on "An Wasserflüssen Babylon".  It alludes to the opening of
Bach's Fantasia in G minor BWV 542: a held G in the treble with a written-out mordent and a turn in
thirty-seconds over a G pedal, the left hand striking chords on beats 1 and 3.  Only the first two
beats follow Bach's figure (after the Mutopia edition of BWV 542, read as data); everything else is
new and written here by hand.

  b1-4    Exordium over the G pedal: i - vii°7 | iv - V7 | i - vii°7 (a run through the diminished
          seventh) | V7, a sudden rest, a falling diminished cascade into the silence.
  b5-8    Recitativo: VI - iv | Neapolitan sixth - V7 | i - VI - vii°7/V | V, a cadenza over the D pedal.
  b9-12   Choral: line 1 of the chorale, in the treble at half speed, over a lament bass
          (G F# F E Eb D) with suspensions in the inner voices -- the fugue's first subject, heard
          once before it is worked.
  b13-16  Conclusio over the D pedal: a phrase and its echo an octave lower, two struck chords with
          rests between them (D7b9, vii°7 of D), and the half cadence on D for the fugue, which
          begins on D alone.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
B = W.Bars(['Diskant', 'Alt', 'Tenor', 'Pedal'], METER)

# ---------------------------------------------------------------- b1-4 Exordium (G pedal)
# b1: G with a written-out mordent and Bach's turn (BWV 542, Fantasia, b1, beats 1-2), then F#
B.bar('exordium: i - vii°7',
      Diskant='G5:0.5 F#5:0.5 G5:1 G5:0.5 Bb5:0.5 A5:0.5 G5:0.5 F#5:0.5 G5:0.5 F#5:0.5 G5:0.5 '
              'G5:1.5 A5:0.5 F#5:2 A5:0.5 G5:0.5 F#5:0.5 G5:0.5 Eb5:0.5 D5:0.5 Eb5:0.5 F5:0.5 '
              'Eb5:1.5 F5:0.5',
      Alt='Bb4:4 R:4 A4:4 R:4',
      Tenor='D4:4 R:4 Eb4:4 R:4',
      Pedal='G2:16~')
B.bar('exordium: iv - V7',
      Diskant='Eb5:2 G5:0.5 F5:0.5 Eb5:0.5 D5:0.5 C5:0.5 D5:0.5 C5:0.5 D5:0.5 D5:1.5 Eb5:0.5 '
              'D5:2 F#5:0.5 E5:0.5 D5:0.5 C5:0.5 Bb4:0.5 C5:0.5 Bb4:0.5 C5:0.5 C5:1.5 D5:0.5',
      Alt='G4:4 R:4 F#4:4 R:4',
      Tenor='C4:4 R:4 C4:4 R:4',
      Pedal='G2:16~')
B.bar('exordium: i - vii°7 (a run through the diminished seventh)',
      Diskant='Bb4:2 D5:0.5 C5:0.5 Bb4:0.5 A4:0.5 G4:0.5 A4:0.5 Bb4:0.5 C#5:0.5 E5:0.5 G5:0.5 '
              'Bb5:0.5 C#6:0.5 E6:4 D6:1 C#6:1 Bb5:1 G5:1',
      Alt='G4:4 R:4 Bb4:4 R:4',
      Tenor='D4:4 R:4 C#4:4 R:4',
      Pedal='G2:16')
B.bar('V7 - sudden rest - cascade',
      Diskant='F#5:4 R:4 Eb6:0.5 C6:0.5 A5:0.5 F#5:0.5 Eb5:0.5 C5:0.5 A4:0.5 F#4:0.5 G4:4',
      Alt='A4:4 R:12',
      Tenor='D4:4 R:12',
      Pedal='D2:4 R:12')

# ---------------------------------------------------------------- b5-8 Recitativo
B.bar('recitativo: VI - iv',
      Diskant='R:2 Eb5:2 G5:1.5 Eb5:0.5 Bb4:1.5 D5:0.5 C5:2 G5:2 Eb6:3 D6:1',
      Alt='G4:16',
      Tenor='Bb3:8 C4:8',
      Pedal='Eb2:8 C2:8')
B.bar('recitativo: Neapolitan sixth - V7',
      Diskant='C6:2 Ab5:0.5 G5:0.5 F5:0.5 Eb5:0.5 F5:2 R:2 F#5:1.5 G5:0.5 A5:1.5 C6:0.5 '
              'Bb5:1 A5:1 G5:1 F#5:1',
      Alt='Ab4:8 A4:8',
      Tenor='C4:16',
      Pedal='C2:8 D2:8')
B.bar('recitativo: i - VI - vii°7/V',
      Diskant='G5:3 D6:1 Eb6:0.5 D6:0.5 C6:0.5 Bb5:0.5 A5:0.5 G5:0.5 F#5:0.5 G5:0.5 Bb5:2 G5:2 '
              'E5:1 G5:1 F#5:1 E5:1',
      Alt='Bb4:12 G4:4',
      Tenor='D4:8 Eb4:4 E4:4',
      Pedal='G2:8 Eb2:4 C#2:4')
B.bar('cadenza over the dominant',
      Diskant='D5:0.5 F#5:0.5 A5:0.5 D6:0.5 C6:0.5 A5:0.5 F#5:0.5 A5:0.5 C6:0.5 Bb5:0.5 A5:0.5 C6:0.5 '
              'Eb6:2 D6:1 C6:1 Bb5:1 A5:1 G5:1 F#5:1 A5:2',
      Alt='F#4:8 A4:8',
      Tenor='A3:8 C4:8',
      Pedal='D2:16')

# ---------------------------------------------------------------- b9-12 Choral: line 1 over a lament bass
# 'An Wasserflüssen Babylon' (BWV 267, soprano, in G minor) at half speed in the treble.
B.bar('choral: line 1',
      Diskant='D5:8 Eb5:8', Alt='Bb4:8 C5:8', Tenor='D4:8 A3:8', Pedal='G2:8 F#2:8')
B.bar('choral: line 1',
      Diskant='D5:4 C5:4 Bb4:4 C5:4', Alt='Bb4:4 A4:4 G4:8~', Tenor='D4:4 Eb4:4 D4:8', Pedal='F2:8 E2:8')
B.bar('choral: line 1',
      Diskant='D5:8 C5:4 Bb4:4', Alt='G4:8 F#4:4 G4:4', Tenor='G3:8 A3:4 Bb3:4', Pedal='Eb2:8 D2:8~')
B.bar('choral: line 1, cadence',
      Diskant='C5:8 Bb4:8', Alt='F#4:8 G4:8', Tenor='A3:8 G3:8', Pedal='D2:8 G2:8')

# ---------------------------------------------------------------- b13-16 Conclusio over the D pedal
B.bar('conclusio: a phrase',
      Diskant='Bb5:2 A5:0.5 G5:0.5 F#5:0.5 G5:0.5 D6:2 C6:0.5 Bb5:0.5 A5:0.5 Bb5:0.5 '
              'A5:2 G5:0.5 F#5:0.5 G5:0.5 A5:0.5 C6:0.5 Bb5:0.5 A5:0.5 G5:0.5 F#5:0.5 E5:0.5 D5:0.5 C5:0.5',
      Alt='G4:8 F#4:8',
      Tenor='G3:8 A3:8',
      Pedal='D2:16~')
B.bar('conclusio: its echo, an octave lower',
      Diskant='Bb4:2 A4:0.5 G4:0.5 F#4:0.5 G4:0.5 D5:2 C5:0.5 Bb4:0.5 A4:0.5 Bb4:0.5 '
              'A4:2 G4:0.5 F#4:0.5 G4:0.5 A4:0.5 C5:2 D5:2',
      Pedal='D2:16~')
B.bar('conclusio: struck chords and rests',
      Diskant='Eb5:4 R:4 E5:4 R:4',
      Alt='C5:4 R:4 C#5:4 R:4',
      Tenor='F#4:4 R:4 G4:4 R:4',
      Pedal='D2:16~')
B.bar('half cadence (attacca)',
      Diskant='D5:16', Alt='A4:16', Tenor='F#4:16', Pedal='D2:16')


def build(path=None):
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Prelude XVI in G minor: Fantasia',
            'composer': 'Claude / Sam (alluding to the opening of J. S. Bach\'s Fantasia BWV 542)',
            'instrument': 'Organ: two hands and pedal',
            'key': 'G', 'mode': 'minor', 'meter': list(METER), 'bpm': 56,
            'tempo_text': 'Fantasia: libero',
            'movement_number': 16, 'piece_type': 'prelude', 'edition': 'third',
            # 16 bars = 64 quarters.  Free at the start; the recitative a little faster; the cadenza
            # held back; the chorale line steady; the struck chords slower; a long last chord.
            'tempo_map': [[0, 56], [12, 52], [16, 60], [28, 58], [32, 42, 'ramp'], [32, 60],
                          [44, 60], [48, 50, 'ramp'], [48, 58], [56, 48], [64, 34, 'ramp']]}
    voices = [('Diskant', 'Disk.', 'treble', 72), ('Alt', 'Alt', 'treble', 60),
              ('Tenor', 'Ten.', 'treble_8', 60), ('Pedal', 'Ped.', 'bass', 70)]

    def dynamics(b):
        return {0: 2, 1: 2, 2: 4, 3: 4, 4: 0, 5: 1, 6: 2, 7: 2, 8: -4, 9: -4, 10: -3, 11: -4,
                12: 2, 13: -8, 14: 4, 15: 2}.get(b, 0)
    return W.build_score(path or HERE / 'prelude.json', meta, voices, B.bars, tags=B.tags, dynamics=dynamics)


if __name__ == '__main__':
    build()
    print('bars', len(B))
