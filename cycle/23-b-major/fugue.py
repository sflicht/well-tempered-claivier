#!/usr/bin/env python3
"""Fugue XXIII in B major, five voices (Bach + 1):
"Fantasia ut re mi fa sol la per tutti i tuoni".

After John Bull's keyboard fantasia "Ut, re, mi, fa, sol, la" (Fitzwilliam Virginal Book
no. LI), in which the hexachord, held in long notes, is moved up a whole tone at a time until it
has stood on all twelve pitch levels.  Bull's order, transposed so that home is B:

    B | C# Eb F G A | (Bull's leap of a minor third) C D E F# Ab Bb | B

Four voices (soprano, alto, tenor, bass) make a fugue in B major on a subject that begins with
the hexachord in quick notes.  The fifth voice, the Cantus, enters after the exposition and carries
the hexachord through Bull's thirteen statements in semibreves, alternately rising (ut..la) and
falling (la..ut), so that every joint between two statements is a single step except Bull's leap
(A -> C) and the last joint, the semitone B-flat -> B that brings the circle home.  The fugue
follows the cantus into each key.

Every note is written in this file.  Thematic statements are explicit transforms of the
hand-written material below (`key` = transposition into a key, `oct` = octave shift); the cantus
statements are `hex_up` / `hex_dn` (the hexachord transposed and set in semibreves).  All other
lines are literal token strings placed at bar.beat positions.  No code chooses pitches.

Build:  python3 cycle/23-b-major/fugue.py   -> fugue.json
"""
from __future__ import annotations

import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
NAMES = ['S', 'A', 'C', 'T', 'B']
LONG = ['Soprano', 'Alto', 'Cantus (ut re mi fa sol la)', 'Tenor', 'Bass']
ABBR = ['S.', 'A.', 'Cant.', 'T.', 'B.']
CLEF = ['treble', 'treble', 'treble', 'treble_8', 'bass']
BASEVEL = [66, 64, 72, 64, 66]

# ------------------------------------------------------------------ material (written in B)
# Subject: Bull's hexachord in miniature.  The head rises ut-re-mi-fa-sol-la (ut held, re mi in
# sixteenths, fa sol in eighths, la); the tail falls back through it in a virginalist division
# (sol fa mi fa | re mi ut re), turns on the leading note and drops to the dominant.
# Harmony: I (beats 1-2), IV (beats 3-4) | V.
SUBJ = "B4:6 C#5:1 D#5:1 E5:2 F#5:2 G#5:4 F#5:1 E5:1 D#5:1 E5:1 C#5:1 D#5:1 B4:1 C#5:1 A#4:2 B4:2 F#4:4"
# Countersubject (above the subject): after a beat's rest, broken thirds in sixteenths, a held
# G#, a run into a syncopated B tied over the barline (a 4-3 suspension against the dominant),
# then a division falling to the leading note.  Invertible at the octave (5-6 instead of 4-3).
CS = "R:4 D#5:1 F#5:1 E5:1 G#5:4 A#5:1 B5:4~ B5:4 A#5:4 F#5:1 E5:1 D#5:1 C#5:1 E5:1 D#5:1 C#5:1 A#4:1"

# Inversion: the diatonic mirror of the subject around the axis between mi and fa (B<->G#,
# C#<->F#, D#<->E).  Its head falls la-sol-fa-mi-re-ut; harmony vi | V.
INV = "G#5:6 F#5:1 E5:1 D#5:2 C#5:2 B4:4 C#5:1 D#5:1 E5:1 D#5:1 F#5:1 E5:1 G#5:1 F#5:1 A#5:2 G#5:2 C#6:4"

# CSI: the countersubject mirrored on the same axis; it lies below the inversion.  Its tied G#
# resolves upward (a retardation), the mirror of the countersubject's 4-3.
CSI = "R:4 E5:1 C#5:1 D#5:1 B4:4 A#4:1 G#4:4~ G#4:4 A#4:4 C#5:1 D#5:1 E5:1 F#5:1 D#5:1 E5:1 F#5:1 A#5:1"

HEX_UP = "B3:16 C#4:16 D#4:16 E4:16 F#4:16 G#4:16"
HEX_DN = "G#4:16 F#4:16 E4:16 D#4:16 C#4:16 B3:16"

LETTERS = 'CDEFGAB'


def pitch(name):
    return W.parse_tok(name + ':1')[0]


