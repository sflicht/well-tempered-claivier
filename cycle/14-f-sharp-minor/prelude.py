#!/usr/bin/env python3
"""Prelude XIV in F-sharp minor: Canon cancrizans a 3 sopra il Thema Regio ("Quaerendo invenietis").

A riddle canon after the "Canon 1 a 2 cancrizans" of the Musical Offering (BWV 1079), where one voice plays the
King's theme forwards while the other plays the same line backwards.  Here, for one pianist, in three voices and
17 bars of common time:

  Cantus  = the theme (b1-9) and then a counter-line (b9-17)
  Altus   = that counter-line backwards an octave lower (b1-9), then the theme backwards an octave lower (b9-17)
  Bassus  = a bass line that is its own retrograde (a palindrome)

so the whole piece read from the last note to the first is the same piece with the two upper voices exchanged
(and moved by an octave).  The turning point is the middle of bar 9.  Every sonority of the second half is a
sonority of the first half (same bass, same pitch classes), met in reverse order.

Written by hand: the theme (Frederick's), the first-half counter-line LINE and the first-half bass BASS1.  The
second half is produced by the named transform wtclib.retrograde (and an octave transposition): that is the canon.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
NB = 17

# Thema Regium in F-sharp minor (as in the fugue), an octave up
THEME = ("F#5:8 A5:8 C#6:8 D6:8 E#5:8 R:4 C#6:4 B#5:8 B5:8 A#5:8 A5:12 G#5:4 G5:4 F#5:4 E#5:4 C#5:4 F#5:4 "
         "B5:4 A5:8 G#5:8 F#5:8")
# the counter-line under the theme (b1-9.2), written to sound from a sixth to a tenth below it on the beats, so
# that its retrograde an octave higher sits a sixth to a tenth above the retrograde theme
LINE = ("A4:2 G#4:2 F#4:2 A4:2 C#5:4 B4:4 "      # b1   i
        "A4:4 C#5:4 B4:8 "                              # b2   i6 - iv
        "G#4:8 C#5:4 E#5:4 "                            # b3   V
        "D#5:8 G#4:8 "                                  # b4   vii7/V - V6/5
        "F#4:4 G#4:4 F#4:8 "                            # b5   V/iv - iv6/5
        "E#4:4 G#4:4 B4:4 A4:4 "                        # b6   V - N6
        "G#4:4 E#4:4 F#4:4 D5:4 "                       # b7   V - iv
        "C#5:8 B4:8 "                                   # b8   i6/4 - V7
        "A4:8")                                         # b9.1 i  (the turning point is b9.3)
# the bass of the first half; the second half is its retrograde
BASS1 = "F#2:16 A2:8 B2:8 C#3:16 D#3:8 E#3:8 F#3:8 D3:8 C#3:8 B2:8 C#3:8 B2:8 C#3:16 F#2:8"


def build(path=None):
    top = THEME + ' ' + W.transpose(W.retrograde(LINE), 12, 7)
    mid = LINE + ' ' + W.transpose(W.retrograde(THEME), -12, -7)
    bass = BASS1 + ' ' + W.retrograde(BASS1)
    bars = {name: W.concat_bars(s, METER) for name, s in (('Cantus', top), ('Altus', mid), ('Bassus', bass))}
    for k, v in bars.items():
        assert len(v) == NB, (k, len(v))
    # the bass's two middle halves (F#2, b9) are one note: tie them
    bars['Bassus'][8] = 'F#2:8~ F#2:8'
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Prelude XIV in F-sharp minor: Canon cancrizans a 3 sopra il Thema Regio',
            'composer': "Claude / Sam (on Frederick the Great's Royal Theme, after J. S. Bach's Musical Offering, BWV 1079)",
            'instrument': 'Piano (three voices)', 'key': 'F#', 'mode': 'minor', 'meter': list(METER), 'bpm': 69,
            'tempo_text': 'Andante, quaerendo invenietis', 'movement_number': 14, 'piece_type': 'prelude',
            'edition': 'third', 'motto': 'Quaerendo invenietis',
            'tempo_map': [[0, 69], [60, 69], [68, 50, 'ramp']],
            'markers': [{'t': 0, 'label': 'Thema Regium (and, below, the line that will return backwards)'},
                        {'t': 34, 'label': 'Turning point: everything now runs backwards'}]}
    voices = [('Cantus', 'C', 'treble', 66), ('Altus', 'A', 'treble', 60), ('Bassus', 'B', 'bass', 62)]
    entries = [('Cantus', 1, 0, 'Thema Regium', 9),
               ('Altus', 9, 2, 'Thema Regium cancrizans (backwards, an octave lower)', 9, 'retrograde')]
    dyn = [-4, -3, -2, -1, 0, 1, 2, 1, 0, 0, 1, 2, 1, 0, -1, -2, -3]
    data = W.build_score(path or HERE / 'prelude.json', meta, voices, bars, entries=entries, subject=THEME,
                         dynamics=lambda b: dyn[b])
    return data


if __name__ == '__main__':
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
    print('bars', NB)
