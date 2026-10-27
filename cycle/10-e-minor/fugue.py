#!/usr/bin/env python3
"""Fugue X in E minor, eleven voices: "Fuga a due cori con corale".

An homage to the opening chorus of the St Matthew Passion, BWV 244 no. 1
(E minor, 12/8, two choirs in dialogue, with a ripieno soprano singing the
chorale "O Lamm Gottes, unschuldig" above).

Voices: Coro I (five), Coro II (five), and the chorale (the eleventh voice).

Every note is written here.  Thematic statements are explicit transforms
(wtclib.transpose / invert_diatonic / scale_rhythm) of the hand-written
subject; all other material is written literally as token strings placed at
bar / dotted-quarter-beat positions.  No code chooses pitches.

The chorale melody (Nikolaus Decius, 1522/1531) is copied from Bach's own
four-part setting of the tune, BWV 401 (soprano), transposed from F to G
major, the key in which the ripieno sings it in BWV 244 no. 1.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (12, 8)
BAR = 24                                        # sixteenths per bar
NAMES = ['S1', 'A1', 'T1', 'Bar1', 'B1', 'S2', 'A2', 'T2', 'Bar2', 'B2', 'CH']
LONG = ['Coro I Soprano', 'Coro I Alto', 'Coro I Tenore', 'Coro I Baritono', 'Coro I Basso',
        'Coro II Soprano', 'Coro II Alto', 'Coro II Tenore', 'Coro II Baritono', 'Coro II Basso',
        'Soprano in ripieno (Choral)']
CLEF = ['treble', 'treble', 'treble_8', 'bass', 'bass',
        'treble', 'treble', 'treble_8', 'bass', 'bass', 'treble']
SC = [4, 6, 7, 9, 11, 0, 3]                     # E harmonic minor, from the tonic

# ---------------------------------------------------------------- material
# The chorale's first line, G G G D D E D (G major), moved into the relative
# minor gives the subject's seven beat-notes E E E B | B C B.
R = 'E4:6 E4:4 D#4:2 E4:2 F#4:2 G4:2 B4:4 A4:2 B4:4 G4:2 C5:6 B4:2 A4:2 G4:2 F#4:2 E4:2 D#4:2'
INV = W.invert_diatonic(R, 'G4', SC)            # B B B E | E D# E: the inversion (axis G) ends on the tonic
RA = W.transpose(R, 7, 4)                       # real answer, B minor
RG = 'G4:6 G4:4 F#4:2 G4:2 A4:2 B4:2 D5:4 C5:2 D5:4 B4:2 E5:6 D5:2 C5:2 B4:2 A4:2 G4:2 F#4:2'  # major: its beat-notes ARE the chorale line
IG = 'D5:6 D5:4 E5:2 D5:2 C5:2 B4:2 G4:4 A4:2 G4:4 B4:2 F#4:6 G4:2 A4:2 B4:2 C5:2 D5:2 E5:2'  # G-major inversion (axis B)
# countersubject (written above the subject; first eighth X = the previous note's continuation)
CS = 'B4:2 E5:2 G5:4 F#5:2 E5:6 D5:6~ D5:4 E5:2 A5:4 G5:2 D#5:6 F#5:6'      # 23 sixteenths after X


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def aug(s, k):
    return W.scale_rhythm(s, k)


def cs(x, level=0, oc=0):
    """countersubject: x = first-eighth pitch name; level 0 = E minor, 7 = B minor."""
    body = CS if level == 0 else tr(CS, 7, 4)
    return f'{x}:2 ' + octv(body, oc)


# ---------------------------------------------------------------- chorale (G major), O Lamm Gottes, unschuldig
CH1 = 'G5:12 G5:12 G5:12 D6:12 D6:12 E6:12 D6:24'               # O Lamm Gottes, unschuldig
CH2 = 'D6:12 G5:12 A5:12 B5:12 C6:12 B5:12 A5:6 G5:6 G5:24'     # am Stamm des Kreuzes geschlachtet
CH5 = 'B5:12 B5:12 B5:12 A5:12 B5:12 G5:6 F#5:6 E5:12 D5:24'    # all Sünd hast du getragen
CH6 = 'D6:12 E6:12 D6:12 D6:12 B5:6 C6:6 D6:12 C6:12 B5:24'     # sonst müssten wir verzagen
CH7 = 'E6:12 D6:6 C6:6 B5:12 A5:12 B5:12 D6:12 B5:6 A5:6 G5:24'  # Erbarm dich unser, o Jesu

# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, beat=1, e=0):
    return Fr(bar - 1) * BAR + (Fr(beat) - 1) * 6 + Fr(e) * 2


def put(v, bar, beat, toks, e=0):
    VO[v].append((pos(bar, beat, e), toks))


def theme(v, bar, beat, toks, label, nbars=None, e=0):
    put(v, bar, beat, toks, e)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / BAR))
    ENTRIES.append((LONG[NAMES.index(v)], bar, (Fr(beat) - 1) * Fr(3, 2) + Fr(e, 2), label, n))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {s / BAR + 1}: {toks[:40]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * BAR)
    if cur > total:
        raise ValueError(f'{v}: runs past the end')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# ================================================================ I. EXPOSITION, CORO I (b1-10)
# Entries descend through the choir (S A T Bar B), so the countersubject always lies above its subject.
theme('S1', 1, 1, R, 'Coro I: subject')
theme('A1', 3, 1, octv(RA, -1), 'Coro I: answer (B minor)')
put('S1', 3, 1, cs('D#4', 7, -1))                      # D# held: the answer arrives on the dominant chord
theme('T1', 5, 1, octv(R, -1), 'Coro I: subject')
put('A1', 5, 1, cs('B3', 0, -1))
put('S1', 5, 1, 'E5:6 D5:4 C5:2 G4:2 A4:2 B4:2 C5:4 B4:2 D5:4 C5:2 E5:6 B4:6 R:6')
theme('Bar1', 7, 1, octv(RA, -2), 'Coro I: answer (B minor)')
put('T1', 7, 1, cs('D#3', 7, -2))
put('A1', 7, 1, 'F#4:12 F#4:2 E4:2 D4:2 A4:4 G4:2 F#4:4 G4:2 B4:6 A#4:6 F#4:6')
put('S1', 7, 2, 'F#5:6 F#5:4 E5:2 D5:6 D5:6 E5:6 C#5:12')
theme('B1', 9, 1, octv(R, -2), 'Coro I: subject in the bass')
put('Bar1', 9, 1, cs('B2', 0, -2))
put('T1', 9, 1, 'E4:6 B3:6 C4:4 B3:2 D4:4 C4:2 B3:4 C4:2 E4:6 B3:12')
put('A1', 9, 1, 'G4:6 B4:6 A4:4 G4:2 G4:4 F#4:2 G4:4 A4:2 C5:4 A4:2 F#4:6 B4:6')
put('S1', 10, 2, 'E5:6 F#5:6 A5:6')

# ================================================================ II. DIALOGUE (b11-13): Sehet! - Wen? - den Braeutigam - Wie? - als wie ein Lamm
# Coro I sings the subject in pieces; Coro II (its first sound) interrupts with questions made of the inversion's head.
put('B1', 11, 1, 'E2:12 G2:6 B2:6 G2:4 E2:2 B2:6 R:12 G2:6 E2:6 R:6 B2:6')
put('Bar1', 11, 1, 'G3:6 A3:4 G3:2 R:12 R:24 R:18 A3:6')
put('T1', 11, 1, 'B3:6 C4:4 B3:2 G3:6 A3:6 G3:6 F#3:6 R:12 B3:6 G3:6 R:6 F#3:6')
theme('A1', 11, 3, 'E4:6 E4:4 D#4:2 E4:2 F#4:2 G4:2 B4:4 A4:2', 'Coro I: "Sehet!" (subject head)', 1)
put('A1', 11, 1, 'B4:6 R:6')
put('A1', 13, 1, 'B4:4 G4:2 C5:6 R:6 C5:4 B4:2')                 # "den Braeutigam" ... "als wie ein Lamm" (the sigh C-B)
put('S1', 11, 1, 'G5:18 F#5:6 E5:6 D#5:6 R:12 D5:6 E5:6 R:6 D#5:6')
theme('S2', 12, 3, 'B4:6 B4:4 C5:2', 'Coro II: "Wen?" (inversion head)', 1)
put('T2', 12, 3, 'G4:4 F#4:2 E4:6')
put('B2', 12, 3, 'E3:6 G2:4 A2:2')
put('S2', 13, 3, 'A4:2 B4:2 C5:2')                                 # "Wie?"
put('A2', 13, 3, 'E4:4 F#4:2')
put('B2', 13, 3, 'C3:4 B2:2')


# ================================================================ III. CHORALE LINE 1 (b14-17): the subject and its source sung together
# The chorale's first line (dotted halves, G major) and the subject (dotted quarters, E minor) start together:
# the fugue subject is the chorale line in diminution, moved to the relative minor.
put('CH', 14, 1, CH1)
theme('T1', 14, 1, 'E3:6 E3:4 D#3:2 E3:2 F#3:2 G3:2 B3:4 A3:2 B3:4 G3:2 C4:6 B3:2 A3:2 G3:2 F#3:2 E3:2 D3:2',
      'Coro I: subject under chorale line 1 (tail in natural minor, against the chorale D)')
put('B1', 14, 1, 'E2:6 G2:6 C3:6 B2:6 G2:6 A2:6 B2:6 A2:6 G2:6 B2:6 C3:6 A2:6')
put('Bar1', 14, 1, 'G3:6')
put('Bar1', 16, 1, 'D3:6 G3:4 F#3:2 E3:6 E3:6')
put('A1', 14, 1, 'B4:2 A4:2 G4:2 E4:4 F#4:2 G4:2 F#4:2 E4:2 D4:4 E4:2 D4:2 E4:2 F#4:2 G4:4 F#4:2 G4:2 F#4:2 E4:2 '
                 'D4:2 E4:2 F#4:2 D4:6 B4:4 A4:2 G4:6 A4:4 G4:2')
put('S1', 14, 1, 'E5:6 B4:6 C5:6 D5:6 B4:6 E5:6 D5:6 F#5:6 G5:6 D5:6 C5:6 C5:4 B4:2')

# ================================================================ IV. CORO II: THE MIRROR EXPOSITION (b17-25)
# Coro II now gives full entries, all in inversion, entering from the bass upward (Coro I entered from the top down).
theme('B2', 17, 1, octv(tr(INV, 7, 4), -2), 'Coro II: inversion (B minor), bass')
theme('T2', 18, 1, octv(tr(INV, 7, 4), -1), 'Coro II: inversion (B minor), tenor, one bar later')
put('S1', 17, 1, 'F#5:6 D5:6 D5:2 E5:2 F#5:2 F#5:4 E5:2 D5:6 E5:6 D5:6 C#5:6 D5:6 E5:6 D5:6 G5:4 A5:2')
put('A1', 17, 1, 'A4:6 A4:4 B4:2 A4:6 B4:4 A#4:2 B4:6 C#5:6 B4:6 G4:6~ G4:4 A4:2 C#5:6 B4:12')
put('B2', 19, 1, 'G2:6 F#2:6 B2:6 E2:6')

put('CH', 20, 1, CH2)
theme('Bar2', 20, 2, octv(INV, -1), 'Coro II: inversion (E minor), baritone, under chorale line 2')
theme('A2', 22, 3, octv(tr(INV, 7, 4), -1), 'Coro II: inversion (B minor), alto')
put('B2', 20, 1, 'B1:6')
put('B1', 20, 2, 'G2:6 E2:6 C3:4 B2:2 A2:6 C3:6 B2:6 R:6 A2:6 F#2:6')
put('T2', 20, 1, 'F#4:6 G4:12 E4:6 C4:6 A3:6 F#3:6 B3:6 G4:6 E4:6')
put('S1', 20, 1, 'F#5:6 D5:6 E5:6 G5:6 C5:6 E5:6 F#5:6 G5:6 E5:6 C5:6')
put('A1', 20, 1, 'D5:2 C#5:2 B4:2 B4:4 C5:2 B4:4 A4:2 E5:6 A4:6 G4:6 A4:6 G4:6')
put('A2', 22, 1, 'C5:4 B4:2 A4:6')
theme('S2', 24, 3, tr(INV, 7, 4), 'Coro II: inversion (B minor), soprano: Coro II alone')
put('B2', 22, 3, 'B2:6 D3:6 F#2:6 G2:6 B2:6 C#3:6 D3:6 G2:6 B2:6 D3:6 F#2:6 G2:6 B2:6 C#3:6')
put('T2', 22, 3, 'D4:18 G3:12 E3:6 G3:6 B3:6 D4:6 B3:4 C#4:2 D4:18 C#4:6')
put('Bar2', 22, 2, 'C4:6')
put('Bar2', 24, 3, 'F#3:12 D3:18 G3:6')
put('A2', 24, 3, 'F#4:6 B4:6 A4:6 G4:6 F#4:6 E4:6')
put('S1', 22, 3, 'D5:6 C#5:4 B4:2 D5:6 E5:4 C#5:2 D5:6 C#5:6 B4:12')


# ================================================================ V. RECOGNITION (b26-29): chorale line 3 (= line 1) over its own diminutions
# Coro I sings the subject in G major, whose beat-notes ARE the chorale line; Coro II sings it in E minor a tenth below.
# For two bars the choirs agree (parallel tenths) -- the one deliberate unanimity of the piece.
put('CH', 26, 1, CH1)
theme('A1', 26, 1, RG, 'Coro I: subject in G major = the chorale line in diminution')
theme('Bar2', 26, 1, octv('E4:6 E4:4 D#4:2 E4:2 F#4:2 G4:2 B4:4 A4:2 B4:4 G4:2 C5:6 B4:2 A4:2 G4:2 F#4:2 E4:2 D4:2', -1),
      'Coro II: subject in E minor a tenth below (natural-minor tail)')
put('T2', 26, 1, 'B3:12 E4:6 D4:6 G4:12 D4:6 C4:6')
theme('B2', 28, 2, octv(RA, -2), 'Coro II: answer (B minor), bass')
theme('S1', 28, 4, tr(IG, 7, 4), 'Coro I: inversion in D major, soprano')
put('A1', 28, 1, 'G4:2 A4:2 B4:2 B4:6 G4:6 F#4:6 F#4:4 G4:2 A4:6 G4:6 A4:6 F#4:6')
put('T2', 28, 1, 'B3:6 D4:6 B3:6 D4:18 B3:6 A3:6 C#4:6 F#4:6')
put('Bar2', 28, 1, 'G3:6 F#3:6 E3:6 F#3:6')

# ================================================================ VI. CHORALE LINE 4 (b30-37) over the subject at half speed
# Coro II sings the G-major subject; one beat later Coro I's bass sings it at half speed (a prolation stretto),
# and that broad bass carries chorale line 4. A Coro I tenor entry (E minor) then cadences in E minor at b37.
theme('A2', 30, 3, RG, 'Coro II: subject in G major')
theme('B1', 30, 4, octv(aug(RG, 2), -2), 'Coro I: subject in G major at half speed, bass (under chorale line 4)', 4)
put('CH', 32, 1, CH2)
theme('T2', 32, 3, octv(IG, -1), 'Coro II: inversion in G major, tenor')
theme('T1', 35, 1, octv(R, -1), 'Coro I: subject (E minor), tenor: cadence in E minor at b37')
put('B2', 30, 2, 'B2:6 G2:6')
put('A1', 30, 2, 'D4:6 E4:6 D4:18 F#4:6 E4:6')
put('T2', 30, 3, 'B3:6 D4:6 D4:4 C4:2 B3:6 A3:6 G3:6')
put('S1', 31, 3, 'G5:12 F#5:6 F#5:4 E5:2 D5:6 D5:6 D5:4 C5:2 C5:6 B4:6 D5:6 E5:12 B4:6 D5:4 E5:2 '
                 'E5:6 B4:6 C5:6 D5:6 E5:18 F#5:6 G5:6')
put('A2', 32, 3, 'G4:6 B4:4 A4:2 F#4:6 E4:12 F#4:6 E4:6 A4:6 D4:12')
put('A1', 34, 3, 'G4:6 B4:6 C5:6 B4:4 A4:2 G4:6 A4:4 B4:2 G4:6 A4:6 G4:6 A4:6 G4:6')
put('B2', 36, 2, 'A2:6 B2:12 E2:6')


# ================================================================ VII. CHORALE LINE 5 (b37-43): B minor, the choirs closer
# A one-beat exchange (Coro II asks, Coro I answers) turns E minor to B minor; then the answer in Coro I's tenor
# and the inverted answer in Coro II's baritone, six beats apart, under "All Suend hast du getragen".
put('S2', 37, 2, 'C5:4 B4:2')
put('T2', 37, 2, 'E4:4 D#4:2')
put('B2', 37, 2, 'A2:6')
put('S1', 37, 3, 'A5:4 G5:2')
put('A1', 37, 3, 'C5:4 E5:2')
put('Bar1', 37, 3, 'F#3:4 A3:2')
put('A2', 37, 4, 'A#4:6')
put('Bar2', 37, 4, 'C#4:6')
put('B2', 37, 4, 'F#2:6')
put('CH', 38, 1, CH5)
theme('T1', 38, 1, octv('B4:6 B4:4 A#4:2 B4:2 C#5:2 D5:2 F#5:4 E5:2 F#5:4 D5:2 G5:6 F#5:2 E5:2 D5:2 C#5:2 B4:2 A4:2', -1),
      'Coro I: answer (B minor), tenor (tail in natural minor, against the chorale A)')
theme('Bar2', 39, 3, octv(tr(INV, 7, 4), -2), 'Coro II: inverted answer (B minor), baritone as the bass')
put('B2', 38, 1, 'B2:6 D3:4 C#3:2 B2:6 D3:6 B2:6 G2:6')
put('S1', 38, 1, 'F#5:6 F#5:4 E5:2 D5:6 D5:4 C#5:2 D5:6 E5:6 F#5:6 E5:6 D5:6 D5:4 E5:2 D5:6 C#5:6 B4:6 B4:6 A4:12 B4:6 B4:6')
put('A2', 38, 1, 'D4:4 C#4:2 F#4:6 A4:4 G4:2 B4:18 F#4:12')
put('T1', 40, 1, 'D4:6 D4:4 C#4:2 D4:6 F#4:6 G4:12 F#4:6 D4:6 F#4:6 G4:6')
put('Bar2', 41, 3, 'B2:6 D3:6 B2:6 G2:6')
# the gap (b42.3-43.1): Coro I calls with the subject's head, Coro II answers with the inversion's head
put('A1', 42, 3, 'E4:6 E4:4 D#4:2 E4:6')
put('T1', 42, 3, 'G4:6 F#4:6 G4:6')
put('S2', 42, 4, 'B4:4 C5:2 B4:6')
put('B1', 42, 3, 'E3:6 B2:6 E3:6')


# ================================================================ VIII. CHORALE LINE 6 (b43-49): toward the dominant
RN = 'E4:6 E4:4 D#4:2 E4:2 F#4:2 G4:2 B4:4 A4:2 B4:4 G4:2 C5:6 B4:2 A4:2 G4:2 F#4:2 E4:2 D4:2'   # natural-minor tail
put('CH', 44, 1, CH6)
theme('B2', 43, 2, octv(RN, -2), 'Coro II: subject in the bass (natural-minor tail, against the chorale D)')
put('B2', 45, 2, 'G2:12 B2:6 E2:6 C3:6 A2:6 E2:6 C3:6 A2:6')
theme('A1', 45, 2, octv(IG, -1), 'Coro I: inversion in G major, alto')
# half cadence: the subject and its inversion together (a mirror pair) in B minor over a dominant pedal
theme('S1', 47, 3, RA[:RA.index('C#5:2 B4:2 A#4:2')].strip(), 'Coro I: answer (B minor), with its mirror below', 2)
theme('A2', 47, 3, octv(tr(INV, 7, 4), -1).rsplit(' ', 3)[0], 'Coro II: inverted answer (B minor), mirror of the soprano', 2)
put('B1', 47, 3, 'B1:24')
put('Bar1', 43, 2, 'B3:6 B3:4 A3:2 G3:6 D4:12 G3:12 A3:6 B3:6')
put('T2', 43, 2, 'E4:6 E4:4 F#4:2 G4:6 F#4:6 G4:6 E4:12 A4:6 G4:6 B4:4 A4:2 G4:6 G4:4 F#4:2 E4:6 A4:6 G4:12 A4:6')
put('S2', 44, 1, 'B4:6 D5:6 C5:6 E5:6 F#5:6 D5:6 D5:4 C5:2 B4:6 B4:6 E5:6 D5:6 B4:6 E5:6 C5:6')
put('Bar2', 47, 3, 'F#3:6 E3:6 D3:6 E3:6 D3:6 E3:6 F#3:6')

# ================================================================ IX. CHORALE LINE 7 (b49-55): the final stretto
CH7F = 'E6:12 D6:6 C6:6 B5:12 A5:12 B5:12 D6:12 B5:6 A5:6 G5:60'     # last line; the final G held to the end
put('CH', 50, 1, CH7F)
theme('B2', 49, 1, octv(IG, -2), 'Coro II: inversion in G major, bass (final stretto 1)')
theme('S2', 50, 1, INV, 'Coro II: inversion (E minor), soprano, under the chorale (final stretto 2)')
theme('T1', 51, 3, octv(R, -1), 'Coro I: subject (E minor), tenor: the final cadence (final stretto 3)')
put('B1', 51, 1, 'E2:6 B2:6 C3:6 B2:6 E2:6 G2:6 E3:6 C3:6 G2:6 B2:6 E2:30 E2:24 E2:12')


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue X in E minor, eleven voices: Fuga a due cori con corale',
            'composer': 'Claude / Sam (chorale: Nikolaus Decius, "O Lamm Gottes, unschuldig"; after J. S. Bach, BWV 244 no. 1)',
            'instrument': 'Two five-part choirs and a ripieno chorale (open score, eleven keyboards)',
            'key': 'E', 'mode': 'minor', 'meter': list(METER), 'bpm': 84,
            'tempo_text': 'Andante, sempre legato (dotted quarter = 56)',
            'movement_number': 10, 'piece_type': 'fugue', 'edition': 'third'}
    voices = [(LONG[i], NAMES[i], CLEF[i], 64 if n != 'CH' else 74) for i, n in enumerate(NAMES)]
    return W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES, subject=R)


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // BAR))
    build(nb)
    print('bars', nb)
