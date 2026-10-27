#!/usr/bin/env python3
"""Prelude X in E minor: "Aria e Presto" (third edition), 4/4.

After WTC I's E-minor prelude, BWV 855: a long-breathed aria over a steady
left-hand figure, which bursts into a two-part Presto.

Aria (b1-17).  The right hand sings a paraphrase of the chorale "O Lamm
Gottes, unschuldig" (Nikolaus Decius, 1522/1531), the chorale the Fugue
carries as its eleventh voice: lines 1, 2, 5, 6 and 7 of the tune, moved into
the relative minor (each note a diatonic third lower, so G-G-G-D-D-E-D becomes
E-E-E-B-B-C-B, the Fugue subject's skeleton), ornamented and re-timed.  Line 5
is sung in G major, the chorale's own key, over the ground transposed.  The
left hand plays a walking ostinato: a chromatic lament ground descending
E-D#-D-C#-C-B in half notes, with a pulsing eighth-note figure above it.

Presto (b18-35).  Two-part invertible counterpoint: a running sixteenth-note
motive M (the subject's beat-notes E E E B | B C B, figured) against an
eighth-note counter-line C.  E minor (M over C, b18) -> B minor with the hands
exchanged (b20) -> a fifths-sequence episode on M's head (b22) -> G major
(b24) -> E minor exchanged again (b26) -> M in canon with itself a beat
later (b28) -> dominant pedal (b30-33) -> run-out on D-sharp (b35), attacca
into the Fugue's first E.

Every pitch is written here.  Playable by one pianist: right hand = aria /
upper Presto line; left hand = ground + figure / lower Presto line.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
B = W.Bars(['RH', 'Figure', 'Bass'], METER)


def fig(*halves):
    """Left-hand figure: each argument is four pitch names (one half bar of eighths)."""
    return ' '.join(f'{p}:2' for h in halves for p in h.split())


EM, B7D, EMD, CSO, AMC, B7 = ('G3 B3 G3 B3', 'A3 F#3 A3 F#3', 'G3 B3 G3 B3', 'E3 G3 E3 G3', 'E3 A3 E3 A3', 'F#3 B3 F#3 A3')
GROUND = ['E3:8 D#3:8', 'D3:8 C#3:8', 'C3:8 B2:8']
FIGS = [fig(EM, B7D), fig(EMD, CSO), fig(AMC, B7)]

# ---------------------------------------------------------------- ARIA (q = 56)
B.bar('1 the ground alone', Figure=fig(EM, EM), Bass='E3:16')
# phrase 1 = chorale line 1 (O Lamm Gottes, unschuldig): E E E B | C B, half cadence
B.bar('2 line 1', RH='E5:8 E5:6 D#5:2', Figure=FIGS[0], Bass=GROUND[0])
B.bar('3', RH='E5:4 F#5:2 G5:2 B4:8', Figure=FIGS[1], Bass=GROUND[1])
B.bar('4 half cadence', RH='C5:4 A4:4 B4:8', Figure=FIGS[2], Bass=GROUND[2])
# phrase 2 = line 2 (am Stamm des Kreuzes geschlachtet): B E F# G A G F# E
B.bar('5 line 2', RH='B4:4 E5:4 F#5:6 E5:2', Figure=FIGS[0], Bass=GROUND[0])
B.bar('6', RH='G5:6 F#5:2 A5:4 G5:4', Figure=FIGS[1], Bass=GROUND[1])
B.bar('7', RH='A5:2 G5:2 F#5:2 E5:2 F#5:8', Figure=FIGS[2], Bass=GROUND[2])
# phrase 3 = line 5 in G major (All Suend hast du getragen) over the ground moved to the relative major
B.bar('8 line 5, G major', RH='E5:4 D5:2 B4:2 A4:8', Figure=fig('B3 D4 B3 D4', 'D4 A3 D4 A3'), Bass='G3:8 F#3:8')
B.bar('9', RH='B4:6 D5:2 C5:4 E5:4', Figure=fig('D4 B3 G3 B3', 'G3 C4 G3 C4'), Bass='F3:8 E3:8')
B.bar('10', RH='G4:4 C5:4 D5:6 C5:2', Figure=fig('G3 C4 G3 C4', 'A3 C4 A3 F#3'), Bass='Eb3:8 D3:8')
# phrase 4 = line 6 (sonst muessten wir verzagen): B C B | B A G A | A C B
B.bar('11 line 6', RH='B4:8 C5:4 B4:4', Figure=FIGS[0], Bass=GROUND[0])
B.bar('12', RH='B4:6 C5:1 B4:1 B4:2 A4:2 G4:2 A4:2', Figure=FIGS[1], Bass=GROUND[1])
B.bar('13 half cadence', RH='C5:4 A4:4 B4:8', Figure=FIGS[2], Bass=GROUND[2])
# phrase 5 = line 7 (Erbarm dich unser, o Jesu): C B A G E | C E D# E
B.bar('14 line 7', RH='C5:4 B4:4 B4:6 A4:2', Figure=FIGS[0], Bass=GROUND[0])
B.bar('15', RH='G4:8 E5:6 D5:2', Figure=FIGS[1], Bass=GROUND[1])
B.bar('16', RH='C5:4 E5:4 D#5:8', Figure=FIGS[2], Bass=GROUND[2])
B.bar('17 cadence', RH='E5:16', Figure=fig(EM, 'G3 B3 E4 B3'), Bass='E3:16')


# ---------------------------------------------------------------- PRESTO (quarter = 132): two-part invertible counterpoint
# M: the subject's beat-notes E E E B | B C B (D#) figured in sixteenths.  C: its eighth-note counter-line.
M = ('E5:1 D#5:1 E5:1 B4:1 E5:1 F#5:1 G5:1 E5:1 E5:1 D#5:1 E5:1 G5:1 B5:1 A5:1 G5:1 F#5:1 '
     'B5:1 A#5:1 B5:1 G5:1 C6:1 B5:1 A5:1 C6:1 B5:1 A5:1 G5:1 F#5:1 G5:1 F#5:1 E5:1 D#5:1')
C = 'G3:2 B3:2 C4:2 B3:2 A3:2 G3:2 F#3:2 D#3:2 E3:2 G3:2 A3:2 F#3:2 D#3:2 B2:2 E3:2 F#3:2'


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def two(rh, lh):
    """Add bars from two equal-length lines (right hand, left hand)."""
    r, l = W.concat_bars(rh, METER), W.concat_bars(lh, METER)
    for a, b in zip(r, l):
        B.bar('presto', RH=a, Bass=b)


two(M, C)                                                     # 18-19 motive above, counter-line below (E minor)
two(tr(C, 19, 11), tr(M, -17, -10))                           # 20-21 hands exchanged, B minor (inversion at the double octave)
# 22-23 episode: the motive's head (x, lower neighbour, x, fourth below) in a fifths sequence, B minor -> E minor -> A minor -> D
two('D5:1 C#5:1 D5:1 A4:1 B4:1 C#5:1 D5:1 B4:1 G4:1 F#4:1 G4:1 D4:1 E4:1 F#4:1 G4:1 E4:1 '
    'C5:1 B4:1 C5:1 G4:1 A4:1 B4:1 C5:1 A4:1 F#4:1 E4:1 F#4:1 D4:1 C4:1 D4:1 E4:1 F#4:1',
    'B3:2 A3:2 G3:2 F#3:2 E3:2 F#3:2 G3:2 A3:2 A3:2 G3:2 F#3:2 E3:2 D3:2 C3:2 B2:2 A2:2')
# 24-25 the motive in G major, the chorale's own key: M and C moved a diatonic third up (D# -> F#, A# -> C#), written out
two('G4:1 F#4:1 G4:1 D4:1 G4:1 A4:1 B4:1 G4:1 G4:1 F#4:1 G4:1 B4:1 D5:1 C5:1 B4:1 A4:1 '
    'D5:1 C#5:1 D5:1 B4:1 E5:1 D5:1 C5:1 E5:1 D5:1 C5:1 B4:1 A4:1 B4:1 A4:1 G4:1 F#4:1',
    'B2:2 D3:2 E3:2 D3:2 C3:2 B2:2 A2:2 F#2:2 G2:2 B2:2 C3:2 A2:2 F#2:2 D2:2 G2:2 A2:2')
two(tr(C, 12, 7), tr(M, -24, -14))                            # 26-27 exchanged again, E minor
B.bars['RH'][-1] = B.bars['RH'][-1].rsplit(' ', 1)[0] + ' B4:2'   # last eighth F#4 -> B4, so the canon's E5 follows by a fourth
two(M + ' E5:4 R:12', 'R:4 ' + tr(M, -24, -14) + ' E3:12')    # 28-30.1 canon: the motive against itself one beat later
B.bars['RH'][-1] = 'E5:4 F#5:1 G5:1 A5:1 B5:1 C6:1 B5:1 A5:1 G5:1 F#5:1 E5:1 D#5:1 E5:1'
B.bars['Bass'][-1] = 'G3:1 F#3:1 E3:1 D#3:1 E3:4 B2:2 B3:2 B2:2 B3:2'
B.tags[-1] = 'presto: dominant'
B.bar('presto: dominant pedal', RH='B4:1 A#4:1 B4:1 F#4:1 B4:1 C5:1 B4:1 A4:1 G4:1 A4:1 B4:1 G4:1 C5:1 B4:1 A4:1 G4:1',
      Bass='B2:2 B3:2 B2:2 B3:2 B2:2 B3:2 B2:2 B3:2')
B.bar('presto', RH='F#4:1 E4:1 D#4:1 E4:1 F#4:1 G4:1 A4:1 B4:1 C5:1 B4:1 A4:1 G4:1 F#4:1 E4:1 D#4:1 F#4:1',
      Bass='B2:2 B3:2 B2:2 B3:2 B2:2 B3:2 B2:2 B3:2')
B.bar('presto: rising', RH='B3:1 D#4:1 F#4:1 A4:1 B4:1 D#5:1 F#5:1 A5:1 B5:1 A5:1 F#5:1 D#5:1 B4:1 A4:1 F#4:1 D#4:1',
      Bass='B2:2 B3:2 B2:2 B3:2 B2:2 B3:2 B2:2 B3:2')
B.bar('presto: run-out', RH='E4:1 D#4:1 E4:1 F#4:1 G4:1 F#4:1 E4:1 D#4:1 E4:1 F#4:1 G4:1 A4:1 C5:1 B4:1 A4:1 G4:1',
      Bass='B2:2 B3:2 G3:2 E3:2 C3:2 E3:2 C3:2 A2:2')
B.bar('presto: attacca on the leading tone', RH='F#4:2 A4:2 G4:2 F#4:2 E4:4 D#4:4', Bass='B2:8 B1:8')


def build():
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Prelude X in E minor: Aria e Presto',
            'composer': 'Claude / Sam (after J. S. Bach, BWV 855; aria paraphrases the chorale "O Lamm Gottes, unschuldig", N. Decius)',
            'instrument': 'Keyboard (one player)', 'key': 'E', 'mode': 'minor', 'meter': list(METER), 'bpm': 56,
            'tempo_text': 'Aria: Adagio cantabile (quarter = 56) - Presto (quarter = 132)',
            # aria breathes into its cadence (b16-17), Presto from b18 (t = 68), broadening only into the attacca
            'tempo_map': [[60, 56], [66, 48, 'ramp'], [68, 132], [132, 132], [140, 96, 'ramp']],
            'movement_number': 10, 'piece_type': 'prelude', 'edition': 'third'}
    voices = [('Right hand', 'RH', 'treble', 70), ('Left-hand figure', 'Fig', 'bass', 52), ('Left-hand ground', 'Bs', 'bass', 60)]
    bars = {'Right hand': B.bars['RH'], 'Left-hand figure': B.bars['Figure'], 'Left-hand ground': B.bars['Bass']}
    dyn = {1: 0, 18: 8, 22: 4, 24: 6, 26: 8, 28: 10, 30: 8, 33: 10, 35: 4}   # aria cantabile; Presto forte, episode a shade softer

    def dynamics(b):
        v = 0
        for k in sorted(dyn):
            if b + 1 >= k:
                v = dyn[k]
        return v
    return W.build_score(HERE / 'prelude.json', meta, voices, bars, tags=B.tags, dynamics=dynamics)


if __name__ == '__main__':
    build()
    print('bars', len(B))
