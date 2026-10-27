#!/usr/bin/env python3
"""Prelude XIX in A major: "Le Maitre a danser" (the dancing-master's prelude).

One pianist.  Before the ball, the dancing master (Pierre Rameau's book of 1725 has this title)
shows the four dances one after the other, each for twelve quarter-beats, in its own metre, on
the one pulse that the fugue will keep for all four at once:

  q0-12   Allemande  4/4   the subject with its sixteenth upbeat, A to a half close on E
  q12-24  Courante   3/2   E major, a hemiola cadence (3 half notes) into F# minor
  q24-36  Sarabande  3/4   F# minor, the long note on beat 2, back to E
  q36-48  Gigue      12/8  the subject in compound time, the left hand answering it
  q48-60  two at once: gigue triplets in the right hand over a courante bass (3/2 with hemiola)
  q60-71  two at once: the allemande subject over a sarabande bass (3/4, weight on beat 2)
  q71-88  the tune itself: the first three bars of the Bourree I of Bach's English Suite in A
          (BWV 806), both hands, at pitch, then a cadence.

Every note is written here as a literal token string (PITCH:SIXTEENTHS; triplet eighth = 4/3).
Thematic statements are the fugue's subject versions (SA, SC, SS, SG) imported from fugue.py.
The bourree bars are Bach's, quoted (source and check in NOTES.md).  The master metre of the file
is 4/4; per-staff time signatures are written into the LilyPond score (score_layout.staff_meters).
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
sys.path.insert(0, str(HERE))
import wtclib as W  # noqa: E402
from fugue import SA, SG, oc, dshift  # noqa: E402

METER = (4, 4)
NAMES = ['Dessus', 'Partie', 'Basse']
VO = {n: [] for n in NAMES}
END = 88


def put(v, q, toks):
    VO[v].append((Fr(q) * 4, ' '.join(toks.split())))


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def assemble(v):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at q{float(s / 4)}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    if cur < END * 4:
        out.append(f'R:{END * 4 - cur}')
    return W.concat_bars(' '.join(out), METER)


ENTRIES = []


def theme(v, q, toks, label):
    put(v, q, toks)
    ENTRIES.append((v, Fr(q), label, dur16(toks) / 4))


# ---- I. Allemande (q0-12): the subject with its upbeat, I - IV - V
theme('Dessus', Fr(3, 4), oc(SA, 1), 'Allemande')
put('Dessus', 5, 'D5:1 C#5:1 B4:1 A4:1 G#4:2 E5:2 F#5:2 G#5:2')
put('Dessus', 8, 'A5:2 E5:2 C#5:2 A4:2 B4:2 D5:2 G#4:4')
put('Basse', 0, 'A2:4 C#3:4 A2:4 E2:4 C#3:4 D3:4 E3:4 D3:4 C#3:4 F#2:4 B2:4 E2:4')
put('Partie', 8, 'C#4:4 E4:4 D4:4 B3:4')

# ---- II. Courante (q12-24, 3/2): E major; the hemiola bar cadences in F# minor
put('Dessus', 12, 'B5:6 A5:2 G#5:4 E5:4 F#5:6 E5:2 D5:4 F#5:4 E#5:2 F#5:2 G#5:4 F#5:8')
put('Partie', 12, 'E4:4 B4:4 C#5:4 B4:4 A4:8 B4:4 A4:4 B4:8 A4:8')
put('Basse', 12, 'E3:4 G#2:4 C#3:8 D3:4 D2:4 D3:8 C#3:8 F#2:8')

# ---- III. Sarabande (q24-36, 3/4): F# minor, the long note on the second beat, to E
put('Dessus', 24, 'C#5:4 F#5:6 E#5:2 G#5:4 A5:8 B5:4 A5:6 G#5:2 F#5:4 E5:4 D5:8/3')
put('Partie', 24, 'A4:4 C#5:6 B4:2 B4:4 A4:8 F#4:4 F#4:6 E4:2 B4:4 B4:6 G#4:2')
put('Basse', 24, 'F#2:4 A2:6 G#2:2 C#3:4 F#2:8 D3:4 B2:6 E3:2 D3:4 E3:6 E2:2')

# ---- IV. Gigue (q36-48, 12/8): the subject over a running bass, then the left hand answers
theme('Dessus', 36 - Fr(1, 3), oc(SG, 1), 'Gigue')
put('Dessus', 42, 'C#6:8/3 B5:4/3 B5:8/3 G#5:4/3 A5:8/3 F#5:4/3 G#5:8/3 B5:4/3 C#6:4/3 B5:4/3 A5:4/3 G#5:8/3 B5:4/3')
put('Basse', 36, 'A2:8/3 C#3:4/3 G#2:8/3 B2:4/3 D3:8/3 B2:4/3 A2:8/3 E2:4/3 F#2:8/3 D2:4/3 E2:8/3')
theme('Basse', 42 - Fr(1, 3), oc(dshift(SG, 4), -2), 'Gigue, answered')

# ---- V. Two at once (q48-60): gigue triplets over a courante bass with its hemiola
put('Dessus', 48, 'C#6:8/3 E6:4/3 A5:8/3 C#6:4/3 A5:4/3 G#5:4/3 F#5:4/3 D6:8/3 A5:4/3 '
                  'B5:8/3 G#5:4/3 E5:4/3 F#5:4/3 G#5:4/3 F#5:8/3 D5:4/3 B5:8/3 A5:4/3 '
                  'G#5:8/3 E5:4/3 B5:8/3 D6:4/3 C#6:8/3 A5:4/3 E5:4/3 A5:4/3 C#6:4/3')
put('Basse', 48, 'A2:6 G#2:2 F#2:4 D2:4 E2:8 D3:8 E3:8 A2:8')

# ---- VI. Two at once (q60-71): the allemande subject over a sarabande bass
theme('Dessus', 60 + Fr(3, 4), oc(SA, 1), 'Allemande over the sarabande')
put('Dessus', 65, 'F#5:1 E5:1 D5:1 F#5:1 D5:2 B4:1 D5:1 E5:1 F#5:1 G#5:1 E5:1 '
                  'B5:2 G#5:1 E5:1 C#6:1 B5:1 A5:1 C#6:1 B5:2 F#5:1 D5:1')
put('Basse', 60, 'A2:4 C#3:6 D3:2 C#3:4 D3:8 B2:4 E3:8 A2:4 D3:4 E3:4')
put('Partie', 66, 'D4:4 B3:4 D4:2 B3:2 C#4:4 D4:4 B3:4')

# ---- VII. The tune itself: Bach, Bourree I (BWV 806), bars 1-3 at pitch, then the cadence
BACH_RH = ('E4:4 A4:2 G#4:2 B4:2 A4:2 C#5:2 B4:2 A4:2 G#4:2 A4:4 E4:4 C#4:2 E4:2 A4:2 B4:2 '
           'C#5:2 B4:2 D5:2 C#5:2 E5:2 D5:2 C#5:2 B4:2')
BACH_LH = 'E3:4 A3:2 G#3:2 B3:2 A3:2 C#4:2 B3:2 A3:2 G#3:2 A3:4 E3:4 C#3:2 E3:2 A3:2 B3:2'
theme('Dessus', 71, BACH_RH, 'Bach, Bourree I (BWV 806), bars 1-3')
theme('Basse', 75, BACH_LH, 'Bach, the bass imitation')
put('Dessus', 84, 'D5:2 C#5:2 B4:4 A4:8')
put('Partie', 84, 'F#4:4 E4:4 C#4:8')
put('Basse', 84, 'D3:4 E3:4 A2:8')


def staff_meters():
    """All staves show the dance of the moment; in the two duets the right hand keeps its dance
    and the left hand its own (q48: 12/8 over 3/2; q60: 4/4 over 3/4); the bourree in 2/2."""
    upper = [[0, 4, 4], [12, 3, 2], [24, 3, 4], [36, 12, 8, '2/3'], [60, 4, 4], [72, 2, 2]]
    lower = [[0, 4, 4], [12, 3, 2], [24, 3, 4], [36, 12, 8, '2/3'], [48, 3, 2], [60, 3, 4], [72, 2, 2]]
    return {'Dessus': upper, 'Partie': upper, 'Basse': lower}


def build(write=True):
    bars = {n: assemble(n) for n in NAMES}
    if not write:
        return bars
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': "Prelude XIX in A major: Le Maitre a danser",
            'composer': "Claude / Sam (quoting the Bourree I of Bach's English Suite in A, BWV 806)",
            'instrument': 'Piano (one player)',
            'key': 'A', 'mode': 'major', 'meter': list(METER), 'bpm': 72,
            'tempo_text': 'Le maitre a danser: one pulse, four dances', 'movement_number': 19,
            'piece_type': 'prelude', 'edition': 'third',
            'tempo_map': [[0, 72], [70, 72], [71, 64, 'ramp'], [72, 66], [84, 66], [88, 50, 'ramp']],
            'score_layout': {'staff_meters': staff_meters()}}
    voices = [('Dessus', 'Des', 'treble', 72), ('Partie', 'Par', 'treble', 58), ('Basse', 'Bas', 'bass', 64)]
    entries = []
    for v, q, label, dq in ENTRIES:
        b0 = int(q // 4) + 1
        entries.append((v, b0, q - 4 * (b0 - 1), label, max(1, round(float(dq) / 4))))

    def dynamics(b):
        return {3: 2, 4: 2, 6: -4, 7: -4, 8: -3, 12: 4, 13: 4, 14: 4, 15: 2, 16: 2, 18: -2, 19: -2, 20: 0, 21: -3}.get(b, 0)
    return W.build_score(HERE / 'prelude.json', meta, voices, bars, entries=entries, subject=SA,
                         dynamics=dynamics, entry_boost=4)


if __name__ == '__main__':
    build()
