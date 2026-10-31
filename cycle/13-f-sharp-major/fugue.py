#!/usr/bin/env python3
"""Fugue XIII in F-sharp major, four voices:
"Fuga canonica a 4 sopra il fondamento di Goldberg".

The fundamentum is the ground of J. S. Bach's Goldberg Variations, BWV 988 (the eight bass notes
G F# E D B C D G of BWV 1087), in F-sharp major (F# E# D# C# A# B C# F#), one note to a 3/4 bar.
The fugue subject is that ground in dotted diminution plus a springing tail, and the bass states it
alone first (bars 1-2).  Seven statements of the ground follow, each carrying a strict canon whose
interval climbs as the Goldberg canons climb, while the ground itself travels through a cadence
(I - IV - ii - V - I, then the tonic minor and major again):

    bars  3-10  F#   Canon I    at the unison,             2 bars apart (S -> A)
    bars 11-18  B    Canon II   at the second below,       1 bar apart  (S -> A)
    bars 19-26  G#m  Canon III  at the third below,        2 bars apart (S -> A)
    bars 27-34  C#   Canon IV   at the fourth below, by inversion, 1 bar apart (S -> T)
    bars 35-38       the bass's own entry (subject on C#) and the dominant pedal
    bars 39-46  F#   Canon V    at the fifth below, by inversion, 2 bars apart (A -> T)
    bars 47-54  F#m  Canon VI   at the sixth above,        2 bars apart (A -> S), Adagio
    bars 55-62  F#   Quodlibet after Var. 30: "Ich bin so lang" in canon at the octave (T -> A),
                     "Kraut und Ruben" (both phrases), the subject, over the ground

Every canon's dux begins with the subject, so its comes answers it at the canon's interval (or
inverted); the voice outside the canon is free or brings another entry.  Every comes is generated
from its dux by the transform in canon() and nothing else (check_canons.py verifies this from the
built JSON).  Every other note is written here as a literal token string, or as the subject or a
tune moved by an explicit transform (shift, mirror, modal, tr).  No code chose a pitch.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (3, 4)
BPM = 72
BAR = 12                     # sixteenths per 3/4 bar
LET = 'CDEFGAB'

# Key signatures (accidental of each letter) of the keys the ground visits.
_SIX = dict(F=1, C=1, G=1, D=1, A=1, E=1, B=0)
_FIVE = dict(F=1, C=1, G=1, D=1, A=1, E=0, B=0)
KEYSIG = {
    'F#': _SIX, 'D#m': _SIX,
    'B': _FIVE, 'G#m': _FIVE,
    'C#': dict(F=1, C=1, G=1, D=1, A=1, E=1, B=1),
    'F#m': dict(F=1, C=1, G=1, D=0, A=0, E=0, B=0),
}


# ---------------------------------------------------------------------------------------------
# Explicit transforms of hand-written material.  Diatonic: they move letter names and keep (shift)
# or negate (mirror) each note's accidental relative to the key signature.

def _parse(tok, key):
    name, d = tok.rsplit(':', 1)
    if name == 'R':
        return None
    p, _, sp, _ = W.parse_tok(name + ':1')
    L = sp[0].upper()
    for o in range(-1, 10):
        alt = p - (12 * (o + 1) + W.NAT[L])
        if -2 <= alt <= 2:
            return o * 7 + LET.index(L), alt - KEYSIG[key][L], d
    raise ValueError(tok)


def _name(idx, rel, key):
    L = LET[idx % 7]
    o = idx // 7
    p = 12 * (o + 1) + W.NAT[L] + KEYSIG[key][L] + rel
    return W.name_of(p, L)


def shift(s, steps, key='F#'):
    """Diatonic transposition by `steps` letter names in `key` (2nd above = 1, 3rd below = -2 ...)."""
    out = []
    for t in s.split():
        r = _parse(t, key)
        out.append(t if r is None else f"{_name(r[0] + steps, r[1], key)}:{r[2]}")
    return ' '.join(out)


def mirror(s, a, b, key='F#'):
    """Diatonic mirror in `key` that maps note a onto note b (e.g. 'F#5' -> 'C#5'); the accidental
    relative to the key signature is negated."""
    ia, ib = _parse(a + ':1', key)[0], _parse(b + ':1', key)[0]
    out = []
    for t in s.split():
        r = _parse(t, key)
        out.append(t if r is None else f"{_name(ia + ib - r[0], -r[1], key)}:{r[2]}")
    return ' '.join(out)


def modal(s, src, dst):
    """Re-reads each note's scale degree and alteration from key signature src in key signature dst
    (F-sharp major -> F-sharp minor: the subject's degrees with the minor mode's sixth and seventh)."""
    out = []
    for t in s.split():
        r = _parse(t, src)
        out.append(t if r is None else f"{_name(r[0], r[1], dst)}:{r[2]}")
    return ' '.join(out)


def tr(s, semis, letters):
    """Chromatic transposition (moves material written in F-sharp to another key)."""
    return W.transpose(s, semis, letters)


def dur16(s):
    return sum(W.parse_tok(t)[1] for t in s.split())


# ---------------------------------------------------------------------------------------------
# Material written by hand.

# The fundamentum: BWV 988's ground (G F# E D B C D G) in F-sharp major.  It is written out
# literally in every statement below, transposed with the key plan.
GROUND = 'F# E# D# C# A# B C# F#'

# The fugue subject: the ground itself in dotted diminution (bar 1: F# E# D# C# A# B, and the first
# two notes of bar 2: C# F#), then a springing tail that climbs back and stops on the supertonic.
SUBJ_BARS = ['F#4:3 E#4:1 D#4:3 C#4:1 A#3:3 B3:1', 'C#4:2 F#4:2 E#4:1 G#4:1 C#5:2 B4:1 A#4:1 G#4:2']
SUBJECT = ' '.join(SUBJ_BARS)
# Its tonal mutation for entries on the mediant: one note of the tail (the fourth of bar 2) is a step
# higher, so that the leap G#-C# does not become the tritone B-E# when the subject starts on A#.
SUBJ_MUT_BARS = [SUBJ_BARS[0], 'C#4:2 F#4:2 E#4:1 A#4:1 C#5:2 B4:1 A#4:1 G#4:2']


def subj(steps=0, key='F#', semis=0, letters=0):
    """The subject's two bars: diatonic shift in F#, then (optionally) chromatic move to a key."""
    bars = [shift(b, steps) for b in SUBJ_BARS]
    if semis or letters:
        bars = [tr(b, semis, letters) for b in bars]
    return bars