def letter_index(name):
    m = re.fullmatch(r'([A-G])(#{0,2}|b{0,2})(-?\d+)', name)
    return 7 * int(m.group(3)) + LETTERS.index(m.group(1))


def key(s, src, dst):
    """Transpose material whose reference note is `src` (e.g. 'B4') so that it falls on `dst`
    (e.g. 'Eb4'): an explicit chromatic + letter transposition."""
    return W.transpose(s, pitch(dst) - pitch(src), letter_index(dst) - letter_index(src))


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def _breath(s, last):
    """Shorten the statement's last semibreve to `last` sixteenths (the cantus breathes)."""
    toks = s.split()
    if last < 16:
        toks[-1] = toks[-1].rsplit(':', 1)[0] + f':{last} R:{16 - last}'
    return ' '.join(toks)


def hex_up(ut, last=16):
    return _breath(key(HEX_UP, 'B3', ut), last)


def hex_dn(la, last=16):
    return _breath(key(HEX_DN, 'G#4', la), last)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


# ------------------------------------------------------------------ placement
class Score:
    """Literal segments placed at bar.beat (bar 1-based, beat 1-based quarters)."""

    def __init__(self):
        self.segs = {n: [] for n in NAMES}
        self.entries = []     # (voice, bar, beat_offset_quarters, label, nbars)
        self.marks = []

    @staticmethod
    def pos(bar, beat):
        return Fr(bar - 1) * 16 + (Fr(beat) - 1) * 4

    def put(self, v, bar, beat, toks):
        self.segs[v].append((self.pos(bar, beat), ' '.join(toks.split())))

    def theme(self, v, bar, beat, toks, label, nbars=2):
        self.put(v, bar, beat, toks)
        self.entries.append((v, bar, Fr(beat) - 1, label, nbars))

    def mark(self, bar, text):
        self.marks.append((bar, text))

    def bars(self, nbars):
        out = {}
        for v in NAMES:
            segs = sorted(self.segs[v], key=lambda x: x[0])
            cur, toks = Fr(0), []
            for s, t in segs:
                if s < cur:
                    raise ValueError(f'{v}: overlap at bar {1 + s / 16} ({t[:40]})')
                if s > cur:
                    toks.append(f'R:{s - cur}')
                toks.append(t)
                cur = s + dur16(t)
            if cur > nbars * 16:
                raise ValueError(f'{v}: runs past bar {nbars}')
            if cur < nbars * 16:
                toks.append(f'R:{nbars * 16 - cur}')
            out[v] = W.concat_bars(' '.join(toks), METER)
        return out


sc = Score()

# ===================================================================== EXPOSITION (bars 1-8)
# Fugue a 4 in B, without the cantus.  Real answer: the subject on the dominant, whose head is the
# hexachord on sol (Guido's "hard" hexachord).
sc.mark(1, 'Exposition a 4')
sc.theme('T', 1, 1, octv(SUBJ, -1), 'Subject (B), tenor')
sc.theme('A', 3, 1, key(SUBJ, 'B4', 'F#4'), 'Answer (F#), alto')
sc.put('T', 3, 1, 'R:4 A#3:1 C#4:1 B3:1 D#4:4 E#4:1 F#4:4~ '               # CS below, in F#
                  'F#4:4 E#4:4 C#4:1 B3:1 A#3:1 G#3:1 A#3:1 G#3:1 F#3:1 E3:1')
sc.theme('S', 5, 1, SUBJ, 'Subject (B), soprano')
sc.put('A', 5, 1, octv(CS, -1) + '~')                                       # CS below (A#3 held into b7)
sc.put('A', 7, 1, 'A#3:4 C#4:4 D#4:4 B3:4 '
                  'C#4:8 B3:4 C#4:4')
sc.put('T', 5, 1, 'D#3:2 C#3:2 B2:2 A#2:2 G#2:2 E3:2 C#3:2 E3:2 '
                  'F#3:6 E3:2 C#3:2 F#2:2 A#2:2 C#3:2')
sc.theme('B', 7, 1, key(SUBJ, 'B4', 'F#2'), 'Answer (F#), bass')
sc.put('S', 7, 1, 'R:4 A#4:1 C#5:1 B4:1 D#5:4 E#5:1 F#5:4~ '               # CS above, in F#
                  'F#5:4 E#5:4 C#5:1 B4:1 A#4:1 G#4:1 A#4:2 R:2')
