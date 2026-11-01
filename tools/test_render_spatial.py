#!/usr/bin/env python3
"""Geometry checks for render_spatial.place(). Run: python3 tools/test_render_spatial.py"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_spatial as rs  # noqa: E402

RATE = rs.RATE


def old_place_side(x, az_deg, dist):
    """The pre-fix implementation at exactly +-90 deg, where nothing should have changed."""
    a, c = 0.0875, 343.0
    th = math.radians(az_deg)
    itd = a / c * (abs(th) + 1.0)
    d = int(round(itd * RATE))
    near = x * 1.25
    far = rs.one_pole_lowpass(x, 1800) * 0.65
    far = np.concatenate([np.zeros(d), far])[:len(x)]
    g = 1.0 / max(1.0, dist / 2.0)
    L, R = (far, near) if az_deg >= 0 else (near, far)
    return L * g, R * g


def signal():
    rng = np.random.default_rng(1)
    x = np.zeros(4096)
    x[100] = 1.0                       # an impulse ...
    x[1000:3000] = rng.standard_normal(2000) * 0.3   # ... and some noise
    return x


def lag(L, R):
    """Interaural lag in samples (positive: right ear leads)."""
    cc = np.correlate(L[:2000], R[:2000], 'full')
    return int(np.argmax(cc)) - 1999


def test_plus_minus_180_are_the_same_place():
    x = signal()
    a, b = rs.place(x, 180, 6), rs.place(x, -180, 6)
    assert np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1])


def test_median_plane_reaches_both_ears_alike():
    x = signal()
    for az in (0, 180, -180, 540):
        L, R = rs.place(x, az, 6)
        assert np.array_equal(L, R), az


def test_rear_is_not_clamped_to_the_side():
    x = signal()
    L100, R100 = rs.place(x, 100, 6)
    L179, R179 = rs.place(x, 179, 6)
    assert not np.allclose(L100, L179)
    assert abs(lag(L179, R179)) < abs(lag(L100, R100))


def test_rear_has_front_lateral_cues_and_is_duller():
    x = signal()
    Lf, Rf = rs.place(x, 45, 6)
    Lb, Rb = rs.place(x, 135, 6)
    assert lag(Lf, Rf) == lag(Lb, Rb) != 0      # same interaural delay (cone of confusion)
    hf = lambda y: np.sum(np.diff(y) ** 2)
    assert hf(Rb) < hf(Rf) and hf(Lb) < hf(Lf)   # behind: both ears duller


def test_left_right_mirror():
    x = signal()
    L, R = rs.place(x, 135, 6)
    L2, R2 = rs.place(x, -135, 6)
    assert np.allclose(L, R2) and np.allclose(R, L2)


def test_smooth_from_side_through_behind():
    """Walk 90 -> 180 -> 270 (= -90) in half degrees: each ear's level moves in small
    steps, the interaural delay changes by at most one sample per step and passes
    through zero behind, never flipping sides at 180."""
    x = signal()
    rms = lambda y: float(np.sqrt(np.mean(y ** 2)))
    prev = None
    for az in np.arange(90, 270.5, 0.5):
        L, R = rs.place(x, az, 6)
        cur = (rms(L), rms(R), lag(L, R))
        if prev is not None:
            assert abs(cur[0] - prev[0]) / prev[0] < 0.03, (az, cur, prev)
            assert abs(cur[1] - prev[1]) / prev[1] < 0.03, (az, cur, prev)
            assert abs(cur[2] - prev[2]) <= 1, (az, cur, prev)
        prev = cur
    L, R = rs.place(x, 179.5, 6)
    L2, R2 = rs.place(x, 180.5, 6)
    assert np.allclose(L, R2, atol=1e-9) and np.allclose(R, L2, atol=1e-9)


def test_sides_unchanged():
    x = signal()
    for az in (90, -90):
        a, b = rs.place(x, az, 6), old_place_side(x, az, 6)
        assert np.allclose(a[0], b[0]) and np.allclose(a[1], b[1]), az


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