VOICES = [  # key, name, abbr, clef, base velocity
    ('S', 'Soprano', 'S.', 'treble', 68),
    ('A', 'Alto', 'A.', 'treble', 66),
    ('T', 'Tenor', 'T.', 'treble_8', 66),
    ('B', 'Bass', 'B.', 'bass', 70),
]
KEYS = [v[0] for v in VOICES]
NAME = {v[0]: v[1] for v in VOICES}

LINES = {k: {} for k in KEYS}      # LINES[voice][bar] = literal bar string (12 sixteenths)
CANONS = []                        # see canon()
ENTRIES = []                       # (voice, bar, beat offset in quarters, label, n bars[, form])


def put(v, bar, bars):
    for k, s in enumerate(bars):
        if bar + k in LINES[v]:
            raise ValueError(f'{v}: bar {bar + k} written twice')
        if dur16(s) != BAR:
            raise ValueError(f'{v} bar {bar + k}: {dur16(s)} sixteenths: {s}')
        LINES[v][bar + k] = s


def entry(v, bar, label, beat=0, n=2, form=None):
    ENTRIES.append((v, bar, beat, label, n) + ((form,) if form else ()))


def canon(name, dux, comes, f, delay, first, last, label, ficta=()):
    """A strict canon: dux bars first..last are copied into the comes `delay` bars later through the
    transform f (and nothing else).  ficta: explicit [(comes bar, old note, new note)] accidentals
    of the minor mode (letters and rhythm stay strict); listed in NOTES.md and checked by
    check_canons.py."""
    CANONS.append(dict(name=name, dux=dux, comes=comes, f=f, delay=delay, first=first, last=last,
                       label=label, ficta=list(ficta)))