sc.put('T', 8, 3, 'G#3:4 E3:4')

# ===================================================================== I. B (bars 9-14), rising
# The fifth voice enters: ut-re-mi-fa-sol-la on B in semibreves.  The subject starts with it, on
# the same note: its head is the cantus in quick notes.  At the cantus's sol the subject enters on
# F# (the "hard" hexachord), whose dominant, C#, is the next key.
sc.mark(9, 'Cantus enters: B (rising)')
sc.theme('C', 9, 1, hex_up('B3'), 'Cantus: B, ut-re-mi-fa-sol-la (rising)', 6)
sc.theme('S', 9, 1, SUBJ, 'Subject (B) over the cantus, soprano')
sc.put('A', 9, 1, 'R:4 D#4:1 F#4:1 E4:1 G#4:4 A#4:1 B4:4~ B4:4 A#4:4 F#4:4')      # CS (low), cut short
sc.put('B', 9, 1, 'B1:2 B2:2 G#2:4 E3:2 D#3:2 B2:4 '
                  'F#3:6 E3:1 D#3:1 C#3:4 E3:4 '
                  'D#3:2 C#3:2 B2:4 B2:2 A#2:2 B2:2 G#2:2 '
                  'E3:2 F#3:2 G#3:2 E3:2 C#3:2 D#3:2 E3:2 C#3:2')
# soprano: a division over b11-12 (I6 - vi | IV - ii7), then rests before the inversion
sc.put('S', 11, 1, 'B4:2 C#5:1 D#5:1 F#5:2 E5:2 D#5:2 B4:2 G#4:2 B4:2 '
                   'E5:1 F#5:1 G#5:1 F#5:1 E5:2 B4:2 C#5:2 E5:2 G#4:2 B4:2')
sc.theme('T', 13, 1, key(SUBJ, 'B4', 'F#3'), "Subject on the dominant (F#), tenor, at the cantus's sol")
sc.put('A', 13, 1, 'R:4 A#4:1 C#5:1 B4:1 D#5:4 E#5:1 F#5:4~ '                     # CS above, in F#
                   'F#5:4 E#5:4 C#5:1 B4:1 A#4:1 C#5:1 E#5:4')

# ===================================================================== II. C# (bars 15-20), falling
# The cantus falls la-sol-fa-mi-re-ut on C#; the subject falls with it (the inversion, la..ut).
sc.mark(15, 'C# (falling)')
sc.theme('C', 15, 1, hex_dn('A#4', last=12), 'Cantus: C#, la-sol-fa-mi-re-ut (falling)', 6)
sc.theme('S', 15, 1, key(INV, 'G#5', 'A#5'), 'Inversion (C#) over the falling cantus, soprano')
sc.put('B', 15, 1, 'A#1:2 B1:2 C#2:2 D#2:2 E#2:4 F#2:2 D#2:2 '
                   'G#1:2 A#1:2 B#1:2 G#1:2 D#2:2 E#2:2 F#2:2 D#2:2 '
                   'G#1:4 B#1:2 A#1:2 G#1:4 D#2:4 '
                   'C#2:2 D#2:2 E#2:2 D#2:2 C#2:2 B#1:2 A#1:2 R:2')
sc.theme('B', 19, 1, key(INV, 'G#5', 'D#3'), "Inversion (F#) in the bass, at the cantus's re")
sc.put('S', 17, 1, 'B#5:2 A#5:2 G#5:2 B#5:2 D#6:2 C#6:2 B#5:2 G#5:2 '
                   'C#6:2 B#5:1 A#5:1 G#5:2 C#6:2 A#5:2 G#5:1 F#5:1 E#5:2 C#5:2 '
                   'F#5:2 G#5:2 A#5:2 B5:2 F#5:2 E#5:2 C#5:2 A#4:2 '
                   'B#4:2 C#5:2 E#5:4 G#5:2 F#5:1 E#5:1 D#5:4')

