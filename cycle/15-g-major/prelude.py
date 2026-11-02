#!/usr/bin/env python3
"""Prelude XV in G major: "Pastorale for the shepherds" (third edition).

One pianist, 12/8.  A musette: the left hand rocks between G and D like a bagpipe drone (and later
walks), the right hand plays a pipe tune over a continuous inner line of eighths.  The tune is
Luther's "Vom Himmel hoch" made pastoral: line 1 (G F# E F# D E F# G) in siciliano rhythm (b3-4),
answered in D (b5-6); lines 2 and 3 pass through D and E minor (b7-10); line 4, the falling octave,
comes as bells over the drone (b11-12), and b13 quotes the shepherds' flutes of Bach's 12/8
setting of the same chorale (BWV 248/23, flute interlude, bar 3, at pitch); the last bars stop on the dominant so that the fugue's first
G answers them.  Chorale source as in fugue.py (music21 corpus, Essen erk30/601).

Right hand: 'Zampogna' (tune) and 'Piffero' (eighths); left hand: 'Bordone'.  Every note is
written here as a literal bar string; the tune bars are the chorale lines with written-out
ornaments (b7-8 with Bach's passing notes from BWV 248/23); b13 is Bach's bar, quoted.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (12, 8)
B = W.Bars(['Zampogna', 'Piffero', 'Bordone'], METER)
REST = 'R:24'

# b1-2: the drone and the piffero alone (G - D rocking, the inner line circling the G chord)
B.bar('drone', Zampogna=REST,
      Piffero='B4:2 D5:2 B4:2 A4:2 C5:2 A4:2 G4:2 B4:2 D5:2 F#4:2 A4:2 C5:2',
      Bordone='G2:6 D3:6 G2:6 D3:6')
B.bar('drone', Zampogna='R:18 D5:6',
      Piffero='B4:2 D5:2 B4:2 A4:2 C5:2 A4:2 G4:2 B4:2 G4:2 F#4:2 A4:2 C5:2',
      Bordone='G2:6 D3:6 G2:6 D3:6')
# b3-4: line 1 in siciliano rhythm -- G (A) G | F# | E (F#) E | F# || D (E) D | E | F# | G
B.bar('line 1', Zampogna='G5:3 A5:1 G5:2 F#5:6 E5:3 F#5:1 E5:2 F#5:6',
      Piffero='B4:2 D5:2 B4:2 A4:2 D5:2 A4:2 G4:2 C5:2 G4:2 A4:2 C5:2 A4:2',
      Bordone='G2:6 D3:6 E3:6 D3:6')
B.bar('line 1', Zampogna='D5:3 E5:1 D5:2 E5:6 F#5:6 G5:6',
      Piffero='B4:2 G4:2 B4:2 C5:2 G4:2 C5:2 A4:2 D5:2 C5:2 B4:2 D5:2 B4:2',
      Bordone='G2:6 C3:6 D3:6 G2:6')
# b5-6: answered in D, an octave lower in the pipe, the drone moving to D - A
B.bar('line 1 in D', Zampogna='D5:3 E5:1 D5:2 C#5:6 B4:3 C#5:1 B4:2 C#5:6',
      Piffero='F#4:2 A4:2 F#4:2 E4:2 A4:2 E4:2 D4:2 G4:2 D4:2 E4:2 G4:2 E4:2',
      Bordone='D3:6 A2:6 B2:6 A2:6')
B.bar('line 1 in D', Zampogna='A4:3 B4:1 A4:2 B4:6 C#5:6 D5:6',
      Piffero='F#4:2 D4:2 F#4:2 G4:2 D4:2 G4:2 E4:2 A4:2 G4:2 F#4:2 A4:2 F#4:2',
      Bordone='D3:6 G2:6 A2:6 D2:6')
# b7-8: line 2 (G G D D B D C B) with Bach's passing notes (BWV 248/23, soprano), towards E minor
B.bar('line 2', Zampogna='G5:6 G5:6 D5:6 D5:4 C5:2',
      Piffero='B4:2 D5:2 B4:2 E5:2 C5:2 E5:2 B4:2 G4:2 B4:2 A4:2 F#4:2 A4:2',
      Bordone='B2:6 C3:6 B2:6 F#2:6')
B.bar('line 2', Zampogna='B4:4 C5:2 D5:6 C5:6 B4:6',
      Piffero='G4:2 E4:2 G4:2 F#4:2 B4:2 F#4:2 A4:2 E4:2 A4:2 G4:2 D#4:2 F#4:2',
      Bordone='E2:6 B2:6 A2:6 B2:6')
# b9-10: line 3 (B E E D F# G E D), E minor turning to D
B.bar('line 3', Zampogna='B4:3 C5:1 B4:2 E5:6 E5:3 F#5:1 E5:2 D5:6',
      Piffero='G4:2 E4:2 G4:2 G4:2 B4:2 G4:2 A4:2 C5:2 A4:2 B4:2 G4:2 B4:2',
      Bordone='E2:6 E3:6 C3:6 B2:6')
B.bar('line 3', Zampogna='F#5:6 G5:6 E5:3 F#5:1 E5:2 D5:6',
      Piffero='A4:2 D5:2 A4:2 B4:2 D5:2 B4:2 C#5:2 A4:2 G4:2 F#4:2 A4:2 F#4:2',
      Bordone='D3:6 G2:6 A2:6 D3:6')
# b11-13: line 4 as bells -- the falling octave, each bell struck and echoed an octave lower in the
# piffero, over the drone back on G
B.bar('line 4, bells', Zampogna='G5:6 F#5:6 E5:6 D5:6',
      Piffero='R:2 G4:2 B4:2 R:2 F#4:2 A4:2 R:2 E4:2 G4:2 R:2 D4:2 F#4:2',
      Bordone='G2:6 D3:6 C3:6 B2:6')
B.bar('line 4, bells', Zampogna='D5:6 C5:3 B4:3 A4:6 G4:6',
      Piffero='R:2 B3:2 F#4:2 R:2 E4:2 G4:2 R:2 D4:2 F#4:2 R:2 B3:2 D4:2',
      Bordone='B2:6 A2:6 D3:6 G2:6')
# b13: the shepherds' flutes of Bach's own 12/8 setting of this chorale (Christmas Oratorio, BWV 248/23,
# flute interlude, bar 3, at pitch); the piffero falls silent and the drone opens to G-B.
B.bar('bells', Zampogna='G5:3 E6:1 D6:2 D6:3 G5:1 F#5:2 G5:3 E6:1 D6:2 D6:3 G5:1 F#5:2',
      Piffero='R:24', Bordone='G2:6 B2:6 G2:6 B2:6')
# b14-16: the head of line 1 once more over a walking bass, then the dominant, held, for the fugue
B.bar('cadence', Zampogna='E5:3 F#5:1 E5:2 A5:6 G5:6 F#5:6',
      Piffero='C5:2 G4:2 C5:2 C5:2 A4:2 F#4:2 B4:2 G4:2 D4:2 D4:2 A4:2 C5:2',
      Bordone='C3:6 D3:6 E3:6 D3:6')
B.bar('cadence', Zampogna='G5:3 F#5:1 E5:2 F#5:6 E5:6 D5:6',
      Piffero='B4:2 D5:2 B4:2 A4:2 D5:2 A4:2 A4:2 C#5:2 A4:2 F#4:2 A4:2 F#4:2',
      Bordone='G2:6 D3:6 A2:6 D2:6')
B.bar('half cadence (attacca)', Zampogna='E5:6 C#5:6 D5:12',
      Piffero='A4:2 G4:2 E4:2 A4:2 G4:2 E4:2 F#4:12',
      Bordone='A2:6 A2:6 D3:12')


def build(path=None):
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': "Prelude XV in G major: Pastorale for the shepherds",
            'composer': "Claude / Sam (on Luther's chorale 'Vom Himmel hoch', 1539)",
            'instrument': 'Piano (one player)',
            'key': 'G', 'mode': 'major', 'meter': list(METER), 'bpm': 78,
            'tempo_text': 'Pastorale (dotted quarter = 52)',
            'movement_number': 15, 'piece_type': 'prelude', 'edition': 'third',
            # 16 bars of 6 quarters = 96 quarters; the drone broadens into the half cadence
            'tempo_map': [[0, 78], [84, 78], [90, 66, 'ramp'], [90, 60], [96, 48, 'ramp']]}
    voices = [('Zampogna', 'Zamp', 'treble', 74), ('Piffero', 'Piff', 'treble', 58), ('Bordone', 'Bord', 'bass', 62)]

    def dynamics(b):
        return {0: -6, 1: -4, 6: 2, 7: 3, 8: 2, 9: 2, 10: 4, 11: 4, 12: 2, 13: 0, 14: -2, 15: -4}.get(b, 0)
    return W.build_score(path or HERE / 'prelude.json', meta, voices, B.bars, tags=B.tags, dynamics=dynamics)


if __name__ == '__main__':
    build()
    print('bars', len(B))