def comes_bars(c):
    out = {}
    for b in range(c['first'], c['last'] + 1):
        s = LINES[c['dux']][b]
        if b == c['last']:
            s = s.replace('~', '')
        out[b + c['delay']] = c['f'](s)
    for b, old, new in c['ficta']:
        toks = out[b].split()
        hit = [i for i, t in enumerate(toks) if t.rsplit(':', 1)[0] == old]
        if not hit:
            raise ValueError(f"ficta {old}->{new} not found in comes bar {b}: {out[b]}")
        for i in hit:
            toks[i] = new + ':' + toks[i].rsplit(':', 1)[1]
        out[b] = ' '.join(toks)
    return out


# =============================================================================================
# Intonazione (bars 1-2): the bass alone states the subject.
put('B', 1, [shift(b, -7) for b in SUBJ_BARS])
entry('B', 1, 'Subject (bass alone)')

# =============================================================================================
# Statement 1 (bars 3-10), F-sharp major: Canon I at the unison, two bars apart.
# Dux soprano (subject on F#4), comes alto at the same pitch; the dux's continuation is in
# triplets (Var. 3's lilt) and begins with a rest, so that the comes enters alone.
put('B', 3, ['F#3:12', 'E#3:12', 'D#3:12', 'C#3:12', 'A#2:12', 'B2:12', 'C#3:12', 'F#2:12'])
put('S', 3, SUBJ_BARS + [
    'R:4 C#5:8/3 B4:4/3 A#4:8/3 C#5:4/3',                        # b5  vi   (I6 in the comes)
    'E#5:8/3 D#5:4/3 E#5:8/3 F#5:4/3 G#5:8/3 F#5:4/3',           # b6  V    (V4/2 in the comes)
    'F#5:4 A#5:6 G#5:2',                                         # b7  I6   free from here
    'G#5:8 A#5:4',                                               # b8  V4/2
    'G#5:6 F#5:2 E#5:4',                                         # b9  V7
    'F#5:2 R:10',                                                # b10 I
])
canon('I', 'S', 'A', lambda s: s, 2, 3, 6, 'Canon I at the unison')
entry('S', 3, 'Canon I dux: subject')
entry('A', 5, 'Canon I comes: subject at the unison')
put('A', 9, ['E#5:4 R:8'])
# The tenor's first entry: the subject inverted (mirror F#<->C#), on C#4 over V7 - I; it ends on
# B3, the tonic of the next statement.
INV_BARS = [mirror(b, 'F#4', 'C#4') for b in SUBJ_BARS]      # C#4 D#4 E#4 F#4 A#4 G#4 | ...
put('T', 9, INV_BARS)
entry('T', 9, 'Tenor: subject inverted (on C#)', form='inversus')

# =============================================================================================
# Statement 2 (bars 11-18), B major: Canon II at the second below, one bar apart.
# Dux soprano (subject on C#5, over V6), comes alto (on B4, over vi); Var. 6's flowing quavers.
put('B', 11, ['B2:12', 'A#2:12', 'G#2:8 D#3:4', 'F#2:12', 'D#2:12', 'E2:12', 'F#2:12', 'B1:12'])
put('T', 11, [
    'B3:2 D#4:2 F#4:6 E4:2~',                                    # b11 I    (alone with the bass)
    'E4:4 C#4:4 A#3:2 C#4:2',                                    # b12 V6/5 (under the dux)
    'B3:4 R:8',                                                  # b13 vi   (makes room for the comes)
    'R:12', 'R:12', 'R:12',                                      # b14-16
    'A#3:4 F#3:4 A#3:4',                                         # b17 V7
    'B3:4 R:8',                                                  # b18 I
])
put('S', 12, [shift(tr(b, 5, 3), 1, 'B') for b in SUBJ_BARS] + [
    'C#5:4 E5:2 D#5:2 C#5:2 E5:2',                               # b14 V    (I6 in the comes)
    'D#5:2 E5:2 F#5:8',                                          # b15 I6   (IV)
    'E5:4 G#5:2 A#5:2 B5:4~',                                    # b16 IV   free from here
    'B5:4 A#5:2 G#5:2 F#5:2 E5:2',                               # b17 V7   (4-3)
    'D#5:4 R:8',                                                 # b18 I
])
canon('II', 'S', 'A', lambda s: shift(s, -1, 'B'), 1, 12, 15, 'Canon II at the second below')
entry('S', 12, 'Canon II dux: subject on C#')
entry('A', 13, 'Canon II comes: subject a second below, on B')
put('A', 17, ['C#5:4 E5:4 C#5:4', 'B4:4 R:8'])


