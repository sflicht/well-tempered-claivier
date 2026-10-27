#!/usr/bin/env python3
"""Workshop for the table canon: derive, verify and inspect a candidate.

    python3 table_workshop.py [--grid] [--bars 9-24] [--file candidate.py]

A candidate module defines DUX (32 bar strings, 3/4, sixteenth units): the one
line printed on the page.  The comes is its retrograde inversion about D4, i.e.
the same page read by a player sitting on the other side of the table.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

from canon_tools import W, flatten, rinv, check_rotation, short_report, dyad_grid, sixteenth_rule, HERE

METER = (3, 4)


def derive(dux_bars):
    s1 = flatten(dux_bars)
    s2 = rinv(s1)
    return s1, s2, W.concat_bars(s2, METER)


def score(dux_bars, comes_bars, bpm=60):
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'workshop', 'key': 'C', 'mode': 'major',
            'meter': list(METER), 'bpm': bpm}
    voices = [('Dux', 'D', 'treble', 70), ('Comes', 'C', 'bass', 68)]
    return W.build_score(HERE / '_workshop.json', meta, voices, {'Dux': dux_bars, 'Comes': comes_bars})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--file', default='table_canon.py')
    ap.add_argument('--grid', action='store_true')
    ap.add_argument('--bars')
    ap.add_argument('--step', type=int, default=4)
    ap.add_argument('--comes', action='store_true')
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location('cand', HERE / a.file)
    mod = importlib.util.module_from_spec(spec)
    sys.argv = [sys.argv[0], '--no-write']
    spec.loader.exec_module(mod)
    dux = mod.DUX
    s1, s2, comes = derive(dux)
    bad = check_rotation(s1, s2)
    print('rotation check:', 'OK' if not bad else bad[:5])
    if a.comes:
        for i, b in enumerate(comes):
            print(f'  comes {i + 1:>2}: {b}')
    data = score(dux, comes)
    short_report(data)
    rule = sixteenth_rule(s1, s2)
    print(f'sixteenth-rule violations ({len(rule)}):', '; '.join(rule))
    if a.grid:
        rng = tuple(int(x) for x in a.bars.split('-')) if a.bars else None
        dyad_grid(s1, s2, 12, a.step, rng)
    (HERE / '_workshop.json').unlink(missing_ok=True)


if __name__ == '__main__':
    main()
