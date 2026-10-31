#!/usr/bin/env python3
"""Fugue X in E minor, three voices: "Fuga a due cori con corale" (third edition, Bach + 1).

An homage to the opening chorus of the St Matthew Passion, BWV 244 no. 1 (E minor, 12/8): two choirs in dialogue
("Sehet! - Wen? - den Braeutigam. Seht ihn! - Wie? - als wie ein Lamm") beneath the chorale "O Lamm Gottes,
unschuldig", sung above phrase by phrase.  Bach's E-minor fugue in WTC I (BWV 855) has two voices; this one has three:
  Coro I    (left in the binaural render)  sings the subject (rectus): the "Sehet!" choir;
  Coro II   (right)                         answers in inversion: the questioning choir;
  Choral    (front)                         the chorale's seven lines in dotted halves, an octave above the
                                            ripieno soprano of BWV 244/1 (G major).
The subject's seven beat-notes, E E E B B C B, are the chorale's first line (G G G D D E D) moved into the relative
minor, so the chorale is the subject's relative in augmentation; the Recognition (b19) makes that audible.

Every note is written here.  Thematic statements are explicit transforms (wtclib.transpose / invert_diatonic /
scale_rhythm) of the hand-written subject, or are written out by hand (RG, IG, SBG); all other material is literal
token strings placed at bar / dotted-quarter-beat positions.  No code chooses pitches.

The chorale melody (Nikolaus Decius, 1522/1531) is copied from the soprano of Bach's four-part setting BWV 401
(music21 corpus, checked), transposed from F to G major, the key in which the ripieno sings it in BWV 244 no. 1.
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
BAR = 24                                        # sixteenths per bar
NAMES = ['CH', 'C1', 'C2']
LONG = ['Choral (soprano in ripieno)', 'Coro I', 'Coro II']
CLEF = ['treble', 'treble', 'bass']
SC = [4, 6, 7, 9, 11, 0, 3]                     # E harmonic minor, from the tonic

# ---------------------------------------------------------------- material
S = 'E4:6 E4:4 D#4:2 E4:2 F#4:2 G4:2 B4:4 A4:2 B4:4 G4:2 C5:6 B4:2 A4:2 G4:2 F#4:2 E4:2 D#4:2'
INV = W.invert_diatonic(S, 'G4', SC)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


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


# ================================================================ I. EXPOSITION
theme('C1', 1, 1, S, 'Coro I: subject (E minor)')
put('C1', 3, 1, 'E4:1 G4:1 B4:1 E5:1 D#5:1 E5:1 G5:3 F#5:1 E5:1 D#5:1 F#5:1 A5:1 G5:1 F#5:1 E5:2 '   # CS: opens with
                'D#5:2 E5:1 C5:1 B4:2 G4:4 A4:2 B4:1 A4:1 G4:1 A4:1 B4:2 A4:2 B4:1 A4:1 G4:1 F#4:1 '      # BWV 855's head
                'G4:2 A4:2 B4:2 C5:2 D5:2 E5:2')
theme('C2', 3, 2, octv(INV, -1), 'Coro II: inversion (answer, from the dominant)')
put('C2', 5, 2, 'B3:4 R:2')
put('C1', 5, 2, 'D#5:2')

# ================================================================ II. DIALOGUE 1 (b5.3-7.4)
# Sehet! - Wen? - den Braeutigam. Seht ihn! - Wie? - als wie ein Lamm.
# Coro I sings the subject in pieces (in B minor, turning to E minor for its last three beats);
# Coro II interrupts with questions made of the inversion's head (a rising semitone).
put('C1', 5, 3, 'B4:6 B4:4 A#4:2')                       # Se-het!
put('C2', 6, 1, 'F#3:4 G3:2')                            # Wen?
put('C1', 6, 2, 'B4:2 C#5:2 D5:2 F#5:4 E5:2 F#5:4 D5:2') # den Braeutigam. Seht ihn!
put('C2', 7, 1, 'B3:4 C4:2')                             # Wie?
put('C1', 7, 2, 'C5:6 B4:2 A4:2 G4:2 F#4:2 E4:2 D#4:2')  # als wie ein Lamm
put('C2', 7, 2, 'A3:6 G3:2 F#3:2 E3:2 B2:6')

# ================================================================ III. CHORALE LINE 1 (b8-11)
CH1 = 'G5:12 G5:12 G5:12 D6:12 D6:12 E6:12 D6:18 R:6'
CH2 = 'D6:12 G5:12 A5:12 B5:12 C6:12 B5:12 A5:6 G5:6 G5:12 R:12'
CH5 = 'B5:12 B5:12 B5:12 A5:12 B5:12 G5:6 F#5:6 E5:12 D5:18 R:6'
CH6 = 'D6:12 E6:12 D6:12 D6:12 B5:6 C6:6 D6:12 C6:12 B5:24'
SN = S.rsplit(' ', 1)[0] + ' D4:2'                       # natural-minor tail
put('CH', 8, 1, CH1)
theme('C1', 8, 1, SN, 'Coro I: subject under chorale line 1 (tail in natural minor, against the chorale D)')
put('C2', 8, 1, 'E3:4 B2:2 C3:4 B2:2 G3:2 A3:2 B3:2 E3:3 D3:1 C3:2 '
                'G2:2 A2:1 B2:1 C3:1 D3:1 E3:2 F#3:2 E3:1 D3:1 G3:2 F#3:2 E3:2 D3:2 C#3:2 B2:2')
# second half of line 1: Coro I in sixteenths above Coro II's walking line; G - e - C#o7 - F#7 (the chorale's E is its
# 7th) - b.  The chorale's fermata is shortened by a beat, so that the line breathes before line 2.
put('C1', 10, 1, 'D5:1 C5:1 B4:1 C5:1 D5:1 B4:1 G5:1 F#5:1 E5:1 F#5:1 G5:1 E5:1 '
                 'G5:1 F#5:1 E5:1 D5:1 C#5:1 D5:1 C#5:1 D5:1 E5:1 C#5:1 A#4:1 C#5:1 '
                 'D5:2 C#5:1 B4:1 C#5:1 D5:1 E5:1 D5:1 E5:1 F#5:1 G5:2 F#5:2 E5:1 D5:1 C#5:1 B4:1 '
                 'B4:2 C5:1 B4:1 A4:1 F#4:1')
put('C2', 10, 1, 'G3:4 F#3:2 E3:6 C#3:4 E3:2 F#3:6 B2:6 G2:4 B2:2 D3:6 B2:2 R:4')

# ================================================================ IV. CHORALE LINE 2 (b12-16.2): Coro II's inversion
put('CH', 12, 1, CH2)
theme('C2', 12, 2, octv(INV, -1), 'Coro II: inversion (E minor) under chorale line 2')
put('C1', 12, 1, 'G4:1 A4:1 B4:1 C5:1 D5:1 B4:1 D5:2 C5:1 B4:1 A4:1 B4:1 D5:1 C5:1 B4:1 C5:1 E5:1 D5:1 D5:2 C5:2 B4:1 A4:1 '
                 'C5:2 B4:1 A4:1 D5:2 C5:2 D5:1 C5:1 B4:2 A4:2 B4:1 A4:1 F#4:2 G4:2 A4:2 B4:2 '
                 'E5:2 D5:2 E5:2 C5:1 B4:1 A4:1 B4:1 C5:1 D5:1 E5:2 D5:1 C5:1 B4:1 A4:1 G4:2 B4:1 A4:1 B4:1 C5:1 '
                 'D5:1 C5:1 B4:1 A4:1 C5:2 B4:12')
put('C2', 14, 2, 'A3:6 G3:6 D3:6 D3:4 F#3:2 G3:6')

# ================================================================ V. EPISODE 1 (b15.3-18.4): the questions in diminution
# The heads of the inversion ("Wen?") and of the subject ("Sehet!") at double speed, tossed between the choirs, from
# G major back to E minor; the chorale is silent from b16 (two voices, as in BWV 855).
put('C2', 15, 3, 'D3:3 D3:2 E3:1 D3:1 C3:1 B2:1 G2:2 A2:1 B2:6 E3:2 D3:2 F#3:2')   # "Wen?" (G)
put('C1', 16, 1, 'G4:3 G4:2 F#4:1 G4:1 A4:1 B4:1 D5:2 C5:1 B4:2 R:4')            # "Sehet!" (G)
put('C2', 16, 3, 'B2:3 B2:2 C3:1 B2:1 A2:1 G2:1 E2:2 F#2:1')                      # "Wen?" (e)
put('C1', 17, 1, 'E5:3 E5:2 D#5:1 E5:1 F#5:1 G5:1 B5:2 A5:1')                     # "Sehet!" (e)
put('C2', 17, 1, 'E2:6 G2:6')
# a falling sequence onto the dominant, then a breath before the Recognition
put('C1', 17, 3, 'G5:2 F#5:1 E5:1 D#5:1 E5:1 F#5:2 E5:1 D#5:1 E5:1 C5:1 '
                 'A4:2 G4:1 F#4:1 G4:1 A4:1 B4:2 A4:1 G4:1 F#4:1 E4:1 D#4:4 R:2 R:6')
put('C2', 17, 3, 'C3:6 A2:6 B2:6 B2:6 B2:4 R:2 R:6')


# ================================================================ VI. RECOGNITION (b19-23.1): chorale line 3 (= line 1)
# The choirs stop arguing.  Coro I sings the subject in G major, whose beat-notes ARE the chorale line (G G G D D E D),
# while Coro II sings it in E minor a tenth below: the subject, its relative-major twin and its source in augmentation,
# all at once.  After a beat's breath the two choirs answer together in inversion (the G-major inversion over the
# B-minor one, in sixths).
RG = 'G4:6 G4:4 F#4:2 G4:2 A4:2 B4:2 D5:4 C5:2 D5:4 B4:2 E5:6 D5:2 C5:2 B4:2 A4:2 G4:2 F#4:2'
IG = 'D5:6 D5:4 E5:2 D5:2 C5:2 B4:2 G4:4 A4:2 G4:4 B4:2 F#4:6 G4:2 A4:2 B4:2 C5:2 D5:2 E5:2'
put('CH', 19, 1, CH1)
theme('C1', 19, 1, RG, 'Recognition: Coro I, subject in G major = the chorale line in diminution')
theme('C2', 19, 1, octv(SN, -1), 'Recognition: Coro II, subject in E minor a tenth below (natural-minor tail)')
theme('C1', 21, 2, IG, 'Recognition: Coro I, inversion in G major')
INVB_NAT = octv(tr(INV, 7, 4), -1).replace('A#3:6', 'A3:6')          # A natural under the chorale's D
theme('C2', 21, 2, INVB_NAT, 'Recognition: Coro II, inversion in B minor a sixth below (A natural against the chorale D)')


# ================================================================ VII. CHORALE LINE 4 (= line 2), b23-28: the subject carried in long notes
# "Holz zum Kreuze selber tragen": Coro II takes the subject in augmentation (each beat-note now as slow as the
# chorale's), entering on the chorale's seventh beat; above it Coro I runs in sixteenths in BWV 855's manner
# (broken chords against a repeated pedal note).
put('CH', 23, 1, CH2)
put('C1', 23, 2, 'D5:2 C5:1 B4:1 A4:1 F#4:1 '
                 'B4:1 A4:1 G4:1 A4:1 B4:1 G4:1 E5:1 D5:1 C5:1 D5:1 E5:1 D5:1 '
                 'F#5:1 E5:1 D5:1 E5:1 F#5:1 D5:1 C5:1 B4:1 A4:1 B4:1 C5:1 A4:1 '
                 'D5:1 C5:1 B4:1 A4:1 G4:1 F#4:1 G4:1 B4:1 E5:1 D#5:1 E5:1 B4:1 '
                 'E5:1 D5:1 C5:1 E5:1 G5:1 E5:1 A5:1 E5:1 C5:1 E5:1 C5:1 A4:1 '
                 'B4:2 A4:1 F#4:1 A4:1 B4:1 G4:1 B4:1 E5:1 B4:1 A4:1 B4:1 '
                 'C5:2 B4:1 A4:1 B4:1 D5:1 D5:1 C5:1 B4:1 C5:1 D5:1 B4:1 G4:2 C5:1 B4:1 C5:1 E5:1 D5:2 B4:1 G4:1 B4:1 D5:1 '
                 'G5:2 E5:2 D5:1 E5:1 E5:2 C5:1 D5:1 E5:1 C5:1 A4:2 G4:1 F#4:1 G4:1 A4:1 '
                 'G4:2 A4:1 B4:1 C5:1 B4:1 F#4:2 G4:1 A4:1 B4:1 G4:1 A4:2 C5:2 G4:2 G4:2 F#4:2 A4:2')
put('C2', 23, 2, 'F#4:2 R:4')
theme('C2', 24, 4, octv(W.scale_rhythm(S, 2), -1), 'Coro II: subject in augmentation (E minor) under chorale line 4', 4)


# ================================================================ VIII. DIALOGUE 2 (b28.4-30.3), in diminution
# Sehet! - Was? - seht die Geduld. Seht! - Wohin? - auf unsre Schuld.  Coro I sings the subject at double speed, one
# beat at a time; Coro II's questions (the inversion's head, also at double speed) cut in between.
put('C1', 28, 4, 'G4:2 R:4')
put('C2', 28, 4, 'E3:2 R:4')
put('C1', 29, 1, 'E5:3 E5:2 D#5:1')                      # Sehet!
put('C2', 29, 2, 'B3:3 B3:2 C4:1')                       # Was?
put('C1', 29, 3, 'E5:1 F#5:1 G5:1 B5:2 A5:1 B5:2 G5:1 C6:3')   # seht die Geduld. Seht!
put('C2', 29, 3, 'E3:2 R:4 E3:2 R:4')
put('C2', 30, 1, 'F#3:3 F#3:2 G3:1')                     # Wohin?
put('C1', 30, 2, 'B5:1 A5:1 G5:1 F#5:1 E5:1 D#5:1 E5:2 R:4')   # auf unsre Schuld
put('C2', 30, 2, 'B2:6 E3:2 R:4')

# ================================================================ IX. CHORALE LINE 5 (b31-35): the choirs exchange forms
# Coro I now sings the inversion (from b30.4, a beat before the chorale), Coro II the subject (b31.2): a stretto at two
# beats, each choir in the other's form.  The line closes in B minor (the chorale's E is the seventh of F#7, as in line 1).
put('CH', 31, 1, CH5)
theme('C1', 30, 4, IG, 'Coro I: inversion (G major), a beat before chorale line 5 (stretto 1)')
theme('C2', 31, 2, octv(S, -1), 'Coro II: subject (E minor), two beats later (stretto 2)')

# line 5, second half: B minor, the chorale descending to its lowest note; E over F#7 into b (b34.3)
put('C1', 32, 4, 'D5:2 C5:2 B4:2 A4:2 G4:2 F#4:2 B4:2 A4:1 G4:1 F#4:1 G4:1 C5:2 B4:1 A4:1 B4:1 C5:1 '
                 'D5:2 C#5:1 B4:1 A4:1 F#4:1 G4:2 A4:1 B4:1 C#5:1 B4:1 A#4:2 B4:1 C#5:1 A#4:1 C#5:1 '
                 'B4:2 F#4:1 G4:1 F#4:1 E4:1 D4:2 E4:1 F#4:1 G4:1 E4:1 F#4:4 R:2 R:6 '
                 'B4:1 C#5:1 D5:1 E5:1 F#5:1 D5:1 E5:1 C#5:1 A#4:1 B4:1 C#5:1 A#4:1 '
                 'F#5:2 E5:1 D5:1 E5:1 F#5:1 G5:2 F#5:1 E5:1 D5:2')
put('C2', 33, 2, 'E3:6 A2:6 D3:6 C#3:4 A#2:2 F#2:6 B2:6 B2:4 C#3:2 D3:4 E3:2 F#3:4 E3:2 D3:4 C#3:2')

# ================================================================ X. CHORALE LINE 6 (b36-40.2): both choirs in G major, stretto
# Coro I the G-major inversion (b36.3), Coro II the G-major subject (b37.1); then a Phrygian half cadence on B.
put('CH', 36, 1, CH6)
put('C2', 36, 1, 'B2:4 A2:2 G2:6 E3:6 R:6')
SBG = 'B4:6 B4:4 A4:2 B4:2 C5:2 D5:2 F#5:4 E5:2 F#5:4 D5:2 G5:6 F#5:2 E5:2 D5:2 C5:2 B4:2 A4:2'   # on B, diatonic in G
theme('C1', 37, 1, SBG, 'Coro I: subject on B (diatonic in G major) under chorale line 6, a tenth above Coro II')
theme('C2', 37, 1, octv(RG, -1), 'Coro II: subject (G major) a tenth below')

# half cadence: VI6 - iv - V (b39-40), the chorale's B over the dominant
put('C1', 39, 1, 'G4:2 A4:1 B4:1 C5:1 A4:1 E5:2 D5:1 C5:1 B4:1 E5:1 D#5:12')
put('C2', 39, 1, 'E3:6 A2:6 B2:12')

# ================================================================ XI. THE BREATH (b40.3-42.4): a pulsing dominant pedal
# As at the opening of BWV 244/1 (whose tonic pedal pulses in eighths), Coro II pulses on B while Coro I falls in
# sixteenths through the subject's head; then both choirs stop for a beat before the last line.
put('C2', 40, 3, 'B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 '
                 'B2:2 B2:2 B2:2 B2:2 B2:2 B2:2 B2:6 R:6')
put('C1', 40, 3, 'F#5:3 E5:2 D#5:1 D#5:1 E5:1 F#5:1 A5:2 G5:1 '
                 'F#5:1 E5:1 D#5:1 E5:1 F#5:1 D#5:1 B4:1 C5:1 B4:1 A4:1 G4:1 F#4:1 '
                 'A4:1 G4:1 F#4:1 G4:1 A4:1 F#4:1 D#4:2 E4:1 F#4:1 G4:1 A4:1 '
                 'B4:2 A4:1 G4:1 F#4:1 E4:1 D#4:1 E4:1 F#4:1 A4:1 G4:1 F#4:1 D#4:6 R:6')

# ================================================================ XII. CHORALE LINE 7 (b43-47.3): the final stretto
# "Erbarm dich unser, o Jesu": Coro II's inversion (b45.1) and Coro I's subject (b45.3) in stretto beneath the last line,
# with nothing else sounding: the subject's leading tone resolves with the chorale's final G (b47.3), which is the
# third of E minor.
CH7 = 'E6:12 D6:6 C6:6 B5:12 A5:12 B5:12 D6:12 B5:12 A5:24 G5:60'
put('CH', 43, 1, CH7)
put('C1', 43, 1, 'E5:1 D5:1 C5:1 D5:1 E5:1 G5:1 C5:1 B4:1 A4:1 B4:1 C5:1 A4:1 '
                 'D5:1 C5:1 B4:1 C5:1 D5:1 B4:1 E5:1 D5:1 C5:1 B4:1 A4:1 F#4:1 '
                 'G4:2 A4:1 B4:1 C5:1 A4:1 B4:2 G4:1 A4:1 B4:1 G4:1 C5:2 A4:1 B4:1 C5:1 A4:1 B4:2 A4:1 F#4:1 A4:1 F#4:1 '
                 'G4:2 R:4 R:6')
put('C2', 43, 1, 'C4:4 B3:2 A3:6 B3:4 G3:2 A3:6 E3:6 G3:6 F#3:6 R:6')
INV_END = octv(INV, -1).rsplit(' ', 2)[0] + ' G3:2 F#3:2'     # the tail turns down into the cadence
theme('C2', 45, 1, INV_END, 'Final stretto: Coro II, inversion (E minor) under the last chorale line (tail turned down to the dominant)')
theme('C1', 45, 3, S, 'Final stretto: Coro I, subject (E minor), two beats later: the final cadence')

# ================================================================ XIII. CODA (b47.3-49.4)
put('C2', 47, 1, 'B3:12 E3:12 E3:24 E2:24')
put('C1', 47, 3, 'E4:2 G4:2 B4:2 E5:3 D#5:1 E5:2 C5:4 B4:2 A4:4 G4:2 F#4:4 E4:2 C5:4 B4:2 B4:24')

MARKS = [(1, 'Exposition: Coro I subject, Coro II inversion'), (5, 'Dialogue: Sehet! - Wen? - Wie?'),
         (8, 'Chorale line 1 over the subject'), (12, 'Line 2 over the inversion'),
         (16, 'Episode: the questions in diminution'), (19, 'Recognition (line 3)'),
         (23, 'Line 4: subject in augmentation'), (29, 'Dialogue in diminution: Was? - Wohin?'),
         (31, 'Line 5: stretto, forms exchanged'), (37, 'Line 6: tenths'), (40, 'Dominant pedal; breath'),
         (43, 'Line 7: final stretto'), (48, 'Coda')]
DYN = {1: -4, 5: -2, 8: 2, 10: 3, 12: 2, 16: -3, 19: 6, 21: 4, 23: 2, 25: 4, 29: 0, 31: 4, 33: 3,
       36: 5, 39: 6, 40: 2, 42: 4, 43: 8, 47: 6, 48: 2, 49: 0}
QUESTIONS = [(30, 31.5), (36, 37.5), (87, 90), (93, 96), (169.5, 171), (174, 175.5)]   # Coro II: Wen? Wie? (dim) Was? Wohin?
SEATS = {'Choral (soprano in ripieno)': [0.0, 4.0], 'Coro I': [-55.0, 6.0], 'Coro II': [55.0, 6.0]}


def dynamics(b):
    v = 0
    for k in sorted(DYN):
        if b + 1 >= k:
            v = DYN[k]
    return v


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    end = nbars * 6
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue X in E minor, three voices: Fuga a due cori con corale',
            'composer': 'Claude / Sam (chorale: Nikolaus Decius, "O Lamm Gottes, unschuldig"; after J. S. Bach, BWV 244 no. 1)',
            'instrument': 'Keyboard, three voices (two choirs and a chorale)',
            'key': 'E', 'mode': 'minor', 'meter': list(METER), 'bpm': 90,
            'tempo_text': 'Andante con moto (dotted quarter = 60)',
            # t in quarters (one 12/8 bar = 6).  Small breaths at the cadences of lines 1, 2 and 5 and before line 5's
            # stretto; a ritardando into the general pause before the Recognition (b18.4); the half cadence (b39-40)
            # broadens and the dominant pedal is a tempo; a breath into the last line (b42.4), which is a little
            # broader; the final ritardando from the cadence (b47.3).
            'tempo_map': [[57, 90], [60, 84, 'ramp'], [61.5, 90, 'ramp'],
                          [82.5, 90], [85.5, 84, 'ramp'], [87, 90, 'ramp'],
                          [103.5, 90], [108, 72, 'ramp'], [108, 90],
                          [175.5, 90], [178.5, 84, 'ramp'], [180, 90, 'ramp'],
                          [199.5, 90], [202.5, 84, 'ramp'], [205.5, 90, 'ramp'],
                          [228, 90], [234, 80, 'ramp'], [237, 90],
                          [246, 90], [250.5, 76, 'ramp'], [252, 86],
                          [270, 86], [279, 74, 'ramp'], [288, 60, 'ramp'], [end, 48, 'ramp']],
            'movement_number': 10, 'piece_type': 'fugue', 'edition': 'third', 'voice_order': 'high_to_low',
            'markers': [{'t': float((b - 1) * 6), 'label': t} for b, t in MARKS]}
    voices = [(LONG[i], ['Ch', 'I', 'II'][i], CLEF[i], [74, 68, 66][i]) for i in range(3)]
    data = W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES, subject=S, dynamics=dynamics)
    # Performance data only (no pitches or rhythms change): Coro II's questions are accented and detached; each
    # voice gets a seat for the binaural render (--layout score): Coro I left, Coro II right, the chorale in front.
    for v in data['voices']:
        v['spatial'] = SEATS[v['name']]
        if v['name'] == 'Coro II':
            for e in v['events']:
                if any(a <= e['t'] < z for a, z in QUESTIONS):
                    e['v'] = max(24, min(118, e['v'] + 6))
                    e['gate'] = 0.72
    (HERE / 'fugue.json').write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // BAR))
    build(nb)
    print('bars', nb)