# ===================================================================== III. E-flat (bars 21-26), rising
sc.mark(21, 'E-flat (rising)')
sc.theme('C', 21, 1, hex_up('Eb4'), 'Cantus: E-flat, ut-la (rising)', 6)
sc.theme('T', 21, 1, key(SUBJ, 'B4', 'Eb3'), 'Subject (E-flat), tenor, with the cantus')
sc.put('A', 21, 1, 'R:4 G4:1 Bb4:1 Ab4:1 C5:4 D5:1 Eb5:4~ '                     # CS above the cantus
                   'Eb5:4 D5:4 Bb4:1 Ab4:1 G4:1 Ab4:1 Bb4:1 C5:1 D5:1 Bb4:1 C5:4 R:12')
# episode b23-24: the soprano's first sixteenth division (Eb - Cm | Ab - Fm7), walking bass
sc.put('S', 23, 1, 'Eb5:1 F5:1 G5:1 Ab5:1 Bb5:1 Ab5:1 G5:1 F5:1 G5:1 Eb5:1 C5:1 Eb5:1 G5:1 Eb5:1 C5:1 Bb4:1 '
                   'C5:1 D5:1 Eb5:1 F5:1 G5:1 Ab5:1 Bb5:1 C6:1 Ab5:1 G5:1 F5:1 G5:1 Ab5:1 F5:1 Eb5:1 D5:1')
sc.put('B', 23, 1, 'Eb3:2 F3:2 G3:2 Eb3:2 C3:2 D3:2 Eb3:2 Bb2:2 '
                   'Ab2:4 C3:2 Ab2:2 F2:4 R:4')
sc.theme('B', 25, 1, key(SUBJ, 'B4', 'Bb2'), "Subject on the dominant (B-flat), bass, at the cantus's sol")
sc.put('S', 25, 1, 'R:4 D5:1 F5:1 Eb5:1 G5:4 A5:1 Bb5:4~ '                       # CS above, in B-flat
                   'Bb5:4 A5:4 F5:1 Eb5:1 D5:1 Eb5:1 F5:1 G5:1 A5:1 F5:1')

# ===================================================================== IV. F (bars 27-32), falling
sc.mark(27, 'F (falling)')
sc.theme('C', 27, 1, hex_dn('D5', last=12), 'Cantus: F, la-ut (falling)', 6)
sc.theme('T', 27, 1, key(INV, 'G#5', 'D4'), 'Inversion (F), tenor, with the falling cantus')
sc.put('B', 27, 1, octv(key(CSI, 'G#5', 'D4'), -1).rsplit(' ', 1)[0] + ' F3:1')   # CSI below; last note to F
sc.put('S', 27, 1, 'F5:6 G5:1 A5:1 Bb5:2 A5:2 G5:2 E5:2 '
                   'G5:4 E5:4 C6:4 Bb5:4~ '
                   'Bb5:4 C6:2 Bb5:2 G5:4 R:4')
# episode b29-30 (Bb - C7 | F - Dm): tenor and bass in dialogue
sc.put('T', 29, 1, 'D4:2 C4:1 Bb3:1 A3:2 Bb3:2 C4:2 Bb3:1 A3:1 G3:2 E3:2 '
                   'F3:2 G3:1 A3:1 C4:2 A3:2 D4:2 C4:1 Bb3:1 A3:2 C4:2')
sc.put('B', 29, 1, 'Bb2:2 D3:2 F3:2 D3:2 E3:2 C3:2 G2:2 C3:2 '
                   'A2:2 F2:2 C3:2 F2:2 D2:2 F2:2 E2:2 F2:2')
sc.theme('S', 31, 1, key(INV, 'G#5', 'G5'), "Inversion (B-flat), soprano, at the cantus's re")
sc.put('T', 31, 1, 'R:4 Eb4:1 C4:1 D4:1 Bb3:4 A3:1 G3:4~ '                      # CSI below, in B-flat
                   'G3:4 A3:4 C4:1 D4:1 Eb4:1 D4:1 C4:1 Bb3:1 A3:1 G3:1')
sc.put('B', 31, 1, 'G2:4 Bb2:2 A2:2 G2:2 A2:2 Bb2:2 C3:2 '
                   'F2:4 C3:2 Bb2:2 A2:4 R:4')

# ===================================================================== V. G (bars 33-38), rising
sc.mark(33, 'G (rising)')
sc.theme('C', 33, 1, hex_up('G4'), 'Cantus: G, ut-la (rising)', 6)
sc.theme('B', 33, 1, key(SUBJ, 'B4', 'G2'), 'Subject (G), bass, with the cantus')
sc.put('A', 33, 1, 'R:4 B4:1 D5:1 C5:1 E5:4 F#5:1 G5:4~ '                       # CS above
                   'G5:4 F#5:4 D5:1 C5:1 B4:1 C5:1 D5:1 E5:1 F#5:1 D5:1')
