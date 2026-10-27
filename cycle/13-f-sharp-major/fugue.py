#!/usr/bin/env python3
"""Fugue XIII in F-sharp major, fourteen voices:
"Fuga canonica a 14 sopra il fondamento di Goldberg".

(Draft skeleton; the header is completed when the piece is.)
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (3, 4)
BAR = 12                     # sixteenths per bar
LET = 'CDEFGAB'
SHARPS = set('FCGDAE')       # F-sharp major: six sharps (B is natural)

# ---------------------------------------------------------------------------------------------
# Explicit canon transforms (diatonic, letter-preserving, in the F-sharp-major key signature).
# A note's accidental relative to the key signature is carried over (shift) or negated (mirror).

def _parse(tok):
    name, d = tok.rsplit(':', 1)
    if name == 'R':
        return None
    p, _, sp, _ = W.parse_tok(name + ':1')
    L = sp[0].upper()
    for o in range(-1, 10):
        alt = p - (12 * (o + 1) + W.NAT[L])
        if -2 <= alt <= 2:
            return o * 7 + LET.index(L), alt - (1 if L in SHARPS else 0), d
    raise ValueError(tok)


def _name(idx, rel):
    L = LET[idx % 7]
    o = idx // 7
    p = 12 * (o + 1) + W.NAT[L] + (1 if L in SHARPS else 0) + rel
    return W.name_of(p, L)


def shift(s, steps):
    """Diatonic transposition by `steps` letter names (canon at the 2nd = 1, 3rd = 2, 6th below = -5...)."""
    out = []
    for t in s.split():
        r = _parse(t)
        out.append(t if r is None else f"{_name(r[0] + steps, r[1])}:{r[2]}")
    return ' '.join(out)


def mirror(s, a, b):
    """Diatonic mirror that maps note a onto note b (e.g. 'F#5' -> 'C#5'); accidentals are negated."""
    ia, ib = _parse(a + ':1')[0], _parse(b + ':1')[0]
    out = []
    for t in s.split():
        r = _parse(t)
        out.append(t if r is None else f"{_name(ia + ib - r[0], -r[1])}:{r[2]}")
    return ' '.join(out)


def dur16(s):
    return sum(W.parse_tok(t)[1] for t in s.split())


# ---------------------------------------------------------------------------------------------
# Material written by hand.

# The fundamentum: BWV 988's ground (G F# E D B C D G), in F-sharp major.
GROUND = ['F#', 'E#', 'D#', 'C#', 'A#', 'B', 'C#', 'F#']

# The fugue subject: the whole ground in dotted diminution (bar 1), then a springing tail that
# climbs back an octave and stops on the supertonic (bar 2).
SUBJECT = 'F#4:3 E#4:1 D#4:3 C#4:1 A#3:3 B3:1 C#4:2 F#4:2 E#4:1 G#4:1 C#5:2 B4:1 A#4:1 G#4:2'
SUBJ_BARS = ['F#4:3 E#4:1 D#4:3 C#4:1 A#3:3 B3:1', 'C#4:2 F#4:2 E#4:1 G#4:1 C#5:2 B4:1 A#4:1 G#4:2']


def subj(octave_shift=0):
    return [shift(b, 7 * octave_shift) for b in SUBJ_BARS]


# The six canons: (number, interval label, transform, delay in bars).  Mirror canons map the dux's
# first note F# onto the comes's first note.
CANONS = [
    ('I', 'unison', lambda s: s, 2),
    ('II', '2nd above', lambda s: shift(s, 1), 1),
    ('III', '3rd above', lambda s: shift(s, 2), 2),
    ('IV', '4th below, by inversion', lambda s: mirror(s, 'F#5', 'C#5'), 4),
    ('V', '5th below, by inversion', lambda s: mirror(s, 'F#5', 'B4'), 3),
    ('VI', '6th below', lambda s: shift(s, -5), 8),
]
CANON = {c[0]: c for c in CANONS}

# Score order (top to bottom) = ring order for the spatial render.
VOICES = [  # key, long name, abbr, clef
    ('VIdx', 'Canon VI dux', 'VId', 'treble'),
    ('VIco', 'Canon VI comes (6th below)', 'VIc', 'treble'),
    ('Vdx', 'Canon V dux', 'Vd', 'treble'),
    ('Vco', 'Canon V comes (5th below, inverted)', 'Vc', 'treble'),
    ('IVdx', 'Canon IV dux', 'IVd', 'treble'),
    ('IVco', 'Canon IV comes (4th below, inverted)', 'IVc', 'treble'),
    ('IIIco', 'Canon III comes (3rd above)', 'IIIc', 'treble'),
    ('IIIdx', 'Canon III dux', 'IIId', 'treble'),
    ('IIco', 'Canon II comes (2nd above)', 'IIc', 'treble'),
    ('IIdx', 'Canon II dux', 'IId', 'treble'),
    ('Sog', 'Soggetto', 'Sog', 'treble'),
    ('Idx', 'Canon I dux', 'Id', 'treble_8'),
    ('Ico', 'Canon I comes (unison)', 'Ic', 'treble_8'),
    ('Fund', 'Fundamentum', 'Fun', 'bass'),
]
KEYS = [v[0] for v in VOICES]

# Literal bars: LINES[voice][bar] = bar string (12 sixteenths).  Comes voices are filled from
# their dux by the canon transform; COMES_FREE holds their bars after the canon has ended.
LINES = {k: {} for k in KEYS}
CANON_SPAN = {}      # canon -> (first dux bar, last dux bar that is copied)
COMES_FREE = {}      # canon -> {bar: string}
ENTRIES = []         # (voice key, bar, beat offset in quarters, label, n bars)


def put(v, bar, bars):
    for k, s in enumerate(bars):
        if bar + k in LINES[v]:
            raise ValueError(f'{v}: bar {bar + k} written twice')
        LINES[v][bar + k] = s


def entry(v, bar, label, beat=0, n=2):
    ENTRIES.append((v, bar, beat, label, n))


# =============================================================================================
# Var. 1 (b1-8), "Aria": the fundamentum and the soggetto alone.
put('Fund', 1, ['F#3:12', 'E#3:12', 'D#3:12', 'C#3:10 B2:2', 'A#2:12', 'B2:12', 'C#3:12', 'F#2:12'])
put('Sog', 1, subj(0) + [
    'A#4:2 F#4:2 D#5:4 C#5:1 B4:1 A#4:1 G#4:1',                 # b3  vi: falls back through the tail
    'F#4:2 E#4:1 F#4:1 G#4:2 E#4:1 G#4:1 A#4:2 B4:2',           # b4  V: climbs into the inversion
    'C#5:3 D#5:1 E#5:3 F#5:1 A#5:3 G#5:1',                      # b5  I6: the subject inverted (mirror F#-C#)
    'F#5:2 C#5:2 D#5:1 B4:1 F#4:2 G#4:1 A#4:1 B4:2',            # b6  ii6
    'G#4:2 C#5:2 E#5:2 G#5:1 F#5:1 E#5:1 D#5:1 C#5:1 B4:1',     # b7  V7
    'A#4:4 C#5:2 A#4:1 F#4:1 G#4:2 A#4:2',                      # b8  I
])
entry('Sog', 1, 'Subject')
entry('Sog', 5, 'Subject inverted (mirror F#-C#)')

# =============================================================================================
# Var. 2 (b9-16): Canon I, at the unison, two bars apart (triplets: Var. 3's lilt).
put('Fund', 9, ['F#2:12', 'E#2:12', 'D#2:12', 'C#2:12', 'A#1:12', 'B1:12', 'C#2:12', 'F#2:12'])
T = '4/3'
def tri(notes):
    return ' '.join(f'{n}:{T}' for n in notes.split())
put('Idx', 9, subj(0) + [
    tri('A#4 B4 C#5 B4 A#4 G#4 A#4 B4 C#5'),                  # b11 vi    (high, over the comes's subject)
    tri('F#5 E#5 D#5 C#5 B4 A#4') + ' G#4:4',                  # b12 V
    'C#4:4 D#4:4 C#4:4',                                       # b13 I6    (low, under its own triplets)
    'D#4:6 E#4:2 F#4:4',                                       # b14 ii6
    tri('C#5 D#5 E#5 F#5 E#5 D#5 E#5 F#5 D#5'),                 # b15 V7    (high)
    tri('C#5 B4 A#4 B4 C#5 D#5 C#5 B4 A#4'),                   # b16 I
])
put('Idx', 17, [
    'F#4:6 E#4:2 F#4:4',                                       # b17 I     (low)
    'G#4:12',                                                  # b18 V6
    'A#4:4 B4:4 A#4:4',                                        # b19 vi    (V3: canon I sings broad notes
    'R:12',                                                    # b20 V      under canon II's quavers;
    'R:12',                                                    # b21 I6     dux and comes take turns)
    'F#4:4 G#4:6 F#4:2',                                       # b22 ii6
    'R:12',                                                    # b23 V7    (canon I breathes, so that
    'R:12',                                                    # b24 I      canon III can enter alone)
    'R:4 A#4:4 C#5:4~',                                        # b25 I
    'C#5:4 G#4:6 E#4:2',                                       # b26 V6
    'R:12',                                                    # b27 vi
    'R:12',                                                    # b28 V
    'R:12',                                                    # b29 I6
    'R:12',                                                    # b30 ii6
    'R:4 C#5:8',                                               # b31 V7
    'C#5:6 B4:2 C#5:4',                                        # b32 I
    'R:12',                                                    # b33 I
    'R:12',                                                    # b34 V6
    'R:12',                                                    # b35
    'R:12',                                                    # b36
    'R:12',                                                    # b37
    'R:12',                                                    # b38
    'R:12',                                                    # b39
    'R:12',                                                    # b40
    'F#3:4 A#3:4 F#3:4',                                       # b41 I   (canon I returns, low and broad)
    'G#3:12',                                                  # b42 V6
    'R:12',                                                    # b43 vi
    'R:12',                                                    # b44
    'R:12',                                                    # b45
    'R:12',                                                    # b46
    'R:12',                                                    # b47
    'R:12',                                                    # b48
    'R:12',                                                    # b49
    'R:12',                                                    # b50
    'A#4:4 R:4 F#4:4',                                         # b51
    'G#4:8 R:4',                                               # b52
    'C#5:6 D#5:2 C#5:4',                                       # b53
    'R:12',                                                    # b54
    'R:12',                                                    # b55
    'R:4 C#4:8',                                               # b56
    'R:8 A#4:4',                                                 # b57
])
CANON_SPAN['I'] = (9, 57)
entry('Idx', 9, 'Canon I dux: subject')
entry('Ico', 11, 'Canon I comes: subject at the unison')
put('Sog', 9, [
    'C#5:4 F#5:4 E#5:2 D#5:2',                                  # b9   a descant over the canon
    'C#5:4 G#5:6 F#5:2',                                        # b10
    'F#5:4 A#5:4 G#5:2 F#5:2',                                  # b11
    'E#5:2 F#5:2 G#5:8',                                        # b12
    'F#5:4 A#5:6 G#5:2~',                                       # b13
    'G#5:4 E#5:2 F#5:2 D#5:4',                                  # b14
    'E#5:6 F#5:2 G#5:2 E#5:2',                                  # b15
    'F#5:4 C#5:4 A#4:2 B4:2',                                   # b16
])

# =============================================================================================
# Var. 3 (b17-24): Canon II, at the 2nd above, one bar apart (scalar quavers: Var. 6).
put('Fund', 17, ['F#2:12', 'E#2:12', 'D#2:10 A#1:2', 'C#2:12', 'A#1:12', 'B1:12', 'C#2:12', 'F#2:12'])
put('IIdx', 17, subj(1) + [
    'F#5:2 E#5:2 D#5:2 C#5:2 D#5:2 F#5:2',                     # b19 vi
    'E#5:2 D#5:2 C#5:2 B4:2 C#5:2 D#5:2',                      # b20 V
    'C#5:4 F#5:4 A#5:4',                                       # b21 I6
    'F#5:2 D#5:2 B4:2 C#5:2 D#5:2 F#5:2',                      # b22 ii6
    'E#5:2 D#5:2 C#5:2 B4:2 C#5:2 G#5:2~',                     # b23 V7
    'G#5:2 F#5:2 E#5:2 D#5:2 C#5:2 D#5:2',                     # b24 I: the 9-8 that the comes needs
    'F#5:2 G#5:2 A#5:2 G#5:2 F#5:2 G#5:2',                     # b25 I
    'C#5:2 E#5:2 D#5:2 C#5:2 D#5:2 E#5:2',                     # b26 V6
    'A#4:2 B4:2 C#5:2 B4:2 A#4:2 G#4:2',                       # b27 vi
    'E#5:2 D#5:2 C#5:2 D#5:2 E#5:2 G#5:2',                     # b28 V
    'C#6:4 B5:2 C#6:2 A#5:2 G#5:2',                            # b29 I6
    'G#5:2 A#5:2 B5:2 A#5:2 G#5:2 F#5:2',                      # b30 ii6
    'E#5:4 G#5:2 F#5:2 E#5:2 G#5:2~',                          # b31 V7
    'G#5:2 F#5:2 E#5:2 D#5:2 C#5:2 D#5:2',                     # b32 I: 9-8
    'R:12',                                                    # b33 I   (canon II breathes for canon IV)
    'R:12',                                                    # b34 V6
    'R:12',                                                    # b35 vi
    'R:4 E#4:2 F#4:2 G#4:2 E#4:2',                             # b36 V   (returns, low)
    'A#3:2 F#4:2 E#4:2 C#4:2 F#4:2 D#4:2',                     # b37 I6  (broken chords in the tenor)
    'R:12',                                                    # b38 ii6
    'C#4:4 B3:2 A#3:2 G#3:4',                                  # b39 V7
    'R:12',                                                    # b40 I
    'R:12',                                                    # b41
    'R:12',                                                    # b42
    'D#4:2 E#4:2 F#4:2 E#4:2 D#4:2 C#4:2',                     # b43 vi
    'R:12',                                                    # b44 V
    'C#6:2 B5:2 A#5:2 G#5:2 F#5:2 G#5:2',                      # b45 I6
    'F#5:2 E#5:2 D#5:2 F#5:2 E#5:2 D#5:2',                     # b46 ii6
    'C#5:2 B4:2 G#4:2 B4:2 C#5:2 D#5:2',                       # b47 V7
    'R:12',                                                    # b48 I
    'R:12',                                                    # b49 I
    'R:4 G#4:2 A#4:2 B4:2 C#5:2',                              # b50 V6
    'D#5:2 C#5:2 D#5:2 E#5:2 F#5:4',                           # b51 vi
    'R:12',                                                    # b52 V
    'R:12',                                                    # b53 I6
    'D#5:4 E#5:2 F#5:2 D#5:4',                                 # b54 ii6
    'B4:2 C#5:2 B4:2 A#4:2 G#4:4',                             # b55 V7
    'R:12',                                                    # b56 I    (canon II: 8 -> 1 rests)
    'R:12',                                                      # b57
])
CANON_SPAN['II'] = (17, 57)
entry('IIdx', 17, 'Canon II dux: subject')
entry('IIco', 18, 'Canon II comes: subject at the 2nd above')

# =============================================================================================
# Var. 4 (b25-32): Canon III, at the 3rd above, two bars apart, entering in the tenor.
put('Fund', 25, ['F#2:12', 'E#2:12', 'D#2:12', 'C#2:12', 'A#1:12', 'B1:12', 'C#2:12', 'F#2:12'])
put('IIIdx', 25, subj(-1) + [
    'D#4:2 E#4:1 F#4:1 G#4:2 A#4:2 G#4:2 F#4:2',               # b27 vi   (Var. 9: gentle semiquaver turns)
    'E#4:2 F#4:1 G#4:1 A#4:2 G#4:2 F#4:2 E#4:2',               # b28 V
    'C#4:2 D#4:1 E#4:1 F#4:2 E#4:2 C#4:4',                     # b29 I6
    'B3:2 C#4:1 D#4:1 E#4:2 F#4:2 D#4:2 B3:2',                 # b30 ii6
    'B3:2 C#4:1 D#4:1 E#4:2 D#4:2 C#4:2 B3:2',                 # b31 V7
    'A#3:2 B3:1 C#4:1 D#4:2 C#4:2 A#3:4',                      # b32 I
    'R:12',                                                    # b33 I
    'R:12',                                                    # b34 V6
    'F#4:2 G#4:1 A#4:1 B4:2 A#4:2 G#4:2 F#4:2',               # b35 vi  (above the soggetto's subject)
    'E#4:2 D#4:1 C#4:1 D#4:2 E#4:2 G#4:4',                     # b36 V
    'R:12',                                                    # b37 I6
    'D#5:4 F#5:2 E#5:1 D#5:1 C#5:2 D#5:2',                     # b38 ii6
    'R:12',                                                    # b39 V7
    'R:12',                                                    # b40 I
    'R:12',                                                    # b41
    'R:12',                                                    # b42
    'R:12',                                                    # b43
    'R:12',                                                    # b44
    'R:12',                                                    # b45
    'B3:4 A#3:2 G#3:2 F#3:4',                                  # b46 ii6  (returns in the tenor)
    'R:12',                                                    # b47 V7
    'R:12',                                                    # b48 I
    'R:12', 'R:12', 'R:12',                                    # b49-51
    'R:8 E#4:4',                                               # b52 V
    'A#3:4 C#4:2 B3:2 R:4',                                    # b53 I6
    'D#4:8 C#4:2 B3:2',                                        # b54 ii6
    'R:12',                                                    # b55 V7
    'R:12',                                                    # b56 I
    'F#3:2 A#3:2 C#4:2 B3:1 A#3:1 G#3:2 F#3:2',                  # b57
])
CANON_SPAN['III'] = (25, 57)
entry('IIIdx', 25, 'Canon III dux: subject (tenor)')
entry('IIIco', 27, 'Canon III comes: subject at the 3rd above')

# =============================================================================================
# Var. 5 (b33-40): Canon IV, at the 4th below by inversion, four bars apart (the tonal mirror
# F#<->C#, as in Var. 12), entering on top while canon II breathes.
put('IVdx', 33, subj(1) + [
    'F#5:8 G#5:4~',                                            # b35 vi   (the tie becomes the comes's 4-3)
    'G#5:4 F#5:2 E#5:2 C#5:2 E#5:2',                           # b36 V
    'A#5:6 C#6:2 F#6:2 C#6:2',                                 # b37 I6   (a descant over its own mirror)
    'B5:4 D#6:4 B5:4',                                         # b38 ii6
    'G#5:6 F#5:2 E#5:4',                                       # b39 V7
    'R:12',                                                    # b40 I
    'R:12',                                                    # b41 I
    'G#5:4 C#6:8',                                             # b42 V6
    'F#6:12',                                                  # b43 vi
    'R:12',                                                    # b44 V
    'F#6:4 C#6:2 A#5:2 C#6:4',                                 # b45 I6
    'R:12',                                                    # b46 ii6
    'C#6:4 B5:4 A#5:4',                                        # b47 V7
    'F#5:6 G#5:2 F#5:2 E#5:2',                                 # b48 I
    'R:12', 'R:12', 'R:12', 'R:12',                            # b49-52
    'R:4 F#5:4 C#6:4',                                         # b53 I6
    'B5:4 R:8',                                                # b54 ii6
    'R:8 C#6:4',                                               # b55 V7
    'R:12',                                                    # b56 I
    'F#6:3 E#6:1 D#6:3 C#6:1 C#6:4',                             # b57
])
CANON_SPAN['IV'] = (33, 57)
put('Sog', 35, subj(-1) + ['R:12', 'R:12', 'R:12', 'R:4 A#4:4 C#5:4',
    'C#5:4 B4:2 A#4:2 G#4:2 F#4:2',                            # b41
    'B4:4 A#4:2 G#4:2 C#5:4',                                  # b42
    'G#4:2 F#4:2 D#4:4 F#4:4',                                 # b43
    'C#4:8 D#4:4',                                             # b44
    'A#3:6 B3:2 C#4:4',                                        # b45
    'R:12', 'R:12',                                            # b46-47
    'R:4 A#3:4 C#4:4',                                         # b48
    'A#3:2 F#3:2 A#3:2 C#4:2 D#4:2 C#4:2',                     # b49 I    (V7: under canon VI's entry)
    'G#3:4 C#4:2 B3:2 G#3:4',                                  # b50 V6
    'A#3:2 B3:2 D#4:2 C#4:2 A#3:2 F#3:2',                      # b51 vi
    'A#3:4 G#3:4 C#4:4',                                       # b52 V
    'F#3:8 A#3:4',                                             # b53 I6
    'F#3:6 G#3:2 A#3:2 B3:2',                                  # b54 ii6
    'G#3:6 A#3:2 B3:4',                                        # b55 V7
    'A#3:4 F#3:8',                                             # b56 I
    'C#3:4 A#2:8',                                               # b57
])
entry('Sog', 35, 'Subject (soggetto returns, tenor)')
entry('IVdx', 33, 'Canon IV dux: subject')
entry('IVco', 37, 'Canon IV comes: subject inverted, a 4th below')

# =============================================================================================
# Var. 6 (b41-48): Canon V, at the 5th below by inversion (mirror F#<->B), three bars apart
# (Var. 15's sighs).
put('Vdx', 41, subj(1) + [
    'A#5:2 G#5:2 F#5:4 F#5:2 E#5:2',                           # b43 vi   (sighs)
    'C#6:6 B5:2 A#5:2 G#5:2',                                  # b44 V
    'R:12',                                                    # b45 I6   (canon V breathes in bars 5 and 8)
    'R:12',                                                    # b46 ii6
    'R:12',                                                    # b47 V7 (clears the register for canon VI)
    'R:12',                                                    # b48 I
    'R:12', 'R:12', 'R:12', 'R:12', 'R:12',                    # b49-53
    'R:8 B4:4',                                                # b54 ii6
    'R:12',                                                    # b55 V7
    'R:12',                                                    # b56 I
    'R:4 C#6:2 A#5:2 R:4',                                       # b57
])
CANON_SPAN['V'] = (41, 57)
entry('Vdx', 41, 'Canon V dux: subject')
entry('Vco', 44, 'Canon V comes: subject inverted, a 5th below')

# =============================================================================================
# Variation 7 (bars 49-56): thirteen voices.  Canon VI (at the sixth below, eight bars apart, so
# the comes plays every dux bar over the same bass note) enters at the top.
put('VIdx', 49, subj(1) + [
    'F#5:8 D#6:4~',                                            # b51 vi   (the dux turns lyrical: its
    'D#6:2 C#6:6 E#5:4',                                       # b52 V     suspensions return a 6th lower
    'F#5:4 A#5:8~',                                            # b53 I6    in the middle of the summit)
    'A#5:2 G#5:2 B5:4 D#6:4',                                  # b54 ii6
    'C#6:6 B5:2 G#5:4',                                        # b55 V7
    'A#5:8 F#5:4',                                             # b56 I
    'A#5:4 F#6:6 E#6:2',                                         # b57
])
CANON_SPAN['VI'] = (49, 57)
entry('VIdx', 49, 'Canon VI dux: subject')
entry('VIco', 57, 'Canon VI comes: subject at the 6th below')

# =============================================================================================
# Variation 8 (bars 57-64): the summit.  Fourteen real voices; every canon runs over the ground
# while the subject enters in stretto, one bar apart: canon VI's comes on A-sharp (bar 57),
# canon II's dux on G-sharp (58), canon II's comes on A-sharp (59), ...
put('IIdx', 58, [shift(b, 1) for b in subj(1)] + [
])
CANON_SPAN['II'] = (17, 59)
entry('IIdx', 58, 'Stretto: canon II dux, subject on G#')
entry('IIco', 59, 'Stretto: canon II comes, subject on A#')

# ---- fundamentum for the rest (plain ground; ornamented later where the texture asks for it)
put('Fund', 33, ['F#2:12', 'E#2:12', 'D#2:12', 'C#2:12', 'A#1:12', 'B1:12', 'C#2:12', 'F#2:12'])
put('Fund', 41, ['F#2:12', 'E#2:12', 'D#2:12', 'C#2:8 B1:4', 'A#1:12', 'B1:12', 'C#2:12', 'F#2:12'])
for _b in (49, 57, 65, 73, 81):
    put('Fund', _b, ['F#2:12', 'E#2:12', 'D#2:12', 'C#2:12', 'A#1:12', 'B1:12', 'C#2:12', 'F#2:12'])

# =============================================================================================
# Assembly

def comes_bars(c, nbars):
    num, _, f, d = CANON[c]
    dx, co = c + 'dx', c + 'co'
    a, z = CANON_SPAN.get(c, (None, None))
    out = {}
    if a is None:
        return out
    for b in range(a, z + 1):
        s = LINES[dx].get(b, f'R:{BAR}')
        if b == z:
            s = s.replace('~', '')
        out[b + d] = f(s)
    for b, s in COMES_FREE.get(c, {}).items():
        if b in out:
            raise ValueError(f'{co}: free bar {b} inside the canon')
        out[b] = s
    return out


def all_lines(nbars):
    lines = {k: dict(LINES[k]) for k in KEYS}
    for c, *_ in CANONS:
        for b, s in comes_bars(c, nbars).items():
            if b in lines[c + 'co']:
                raise ValueError(f'{c}co: bar {b} both written and copied')
            lines[c + 'co'][b] = s
    return lines


def bars_of(lines, nbars):
    out = {}
    for k in KEYS:
        seq = []
        for b in range(1, nbars + 1):
            s = lines[k].get(b, f'R:{BAR}')
            if dur16(s) != BAR:
                raise ValueError(f'{k} bar {b}: {dur16(s)} sixteenths: {s}')
            seq.append(s)
        out[k] = seq
    return out


def nbars_written():
    lines = all_lines(999)
    return max(max(v) for v in lines.values() if v)


def build(path=None, nbars=None):
    nbars = nbars or nbars_written()
    lines = all_lines(nbars)
    bars = bars_of(lines, nbars)
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XIII in F-sharp major, fourteen voices: Fuga canonica sopra il fondamento di Goldberg',
            'composer': 'Claude / Sam (ground: J. S. Bach, BWV 988 and BWV 1087)',
            'instrument': 'Fourteen keyboards (open score)',
            'key': 'F#', 'mode': 'major', 'meter': list(METER), 'bpm': 76,
            'tempo_text': 'Allegretto, con brio', 'movement_number': 13, 'piece_type': 'fugue',
            'edition': 'third'}
    voices = [(name, abbr, clef, 62) for k, name, abbr, clef in VOICES]
    named = {VOICES[KEYS.index(k)][1]: bars[k] for k in KEYS}
    ents = [(VOICES[KEYS.index(v)][1], b, o, l, n) for v, b, o, l, n in ENTRIES]
    return W.build_score(path or HERE / 'fugue.json', meta, voices, named, entries=ents, subject=SUBJECT)


if __name__ == '__main__':
    d = build()
    print('built', HERE / 'fugue.json', nbars_written(), 'bars')
