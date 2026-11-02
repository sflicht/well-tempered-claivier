#!/usr/bin/env python3
"""Evaluate a candidate melody M for the canon per tempora with tools/critic.py.

    python3 tempo_workshop.py "<M tokens>" [--grid] [--bars 17-24]
    python3 tempo_workshop.py --from tempo_canon.py [--grid]
"""
import argparse
import importlib.util
import sys

from canon_tools import W, HERE
from tempo_tools import derive, report, chord_grid

VOICES = [('Bass (Big Ben, x4)', 'B', 'bass', 4, -24, -14),
          ('Tenor (x3)', 'T', 'bass', 3, -12, -7),
          ('Alto (x2)', 'A', 'treble', 2, 0, 0),
          ('Soprano (x1)', 'S', 'treble', 1, 12, 7)]


def build(m, bpm=100, path=None):
    bars, T, streams = derive(m, VOICES)
    meta = {'title': 'workshop', 'subtitle': 'canon per tempora', 'key': 'E', 'mode': 'major',
            'meter': [6, 4], 'bpm': bpm}
    data = W.build_score(path or (HERE / '_tw.json'), meta, [v[:3] + (70,) for v in VOICES],
                         {v[0]: bars[v[0]] for v in VOICES})
    return data, bars, T, streams


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('m', nargs='?')
    ap.add_argument('--from', dest='src')
    ap.add_argument('--grid', action='store_true')
    ap.add_argument('--bars')
    a = ap.parse_args()
    if a.src:
        spec = importlib.util.spec_from_file_location('cand', HERE / a.src)
        mod = importlib.util.module_from_spec(spec)
        sys.argv = [sys.argv[0], '--no-write']
        spec.loader.exec_module(mod)
        m = mod.M
    else:
        m = a.m
    data, bars, T, streams = build(m)
    report(data)
    if a.grid:
        rng = tuple(int(x) for x in a.bars.split('-')) if a.bars else None
        chord_grid(streams, T, [v[0] for v in VOICES], 4, rng)
    (HERE / '_tw.json').unlink(missing_ok=True)


if __name__ == '__main__':
    main()