sc.put('T', 33, 1, 'R:4 D4:4 C4:4 B3:4 '
                   'C4:8 A3:4 C4:4')
# episode b35-36 (G/B - Em | C - Am7): the soprano returns with a division; the alto hands over
sc.put('S', 35, 1, 'G5:1 F#5:1 G5:1 A5:1 B5:2 G5:2 E5:1 F#5:1 G5:1 E5:1 G5:2 A5:2 '
                   'C6:2 B5:1 A5:1 G5:2 E5:2 A5:2 G5:1 F#5:1 E5:2 D5:2')
sc.put('A', 35, 1, 'G4:2 F#4:2 G4:2 A4:2 G4:4 E4:4 '
                   'E4:2 F#4:2 E4:4 R:8')
sc.put('T', 35, 1, 'D4:4 B3:4 G3:4 B3:4 '
                   'E4:4 C4:4 C4:4 A3:4')
sc.put('B', 35, 1, 'B2:2 A2:2 G2:2 B2:2 E2:2 F#2:2 E2:2 G2:2 '
                   'C3:2 E3:2 A2:2 G2:2 A2:2 B2:2 C3:2 A2:2')
sc.theme('A', 37, 1, key(SUBJ, 'B4', 'D4'), "Subject on the dominant (D), alto, at the cantus's sol")
sc.put('S', 37, 1, 'R:4 F#5:1 A5:1 G5:1 B5:4 C#6:1 D6:4~ '                      # CS above, in D
                   'D6:4 C#6:4 A5:1 G5:1 F#5:1 G5:1 A5:1 B5:1 C#6:1 A5:1')
sc.put('B', 37, 1, 'R:8 E2:2 A2:2 D3:2 C#3:2 '
                   'A2:4 C#3:2 A2:2 E2:4 A1:4')

# ===================================================================== VI. A (bars 39-44), falling
sc.mark(39, 'A (falling): the first staircase ends')
sc.theme('C', 39, 1, hex_dn('F#5', last=12), 'Cantus: A, la-ut (falling)', 6)
sc.theme('T', 39, 1, key(INV, 'G#5', 'F#3'), 'Inversion (A), tenor, with the falling cantus')
sc.put('B', 39, 1, key(CSI, 'G#5', 'F#3'))                                     # CSI below
sc.put('S', 39, 1, 'C#6:8 A5:8~ '
                   'A5:4 G#5:12 '
                   'F#5:4 A5:4 B5:6 A5:2 '
                   'A5:4 C#6:2 B5:2 A5:4 R:4')
# b41-42 (D - E7 | A/C# - F#m): the cantus's D is the seventh of E7 and falls to C#
sc.put('A', 41, 1, 'A4:2 B4:2 A4:2 F#4:2 E4:2 F#4:2 G#4:2 B4:2 '
                   'A4:2 G#4:2 A4:2 E4:2 F#4:2 G#4:2 A4:2 F#4:2 '
                   'D4:4 C#4:2 D4:2 B3:4 F#4:4 '
                   'C#4:4 E4:4 A3:4 R:4')
sc.put('B', 41, 1, 'D3:4 F#2:2 E2:2 G#2:4 B2:4 '
                   'C#3:2 D3:2 E3:2 C#3:2 A2:2 B2:2 F#2:2 A2:2 '
                   'B2:2 A2:2 B2:2 C#3:2 D3:2 C#3:2 D3:4 '
                   'A2:4 C#3:2 A2:2 E2:4 R:4')
sc.theme('S', 43, 1, key(INV, 'G#5', 'B5'), "Inversion (D), soprano, at the cantus's re")
sc.put('T', 43, 1, 'R:4 F#3:4 B3:4 F#3:4 '
                   'A3:4 E3:4 C#3:4 R:4')

