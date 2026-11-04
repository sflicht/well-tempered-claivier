#!/usr/bin/env python3
"""Checks of render_walk.draw_map() (the --map PNG). Run: python3 tools/test_walk_map.py

A made-up walk retraces its first lap mirror-reversed and stops at the centre four times (the
case where the old map drew lap 2 over lap 1 and piled the time labels into a blot):
- each hearing state has its own panel, holding only the path walked in that state;
- every spot where the listener stands gets one label listing all its stays;
- no two labels overlap, and labels keep off the path drawn in their panel.
The PNG goes to a temporary directory; nothing in the repository is written.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_music as rm  # noqa: E402
import render_walk as rw  # noqa: E402

LAP = [(5.0, 4.0, 0), (6.5, 5.5, 45), (6.5, 2.5, 135), (3.5, 2.5, 225), (5.0, 4.0, 315)]


def walk_score():
    keys, t = [], 0.0
    for lap in range(2):
        for x, y, f in LAP:
            f += 360 * lap
            keys += [[t, x, y, f], [t + 4, x, y, f]]   # stand 4 beats, then walk 4
            t += 8
    keys.append([t + 8, 5.0, 4.0, 720 + 270])          # a coda turning on the spot
    seats = [[2.5, 6.5], [7.5, 6.5], [7.5, 1.5], [2.5, 1.5]]
    return {'metadata': {'meter': [4, 4], 'bpm': 60, 'key': 'C',
                         'walk': {'room': [10.0, 8.0], 'listener': keys, 'mirror': [[38.0, 78.0]]}},
            'voices': [{'name': f'Player {k + 1}', 'seat': s, 'events': [{'t': 0, 'd': t + 8, 'p': 60 + k}]}
                       for k, s in enumerate(seats)]}


def draw(data):
    meta = rm.meta_of(data)
    pts = rm.tempo_points(meta)
    n_ctrl = int((rm.seconds_at(float(rm.score_duration(data)), pts) + 1) * rw.CTRL) + 2
    track = rw.listener_track(meta['walk'], pts, n_ctrl)
    mirror = rw.mirror_track(meta['walk'], pts, n_ctrl)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'map.png'
        panels = rw.draw_map(data, track, mirror, out)
        assert out.stat().st_size > 10000
    return panels, track, mirror


def overlap(a, b):
    return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))


def test_each_lap_has_its_own_panel():
    panels, track, mirror = draw(walk_score())
    assert [p['mirrored'] for p in panels] == [False, True], [p['mirrored'] for p in panels]
    for p in panels:
        for a, b in p['spans_s']:
            flags = mirror[int(a * rw.CTRL) + 5:int(b * rw.CTRL) - 5] < 0
            assert flags.size and (flags == p['mirrored']).all(), (p['mirrored'], a, b)
    # the mirrored lap retraces the first: both panels draw the same square
    for p in panels:
        assert p['path'][:, 0].min() < 3.6 and p['path'][:, 0].max() > 6.4


def test_one_label_per_spot_listing_every_stay():
    panels, _, _ = draw(walk_score())
    for p in panels:
        stays = [t for t, _ in p['labels'] if ' s ' in t and not t.startswith('mirror')]
        assert len(stays) == len(LAP) - 1, stays       # the centre is visited twice per lap: one label
        centre = max(stays, key=lambda t: t.count('\n'))
        assert centre.count(' s ') >= 2, centre
    normal = panels[0]['labels']
    assert any('right to ←' in t for t, _ in normal), normal   # the coda turns right on the spot to face left


def test_labels_do_not_overlap_each_other_or_the_path():
    panels, _, _ = draw(walk_score())
    for p in panels:
        boxes = [b for _, b in p['labels']]
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                assert overlap(boxes[i], boxes[j]) == 0, (p['labels'][i][0], p['labels'][j][0])
        path = p['path'][::20]
        for text, (x0, y0, x1, y1) in p['labels']:
            inside = np.sum((path[:, 0] > x0) & (path[:, 0] < x1) & (path[:, 1] > y0) & (path[:, 1] < y1))
            assert inside <= 0.02 * len(path), (text, int(inside))


def main():
    tests = [(n, f) for n, f in globals().items() if n.startswith('test_') and callable(f)]
    failed = 0
    for name, f in tests:
        try:
            f()
            print(f'ok    {name}')
        except AssertionError as e:
            failed += 1
            print(f'FAIL  {name}: {e}')
    print(f'{len(tests) - failed}/{len(tests)} passed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
