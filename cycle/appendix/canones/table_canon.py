#!/usr/bin/env python3
"""Appendix canon I: Canon cancrizans per motum contrarium (a table canon).

One line is printed.  Player I (Dux) reads it from the near side of the table.
Player II (Comes) reads the same page from the far side: the page turned
through 180 degrees, i.e. the line backwards (cancrizans) and upside down
(per motum contrarium).  In pitch terms the comes is the retrograde of the dux
mirrored about D4, the one pitch that maps to itself; around D the C-major
collection maps onto itself (C<->E, F<->B, G<->A, D fixed), so the canon
begins in A minor and ends in C major.

The DUX below is the authored text, every note written literally.  The COMES
is produced by two explicit, named operations from tools/wtclib.py
(invert_diatonic about D4, then retrograde); its bars are written into the
JSON.  The build refuses to write a score unless the whole two-voice score is
note-for-note identical to itself rotated through 180 degrees.

Sarabande, 3/4.  Plan (mirror pairs: bar k <-> bar 33-k):
  1-8    Thema, A minor.  The beat-2 notes of bars 1-8 (E A B C A G F E) are
         the retrograde inversion of the Goldberg ground in C, which the
         comes therefore plays, rectus, in bars 25-32.
  9-15   Double: sixteenths over the sarabande bass, A minor -> D minor.
  16-17  Cardo (hinge): E4/C#4 -> unison D4, the mirror axis -> Eb4/C4.
  18-24  The double rotated: running bass under the sarabande tune, G -> C.
  25-32  Fundamentum: BWV 988's ground (C B A G E F G C) in the comes.
"""
import sys

from canon_tools import W, C_MAJOR, flatten, rinv, check_rotation, HERE

METER = (3, 4)
AXIS = 'D4'

DUX = [
    # Thema (A minor).  Beat-2 skeleton = RI of the Goldberg ground.
    'E5:12', 'A4:12', 'D5:4 B4:8', 'C5:12',                            # 1-4
    'B4:4 A4:8', 'B4:4 G4:8', 'A4:4 F4:8', 'E4:12',                    # 5-8
    # Double.  Sixteenth positions 1-2 of a beat carry the passing notes;
    # positions 0 and 3 are consonant, because rotation swaps 0<->3, 1<->2.
    'F4:1 G4:1 A4:1 B4:1 D5:1 C5:1 B4:1 A4:1 G#4:1 A4:1 B4:1 D5:1',    # 9
    'E5:1 D5:1 C5:1 B4:1 G#4:1 B4:1 D5:1 E5:1 F5:1 E5:1 D5:1 B4:1',    # 10
    'C5:1 D5:1 E5:1 F5:1 E5:1 F5:1 G5:1 F5:1 E5:1 F5:1 G5:1 A5:1',     # 11
    'B5:1 C6:1 B5:1 G5:1 C6:1 B5:1 A5:1 G5:1 A5:1 G5:1 F5:1 E5:1',     # 12
    'F5:1 E5:1 D5:1 C5:1 D5:1 C5:1 Bb4:1 A4:1 Bb4:1 A4:1 G4:1 A4:1',   # 13
    'Bb4:1 A4:1 Bb4:1 D5:1 F5:1 E5:1 F5:1 D5:1 E5:1 D5:1 C#5:1 D5:1',  # 14
    'F5:1 E5:1 D5:1 C#5:1 A4:1 G4:1 F4:1 E4:1 F4:2 G4:1 F4:1',         # 15
    # Cardo: the dux falls E4 -> D4 while the comes rises C#4 -> D4.
    'E4:4 D4:8~', 'D4:8 Eb4:4',                                        # 16-17
    # The sarabande tune over the rotated double (G major -> C major).
    'G4:4 G5:8', 'A5:4 F#5:8', 'D5:4 B4:8',                            # 18-20
    'E5:4 C5:8', 'E5:4 G5:8', 'Ab5:4 C5:8', 'F5:4 D5:8',               # 21-24
    # Fundamentum: the comes has the ground; the dux sings over it.
    'E5:4 G5:8', 'Ab5:8 B4:4', 'C5:4 E5:4 A4:4', 'D5:4 B4:4 D5:4',     # 25-28
    'C5:4 E5:4 G5:4', 'C6:4 Ab5:4 F5:4', 'D5:4 C5:4 B4:4', 'C5:12',     # 29-32
]


def derive():
    dux_stream = flatten(DUX)
    # The two canonic operations, applied explicitly and in this order.
    inverted = W.invert_diatonic(dux_stream, AXIS, C_MAJOR)
    comes_stream = W.retrograde(inverted)
    assert comes_stream == rinv(dux_stream)
    return dux_stream, comes_stream, W.concat_bars(comes_stream, METER)


def dynamics(b):
    """Phrase shaping by bar index (0-based); not part of the canon."""
    arc = [-8, -6, -5, -6, -5, -4, -3, -6,           # 1-8 thema
           -4, -2, 0, 3, 1, -1, -3, -6,             # 9-16 double, to the cardo
           -6, -3, -1, 0, 1, 3, 2, 0,               # 17-24
           -2, -1, 0, 1, 2, 4, 1, -2]               # 25-32 fundamentum
    return arc[b]


def build(out=HERE / 'table-canon.json'):
    dux_stream, comes_stream, COMES = derive()
    bad = check_rotation(dux_stream, comes_stream, axis_midi=62)
    if bad:
        raise SystemExit('rotation symmetry broken: ' + '; '.join(bad[:6]))
    bq = 3  # quarters per bar
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Appendix: Canones. I. Canon cancrizans per motum contrarium (Tafelkanon)',
        'composer': 'Claude / Sam',
        'instrument': 'Two keyboards facing each other (or one piano, four hands)',
        'score_tagline': 'One line, two readers: the comes is the dux turned through 180 degrees',
        'key': 'A', 'mode': 'minor', 'meter': list(METER), 'bpm': 60,
        'tempo_text': 'Sarabande. Grave, ma con moto',
        'markers': [{'t': 0, 'label': 'Thema'}, {'t': 8 * bq, 'label': 'Double'},
                    {'t': 15 * bq, 'label': 'Cardo'}, {'t': 17 * bq, 'label': 'Double rovescio'},
                    {'t': 24 * bq, 'label': 'Fundamentum'}],
    }
    voices = [('Dux', 'Dux', 'treble', 72),
              ('Comes (rotated)', 'Com', 'bass', 70)]
    entries = [(voices[1][0], 25, 0, 'Goldberg ground, BWV 988 (in C)', 8)]
    W.build_score(out, meta, voices,
                  {voices[0][0]: DUX, voices[1][0]: COMES},
                  entries=entries, dynamics=dynamics,
                  tags=['thema'] * 8 + ['double'] * 7 + ['cardo'] * 2 + ['double rovescio'] * 7
                  + ['fundamentum'] * 8,
                  extra={'canon': {'kind': 'retrograde inversion (table canon)', 'axis': AXIS,
                                   'axis_midi': 62, 'rule': 'comes(t) = 124 - dux(T - t)',
                                   'rotation_check': 'passed', 'dux_bars': DUX}})
    return COMES


if __name__ == '__main__' and '--no-write' not in sys.argv:
    comes = build()
    print('wrote', HERE / 'table-canon.json')
    for i, b in enumerate(comes, 1):
        print(f'  comes {i:>2}: {b}')
