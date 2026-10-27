#!/usr/bin/env python3
"""Prelude V in D major, third edition (two hands, one player).

Right hand: continuous sixteenths that carry a written top line (stepwise
turns around the melody notes, after the figure of BWV 850's prelude), mostly
between A4 and D6. Left hand: a walking bass in eighths (bass note + upper
note), except in the climb (bb. 21-32), where it doubles its speed.

Form (41 bars): A 1-6 (D) | B 7-14 (B minor region) | C 15-20 (development:
the fugue's tattoo, passed between the hands, over the fugue's Episode-1
progression) | D 21-32 (7th chain, dominant climb, deceptive cadence,
G#o7, arrival - the v1 climax arc, re-registered) | E 33-38 (return over the
fugue subject's head in the bass, C natural and B flat colours) | F 39-41
(improvisatory flourish; the fugue subject in diminution; attacca).

Run:  python3 cycle/05-d-major/prelude.py  -> cycle/05-d-major/prelude.json
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import build_score, scale_rhythm  # noqa: E402

U, L, TAGS = [], [], []


def S(s):
    """'A5 B5 ...' -> sixteenth tokens; tokens with ':' are kept as written."""
    return ' '.join(t if ':' in t else t + ':1' for t in s.split())


def E(s):
    """eighth-note shorthand for the left hand."""
    return ' '.join(t if ':' in t else t + ':2' for t in s.split())


def bar(u, l, tag=''):
    U.append(S(u))
    L.append(E(l))
    TAGS.append(tag)


# ---- A (1-6) D major. Top line: F#5 F#5 E5 A5 | B5 B5 A5 A5 | ...
bar('F#5 E5 D5 E5  F#5 A5 G5 F#5  E5 D5 C#5 D5  A4 D5 F#5 A5', 'D3 A3 F#3 D4 D3 A3 A2 A3', 'A: D')
bar('B5 A5 G5 A5  B5 D6 C#6 B5  A5 G5 F#5 G5  A5 F#5 E5 D5', 'G2 D3 B2 G3 F#2 D3 D3 A3', 'IV - I6')
bar('E5 F#5 G5 B5  D6 C#6 B5 G5  C#6 B5 A5 G5  E5 C#5 A4 C#5', 'E2 B2 G2 E3 A2 E3 C#3 G3', 'ii7 - V7')
bar('D5 F#5 A5 F#5  D6 C#6 B5 A5  B5 A5 G5 F#5  F#5 E5 D5 B4', 'D3 A3 F#3 A3 B2 F#3 D3 B3', 'I - vi')
bar('G4 B4 D5 G5  B5 A5 G5 F#5  E5 G5 C#6 E6  D6 C#6 B5 A5', 'G2 D3 B2 G3 A2 E3 A2 G3', 'IV - V7')
bar('F#5 A5 D6 A5  F#5 D5 A4 D5  F#5 E5 D5 C#5  A#4 C#5 E5 F#5', 'D3 A3 F#3 A3 F#2 C#3 A#2 E3', 'I - V7/vi')
# ---- B (7-14) B minor region
bar('D5 C#5 B4 C#5  D5 F#5 E5 D5  C#5 B4 A#4 B4  C#5 E5 D5 C#5', 'B2 F#3 D3 B3 C#3 F#3 A#2 F#3', 'B: B minor')
bar('B4 D5 F#5 D5  B5 A5 G5 F#5  G#5 F#5 E5 D5  D5 B4 G#4 B4', 'D3 B3 F#3 B3 E3 B3 G#2 E3', 'i - V7/iv')
bar('C#5 E5 A5 E5  C#6 B5 A5 G5  F#5 E5 D5 C#5  D5 F#5 A5 D6', 'A2 E3 C#3 A3 D3 A3 F#3 A3', 'VII - III (A - D)')
bar('B5 A5 G5 F#5  G5 B5 D6 B5  G5 E5 C#5 E5  G5 E5 C#5 B4', 'G2 D3 B2 G3 C#3 G3 E3 A#3', 'VI - ii-ish (C#o7)')
bar('A#4 C#5 E5 C#5  F#5 E5 D5 C#5  A#4 C#5 E5 G5  F#5 E5 D5 C#5', 'F#2 C#3 A#2 C#3 F#2 E3 A#2 E3', 'V7 of B minor')
bar('D5 C#5 B4 C#5  D5 F#5 B5 F#5  D5 B4 A4 G4  F#4 A4 D5 F#5', 'B2 F#3 D3 B3 A2 F#3 D3 A3', 'i - (to D)')
bar('G5 F#5 E5 F#5  G5 B5 E6 B5  G5 F#5 E5 D5  C#5 E5 A5 G5', 'E3 B3 G3 B3 A2 E3 C#3 G3', 'ii - V7')
bar('F#5 E5 D5 E5  F#5 A5 D6 C#6  B5 A5 G5 F#5  E5 G5 B5 D6', 'D3 A3 F#3 A3 G2 D3 B2 G3', 'I - IV')
# ---- C (15-20) development: the fugue's head cell + tattoo, passed between the
#      hands, over the fugue's Episode-1 progression (D-Bm | G-Em | A-F#m | ...)
bar('A5:4 D6:2 D6:1 D6:1  F#5:4 B5:2 B5:1 B5:1',
    'D3:1 F#3:1 A3:1 F#3:1 D3:1 A3:1 F#3:1 D3:1 B2:1 D3:1 F#3:1 D3:1 B2:1 F#3:1 D3:1 B2:1', 'C: tattoo in the right hand')
bar('D5:4 G5:2 G5:1 G5:1  B4:4 E5:2 E5:1 E5:1',
    'G2:1 B2:1 D3:1 B2:1 G2:1 D3:1 B2:1 G2:1 E2:1 G2:1 B2:1 G2:1 E2:1 B2:1 G2:1 E2:1', 'G - Em')
bar('A4 C#5 E5 A5  C#6 B5 A5 G#5  F#5 A5 C#6 A5  F#5 E5 D5 C#5', 'E2:4 A2:2 A2:1 A2:1 C#3:4 F#2:2 F#2:1 F#2:1', 'tattoo in the left hand: A - F#m')
bar('D5 F#5 A5 F#5  D6 C#6 B5 A5  B5 A5 G5 F#5  D#5 F#5 A5 B5', 'A2:4 D3:2 D3:1 D3:1 F#2:4 B2:2 B2:1 B2:1', 'D - B7')
bar('G5:4 B5:2 B5:1 B5:1  G5:4 E5:2 E5:1 E5:1', 'E2:1 G2:1 B2:1 E3:1 G3:1 E3:1 B2:1 G2:1 C#3:1 E3:1 G3:1 E3:1 C#3:1 G3:1 E3:1 C#3:1',
    'Em - C#o7 (tattoo back in the right hand)')
bar('A5 G#5 F#5 G#5  A5 C#6 B5 A5  G#5 F#5 E#5 F#5  G#5 B5 A5 G#5', 'F#2:4 A2:2 A2:1 A2:1 C#3:4 C#2:2 C#2:1 C#2:1', 'F#m - C#7')
# ---- D (21-32) the climb: v1's arc (7th chain, A pedal, deceptive Bm, G#o7,
#      A7 falling, arrival on D), right hand an octave lower than v1.
bar('F#5 A5 C#6 E6  E6 C#6 A5 F#5  A5 C#6 E6 C#6  A5 E5 C#5 A4',
    'F#2:1 C#3:1 E3:1 A3:1 C#3:1 A2:1 C#3:1 E3:1 F#2:1 C#3:1 A3:1 C#3:1 F#2:1 E3:1 A3:1 C#3:1', 'D: 7th chain F#m7')
bar('B4 D5 F#5 A5  A5 F#5 D5 B4  D5 F#5 A5 D6  D6 A5 F#5 D5',
    'B2:1 F#3:1 A3:1 D3:1 D3:1 F#3:1 B2:1 F#2:1 B2:1 F#3:1 D3:1 F#3:1 B2:1 A2:1 D3:1 F#3:1', 'Bm7')
bar('G5 E5 B4 G4  B4 G4 E4 G4  D5 B4 G4 B4  G5 B4 D5 B4',
    'E2:1 B2:1 D3:1 G2:1 E2:1 B2:1 E3:1 B2:1 G2:1 D3:1 B2:1 D3:1 E2:1 G2:1 B2:1 D3:1', 'Em7')
bar('E5 C#5 A4 G4  C#5 A4 G4 E4  A4 G4 E4 C#5  G5 E5 C#5 A4',
    'A1:1 E2:1 G2:1 C#3:1 A1:1 E2:1 A2:1 E2:1 A1:1 C#2:1 E2:1 G2:1 E2:1 G2:1 C#3:1 E2:1', 'A7')
bar('F#4 A4 D5 A4  F#4 A4 D5 F#5  C#5 A4 E5 C#5  A4 C#5 G5 E5',
    'A2:1 D3:1 F#3:1 D3:1 A2:1 D3:1 F#3:1 A2:1 A2:1 E3:1 G3:1 E3:1 A2:1 E3:1 C#3:1 G2:1', 'A pedal: D/A - A7')
bar('E4 G4 C#5 E5  C#5 G5 E5 C#5  A4 E5 C#5 G5  E5 C#5 A4 C#5',
    'A2:1 E3:1 A3:1 E3:1 A2:1 E3:1 A3:1 E3:1 A2:1 C#3:1 E3:1 A3:1 A2:1 E3:1 C#3:1 E3:1', 'A7')
bar('A4 D5 F#5 A5  F#5 D5 A4 F#4  A4 D5 F#5 A5  F#5 A5 D6 A5',
    'A2:1 F#3:1 A3:1 D3:1 A2:1 D3:1 F#3:1 A3:1 A2:1 F#3:1 D3:1 F#3:1 A2:1 D3:1 F#3:1 A3:1', 'D/A, climbing')
bar('E5 G5 C#6 G5  E5 G5 B5 G5  E5 G5 C#6 E6  C#6 G5 E5 C#5',
    'A2:1 E3:1 G3:1 E3:1 A2:1 C#3:1 G3:1 C#3:1 A2:1 E3:1 G3:1 A3:1 A2:1 E3:1 G3:1 E3:1', 'A7 at the top')
bar('D5 F#5 B5 F#5  D5 F#5 B5 D6  B5 F#5 D5 B4  F#5 D5 B4 F#4',
    'B2:1 F#3:1 D3:1 F#3:1 B2:1 D3:1 F#3:1 B2:1 B2:1 D3:1 F#3:1 D3:1 D3:1 B2:1 F#2:1 B2:1', 'deceptive: Bm')
bar('G#4 B4 D5 F5  B4 D5 F5 G#5  D5 F5 G#5 B5  F5 G#5 B5 D6',
    'G#2:1 D3:1 F3:1 B2:1 G#2:1 D3:1 B2:1 D3:1 G#2:1 F3:1 D3:1 F3:1 G#2:1 B2:1 F3:1 D3:1', 'G#o7 climbing')
bar('E6 C#6 A5 G5  E5 C#5 A4 G4  C#5 A4 E4 G4  C#5 E5 A5 C#6',
    'A2:1 E3:1 A3:1 C#3:1 A2:1 E3:1 G3:1 C#3:1 A2:1 C#3:1 G3:1 E3:1 A2:1 E3:1 G3:1 A3:1', 'apex E6, falling A7')
bar('D6 A5 F#5 A5  D6 F#6 D6 A5  F#5 D5 A4 D5  F#5 A5 D6 C6',
    'D2:2 D3:2 A2:2 D3:2 F#2:2 D3:2 A2:2 D3:2', 'ARRIVAL on D')
# ---- E (33-38) return: the fugue subject's head in the bass (augmented), C natural and B flat
bar('B5 A5 G5 A5  B5 G5 D5 G5  A5 G5 F#5 G5  A5 F#5 D5 F#5', 'G2:4 B2:2 B2:1 B2:1 D3:2 D3:1 D3:1 F#2:4', 'E: IV over the head (G - D/F#)')
bar('E5 F#5 G5 B5  E6 D6 C#6 B5  A5 G5 F#5 E5  C#5 E5 A5 G5', 'E2:4 G2:2 G2:1 G2:1 A2:4 C#3:4', 'ii - V7')
bar('F#5 E5 D5 E5  F#5 A5 D6 A5  C6 B5 A5 G5  F#5 A5 C6 A5', 'D3:4 A2:2 A2:1 A2:1 F#2:4 D2:2 D2:1 D2:1', 'I - I7 (C natural)')
bar('B5 A5 G5 A5  B5 D6 B5 G5  Bb5 A5 G5 A5  Bb5 D6 Bb5 G5', 'G2 D3 B2 D3 G2 D3 Bb2 D3', 'IV - iv (B flat)')
bar('A5 G5 F#5 G5  A5 F#5 D5 F#5  E5 F#5 G5 E5  C#5 E5 G5 Bb5?'.replace('Bb5?', 'A5'), 'A2 D3 F#3 D3 A2 E3 G3 E3', 'I6/4 - V7')
bar('F#5 E5 D5 C#5  D5 A4 F#4 A4  D5 E5 F#5 G5  A5 B5 C#6 D6', 'D3 A3 F#3 A3 D3 A3 D2 A2', 'I (rising toward the flourish)')
# ---- F (39-41) improvisatory flourish (rit.), then the fugue subject in diminution: attacca
bar('E6:0.5 D6:0.5 C#6:0.5 B5:0.5 A5:0.5 G5:0.5 F#5:0.5 E5:0.5  D5:0.5 C#5:0.5 B4:0.5 A4:0.5 G4:0.5 A4:0.5 B4:0.5 C#5:0.5 '
    'D5:0.5 E5:0.5 F#5:0.5 G5:0.5 A5:0.5 B5:0.5 C#6:0.5 D6:0.5  E6:2 C#6:1 A5:1',
    'A2:8 A2:8', 'F: flourish over the dominant')
bar(scale_rhythm('A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2', '1/2'),
    'D3:4 A2:4 A2:4 D2:4', 'the fugue subject in diminution')
bar('D5:16', 'D2:16', 'attacca')

BPM = 104
NB = len(U)


def DYN(b):
    bar_ = b + 1
    for lo, hi, v in [(1, 6, 0), (7, 12, -3), (13, 14, -1), (15, 20, 1), (21, 24, 3), (25, 28, 5),
                      (29, 31, 9), (32, 32, 10), (33, 38, 0), (39, 40, 2), (41, 41, -2)]:
        if lo <= bar_ <= hi:
            return v
    return 0


if __name__ == '__main__':
    end = NB * 4
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Prelude V in D major',
            'composer': 'Recomposed by Claudia / Sam', 'instrument': 'Piano', 'key': 'D', 'mode': 'major',
            'meter': [4, 4], 'bpm': BPM, 'tempo_text': 'Allegro; bright', 'movement_number': 5,
            'piece_type': 'prelude', 'edition': 'third',
            # the flourish (b39) broadens, the diminished subject is played a tempo-ish, the end breathes
            'tempo_map': [[(39 - 1) * 4, BPM], [(40 - 1) * 4, 76, 'ramp'], [(40 - 1) * 4 + 0.01, 92],
                          [end - 6, 92], [end, 70, 'ramp']],
            'markers': [{'t': (i) * 4, 'label': t} for i, t in enumerate(TAGS) if t.split(':')[0] in 'ABCDEF' and ':' in t]}
    voices = [('Right hand', 'R.H.', 'treble', 76), ('Left hand', 'L.H.', 'bass', 70)]
    build_score(HERE / 'prelude.json', meta, voices, {'Right hand': U, 'Left hand': L},
                dynamics=DYN, tags=TAGS)
    print('bars', NB)
