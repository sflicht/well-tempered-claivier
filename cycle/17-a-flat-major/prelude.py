#!/usr/bin/env python3
"""Prelude XVII in A-flat major: "Wiegenlied" (the lullaby that never quite ends).

The children sing their father to sleep.  Their lullaby is the fugue's subject in augmentation, over a
rocking left hand: it is the tune the father will come down singing at the end of the fugue.  Each verse
is deflected at its last note:
  verse 1 rests on the dominant, and verse 2 starts over a first-inversion tonic before it can end;
  verse 2 ends with a deceptive cadence (V -> vi), and the alto sings verse 3 in F minor;
  verse 3 reaches V7, but the bass stays where it is (V7 -> I6/4 over the same E-flat): a dominant pedal;
  verse 4 is sung over that pedal, pianissimo, and at its end the hands resolve to the tonic while the bass
  never arrives.  Only the father, at the end of the fugue, supplies it.

One pianist: the tune (soprano, and a second voice in verse 2), the rocking figure and the bass.  Every
note is written here as a literal token string; the tune is the hand-written subject of fugue.py put
through named transforms (key, mode, augmentation).  Units: sixteenths; a 12/8 bar is 24.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (12, 8)
BAR = 24
VOICES = [
    ('S', 'Soprano (the tune)', 'treble', 64),
    ('A', 'Alto (a second voice)', 'treble', 55),
    ('C', 'Cradle (left hand)', 'bass', 50),
    ('B', 'Bass', 'bass', 56),
]
NAMES = [v[0] for v in VOICES]
LONG = {v[0]: v[1] for v in VOICES}

# The fugue's subject, as scale degrees (see fugue.py): do. | DO' ti | la sol fa | mi fa || re mi | fa sol la |
# sol. fa mi | re.
SUBJ_DEG = [(0, 6), (7, 4), (6, 2), (5, 2), (4, 2), (3, 2), (2, 4), (3, 2),
            (1, 4), (2, 2), (3, 2), (4, 2), (5, 2), (4, 3), (3, 1), (2, 2), (1, 6)]
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]
NAT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
LET = 'CDEFGAB'


def tune(tonic, mode='major', octave=4, upto=None):
    """The subject in augmentation (x2) in a key: the lullaby."""
    L = tonic[0]
    t = 12 * (octave + 1) + NAT[L] + tonic.count('#') - tonic.count('b')
    sc = MAJOR if mode == 'major' else MINOR
    out = []
    for d, u in SUBJ_DEG[:upto]:
        p = t + 12 * (d // 7) + sc[d % 7]
        out.append(f'{W.name_of(p, LET[(LET.index(L) + d) % 7])}:{2 * u}')
    return ' '.join(out)


VO = {n: [] for n in NAMES}
ENTRIES = []


def put(v, bar, e, toks):
    VO[v].append((Fr(bar - 1) * BAR + Fr(e) * 2, ' '.join(toks.replace('|', ' ').split())))


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def assemble(v, nbars):
    out, cur = [], Fr(0)
    for s, toks in sorted(VO[v], key=lambda x: x[0]):
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / BAR + 1):.3f}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    if cur > nbars * BAR:
        raise ValueError(f'{v}: runs past the end')
    if cur < nbars * BAR:
        out.append(f'R:{nbars * BAR - cur}')
    return W.concat_bars(' '.join(out), METER)


# Bars 1-2: the cradle alone (A-flat, then IV6/4 - I over the A-flat).
put('B', 1, 0, 'Ab2:24 | Ab2:24')
put('C', 1, 0, 'Ab3:4 C4:2 Eb3:4 Ab3:2 Ab3:4 C4:2 Eb3:4 Ab3:2 | Ab3:4 Db4:2 F3:4 Ab3:2 Ab3:4 C4:2 Eb3:4 Ab3:2')

# Verse 1 (bars 3-6): I | IV - vi | ii - IV | I6/4 - V.  It rests on the dominant, the tune on re.
put('S', 3, 0, tune('Ab'))
ENTRIES.append((LONG['S'], 3, 0, 'verse 1: the fugue subject in augmentation', 4))
put('B', 3, 0, 'Ab2:12 C3:12 | Db3:12 F2:12 | Bb2:24 | Eb3:12 Eb2:12')
put('C', 3, 0, 'Ab3:4 C4:2 Eb3:4 Ab3:2 Ab3:4 C4:2 Eb3:4 Ab3:2 | Ab3:4 Db4:2 F3:4 Ab3:2 Ab3:4 C4:2 F3:4 Ab3:2 |'
               ' Db4:4 F3:2 Bb3:4 Db4:2 F3:4 Bb3:2 Db4:4 F3:2 | Ab3:4 C4:2 C4:4 Ab3:2 G3:4 Bb3:2 Eb3:4 G3:2')

# Verse 2 (bars 7-10): it starts over I6 before verse 1 can end; a second voice sings in sixths below.  It
# ends V -> vi (the deceptive cadence).
put('S', 7, 0, tune('Ab'))
ENTRIES.append((LONG['S'], 7, 0, 'verse 2 (over I6), with a second voice', 4))
put('A', 7, 0, 'Eb4:12 C5:8 Bb4:4 | Ab4:4 G4:4 F4:4 Ab4:8 Bb4:4 | Db4:8 Eb4:4 F4:4 G4:4 Ab4:4 | Eb4:12')
put('B', 7, 0, 'C3:12 Ab2:12 | Db3:12 Ab2:12 | Bb2:24 | Eb3:12 Eb2:12')
put('C', 7, 0, 'Ab3:4 C4:2 Eb3:4 Ab3:2 Ab3:4 C4:2 Eb3:4 Ab3:2 | F3:4 Ab3:2 F3:4 Ab3:2 C4:4 Ab3:2 Eb3:2 Ab3:2 C4:2 |'
               ' Db4:4 F3:2 Bb3:4 Db4:2 F3:4 Bb3:2 Db4:4 F3:2 | Ab3:4 C4:2 C4:4 Ab3:2 G3:4 Bb3:2 Eb3:4 G3:2')

# Verse 3 (bars 11-14): F minor; the alto sings the tune's first half (the soprano listens), then the
# harmony turns home: IV - ii7 | ii6/5 - V7 ...
put('S', 11, 0, 'Ab4:6')
put('A', 11, 0, tune('F', 'minor', upto=8))
ENTRIES.append((LONG['A'], 11, 0, 'verse 3: the first half in F minor (alto)', 2))
put('A', 13, 0, 'Ab4:36 G4:12')
put('B', 11, 0, 'F2:12 Ab2:12 | Bb2:12 Db3:12 | Db3:12 Bb2:12 | Db3:12 Eb3:12')
put('C', 11, 0, 'Ab3:4 C4:2 F3:2 Ab3:2 C4:2 C4:4 F3:2 Ab3:4 C4:2 | Db4:4 F3:2 Bb3:4 Db4:2 F3:4 Ab3:2 F3:2 Ab3:2 Db4:2 |'
                ' Ab3:4 Db4:2 F3:4 Ab3:2 Bb3:4 Db4:2 F3:4 Ab3:2 | F3:4 Ab3:2 Bb3:4 F3:2 G3:4 Bb3:2 Db4:4 Bb3:2')

# Verse 4 (bars 15-18): ... and the bass stays on E-flat (V7 -> I6/4 over the same note).  The last verse is
# sung over that dominant pedal; the cradle climbs a little, then slows (held beats), and the second voice
# is asleep.
put('S', 15, 0, tune('Ab'))
ENTRIES.append((LONG['S'], 15, 0, 'verse 4, over the dominant pedal', 4))
put('B', 15, 0, 'Eb3:96')
put('C', 15, 0, 'Ab3:4 C4:2 Eb4:4 C4:2 Ab3:4 C4:2 Eb4:4 C4:2 | Ab3:4 Db4:2 F4:4 Db4:2 Ab3:4 C4:2 Eb4:6 |'
                ' G3:4 Bb3:2 Bb3:6 G3:4 Bb3:2 Db4:6 | Ab3:4 C4:2 Ab3:6 G3:4 Bb3:2 Bb3:6')

# Bar 19: the hands resolve to the tonic.  The bass does not come.
put('S', 19, 0, 'Ab4:24')
put('A', 19, 0, 'Eb4:24')
put('C', 19, 0, 'C4:24')

NB = 19


def q(bar, beat=1):
    return float((bar - 1) * 6 + (beat - 1) * Fr(3, 2))


# Andante tranquillo, dotted quarter = 50 (quarter = 75); each verse's end broadens; the last verse is slower
# and slows to the end; the last chord is held (quarter = 30, about 12 s for the bar).
TEMPO = [[0, 75], [q(6, 3), 75], [q(7), 66, 'ramp'], [q(7), 75], [q(10, 3), 75], [q(11), 64, 'ramp'],
         [q(11), 75], [q(14, 3), 75], [q(15), 62, 'ramp'], [q(15), 68], [q(17), 68], [q(19), 52, 'ramp'],
         [q(19), 30]]
DYN = {1: -6, 3: 0, 7: -2, 11: 2, 13: 0, 15: -6, 17: -8, 19: -12}


def build(path=None):
    path = Path(path or HERE / 'prelude.json')
    bars = {LONG[n]: assemble(n, NB) for n in NAMES}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'XVII. Prelude in A-flat major: Wiegenlied (the lullaby that never quite ends)',
            'composer': 'Claude / composed for Sam', 'instrument': 'Piano',
            'key': 'Ab', 'mode': 'major', 'meter': list(METER), 'bpm': 75,
            'tempo_text': 'Andante tranquillo, cullando (dotted quarter = 50)', 'movement_number': 17,
            'piece_type': 'prelude', 'edition': 'third', 'tempo_map': TEMPO,
            'score_layout': {'hide_empty_staves': True},
            'markers': [{'t': q(1), 'label': 'The cradle'}, {'t': q(3), 'label': 'Verse 1'},
                        {'t': q(7), 'label': 'Verse 2 (before verse 1 can end)'},
                        {'t': q(11), 'label': 'Verse 3: F minor (after V - vi)'},
                        {'t': q(15), 'label': 'Verse 4: over the dominant (V7 - I6/4)'},
                        {'t': q(19), 'label': 'The hands resolve; the bass never comes'}]}
    voices = [(LONG[n], n, clef, vel) for n, _, clef, vel in VOICES]

    def dynamics(b):
        v = 0
        for k in sorted(DYN):
            if b + 1 >= k:
                v = DYN[k]
        return v
    data = W.build_score(path, meta, voices, bars, entries=ENTRIES, subject=tune('Ab'), dynamics=dynamics,
                         accents=False)
    for v in data['voices']:
        for e in v['events']:
            ph = Fr(e['t']).limit_denominator(48) % 6
            e['v'] = max(24, min(118, int(e['v']) + (3 if ph == 0 else 1 if ph == 3 else 0)))
        v['piano_pan'] = {'S': 72, 'A': 66, 'C': 58, 'B': 54}[v['abbr']]
    path.write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
    print('bars', NB)
