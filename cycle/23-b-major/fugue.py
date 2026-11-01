#!/usr/bin/env python3
"""Fugue XXIII in B major, five voices (Bach + 1):
"Fantasia ut re mi fa sol la per tutti i tuoni".

After John Bull's keyboard fantasia "Ut, re, mi, fa, sol, la" (Fitzwilliam Virginal Book
no. LI), in which the hexachord, held in long notes, is moved up a whole tone at a time until it
has stood on all twelve pitch levels.  Bull's order, transposed so that home is B:

    B | C# Eb F G A | (Bull's leap of a minor third) C D E F# Ab Bb | B

Four voices (soprano, alto, tenor, bass) make a fugue in B major on a subject whose head is the
hexachord in quick notes.  The fifth voice, the Cantus, enters after the exposition and carries
the hexachord through Bull's thirteen statements in semibreves (the twelfth, on B-flat, partly in
minims), alternately rising (ut..la) and
falling (la..ut), so that every joint between two statements is a single step except Bull's leap
(A -> C) and the last joint, the semitone B-flat (= A#) -> B that brings the circle home.  The
fugue follows the cantus into each key: over a rising statement the subject enters rectus (its
head is the cantus in quick notes); over a falling one it enters inverted (la..ut).

Form (89 bars, q = 100):
  1-8     exposition a 4 (tenor B, alto F#, soprano B, bass F#)
  9-14    cantus B rising; subject B (soprano) on its ut, subject F# (tenor) on its sol
  15-20   C# falling;  inversion C# (soprano) on la, inversion F# (bass) on re
  21-26   E-flat rising; subject Eb (tenor), episode, subject Bb (bass)
  27-32   F falling;   inversion F (tenor), episode, inversion Bb (soprano)
  33-38   G rising;    subject G (bass), episode a 5, subject D (alto)
  39-44   A falling;   inversion A (tenor), episode, inversion D (soprano): the first staircase ends
  45-50   Bull's leap: C rising, subject C in the deep bass, triplet division; subject G (tenor)
  51-56   D falling;   inversion D (bass), episode, a dotted division instead of a second entry
  57-62   E rising;    subject E (tenor), episode a 5, subject B (bass)
  63-68   F# falling;  inversion F# (alto), episode, inversion B (soprano)
  69-74   A-flat rising: a bare A-flat/E-flat drone (the meantone wolf), subject Bb, B-flat minor, subject Eb
  75-78   B-flat falling (the cantus on top), the one compressed statement: la-sol-fa-mi in minims
          over the bass's inversion (Bb), then re = C (Neapolitan of B) and ut = A# in F#7
  79-84   B rising, home: subject B (bass), subject E (tenor), inversion B (bass) under the cantus's la
  85-89   coda: the cantus falls home, sol fa mi re ut

Every note is written in this file.  Thematic statements are explicit transforms of the
hand-written material below (`key` = transposition into a key, `octv` = octave shift); the cantus
statements are `hex_up` / `hex_dn` (the hexachord transposed and set in semibreves), except the
B-flat statement, written out by hand with its first four notes in minims.  All other
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
LONG = ['Soprano', 'Alto', 'Cantus', 'Tenor', 'Bass']
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
sc.theme('C', 9, 1, hex_up('B3'), 'Cantus: B, ut-la (rising)', 6)
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
sc.theme('C', 15, 1, hex_dn('A#4', last=12), 'Cantus: C#, la-ut (falling)', 6)
sc.theme('S', 15, 1, key(INV, 'G#5', 'A#5'), 'Inversion (C#) over the falling cantus, soprano')
sc.put('B', 15, 1, 'A#1:2 B1:2 C#2:2 D#2:2 E#2:4 F#2:2 D#2:2 '
                   'G#1:2 A#1:2 B#1:2 G#1:2 D#2:2 E#2:2 F#2:2 D#2:2 '
                   'G#1:4 B#1:2 A#1:2 G#1:4 D#2:4 '
                   'C#2:2 D#2:2 E#2:2 D#2:2 C#2:2 B#1:2 A#1:2 R:2')
sc.theme('B', 19, 1, key(INV, 'G#5', 'D#3'), "Inversion (F#) in the bass, at the cantus's re")
# (each bar's division starts within a tenth of the cantus's new note, so one hand strikes both)
sc.put('S', 17, 1, 'D#5:2 G#5:2 A#5:2 B#5:2 D#6:2 C#6:2 B#5:2 G#5:2 '
                   'E#5:2 G#5:1 A#5:1 G#5:2 C#6:2 A#5:2 G#5:1 F#5:1 E#5:2 C#5:2 '
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
sc.put('B', 27, 1, key(CSI, 'G#5', 'D4').rsplit(' ', 1)[0] + ' F3:1')            # CSI below; last note to F
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
sc.put('T', 35, 1, 'D4:4 B3:4 G3:8 '
                   'E4:4 C4:4 C4:4 A3:4')
sc.put('B', 35, 1, 'B2:4 G2:2 B2:2 E2:2 F#2:2 E2:2 G2:2 '
                   'C3:2 E3:2 A2:2 G2:2 A2:2 B2:2 C3:2 A2:2')
sc.theme('A', 37, 1, key(SUBJ, 'B4', 'D4'), "Subject on the dominant (D), alto, at the cantus's sol")
sc.put('S', 37, 1, 'R:4 F#5:1 A5:1 G5:1 B5:4 C#6:1 D6:4~ '                      # CS above, in D
                   'D6:4 C#6:4 A5:1 G5:1 F#5:1 G5:1 A5:1 B5:1 C#6:1 A5:1')

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
sc.put('A', 41, 1, 'A4:2 B4:2 A4:2 F#4:2 G#4:2 A4:2 G#4:2 B4:2 '
                   'A4:2 G#4:2 A4:2 E4:2 F#4:2 G#4:2 A4:2 F#4:2 '
                   'D4:4 C#4:2 D4:2 B3:4 F#4:4 '
                   'C#4:8 R:8')                                                  # rests before its triplets
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
sc.put('A', 45, 1, 'R:4 E4:4/3 F4:4/3 G4:4/3 A4:4/3 B4:4/3 C5:4/3 A4:4/3 G4:4/3 F4:4/3 '
                   'F4:4/3 G4:4/3 A4:4/3 B4:4/3 C5:4/3 B4:4/3 D5:4/3 C5:4/3 B4:4/3 G4:4/3 A4:4/3 B4:4/3 '
                   'G4:4/3 A4:4/3 B4:4/3 C5:4/3 D5:4/3 E5:4/3 C5:4/3 B4:4/3 A4:4/3 E5:4/3 D5:4/3 C5:4/3 '
                   'A4:4/3 B4:4/3 C5:4/3 A4:4/3 B4:4/3 C5:4/3 D5:4/3 C5:4/3 D5:4/3 A4:4/3 B4:4/3 C5:4/3 '
                   )
sc.put('S', 47, 1, 'R:4 G5:4 C6:4 A5:4~ '
                   'A5:4 G5:2 F5:2 A5:4 C6:4 '
                   'B5:4 R:12')
sc.put('B', 47, 1, 'R:8 A2:2 B2:2 C3:2 A2:2 '
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
                   'D2:4 F#2:2 A2:2 D2:4 A1:4')
# b55-56: no second entry here (the only falling region without one); instead the soprano's
# division turns dotted, Em | D - A, and runs on into the E region.
sc.put('S', 55, 1, 'B4:3 D5:1 E5:3 F#5:1 G5:3 F#5:1 E5:3 D5:1 '
                   'F#5:3 E5:1 D5:3 E5:1 F#5:3 E5:1 A5:4')
# (the tenor rests from b53 until its entry at b57: the D region thins to a trio)
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
# (from b64 to b67 the bass lies an octave higher than a bass usually would, so that one hand can
#  take it with the inner voice while the other holds the cantus and the soprano)
sc.put('B', 63, 1, 'D#2:2 E#2:2 F#2:2 G#2:2 A#2:2 B2:2 A#2:4 '
                   'C#3:2 D#3:2 E#3:2 F#3:2 G#3:2 F#3:2 E#3:2 C#3:2')
sc.put('S', 63, 1, 'F#5:8 C#6:8 '
                   'G#5:4 E#5:4 C#6:4 G#5:4')
# episode b65-66 (G#m7 - C#7 | F# - D#m): the cantus's B is the seventh of C#7 and falls to A#
sc.put('S', 65, 1, 'B5:6 A#5:2 G#5:4 C#6:4 '
                   'F#5:4 A#5:4 D#5:4 R:4')
sc.put('A', 65, 1, 'R:2 G#4:2 F#4:2 D#4:2 E#4:2 G#4:2 E#4:2 C#4:2 '
                   'C#5:4 F#4:4 F#4:4 D#4:4')
sc.put('T', 65, 1, 'R:4 D#4:4 G#3:8 '
                   'A#3:2 B3:2 C#4:2 A#3:2 F#3:4 A#3:2 F#3:2')
sc.put('B', 65, 1, 'G#2:4 B2:4 C#3:8 '
                   'F#3:2 E#3:2 D#3:2 E#3:2 D#3:2 C#3:2 D#3:4')
sc.theme('S', 67, 1, key(INV, 'G#5', 'G#5'), "Inversion (B, home), soprano, at the cantus's re")

sc.put('A', 67, 1, 'B3:4 D#4:4 B3:4 D#4:4 '
                   'A#3:4 C#4:4 C#4:4 E#4:4')
sc.put('B', 67, 1, 'G#2:2 A#2:2 B2:2 C#3:2 D#3:2 E3:2 F#3:4 '
                   'F#2:2 G#2:2 A#2:2 B2:2 C#3:8')

# ===================================================================== XI. A-flat (bars 69-74), rising: the wolf
# The cantus reaches A-flat = G#.  The first bar is a bare fifth A-flat / E-flat in every voice, a
# drone: in Bach-Lehman a calm open fifth (700 cents), in quarter-comma meantone the wolf
# (G# - Eb, 737.6 cents).  Then the subject on B-flat (the next key, at the cantus's re), a turn to
# B-flat minor, and the subject on E-flat at the cantus's sol.
sc.mark(69, 'A-flat (rising): the wolf fifth')
sc.theme('C', 69, 1, hex_up('Ab4'), 'Cantus: A-flat, ut-la (rising)', 6)
sc.put('S', 69, 1, 'Eb5:16')
sc.put('A', 69, 1, 'Ab3:16')
sc.put('T', 69, 1, 'Eb3:12 R:4')
sc.put('B', 69, 1, 'Ab2:12 C3:4')
sc.theme('T', 70, 1, key(SUBJ, 'B4', 'Bb3'), "Subject (B-flat), tenor, at the cantus's re")
sc.put('S', 70, 1, 'R:4 D5:1 F5:1 Eb5:1 G5:4 A5:1 Bb5:4~ '                      # CS above
                   'Bb5:4 A5:4 F5:1 Eb5:1 D5:1 Eb5:1 F5:1 G5:1 A5:1 F5:1')
sc.put('B', 70, 1, 'Bb2:8 G2:8 '
                   'F3:4 A2:4 D3:4 A2:4')
# b72: B-flat minor (the cantus's D-flat), ii7 of A-flat, leading to E-flat
sc.put('S', 72, 1, 'F5:4 Bb5:2 Ab5:2 Db6:4 Ab5:4')
sc.put('T', 72, 1, 'Db4:8 Bb3:4 Ab3:4')
sc.put('B', 72, 1, 'Bb2:4 Ab2:4 Gb2:4 F2:4')
sc.theme('A', 73, 1, key(SUBJ, 'B4', 'Eb4'), "Subject on the dominant (E-flat), alto, at the cantus's sol")
sc.put('S', 73, 1, 'R:4 G5:1 Bb5:1 Ab5:1 C6:4 D6:1 Eb6:4~ '                      # CS above, in E-flat
                   'Eb6:4 D6:4 Bb5:1 Ab5:1 G5:1 Ab5:1 Bb5:1 C6:1 D6:1 Bb5:1')
sc.put('T', 73, 1, 'G3:4 Bb3:4 C4:4 Ab3:4 '
                   'F3:4 Ab3:4 F3:4 R:4')
sc.put('B', 73, 1, 'R:8 Ab2:4 Eb3:4 '
                   'Bb2:4 D3:8 R:4')


# ===================================================================== XII. B-flat (bars 75-78), falling, compressed
# The one statement that breaks the six-bar clock.  After the wolf the cantus, now the top voice,
# takes la-sol-fa-mi in minims, twice its rate, over the bass's inversion (la..ut in quick notes):
# the statement lasts four bars instead of six, and home arrives two bars before the ear expects it.
# Its last two notes return to semibreves and are re-read: C is the Neapolitan of B, and B-flat is
# A-sharp, the third of F#7, so that the circle closes by a semitone.
sc.mark(75, 'B-flat (falling), in minims: the cantus hurries home')
sc.theme('C', 75, 1, 'G5:8 F5:8 Eb5:8 D5:8 C5:16 Bb4:16',
         'Cantus: B-flat, la-ut (falling), la-sol-fa-mi in minims; its B-flat becomes A#, the leading note of B', 4)
sc.theme('B', 75, 1, key(INV, 'G#5', 'G2'), 'Inversion (B-flat), bass, with the falling cantus')
# b75-76: Gm - Bb/D | F7 - G7 - C.  The cantus's E-flat (the seventh of F7) falls to D, which hangs
# over the bass's C at 76.4 (9-8) and resolves when the cantus reaches C at b77.
sc.put('A', 75, 1, 'Bb4:16 '
                   'A4:8 F4:4 E4:4 '
                   'G4:4 A4:2 G4:2 G4:8 '
                   'E4:4 F#4:4 E4:4 C#4:4')
sc.put('T', 76, 3, 'B3:4 C4:4 '
                   'E4:4 C4:2 D4:2 E4:4 C4:4 '
                   'C#4:8 F#3:4 R:4')
sc.put('B', 77, 1, 'E2:2 F2:2 G2:2 A2:2 G2:2 F2:2 E2:4 '
                   'F#2:4 E2:4 C#3:4 R:4')

# ===================================================================== XIII. B (bars 79-84), rising: home
sc.mark(79, 'B (rising): home, five voices')
sc.theme('C', 79, 1, hex_up('B4'), 'Cantus: B, ut-la (rising), home an octave higher', 6)
sc.theme('B', 79, 1, key(SUBJ, 'B4', 'B2'), 'Subject (B), bass, with the cantus: home')
sc.put('S', 79, 1, 'R:4 D#5:1 F#5:1 E5:1 G#5:4 A#5:1 B5:4~ '                      # CS above
                   'B5:4 A#5:4 F#5:1 E5:1 D#5:1 E5:1 F#5:1 G#5:1 A#5:1 F#5:1')
sc.put('A', 79, 1, 'F#4:8 E4:8 '
                   'C#4:4 E4:12')
sc.put('T', 79, 1, 'D#4:4 B3:4 B3:4 B3:4 '
                   'A#3:4 C#4:4 C#4:4 A#3:4')

# b81 (B/D# - G#m): the soprano's last division
sc.put('S', 81, 1, 'B5:1 A#5:1 B5:1 C#6:1 D#6:1 C#6:1 B5:1 A#5:1 G#5:2 B5:2 D#6:2 B5:2')
sc.put('T', 81, 1, 'D#4:4 F#3:4 G#3:4 R:4')
sc.put('B', 81, 1, 'D#3:4 B2:4 G#2:4 B2:4')
sc.theme('T', 82, 1, key(SUBJ, 'B4', 'E3'), "Subject on the subdominant (E), tenor, at the cantus's fa")
sc.put('S', 82, 1, 'R:4 G#5:1 B5:1 A5:1 C#6:4 D#6:1 E6:4~ '                      # CS above, in E
                   'E6:4 D#6:4 B5:1 A5:1 G#5:1 A5:1 B5:1 C#6:1 D#6:1 B5:1')
sc.put('A', 82, 1, 'G#4:4 B4:4 C#5:8 '
                   'F#4:4 B4:4 D#5:8')
sc.put('B', 82, 3, 'C#3:8 '
                   'D#3:4 B2:8 R:4')

# ===================================================================== the summit: la, and the turn
# The cantus reaches its la, G#5, and is the top voice for that bar; the bass sings the inversion
# (la..ut) under it, and from here the cantus falls home: sol fa mi re ut.
sc.theme('B', 84, 1, key(INV, 'G#5', 'G#2'), "Inversion (B), bass, under the cantus's la: the turn")
sc.put('S', 84, 1, 'R:16 '
                   'A#5:6 C#6:2 E6:4 C#6:4')
sc.put('A', 84, 1, 'B4:4 D#5:4 B4:4 G#4:4 '
                   'C#5:16~')                                                   # held into the coda (6-5)
sc.put('T', 84, 1, 'B3:4 G#3:4 F#3:4 B2:4')

# ===================================================================== CODA (bars 85-89): the cantus falls home
sc.mark(85, 'Coda: the cantus falls home')
sc.theme('C', 85, 1, 'F#5:16 E5:16 D#5:16 C#5:16 B4:16', 'Cantus: B, sol-fa-mi-re-ut (falling home)', 5)

# The soprano comes down a ninth in syncopated steps (E6 ... D#5) to settle a third above the
# cantus's last ut.  The alto stays in the right hand under the cantus (6-5 at 86.1, 4-3 at 87.1);
# the tenor stays within a tenth of the deep bass, so that each hand can reach its notes.
sc.put('S', 86, 1, 'E6:4 D#6:2 C#6:6 B5:4~ '
                   'B5:4 A#5:2 G#5:6 F#5:4~ '
                   'F#5:8 E5:8 '
                   'D#5:16')
sc.put('A', 86, 1, 'C#5:4 B4:8 G#4:4~ '
                   'G#4:4 F#4:4 B4:8 '
                   'A#4:8 F#4:8~ '
                   'F#4:16')
sc.put('T', 86, 1, 'G#3:12 B2:4~ '
                   'B2:16 '
                   'C#3:8 A#2:8 '
                   'B2:16')
sc.put('B', 86, 1, 'E2:2 F#2:2 G#2:4 E2:4 B1:4 '
                   'D#2:4 B1:2 A#1:2 G#1:4 B1:4 '
                   'F#2:8 F#1:8 '
                   'B1:16')

NBARS = 89


# phrase dynamics (velocity offsets by bar): quiet after Bull's leap, loud at the wolf and at home
LEVEL = {1: 0, 5: 2, 9: 4, 11: 1, 15: -2, 21: 0, 27: -1, 33: 2, 39: 5, 43: 7, 45: -6, 49: -3, 51: -3,
         57: 0, 61: 2, 63: 1, 69: 6, 70: 3, 75: 2, 77: 5, 79: 8, 85: 6, 87: 3, 89: 2}


def dynamics(b):
    bar, v = b + 1, 0
    for k in sorted(LEVEL):
        if k <= bar:
            v = LEVEL[k]
    return v


def q(bar, beat=1):
    return float((bar - 1) * 4 + (beat - 1))


BPM = 100
TEMPO = [[q(1), BPM], [q(44), BPM], [q(44, 4), 80, 'ramp'], [q(45), BPM],      # breath at Bull's leap
         [q(68, 3), BPM], [q(69), 90, 'ramp'], [q(70), BPM],                    # the wolf bar, a little broader
         [q(78, 2), BPM], [q(79), 92, 'ramp'],                                  # home
         [q(86), 92], [q(89), 66, 'ramp'], [q(90), 60, 'ramp']]                 # the cantus falls home


def main():
    bars = sc.bars(NBARS)
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Fugue XXIII in B major, five voices: Fantasia ut re mi fa sol la per tutti i tuoni',
        'composer': 'Claude / Sam, after John Bull',
        'instrument': 'Keyboard - five voices (a four-voice fugue and a cantus)',
        'key': 'B', 'mode': 'major', 'meter': list(METER), 'bpm': BPM, 'tempo_map': TEMPO,
        'tempo_text': 'Allegro moderato, alla fantasia',
        'movement_number': 23, 'piece_type': 'fugue', 'edition': 'third',
        'score_tagline': 'The Well-Tempered clAIvier - third edition',
        'voice_order': 'high_to_low',
        'markers': [{'t': float((b - 1) * 4), 'label': txt} for b, txt in sc.marks],
    }
    voices = [(LONG[i], ABBR[i], CLEF[i], BASEVEL[i]) for i in range(len(NAMES))]
    named = {LONG[i]: bars[NAMES[i]] for i in range(len(NAMES))}
    entries = [(LONG[NAMES.index(v)], b, off, lab, n) for v, b, off, lab, n in sc.entries]
    W.build_score(HERE / 'fugue.json', meta, voices, named, entries=entries, subject=SUBJ,
                  dynamics=dynamics, tags=None)
    print(f"wrote {HERE / 'fugue.json'}: {NBARS} bars")


if __name__ == '__main__':
    main()