# =============================================================================================
# Statement 3 (bars 19-26), G-sharp minor: Canon III at the third below, two bars apart.
# The ground in the minor descends through the natural seventh (G# F# E D#: the lament tetrachord,
# i - v6 - VI - V).  A trio: dux soprano (subject on B4, the mediant), comes alto (on G#4, over VI);
# the tenor rests.  The dux breathes as the comes enters; then a sigh.
put('B', 19, ['G#2:12', 'F#2:12', 'E2:12', 'D#2:12', 'B1:12', 'C#2:12', 'D#2:12', 'G#2:12'])
put('S', 19, [tr(b, 5, 3) for b in SUBJ_BARS] + [
    'R:4 B4:2 A#4:2 G#4:2 A#4:2',                                # b21 VI   (i6 in the comes)
    'D#5:4 R:8',                                                 # b22 V    (iv7)
    'B5:6 A#5:2 G#5:2 F#5:2',                                    # b23 i6   free from here
    'E5:4 G#5:4 B5:4',                                           # b24 iv7
    'A#5:4 F##5:4 D#5:2 C#5:2',                                  # b25 V7
    'B#4:12',                                                    # b26 I    (Picardy third)
])
canon('III', 'S', 'A', lambda s: shift(s, -2, 'G#m'), 2, 19, 22, 'Canon III at the third below',
      ficta=[(22, 'F#4', 'F##4')])
entry('S', 19, 'Canon III dux: subject on B (mediant)')
entry('A', 21, 'Canon III comes: subject a third below, on G#')
put('A', 25, ['A#4:6 B4:2 A#4:2 F##4:2', 'G#4:12'])

# =============================================================================================
# Statement 4 (bars 27-34), C-sharp major: Canon IV at the fourth below, by inversion, one bar
# apart (the tonal mirror C#<->G#, as in Var. 12).  The alto announces the subject (on E#), then the
# dux enters on top, the comes a bar later in the tenor, rising where the dux falls.
put('B', 27, ['C#3:12', 'B#2:12', 'A#2:12', 'G#2:4 R:8', 'E#2:4 C#2:8', 'F#2:12', 'G#2:12', 'C#2:12'])
put('A', 27, [shift(tr(b, -5, -3), 2, 'C#') for b in SUBJ_MUT_BARS] + [
    'E#4:4 C#4:4 R:4',                                           # b29 vi   (makes room)
])
entry('A', 27, 'Alto: subject on E# (C# major)')
put('S', 29, [tr(b, 7, 4) for b in SUBJ_BARS] + [
    'G#4:10 F#4:1 G#4:1',                                        # b31 I6-I (IV in the comes)
    'A#4:2 B#4:2 C#5:4 A#4:4',                                   # b32 IV   (V7)
    'B#4:4 A#4:2 G#4:2 A#4:2 G#4:2',                             # b33 V7   (I)
])
canon('IV', 'S', 'T', lambda s: mirror(s, 'C#5', 'G#3', 'C#'), 1, 29, 33,
      'Canon IV at the fourth below, by inversion')
entry('S', 29, 'Canon IV dux: subject on C#')
entry('T', 30, 'Canon IV comes: subject inverted, on G# (a fourth below)', form='inversus')


# =============================================================================================
# Link (bars 35-38): the bass's own entry, the subject on C# (the dominant of F#), then a dominant
# pedal with the head in stretto above it - the retransition.
put('B', 35, ['C#3:3 B2:1 A#2:3 G#2:1 E#2:3 F#2:1', 'G#2:2 C#3:2 B2:1 D#3:1 G#3:2 F#3:1 E#3:1 D#3:2',
              'C#3:12', 'C#3:12'])
