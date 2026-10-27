#!/usr/bin/env python3
"""Prelude IX in E major: Pastorale in just intonation (the comma pump).

WTC I's E-major prelude (BWV 854) is a 12/8 pastorale; so is this one: a lilting tune over a rocking
tenor and a slow bass, for one pianist (right hand: soprano + alto; left hand: tenor + bass).

The harmony of the 8-bar theme is I - vi - ii7 - V7 | I - IV - I6/4 V7 - I.  Its antecedent is the
classic comma pump: when every chord is tuned pure and the common tones keep their pitch
(I->vi keeps E and G#, vi->ii7 keeps C# and E, ii7->V7 keeps F# and A, V->I keeps B), the new tonic
is a syntonic comma (21.5 c) flat.  The written voices hold those common tones literally (ties in
S, A, T across bars 1-5 of each cycle).  The theme returns four times, so the piece settles by
four commas (86 c, the better part of a semitone); then the coda plays the same loop on a
well-tempered keyboard (Bach-Lehman), which does not drift: the tonic jumps back up by 86 c to
the pitch it started from.  That jump is the problem the well-tempered keyboard solved.

  cycle 1 (b1-8)    the theme
  cycle 2 (b9-16)   the pipes: the tune over an alto countermelody in eighths
  cycle 3 (b17-24)  the tune moves into the alto, an octave lower, under a new descant
  cycle 4 (b25-32)  da capo: the same notes as cycle 1, three commas lower; a breath
  coda (b33-36)     the loop once more, in Bach-Lehman

Every note is written here.  The tuning is performance, not composition: tune_prelude.py derives
every note's 'cents' from these notes and the chord chart below (CYCLE_HARMONY, CODA_HARMONY), and
also writes prelude-tempered.json (the same notes without cents) for comparison renders.
Render prelude.json with --temperament equal so that only those cents apply.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (12, 8)
VOICES = ['Soprano', 'Alto', 'Tenor', 'Bass']


def e(s):
    """A run of eighths: each argument pitch gets the eighth-note value (the pitches are written by hand)."""
    return ' '.join(f'{p}:2' for p in s.split())


# ------------------------------------------------------------------ the theme (cycle 1)
TUNE = ['B4:4 C#5:2 B4:4 E5:2 G#5:12~',
        'G#5:4 A5:2 G#5:4 F#5:2 E5:6 C#5:6~',
        'C#5:6 E5:4 F#5:2 A5:12~',
        'A5:4 G#5:2 F#5:4 E5:2 D#5:6 B4:6',
        'B4:4 C#5:2 B4:4 E5:2 G#5:6 B5:6~',
        'B5:4 A5:2 G#5:4 F#5:2 E5:6 C#6:6',
        'B5:4 A5:2 G#5:6 F#5:6 A5:6',
        'G#5:4 F#5:2 E5:18']
BASS = ['E3:12 B2:12', 'C#3:24', 'F#2:24', 'B2:24', 'E3:12 G#2:12', 'A2:24', 'B2:24', 'E3:12 E2:12']
A1 = ['E4:12 B4:12', 'G#4:18 E4:6~', 'E4:12 F#4:12~', 'F#4:18 D#4:6', 'E4:12 B4:12', 'A4:12 C#5:12',
      'G#4:12 A4:12', 'E4:12 G#4:12']
T1 = ['B3:6 G#3:6 B3:6 G#3:6', 'C#4:6 G#3:6 C#4:6 G#3:6', 'A3:12 F#3:12~', 'F#3:6 B3:6 A3:12',
      'G#3:6 B3:6 E3:12', 'A3:12 E3:12', 'G#3:6 B3:6 A3:6 F#3:6', 'G#3:12 E3:12']
# ------------------------------------------------------------------ cycle 2: the pipes (alto countermelody in eighths)
A2 = [e('E4 D#4 E4 G#4 F#4 E4 B4 A4 G#4 E4 F#4 G#4'),
      e('E4 D#4 C#4 E4 F#4 G#4 G#4 F#4 G#4 E4 D#4 E4'),
      e('E4 F#4 E4 A4 G#4 E4 A4 G#4 F#4 A4 G#4 F#4'),
      e('F#4 G#4 F#4 D#4 E4 F#4 B4 A4 G#4 F#4 E4 F#4'),
      e('G#4 F#4 E4 E4 F#4 G#4 B4 C#5 A4 B4 C#5 B4'),
      e('A4 B4 C#5 B4 A4 G#4 A4 G#4 F#4 C#5 B4 A4'),
      e('G#4 A4 B4 A4 G#4 E4 D#4 E4 F#4 B4 A4 F#4'),
      'E4:2 F#4:2 G#4:2 B4:2 A4:2 G#4:2 G#4:12']
T2 = ['B3:12 G#3:12', 'C#4:12 G#3:12', 'A3:12 F#3:12~', 'F#3:12 A3:12', 'G#3:12 E3:12', 'C#4:12 E3:12',
      'G#3:12 B3:12', 'G#3:24']
# ------------------------------------------------------------------ cycle 3: the tune in the alto, a descant above
TUNE_LOW = [W.transpose(s, -12, -7) for s in TUNE]
S3 = ['G#4:4 A4:2 G#4:4 B4:2 E5:12~',
      'E5:4 F#5:2 E5:4 D#5:2 C#5:6 E5:6~',
      'E5:6 C#5:4 A4:2 C#5:12~',
      'C#5:4 B4:2 A4:4 G#4:2 B4:6 D#5:6',
      'E5:10 F#5:2 G#5:6 E5:6~',
      'E5:6 C#5:12 E5:6',
      'E5:6 B4:6 D#5:6 F#5:6',
      'E5:4 D#5:2 E5:18']
T3 = ['G#3:24', 'C#4:12 G#3:12', 'A3:12 F#3:12~', 'F#3:12 A3:12', 'G#3:12 E3:12', 'A3:12 C#4:12',
      'G#3:12 B3:12', 'G#3:12 E3:12']

# ------------------------------------------------------------------ cycle 4: da capo (the same notes as cycle 1), with a breath
# before the keyboard 'corrects' it
END4 = {'Soprano': 'G#5:4 F#5:2 E5:12 R:6', 'Alto': 'E4:12 G#4:6 R:6', 'Tenor': 'G#3:12 E3:6 R:6', 'Bass': 'E3:12 E2:6 R:6'}
# ------------------------------------------------------------------ coda (b33-36): the same loop on the well-tempered keyboard
CODA = {'Soprano': ['B4:4 C#5:2 B4:4 E5:2 G#5:6 E5:6', 'F#5:4 E5:2 A5:6 A5:4 G#5:2 F#5:6', 'G#5:4 F#5:2 E5:18~', 'E5:24'],
        'Alto': ['G#4:12 G#4:12', 'A4:12 A4:12', 'G#4:24~', 'G#4:24'],
        'Tenor': ['B3:12 C#4:12', 'A3:12 B3:6 D#4:6', 'E4:12 G#3:12~', 'G#3:24'],
        'Bass': ['E3:12 C#3:12', 'F#2:12 B2:12', 'E3:12 E2:12~', 'E2:24']}

# The harmony of one cycle, (bar, dotted-quarter beat, chord).  This chart IS the analysis the tuning script uses.
CYCLE_HARMONY = [(1, 1, 'E'), (2, 1, 'C#m'), (3, 1, 'F#m7'), (4, 1, 'B7'), (5, 1, 'E'), (6, 1, 'A'),
                 (7, 1, 'E'), (7, 3, 'B7'), (8, 1, 'E')]
CODA_HARMONY = [(33, 1, 'E'), (33, 3, 'C#m'), (34, 1, 'F#m7'), (34, 3, 'B7'), (35, 1, 'E')]

B = W.Bars(VOICES, METER)
for k in range(8):
    B.bar(f'{1 + k} cycle 1 (theme)', Soprano=TUNE[k], Alto=A1[k], Tenor=T1[k], Bass=BASS[k])
for k in range(8):
    B.bar(f'{9 + k} cycle 2 (pipes)', Soprano=TUNE[k], Alto=A2[k], Tenor=T2[k], Bass=BASS[k])
for k in range(8):
    B.bar(f'{17 + k} cycle 3 (tune in the alto)', Soprano=S3[k], Alto=TUNE_LOW[k], Tenor=T3[k], Bass=BASS[k])
for k in range(7):
    B.bar(f'{25 + k} cycle 4 (da capo)', Soprano=TUNE[k], Alto=A1[k], Tenor=T1[k], Bass=BASS[k])
B.bar('32 cycle 4 ends, a breath', **END4)
for k in range(4):
    B.bar(f'{33 + k} coda (well-tempered)', **{v: CODA[v][k] for v in VOICES})


def harmony_chart():
    out = []
    for c in range(4):
        out += [[(8 * c + b - 1) * 6 + (beat - 1) * 1.5, ch] for b, beat, ch in CYCLE_HARMONY]
    out += [[(b - 1) * 6 + (beat - 1) * 1.5, ch] for b, beat, ch in CODA_HARMONY]
    return out


def build():
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Prelude IX in E major: Pastorale in just intonation (the comma pump)',
            'composer': 'Claude / Sam', 'instrument': 'Keyboard (one player), adaptive just intonation',
            'key': 'E', 'mode': 'major', 'meter': list(METER), 'bpm': 84,
            'tempo_text': 'Pastorale, dotted quarter = 56',
            'movement_number': 9, 'piece_type': 'prelude', 'edition': 'third',
            # each cycle breathes at its cadence; cycle 4 slows into the breath; the coda a tempo, then broad
            'tempo_map': [[42, 84], [48, 76, 'ramp'], [48, 84], [90, 84], [96, 76, 'ramp'], [96, 84], [138, 84],
                          [144, 74, 'ramp'], [186, 74], [192, 58, 'ramp'], [192, 80], [204, 80], [216, 52, 'ramp']],
            'harmony': harmony_chart(), 'tuning': {'just_until_q': 192.0, 'then': 'bach-lehman'}}
    voices = [('Soprano', 'S', 'treble', 60), ('Alto', 'A', 'treble', 58), ('Tenor', 'T', 'bass', 54), ('Bass', 'B', 'bass', 58)]
    # the tune is brought out wherever it is (entry_boost): soprano in cycles 1, 2, 4 and the coda, alto in cycle 3
    tune = [('Soprano', 1, 0, 'tune (cycle 1)', 8), ('Soprano', 9, 0, 'tune (cycle 2)', 8),
            ('Alto', 17, 0, 'tune (cycle 3, alto)', 8), ('Soprano', 25, 0, 'tune (cycle 4, da capo)', 8),
            ('Soprano', 33, 0, 'tune head (coda, tempered)', 2)]
    dyn = {1: -4, 9: 0, 13: 2, 17: -6, 21: -4, 25: -2, 29: -6, 31: -10, 33: -2, 35: -6}

    def dynamics(b):
        v = 0
        for k in sorted(dyn):
            if b + 1 >= k:
                v = dyn[k]
        return v
    return W.build_score(HERE / 'prelude.json', meta, voices, B.bars, entries=tune, dynamics=dynamics, tags=B.tags,
                         entry_boost=8)


if __name__ == '__main__':
    build()
    print('bars', len(B))
    import tune_prelude
    tune_prelude.main()
