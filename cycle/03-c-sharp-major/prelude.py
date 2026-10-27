#!/usr/bin/env python3
"""Prelude III in C-sharp major, "Glass bells" -- literal source.

12/8, quarter = 96 (dotted quarter = 64), 24 bars, four layers.  Every bar is
one harmony struck as a cascade of bells: nine attacks in one fixed rhythm
(sixteenths 0 2 4 6 10 14 16 18 20 of 24), handed between four registers, with
the silences between attacks part of the phrase.  The bass is one deep bell per
bar.

This is the second complete draft's Prelude III (the version Sam likes),
re-expressed as literal bar strings, with the few corrections listed in
NOTES.md.  Corrected bars are marked `# FIX n` and the second-draft reading is
kept in SECOND_DRAFT so that every change can be audited (`--second-draft`
rebuilds the unaltered version for comparison).

Keyboard realisation: the bass is caught by the sostenuto (middle) pedal at
each downbeat (it is always struck together with the melody's first bell, and
the melody note is released before the next attack), so the deep bell rings
through the bar while the upper layers keep their silences dry.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from wtclib import build_score  # noqa: E402

HERE = Path(__file__).resolve().parent

# Rhythm of every bar (sixteenths):        M 0..3   U 2..6   L 4..9   M 6..8   U 10..13
#                                          M 14..18 L 16..21 U 18..21 M 20..23
MELODY = [
    "G#5:3 R:3 C#5:2 R:6 C#6:4 R:2 E#5:3 R:1",     # 1  I
    "G#5:3 R:3 C#5:2 R:6 C#6:4 R:2 E#5:3 R:1",     # 2  I6
    "E#5:3 R:3 A#4:2 R:6 A#5:4 R:2 C#5:3 R:1",     # 3  vi
    "G#5:3 R:3 B#4:2 R:6 B#4:4 R:2 E#4:3 R:1",     # 4  iii
    "C#5:3 R:3 F#4:2 R:6 F#5:4 R:2 A#4:3 R:1",     # 5  IV
    "G#5:3 R:3 C#5:2 R:6 C#6:4 R:2 E#5:3 R:1",     # 6  I6
    "D#6:3 R:3 F#5:2 R:6 F#6:4 R:2 A#5:3 R:1",     # 7  ii6
    "D#5:3 R:3 G#4:2 R:6 G#5:4 R:2 B#4:3 R:1",     # 8  V (half cadence)
    "E#5:3 R:3 G#4:2 R:6 G#5:4 R:2 B#4:3 R:1",     # 9  iii
    "E#5:3 R:3 G##4:2 R:6 G##5:4 R:2 B#4:3 R:1",   # 10 V/vi
    "A#5:3 R:3 C#5:2 R:6 C#6:4 R:2 E#5:3 R:1",     # 11 vi
    "F#5:3 R:3 F#4:2 R:6 F#5:4 R:2 A#4:3 R:1",     # 12 IV          FIX 1 (first bell C#5 -> F#5)
    "A#4:3 R:3 F#5:2 R:6 F#4:4 R:2 D#5:3 R:1",     # 13 ii6
    "A#4:3 R:3 F##5:2 R:6 F##4:4 R:2 D#5:3 R:1",   # 14 V/V
    "D#5:3 R:3 B#5:2 R:6 B#4:4 R:2 G#5:3 R:1",     # 15 V (of C#; I of G#)
    "G#4:3 R:3 D#5:2 R:6 D#5:4 R:2 B#5:3 R:1",     # 16 V
    "G#5:3 R:3 E#6:2 R:6 E#5:4 R:2 C#6:3 R:1",     # 17 I (return)
    "C#6:3 R:3 A#6:2 R:6 A#5:4 R:2 F#6:3 R:1",     # 18 IV
    "C#6:3 R:3 F#5:2 R:6 F#6:4 R:2 A5:3 R:1",      # 19 iv
    "E#6:3 R:3 G#5:2 R:6 G#5:4 R:2 C#5:3 R:1",     # 20 I6
    "A#5:3 R:3 D#5:2 R:6 D#6:4 R:2 A#5:3 R:1",     # 21 ii6         FIX 3 (last bell F#5 -> A#5)
    "G#5:3 R:3 C#5:2 R:6 C#6:4 R:2 E#5:3 R:1",     # 22 I6/4
    "D#5:3 R:3 G#4:2 R:6 G#5:4 R:2 B#4:3 R:1",     # 23 V7
    "C#5:24",                                      # 24 I
]

UPPER = [
    "R:2 E#4:4 R:4 G#4:3 R:5 C#4:3 R:3",     # 1
    "R:2 E#4:4 R:4 G#4:3 R:5 C#4:3 R:3",     # 2
    "R:2 C#4:4 R:4 E#4:3 R:5 A#3:3 R:3",     # 3
    "R:2 G#3:4 R:4 B#3:3 R:5 E#3:3 R:3",     # 4
    "R:2 A#3:4 R:4 C#4:3 R:5 F#4:3 R:3",     # 5   FIX 4 (F#3 -> F#4)
    "R:2 E#4:4 R:4 G#4:3 R:5 C#4:3 R:3",     # 6
    "R:2 F#4:4 R:4 A#4:3 R:5 D#4:3 R:3",     # 7
    "R:2 B#3:4 R:4 D#4:3 R:5 G#3:3 R:3",     # 8
    "R:2 G#3:4 R:4 B#3:3 R:5 E#3:3 R:3",     # 9
    "R:2 G##3:4 R:4 B#3:3 R:5 E#3:3 R:3",    # 10
    "R:2 C#4:4 R:4 E#4:3 R:5 A#3:3 R:3",     # 11
    "R:2 A#3:4 R:4 C#4:3 R:5 F#3:3 R:3",     # 12
    "R:2 F#4:4 R:4 A#4:3 R:5 D#4:3 R:3",     # 13
    "R:2 F##4:4 R:4 A#4:3 R:5 D#4:3 R:3",    # 14
    "R:2 B#3:4 R:4 D#4:3 R:5 G#3:3 R:3",     # 15
    "R:2 B#3:4 R:4 D#4:3 R:5 G#3:3 R:3",     # 16
    "R:2 E#4:4 R:4 G#4:3 R:5 C#4:3 R:3",     # 17
    "R:2 A#4:4 R:4 C#5:3 R:5 F#4:3 R:3",     # 18
    "R:2 A4:4 R:4 C#5:3 R:5 F#4:3 R:3",      # 19
    "R:2 E#4:4 R:4 G#4:3 R:5 C#4:3 R:3",     # 20  FIX 2 (down an octave)
    "R:2 F#4:4 R:4 A#4:3 R:5 D#4:3 R:3",     # 21
    "R:2 E#4:4 R:4 G#4:3 R:5 C#4:3 R:3",     # 22
    "R:2 B#3:4 R:4 D#4:3 R:5 G#3:3 R:3",     # 23
    "G#3:24",                                # 24
]

LOWER = [
    "R:4 G#3:5 R:7 E#3:5 R:3",     # 1
    "R:4 G#3:5 R:7 E#3:5 R:3",     # 2
    "R:4 E#3:5 R:7 C#3:5 R:3",     # 3
    "R:4 B#2:5 R:7 G#2:5 R:3",     # 4
    "R:4 A#2:5 R:7 C#3:5 R:3",     # 5
    "R:4 E#3:5 R:7 G#3:5 R:3",     # 6
    "R:4 A#3:5 R:7 F#3:5 R:3",     # 7
    "R:4 D#3:5 R:7 B#2:5 R:3",     # 8
    "R:4 B#2:5 R:7 G#2:5 R:3",     # 9
    "R:4 B#2:5 R:7 B#2:5 R:3",     # 10
    "R:4 E#3:5 R:7 C#3:5 R:3",     # 11
    "R:4 C#3:5 R:7 C#3:5 R:3",     # 12
    "R:4 F#3:5 R:7 F#3:5 R:3",     # 13
    "R:4 A#3:5 R:7 F##3:5 R:3",    # 14
    "R:4 D#3:5 R:7 D#3:5 R:3",     # 15
    "R:4 D#3:5 R:7 D#3:5 R:3",     # 16
    "R:4 E#3:5 R:7 G#3:5 R:3",     # 17
    "R:4 A#3:5 R:7 A#3:5 R:3",     # 18
    "R:4 C#4:5 R:7 C#4:5 R:3",     # 19
    "R:4 C#4:5 R:7 G#3:5 R:3",     # 20  FIX 2 (E#4 C#4 -> C#4 G#3)
    "R:4 A#3:5 R:7 F#3:5 R:3",     # 21
    "R:4 G#3:5 R:7 E#3:5 R:3",     # 22
    "R:4 D#3:5 R:7 F#3:5 R:3",     # 23
    "E#3:24",                      # 24
]

BASS = [
    "C#2:24", "E#2:24", "A#1:24", "E#1:24", "F#1:24", "E#1:24", "F#1:24", "G#1:24",   # 1-8
    "E#1:24", "E#1:24", "A#1:24", "F#1:24", "F#1:24", "D#1:24", "G#1:24", "G#1:24",   # 9-16
    "C#2:24", "F#1:24", "F#1:24", "E#1:24", "F#1:24", "G#1:24", "G#1:24", "C#2:24",   # 17-24
]

# Second-draft readings of every corrected bar: {(layer, bar): bar string}.
SECOND_DRAFT = {
    ('M', 12): "C#5:3 R:3 F#4:2 R:6 F#5:4 R:2 A#4:3 R:1",   # FIX 1
    ('U', 20): "R:2 E#5:4 R:4 G#5:3 R:5 C#5:3 R:3",         # FIX 2
    ('L', 20): "R:4 E#4:5 R:7 C#4:5 R:3",                   # FIX 2
    ('M', 21): "A#5:3 R:3 D#5:2 R:6 D#6:4 R:2 F#5:3 R:1",   # FIX 3
    ('U', 5): "R:2 A#3:4 R:4 C#4:3 R:5 F#3:3 R:3",          # FIX 4
}

# Phrase dynamics (velocity offset per bar), transcribed from the second
# draft's performance: growth to the low-register "contrasting span" (13-14),
# a second wave at 17-18, then the hush of the minor iv at bar 19 and a fade.
DYN = [0, 3, 5, 5, 5, 5, 9, 5, 6, 9, 11, 11, 18, 18, 16, 12, 13, 16, 2, 2, 2, 2, -3, -7]


def build(out=HERE / 'prelude.json', second_draft=False):
    layers = {'Melody': MELODY, 'Upper inner': UPPER, 'Lower inner': LOWER, 'Bass': BASS}
    if second_draft:
        keys = {'M': 'Melody', 'U': 'Upper inner', 'L': 'Lower inner', 'B': 'Bass'}
        layers = {k: list(v) for k, v in layers.items()}
        for (lay, bar), s in SECOND_DRAFT.items():
            layers[keys[lay]][bar - 1] = s
    meta = {
        'title': 'The Well-Tempered clAIvier', 'subtitle': 'III. Prelude in C-sharp major',
        'composer': 'Claude / composed for Sam', 'instrument': 'Piano (four layers; sostenuto pedal for the bass)',
        'key': 'C#', 'mode': 'major', 'meter': [12, 8], 'bpm': 96,
        'tempo_text': 'Moderato, luminoso', 'character': 'Glass bells',
        'tempo_map': [[132, 96], [144, 72, 'ramp']],          # breathe into the last chord
        'score_tagline': 'Third edition - second-draft Prelude III, corrected (see NOTES.md)',
        'markers': [{'t': 0.0, 'label': 'Bells'}, {'t': 48.0, 'label': 'Contrasting span'},
                    {'t': 96.0, 'label': 'Return'}, {'t': 120.0, 'label': 'Cadence'}],
    }
    voices = [('Melody', 'M.', 'treble', 55), ('Upper inner', 'U.', 'treble', 43),
              ('Lower inner', 'L.', 'bass', 42), ('Bass', 'B.', 'bass', 54)]
    data = build_score(out, meta, voices, layers, dynamics=lambda b: DYN[b])
    # Keep the second draft's ringing articulation and keyboard placement.
    pans = {'Melody': 71, 'Upper inner': 65, 'Lower inner': 61, 'Bass': 53}
    for v in data['voices']:
        v['piano_pan'] = pans[v['name']]
        for e in v['events']:
            e['gate'] = 0.985
    import json
    Path(out).write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    if '--second-draft' in sys.argv:
        build(HERE / 'prelude-second-draft.json', second_draft=True)
    else:
        build()