entry('B', 35, 'Bass: subject on C# (retransition)')
put('S', 34, ['R:12',
              'E#5:4 F#5:4 G#5:4',                               # b35 V - I6 - V6/5
              'B5:4 G#5:4 A#5:2 B5:2',                           # b36 ii - ii6 - I
              'G#5:3 F#5:1 E#5:3 D#5:1 B4:3 C#5:1',              # b37 head on G#, over the pedal
              'B4:4 C#5:4 E#5:4'])                               # b38 V7
put('A', 34, ['R:12',
              'C#5:4 C#5:4 B4:4',                                # b35
              'G#4:4 D#5:4 A#4:4',                               # b36
              'R:4 B4:3 A#4:1 G#4:3 F#4:1',                      # b37 head on B, a beat later
              'D#4:3 E#4:1 R:8'])                                # b38
put('T', 35, ['R:12', 'R:12',
              'R:8 E#4:3 D#4:1',                                 # b37 head on E#, a beat later still
              'C#4:3 B3:1 G#3:3 A#3:1 R:4'])                     # b38

# =============================================================================================
# Statement 5 (bars 39-46), F-sharp major, the return: Canon V at the fifth below, by inversion,
# two bars apart.  The dux (alto) brings the subject back in the tonic, on A#; the comes (tenor)
# answers with the inversion on D# (mirror A#<->D#, F# fixed).
put('B', 39, ['F#2:4 F#3:8', 'E#3:12', 'D#3:12', 'C#3:12', 'A#2:12', 'B2:12', 'C#3:12', 'F#3:12'])
put('A', 39, [shift(b, 2) for b in SUBJ_BARS] + [
    'F#4:2 A#4:2 F#5:4 D#5:4',                                   # b41 vi   (I6 in the comes)
    'E#5:2 D#5:2 C#5:2 B4:2 C#5:4',                              # b42 V    (ii6)
    'C#5:10 D#5:1 C#5:1',                                        # b43 I6   (V7)
    'B4:4 F#4:4 D#4:2 R:2',                                      # b44 IV   (I)
    'G#4:4 C#5:8',                                               # b45 V7   free
    'A#4:4 R:8',                                                 # b46 I
])
canon('V', 'A', 'T', lambda s: mirror(s, 'A#4', 'D#4'), 2, 39, 44,
      'Canon V at the fifth below, by inversion')
entry('A', 39, 'Canon V dux: subject on A# (the return)')
entry('T', 41, 'Canon V comes: subject inverted, on D# (a fifth below)', form='inversus')
put('S', 39, [
    'F#5:12',                                                    # b39 I
    'G#5:6 F#5:2 E#5:4',                                         # b40 V6
    'F#5:4 A#5:8',                                               # b41 vi
    'B5:6 G#5:2 E#5:4',                                          # b42 V
    'F#5:4 A#5:8',                                               # b43 I6
    'F#5:4 G#5:4 A#5:2 G#5:2',                                   # b44 IV
    'E#5:6 F#5:2 G#5:4',                                         # b45 V7
    'F#5:12',                                                    # b46 I
])


# =============================================================================================
# Statement 6 (bars 47-54), F-sharp minor, Adagio: Canon VI at the sixth above, two bars apart
# (the Goldberg set's minor variations, 15, 21 and 25, are in the tonic minor).  The ground descends
# through the lament tetrachord F# E D C#.  Dux alto (subject on A, the mediant), comes soprano a
# sixth higher (on F#); after the subject the dux only holds long notes, so the comes sings alone
# above it.  The tenor is a free low line.  The last bar turns to F-sharp major and the tenor's
# upbeat starts the quodlibet.
put('B', 47, ['F#3:12', 'E3:8 C#3:4', 'D3:12', 'C#3:12', 'A2:12', 'B2:12', 'C#3:12', 'F#2:12'])
put('A', 47, [shift(modal(b, 'F#', 'F#m'), 2, 'F#m') for b in SUBJ_BARS] + [
    'A4:8 R:4',                                                  # b49 VI   (i6 in the comes)
    'R:2 C#5:10',                                                # b50 V    (iv7)
    'C#5:6 B4:2 A4:4',                                           # b51 i6   free from here
    'D5:6 C#5:2 B4:4',                                           # b52 iv7
    'B4:12',                                                     # b53 V7
    'A#4:6 R:6',                                                 # b54 I    (Picardy third)
])
canon('VI', 'A', 'S', lambda s: shift(s, 5, 'F#m'), 2, 47, 50, 'Canon VI at the sixth above',
      ficta=[(50, 'E5', 'E#5')])
