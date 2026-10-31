#!/usr/bin/env python3
"""Fugue X in E minor, three voices: "Fuga a due cori con corale".

WORK IN PROGRESS (recomposition at Bach + 1 = three voices).
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
CH5 = 'B5:12 B5:12 B5:12 A5:12 B5:12 G5:6 F#5:6 E5:12 D5:24'
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
put('C2', 10, 1, 'G3:4 F#3:2 E3:6 C#3:4 E3:2 F#3:6 B2:6 G2:4 E2:2 D3:6 B2:2 R:4')

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
                 'B4:1 A4:1 G4:1 A4:1 B4:1 G4:1 E5:1 D5:1 C5:1 D5:1 E5:1 C5:1 '
                 'F#5:1 E5:1 D5:1 E5:1 F#5:1 D5:1 C5:1 B4:1 A4:1 B4:1 C5:1 A4:1 '
                 'D5:1 C5:1 B4:1 A4:1 G4:1 F#4:1 G4:1 B4:1 E5:1 D#5:1 E5:1 B4:1 '
                 'C5:1 B4:1 C5:1 E5:1 G5:1 E5:1 A5:1 E5:1 C5:1 E5:1 C5:1 A4:1 '
                 'B4:2 A4:1 F#4:1 A4:1 B4:1 G4:1 B4:1 E5:1 B4:1 A4:1 B4:1 '
                 'C5:2 B4:1 A4:1 B4:1 D5:1 D5:1 C5:1 B4:1 C5:1 D5:1 B4:1 G4:2 C5:1 B4:1 C5:1 E5:1 D5:2 B4:1 G4:1 B4:1 D5:1 '
                 'G5:2 F#5:1 E5:1 D5:1 E5:1 E5:2 D5:1 C5:1 B4:1 A4:1 F#4:2 G4:1 A4:1 G4:1 F#4:1 '
                 'E5:2 D#5:1 E5:1 F#5:1 E5:1 F#4:2 G4:1 A4:1 B4:1 G4:1 A4:2 C5:2 G4:2 G4:2 F#4:2 A4:2')
put('C2', 23, 2, 'F#4:2 R:4')
theme('C2', 24, 4, octv(W.scale_rhythm(S, 2), -1), 'Coro II: subject in augmentation (E minor) under chorale line 4', 4)


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue X in E minor, three voices: Fuga a due cori con corale',
            'composer': 'Claude / Sam (chorale: Nikolaus Decius, "O Lamm Gottes, unschuldig"; after J. S. Bach, BWV 244 no. 1)',
            'instrument': 'Keyboard (three voices)',
            'key': 'E', 'mode': 'minor', 'meter': list(METER), 'bpm': 90,
            'tempo_text': 'Andante con moto (dotted quarter = 60)',
            'movement_number': 10, 'piece_type': 'fugue', 'edition': 'third', 'voice_order': 'high_to_low'}
    voices = [(LONG[i], ['Ch', 'I', 'II'][i], CLEF[i], [74, 68, 66][i]) for i in range(3)]
    data = W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES, subject=S)
    return data


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // BAR))
    build(nb)
    print('bars', nb)