# ===================================================================== Bull's leap; VII. C (bars 45-50), rising
# Where the next step would bring B back too soon, Bull leaps a minor third (F -> A-flat in his G
# tour; here A -> C).  The cantus drops a major sixth to C4 and the second staircase begins, quietly,
# with the subject in the deep bass and a new division in triplets (Bull's sesquialtera).
sc.mark(45, "Bull's leap: C (rising), the second staircase")
sc.theme('C', 45, 1, hex_up('C4'), "Cantus: C, ut-la (rising), after Bull's leap", 6)
sc.theme('B', 45, 1, key(SUBJ, 'B4', 'C2'), 'Subject (C), deep bass')
sc.put('A', 45, 1, 'R:4 E4:4/3 G4:4/3 C5:4/3 B4:4/3 C5:4/3 A4:4/3 F4:4/3 A4:4/3 B4:4/3 '
                   'D5:4/3 B4:4/3 G4:4/3 F4:4/3 G4:4/3 B4:4/3 D5:4/3 C5:4/3 B4:4/3 A4:4/3 G4:4/3 F4:4/3 '
                   'G4:4/3 C5:4/3 E5:4/3 D5:4/3 C5:4/3 B4:4/3 A4:4/3 C5:4/3 E5:4/3 D5:4/3 C5:4/3 A4:4/3 '
                   'A4:4/3 C5:4/3 F5:4/3 E5:4/3 D5:4/3 C5:4/3 B4:4/3 D5:4/3 F5:4/3 E5:4/3 D5:4/3 B4:4/3 '
                   )
sc.put('S', 47, 1, 'R:4 G5:4 C6:4 A5:4~ '
                   'A5:4 G5:2 F5:2 A5:4 C6:4 '
                   'B5:4 R:12')
sc.put('B', 47, 1, 'E2:2 F2:2 G2:2 E2:2 A2:2 B2:2 C3:2 A2:2 '
                   'F2:2 G2:2 A2:2 F2:2 D2:2 E2:2 D2:4')
sc.theme('T', 49, 1, key(SUBJ, 'B4', 'G3'), "Subject on the dominant (G), tenor, at the cantus's sol")
sc.put('A', 49, 1, 'R:4 B4:1 D5:1 C5:1 E5:4 F#5:1 G5:4~ '                       # CS above, in G
                   'G5:4 F#5:4 D5:1 C5:1 B4:1 C5:1 D5:1 E5:1 F#5:1 D5:1')

# ===================================================================== VIII. D (bars 51-56), falling
sc.mark(51, 'D (falling)')
sc.theme('C', 51, 1, hex_dn('B4', last=12), 'Cantus: D, la-ut (falling)', 6)
sc.theme('B', 51, 1, key(INV, 'G#5', 'B2'), 'Inversion (D), bass, with the falling cantus')

sc.put('S', 51, 1, 'R:4 F#5:4 D5:4 B5:4~ '
                   'B5:4 A5:4 E5:4 C#6:4 '
                   'B5:8 A5:4 E5:4 '
                   'F#5:4 A5:4 R:8')
sc.put('T', 51, 1, 'D4:2 C#4:2 B3:4 D4:4 F#3:2 A3:2 '
                   'E4:4 C#4:4 A3:2 G#3:2 A3:4')
# episode b53-54 (G - A7 | D - Bm - B7): the cantus's G is the seventh of A7 and falls to F#
sc.put('A', 53, 1, 'D5:2 C#5:2 B4:2 D5:2 C#5:2 B4:2 A4:2 E5:2 '
                   'D5:2 C#5:2 A4:2 B4:2 B4:2 C#5:2 A4:2 B4:2')
sc.put('B', 53, 1, 'G2:2 A2:2 B2:2 G2:2 E2:2 F#2:2 C#3:4 '
                   'D3:4 F#3:2 E3:2 B2:2 F#2:2 D#2:4 '
                   'E2:2 F#2:2 G2:2 A2:2 G2:2 F#2:2 B1:4 '
                   'D2:4 F#2:2 E2:2 D2:4 A1:4')
sc.theme('S', 55, 1, key(INV, 'G#5', 'E5'), "Inversion (G), soprano, at the cantus's re")
sc.put('T', 55, 1, 'B3:2 C4:2 B3:2 G3:2 B3:2 C4:2 B3:2 G3:2 '
                   'F#3:4 A3:4 F#3:4 R:4')
sc.put('A', 56, 4, 'C#5:4')