entry('A', 47, 'Canon VI dux: subject on A (F-sharp minor)')
entry('S', 49, 'Canon VI comes: subject a sixth above, on F#')
put('S', 53, ['G#5:6 F#5:2 E#5:4', 'F#5:6 R:6'])
put('T', 47, [
    'R:12',                                                      # b47 i
    'R:4 B3:8',                                                  # b48 v7
    'F#3:12',                                                    # b49 VI
    'E#3:8 G#3:4',                                               # b50 V
    'A3:6 G#3:2 F#3:4',                                          # b51 i6
    'D3:4 F#3:4 B3:4',                                           # b52 iv7
    'G#3:4 E#3:4 G#3:4',                                         # b53 V7
    'F#3:6 R:3 C#3:3',                                           # b54 I    (upbeat of "Ich bin")
])


# =============================================================================================
# Statement 7 (bars 55-62), F-sharp major: Quodlibet, after Var. 30 of BWV 988.
# Bach's two folk songs, in his rhythm stretched 3:2 (his 4/4 bar carries two ground notes, ours
# one: his quaver becomes a dotted quaver, so the tunes swing in 6/8 against the 3/4 ground):
#   "Ich bin so lang nicht bei dir g'west" - tenor, from the upbeat, and in canon at the octave above
#      in the alto two bars (one of Bach's bars) later, as Bach's tenor and soprano have it;
#   "Kraut und Ruben haben mich vertrieben" - its first phrase in the soprano (Bach's soprano,
#      bars 3-4, over the same four ground notes), its second phrase (Bach's tenor, bars 7-8) in
#      the bass, which here leaves the ground: three of its four downbeats are the ground's notes.
# The fugue subject joins them at the start, in the soprano over "Ich bin".
ICH = ['F#3:3 G#3:3 A#3:3 B3:3', 'C#4:3 B3:3/2 A#3:3/2 G#3:3 F#3:3/2 G#3:3/2',
       'A#3:3 G#3:3 F#3:6~', 'F#3:6 E#3:3 D#3:3/2 E#3:3/2']
KRAUT1 = ['C#5:6 C#5:6', 'D#5:6 D#5:6', 'C#5:3 D#5:3 C#5:3 B4:3', 'A#4:3 G#4:3 F#4:6']
KRAUT2 = ['A#2:3 B2:3 C#3:3 A#2:3', 'B2:3 A#2:3 G#2:3 F#2:3', 'E#2:3 F#2:3 G#2:3 E#2:3', 'F#2:12~']
put('B', 55, ['F#2:12', 'E#2:4 C#3:4 A#2:4', 'D#3:12', 'C#3:12'] + KRAUT2 + ['F#2:12'])
entry('B', 59, 'Quodlibet: Kraut und Ruben, second phrase (the ground becomes the tune)', n=4)
put('T', 55, ICH + [
    'F#3:6 R:6',                                                 # b59 the tune's last note
    'R:12',                                                      # b60
    'C#4:6 G#3:6',                                               # b61 V
    'A#3:12~', 'A#3:12',                                         # b62-63 I
])
entry('T', 54, "Quodlibet: Ich bin so lang nicht bei dir g'west", beat=Fr(9, 4), n=5)
put('A', 56, ['R:9 C#4:3'])                                    # the follower's upbeat (= T's b54)
canon('8ve', 'T', 'A', lambda s: shift(s, 7), 2, 55, 58, "Ich bin so lang, in canon at the octave")
entry('A', 56, "Ich bin so lang, canon at the octave above", beat=Fr(9, 4), n=5)
put('A', 61, ['F#4:6 E#4:3 G#4:3', 'F#4:3 D#4:3 C#4:6~', 'C#4:12'])     # b61 the follower's last note as a 9-8
put('S', 55, [shift(b, 7) for b in SUBJ_BARS] + ['R:12', 'R:12'] + KRAUT1[:3]
    + ['A#4:3 G#4:3 F#4:6~', 'F#4:12'])                          # b62-63: the tune ends on the tonic
