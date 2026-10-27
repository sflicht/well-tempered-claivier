#!/usr/bin/env python3
"""Prelude XX in A minor: Preludio per violino solo.  Third edition, Pair XX.

One line only: a perpetual-motion preludio for one violin (in the manner of the Preludio of
BWV 1006 and the solo-violin writing of BWV 1003), playable by one pianist with one hand.
It foreshadows the fugue in three ways:
  * its single line is compound: every bar is two or three strands sounded one sixteenth at a
    time (bass, middle, top), the polyphony the fugue will make real;
  * bar 1 interleaves Bach's subject head (BWV 1003: E D# E E A C B D) with a pedal on the
    open A string, so the fugue's subject is heard first as a strand inside a figuration;
  * the harmony is the fugue's summit ground, the lament A G# G F# F E (bars 5-7, 26-28),
    and bar 29 is the fugue's own tail, whose lower strand is that lament in one bar.

Plan (2 chords a bar):
  1-4    Am, tonic pedal on the open A (subject head inside the bariolage); F | E
  5-8    the lament ground in the lowest strand: Am E/G# | C/G D/F# | Dm/F E | Am A7
  9-12   circle of fifths: Dm G7 | C F | B-half-dim E7 | Am G7
  13-18  C major, then E minor: C C/E | F G7 | C B7 | Em B7 | Em Am/C | B7 Em
  19-22  back to A minor: E7 Am | Dm E7 | Am F | Dm/F E
  23-25  dominant pedal on the open E string (bariolage), the harmony moving above it
  26-28  the lament ground again, swept across all four strings
  29-30  the fugue's tail; A.
Every note is written literally below, one call per bar.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import Bars, build_score  # noqa: E402

METER = (4, 4)
B = Bars(['violin'], METER)


def s16(text):
    """Sixteenths: 'E5 A4 D#5' -> 'E5:1 A4:1 D#5:1' (a notation shorthand; every pitch is written)."""
    out = []
    for t in text.replace('|', ' ').split():
        out.append(t if ':' in t else f'{t}:1')
    return ' '.join(out)


def bar(text, tag=''):
    B.bar(tag, violin=s16(text))


# 1-4: tonic pedal on the open A string; the subject head on the odd sixteenths of bar 1
bar('E5 A4 D#5 A4 E5 A4 E4 A4 | A4 E4 C5 E4 B4 E4 D5 E4', 'subject head inside the bariolage')
bar('C5 E4 A4 E4 C5 E4 E5 E4 | D5 A4 F5 A4 D5 A4 F4 A4')
bar('B4 G#4 D5 G#4 B4 G#4 E5 G#4 | C5 A4 E5 A4 C5 A4 A5 A4')
bar('A5 F5 C5 F5 A5 F5 C5 A4 | G#4 B4 E5 B4 G#4 B4 D5 B4')
# 5-8: the lament ground in the lowest strand (A G# G F# F E)
bar('A3 E4 C5 E4 A4 E4 C5 E4 | G#3 E4 B4 E4 G#4 E4 B4 E4', 'the lament ground')
bar('G3 E4 C5 E4 G4 E4 C5 E4 | F#4 A4 D5 A4 F#4 A4 C5 A4')
bar('F4 A4 D5 A4 F4 A4 D5 A4 | E4 G#4 B4 G#4 E4 G#4 D5 G#4')
bar('A4 C5 E5 C5 A4 C5 E5 A5 | G5 E5 C#5 E5 A4 C#5 E5 G5')
# 9-12: circle of fifths
bar('F5 D5 A4 D5 F5 D5 A5 F5 | F5 D5 B4 D5 G4 B4 D5 F5', 'circle of fifths')
bar('E5 C5 G4 C5 E5 C5 G5 E5 | C5 A4 F4 A4 C5 A4 F5 C5')
bar('B4 D5 F5 D5 A5 F5 D5 B4 | G#4 B4 D5 B4 E5 D5 B4 G#4')
bar('A4 C5 E5 C5 A5 E5 C5 A4 | B4 D5 G5 D5 F5 D5 B4 G4')
# 13-18: C major, then E minor
bar('C5 E5 G5 E5 C6 G5 E5 C5 | E5 G5 C6 G5 E5 C5 G4 C5', 'C major')
bar('A4 C5 F5 C5 A5 F5 C5 A4 | B4 D5 G5 D5 F5 D5 B4 G4')
bar('C5 E5 G5 E5 C5 G4 E4 G4 | D#4 F#4 B4 F#4 A4 F#4 B4 D#5')
bar('E5 B4 G4 B4 E5 G5 B5 G5 | F#5 D#5 A4 D#5 B4 D#5 F#5 A5', 'E minor')
bar('G5 E5 B4 E5 G5 E5 B4 G4 | A4 C5 E5 C5 A4 E4 C4 E4')
bar('D#4 F#4 A4 B4 C5 B4 A4 F#4 | G4 E4 B4 E4 G4 B4 E5 G4')
# 19-22: back to A minor
bar('G#4 B4 D5 E5 D5 B4 G#4 E4 | A4 C5 E5 A5 E5 C5 A4 E4', 'A minor')
bar('F4 A4 D5 F5 D5 A4 F4 D4 | E4 G#4 B4 D5 B4 G#4 E4 D4')
bar('C4 E4 A4 C5 A4 E4 C4 E4 | C4 F4 A4 C5 A4 F4 C4 F4')
bar('F4 A4 D5 F5 D5 A4 F4 A4 | E4 G#4 B4 E5 B4 G#4 E4 G#4')
# 23-25: dominant pedal on the open E string
bar('C5 E5 A4 E5 C5 E5 A4 E5 | B4 E5 G#4 E5 D5 E5 B4 E5', 'dominant pedal (open E)')
bar('D5 E5 F4 E5 D5 E5 A4 E5 | B4 E5 G#4 E5 B4 E5 D5 E5')
bar('C5 E5 A4 E5 F5 E5 C5 E5 | G#4 E5 B4 E5 D5 E5 B4 E5')
# 26-28: the lament ground swept across the four strings
bar('A3 E4 C5 A5 C5 E4 A3 E4 | G#3 E4 B4 G#5 B4 E4 G#3 E4', 'the lament ground, four strings')
bar('G3 E4 C5 G5 C5 E4 G3 E4 | F#4 A4 D5 A5 D5 A4 F#4 A4')
bar('F4 A4 D5 F5 D5 A4 F4 A4 | E4 G#4 B4 E5 D5 B4 G#4 B4')
# 29: the fugue's tail (upper strand C E D C B A G#, lower strand A G# G F# F E)
bar('C5 A4 E5 G#4 D5 G4 C5 F#4 B4 F4 A4 E4 G#4:4', "the fugue's tail")
bar('A3 E4 C5 E5 A4:12')


def main():
    assert len(B) == 30, len(B)
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'XX. Prelude in A minor - Preludio per violino solo',
        'number': 20, 'movement_number': 20, 'piece_type': 'prelude',
        'key': 'A', 'mode': 'minor', 'meter': list(METER), 'bpm': 72,
        'tempo_map': [[0, 72], [112, 72], [120, 52, 'ramp']],
        'tempo_text': 'Allegro moderato (one line: violin, or one hand)',
        'composer': 'Original composition (Claude) for Sam; bar 1 carries the head of J. S. Bach\'s '
                    'subject from BWV 1003',
        'instrument': 'Solo violin (or one hand at the keyboard)',
        'score_tagline': 'The Well-Tempered clAIvier - third edition',
        'markers': [{'t': float((b - 1) * 4), 'label': t} for b, t in enumerate(B.tags, 1) if t],
    }
    out = HERE / 'prelude.json'
    build_score(out, meta, [('violin', 'Vl', 'treble', 70)], B.bars, accents=True, tags=B.tags)
    data = json.loads(out.read_text())
    for v in data['voices']:
        v['gm_program'] = 40
        v['pan'] = 64
    out.write_text(json.dumps(data, indent=1))
    print('bars', len(B), 'events', sum(len(v['events']) for v in data['voices']))


if __name__ == '__main__':
    main()