# ===================================================================== IX. E (bars 57-62), rising
sc.mark(57, 'E (rising)')
sc.theme('C', 57, 1, hex_up('E4'), 'Cantus: E, ut-la (rising)', 6)
sc.theme('T', 57, 1, key(SUBJ, 'B4', 'E3'), 'Subject (E), tenor, with the cantus')
sc.put('A', 57, 1, 'R:4 G#4:1 B4:1 A4:1 C#5:4 D#5:1 E5:4~ '                     # CS above the cantus
                   'E5:4 D#5:4 B4:1 A4:1 G#4:1 A4:1 B4:1 C#5:1 D#5:1 B4:1')
sc.put('B', 57, 4, 'E2:4 '
                   'B1:4 D#2:4 F#2:4 D#2:4')
# episode b59-60 (E/G# - C#m | A - F#m7), five voices
sc.put('S', 59, 1, 'B5:2 A5:1 G#5:1 E5:2 G#5:2 C#6:2 B5:1 A5:1 B5:2 E5:2 '
                   'A5:2 B5:1 C#6:1 E6:2 C#6:2 A5:2 G#5:1 F#5:1 E5:2 D#5:2')
sc.put('A', 59, 1, 'E5:4 B4:4 E5:4 C#5:4 '
                   'E5:4 C#5:12')
sc.put('T', 59, 1, 'B3:4 G#3:4 E4:4 G#3:4 '
                   'C#4:4 A3:4 A3:4 R:4')
sc.put('B', 59, 1, 'G#2:4 B2:2 A2:2 C#3:2 G#2:2 C#3:4 '
                   'A2:4 C#3:2 B2:2 F#2:4 R:4')
sc.theme('B', 61, 1, key(SUBJ, 'B4', 'B2'), "Subject on the dominant (B, home), bass, at the cantus's sol")
sc.put('S', 61, 1, 'R:4 D#5:1 F#5:1 E5:1 G#5:4 A#5:1 B5:4~ '                     # CS above, in B
                   'B5:4 A#5:4 F#5:1 E5:1 D#5:1 E5:1 F#5:1 G#5:1 A#5:1 F#5:1')

# ===================================================================== X. F# (bars 63-68), falling
sc.mark(63, 'F# (falling)')
sc.theme('C', 63, 1, hex_dn('D#5', last=12), 'Cantus: F#, la-ut (falling)', 6)
sc.theme('A', 63, 1, key(INV, 'G#5', 'D#4'), 'Inversion (F#), alto, with the falling cantus')
sc.put('B', 63, 1, 'D#2:2 E#2:2 F#2:2 G#2:2 A#2:2 B2:2 A#2:4 '
                   'C#2:2 D#2:2 E#2:2 F#2:2 G#2:2 F#2:2 E#2:2 C#2:2')
sc.put('S', 63, 1, 'F#5:8 C#6:8 '
                   'G#5:4 E#5:4 C#6:4 G#5:4')
# episode b65-66 (G#m7 - C#7 | F# - D#m): the cantus's B is the seventh of C#7 and falls to A#
sc.put('S', 65, 1, 'B5:6 A#5:2 G#5:4 C#6:4 '
                   'F#5:4 A#5:4 D#5:4 R:4')
sc.put('A', 65, 1, 'F#4:2 G#4:2 F#4:2 D#4:2 E#4:2 G#4:2 E#4:2 C#4:2 '
                   'C#5:4 F#4:4 F#4:4 D#4:4')
sc.put('T', 65, 1, 'R:4 D#4:4 G#3:8 '
                   'A#3:2 B3:2 C#4:2 A#3:2 F#3:4 A#3:2 F#3:2')
sc.put('B', 65, 1, 'G#1:4 B1:4 C#2:8 '
                   'F#2:2 E#2:2 D#2:2 E#2:2 D#2:2 C#2:2 D#2:4')
sc.theme('S', 67, 1, key(INV, 'G#5', 'G#5'), "Inversion (B, home), soprano, at the cantus's re")

sc.put('A', 67, 1, 'B3:4 D#4:4 D#4:4 B3:4 '
                   'A#3:4 C#4:4 C#4:4 E#4:4')
sc.put('B', 67, 1, 'G#1:4 B1:4 D#2:4 G#2:4 '
                   'F#2:4 A#1:4 C#2:8')