entry('S', 55, 'Quodlibet: the subject over Ich bin')
entry('S', 59, 'Quodlibet: Kraut und Ruben, first phrase', n=4)


# =============================================================================================
# Assembly

def all_lines():
    lines = {k: dict(LINES[k]) for k in KEYS}
    for c in CANONS:
        for b, s in comes_bars(c).items():
            if b in lines[c['comes']]:
                raise ValueError(f"{c['comes']}: bar {b} both written and copied")
            lines[c['comes']][b] = s
    return lines


def build(path=None):
    lines = all_lines()
    nbars = max(max(v) for v in lines.values() if v)
    bars = {}
    for k in KEYS:
        seq = []
        for b in range(1, nbars + 1):
            s = lines[k].get(b, f'R:{BAR}')
            if dur16(s) != BAR:
                raise ValueError(f'{k} bar {b}: {dur16(s)} sixteenths: {s}')
            seq.append(s)
        bars[NAME[k]] = seq
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XIII in F-sharp major (a 4): Fuga canonica sopra il fondamento di Goldberg',
            'composer': 'Claude / Sam (ground and folk songs after J. S. Bach, BWV 988)',
            'instrument': 'Keyboard (four voices)',
            'key': 'F#', 'mode': 'major', 'meter': list(METER), 'bpm': BPM,
            # gentler in G# minor (b19), brisker in C# (b27), broadening over the dominant pedal into
            # the return (b37-38), a breath before the Adagio in F# minor (b47), the quodlibet a
            # tempo (b55) and a final ritardando
            'tempo_map': [[52, 72], [54, 64, 'ramp'], [78, 74], [108, 74], [114, 58, 'ramp'],
                          [114, 72], [133, 72], [138, 56, 'ramp'], [138, 52], [156, 52],
                          [162, 42, 'ramp'], [162, 76], [180, 76], [186, 50, 'ramp'], [189, 40, 'ramp']],
            'tempo_text': 'Allegretto; Adagio in F-sharp minor; Quodlibet',
            'movement_number': 13, 'piece_type': 'fugue', 'edition': 'third',
            'score_tagline': 'Third edition - Fugue XIII (see NOTES.md)',
            'markers': [{'t': float((b - 1) * 3), 'label': txt} for b, txt in MARKS]}
    voices = [(n, a, c, v) for k, n, a, c, v in VOICES]
    ents = [(NAME[e[0]],) + tuple(e[1:]) for e in ENTRIES]
    data = W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=ents,
                         subject=SUBJECT, dynamics=dynamics)
    pans = {'Soprano': 74, 'Alto': 66, 'Tenor': 60, 'Bass': 54}
    for v in data['voices']:
        v['piano_pan'] = pans[v['name']]
    (path or HERE / 'fugue.json').write_text(__import__('json').dumps(data, indent=1))
    return data


MARKS = [(1, 'Intonazione: the subject in the bass'), (3, 'Canon I at the unison (F#)'),
         (11, 'Canon II at the second (B)'), (19, 'Canon III at the third (G# minor)'),
         (27, 'Canon IV at the fourth, by inversion (C#)'), (35, 'Bass entry, dominant pedal'),
         (39, 'Return: Canon V at the fifth, by inversion (F#)'),
         (47, 'Canon VI at the sixth (F# minor, Adagio)'), (55, 'Quodlibet (after Var. 30)')]

# Phrase dynamics: velocity offset from each listed bar on.
LEVEL = {1: 0, 3: -2, 5: 0, 9: 2, 11: 0, 12: 2, 15: 4, 17: 5, 18: 2, 19: -4, 21: -3, 23: -1,
         25: 0, 26: -2, 27: 2, 29: 4, 31: 5, 33: 4, 35: 6, 37: 8, 38: 9, 39: 10, 41: 9, 43: 8,
         45: 6, 46: 4, 47: -6, 49: -5, 51: -4, 53: -5, 54: -6, 55: 3, 57: 4, 59: 6, 61: 5, 62: 3}


def dynamics(b):
    """Bar index (0-based) -> velocity offset."""
    v = 0
    for k in sorted(LEVEL):
        if k <= b + 1:
            v = LEVEL[k]
    return v


if __name__ == '__main__':
    build()
    print('built', HERE / 'fugue.json')
