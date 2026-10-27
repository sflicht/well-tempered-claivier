#!/usr/bin/env python3
"""Fugue XXIV in B minor -- the convergence, as a standalone study (stage 1).

Fourteen bars: one lead-in bar on the dominant (c0, standing in for the end of the
build-up), the eleven bars of the cantus (the twelve-tone subject in four-fold
augmentation in the Contrabass, c1-c11), and a two-bar close.  Over the cantus four
earlier subjects of this edition return as guests, three of them at their own pitch:
Fugue V (D major) over the cantus's B-D-C#, Fugue VIII (E-flat = D-sharp minor) over the
cantus's held D#, Fugue II (C minor) over C-B, Fugue IV (transposed to B minor) over the
final chromatic climb G-G#-A-A#-B.  Every note is written in conv_a.py, conv_b.py and
conv_c.py; the themes are explicit transpositions of the material in xxiv.py.

Build:  python3 cycle/24-b-minor/convergence.py   -> convergence.json
Check:  python3 cycle/24-b-minor/check.py cycle/24-b-minor/convergence.json
        python3 cycle/24-b-minor/nct.py cycle/24-b-minor/convergence.json
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from xxiv import *  # noqa
from conv_a import part_a, plan_a  # noqa
from conv_b import part_b, plan_b  # noqa
from conv_c import part_c, plan_c  # noqa

NB = 14


def themes_json(sc):
    return [{'voice': v, 't': float(t / 4), 'label': l, 'key': k, 'scale': s, 'semis': se, 'inverted': inv}
            for v, t, l, k, s, se, inv in sc.entries]


def main():
    sc = Score(1)
    part_a(sc, 1); part_b(sc, 1); part_c(sc, 1)
    bars = sc.bars(NB)
    voices = [(n, n, clef, 64 if n != 'B5' else 70) for n, long, clef in VOICES]
    names = {n: long for n, long, clef in VOICES}
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue XXIV in B minor: the convergence (study, 25 voices)',
            'composer': 'Claude / Sam', 'instrument': '25 players or ranks', 'key': 'B', 'mode': 'minor',
            'meter': [4, 4], 'bpm': 58, 'tempo_text': 'Largo, con fuoco',
            'tempo_map': [[36, 58], [44, 50, 'ramp'], [48, 50], [56, 40, 'ramp']],
            'movement_number': 24, 'piece_type': 'fugue-study', 'edition': 'third',
            'credits': 'Guest subjects quoted from this edition: Fugue II (C minor), IV (C-sharp minor), V (D major), '
                       'VIII (E-flat minor; its head is J. S. Bach, WTC I/8, BWV 853).',
            'markers': [{'t': 4, 'label': 'cantus (subject x4)'}, {'t': 5.5, 'label': 'Fugue V'},
                        {'t': 20, 'label': 'D# minor: Fugue VIII'}, {'t': 30, 'label': 'Fugue II'},
                        {'t': 39, 'label': 'Fugue IV'}, {'t': 44, 'label': 'arrival'}],
            'score_layout': {'paper': 'a2', 'hide_empty_staves': True}}
    entries = [(v, 1 + int(t // 16), float((t % 16) / 4), lab, 2) for v, t, lab, k, s, se, inv in sc.entries]
    entries = [(names[v], b, off, lab, n) for v, b, off, lab, n in entries]
    data = W.build_score(HERE / 'convergence.json', meta,
                         [(names[n], n, clef, base) for n, _, clef, base in voices],
                         {names[n]: bars[n] for n in NAMES}, entries=entries, subject=S, entry_boost=8,
                         extra={'harmonic_plan': plan_a(0) + plan_b(20) + plan_c(36), 'themes': themes_json(sc)})
    print('bars', NB, 'voices', len(data['voices']))


if __name__ == '__main__':
    main()