# ===================================================================== XI. A-flat (bars 69-74), rising: the wolf
# The cantus reaches A-flat = G#.  The first bar is a bare fifth A-flat / E-flat in every voice, a
# bagpipe drone: in Bach-Lehman a calm open fifth (700 cents), in quarter-comma meantone the wolf
# (G# - Eb, 737.6 cents).  Then the subject on B-flat (the next key, at the cantus's re), a turn to
# B-flat minor, and the subject on E-flat at the cantus's sol.
sc.mark(69, 'A-flat (rising): the wolf fifth')
sc.theme('C', 69, 1, hex_up('Ab4'), 'Cantus: A-flat, ut-la (rising)', 6)
sc.put('S', 69, 1, 'Eb5:12 Eb5:4')
sc.put('A', 69, 1, 'Ab3:12 G3:4')
sc.put('T', 69, 1, 'Eb3:12 R:4')
sc.put('B', 69, 1, 'Ab2:12 Eb2:4')
sc.theme('T', 70, 1, key(SUBJ, 'B4', 'Bb3'), "Subject (B-flat), tenor, at the cantus's re")
sc.put('S', 70, 1, 'R:4 D5:1 F5:1 Eb5:1 G5:4 A5:1 Bb5:4~ '                      # CS above
                   'Bb5:4 A5:4 F5:1 Eb5:1 D5:1 Eb5:1 F5:1 G5:1 A5:1 F5:1')
sc.put('A', 70, 1, 'F3:4 D4:4 Eb4:4 G4:4 '
                   'F4:4 A3:4 C4:4 Eb4:4')
sc.put('B', 70, 1, 'Bb1:4 D2:4 Eb2:4 C2:4 '
                   'F2:4 Eb2:4 D2:4 A1:4')
# b72: B-flat minor (the cantus's D-flat), the only minor tonic of the tour
sc.put('S', 72, 1, 'Db5:2 F5:1 Gb5:1 F5:2 Db5:2 Bb5:2 Ab5:1 G5:1 Ab5:2 F5:2')
sc.put('A', 72, 1, 'F4:2 Gb4:2 F4:2 Eb4:2 Db4:4 R:4')
sc.put('T', 72, 1, 'Bb3:4 Ab3:2 Gb3:2 F3:4 Bb3:4')
sc.put('B', 72, 1, 'Bb2:2 C3:2 Db3:2 Bb2:2 Gb2:4 F2:4')
sc.theme('A', 73, 1, key(SUBJ, 'B4', 'Eb4'), "Subject on the dominant (E-flat), alto, at the cantus's sol")
sc.put('S', 73, 1, 'R:4 G5:1 Bb5:1 Ab5:1 C6:4 D6:1 Eb6:4~ '                      # CS above, in E-flat
                   'Eb6:4 D6:4 Bb5:1 Ab5:1 G5:1 Ab5:1 Bb5:1 C6:1 D6:1 Bb5:1')
sc.put('T', 73, 1, 'G3:4 Bb3:4 Ab3:4 C4:4 '
                   'Bb3:4 F3:4 D3:4 R:4')
sc.put('B', 73, 1, 'Eb2:2 F2:2 G2:2 Eb2:2 Ab2:2 G2:2 F2:2 Ab2:2 '
                   'Bb2:4 D2:2 C2:2 Bb1:4 R:4')

NBARS = 74


def main():
    bars = sc.bars(NBARS)
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Fugue XXIII in B major, five voices: Fantasia ut re mi fa sol la per tutti i tuoni',
        'composer': 'Claude / Sam, after John Bull',
        'instrument': 'Keyboard - five voices (four-voice fugue and cantus)',
        'key': 'B', 'mode': 'major', 'meter': list(METER), 'bpm': 100,
        'tempo_text': 'Allegro moderato, alla fantasia',
        'movement_number': 23, 'piece_type': 'fugue', 'edition': 'third',
        'score_tagline': 'The Well-Tempered clAIvier - third edition',
        'voice_order': 'high_to_low',
        'markers': [{'t': float((b - 1) * 4), 'label': txt} for b, txt in sc.marks],
    }
    voices = [(LONG[i], ABBR[i], CLEF[i], BASEVEL[i]) for i in range(len(NAMES))]
    named = {LONG[i]: bars[NAMES[i]] for i in range(len(NAMES))}
    entries = [(LONG[NAMES.index(v)], b, off, lab, n) for v, b, off, lab, n in sc.entries]
    W.build_score(HERE / 'fugue.json', meta, voices, named, entries=entries, subject=SUBJ)
    print(f"wrote {HERE / 'fugue.json'}: {NBARS} bars")


if __name__ == '__main__':
    main()
