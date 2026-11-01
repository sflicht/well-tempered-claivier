#!/usr/bin/env python3
"""Positive and negative controls for critic.py.

Each case is a tiny score whose correct verdict is known. Run:
    python3 tools/test_critic.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import critic  # noqa: E402


def score(*voices, meta=None, **extra):
    m = {'meter': [4, 4], 'bpm': 60, 'key': 'C'}
    m.update(meta or {})
    vs = []
    for k, v in enumerate(voices):
        name, evs = v if isinstance(v, tuple) else (f'V{k}', v)
        vs.append({'name': name, 'events': [{'t': t, 'd': d, 'p': p} for t, d, p in evs]})
    for k, val in extra.items():
        for v in vs:
            if v['name'] == k:
                v.update(val)
    return {'metadata': m, 'voices': vs}


def quarters(ps, t0=0):
    return [(t0 + i, 1, p) for i, p in enumerate(ps)]


def summary(data):
    return critic.analyse(data)['summary']


def dis_kinds(data):
    return [(x['loc'], x['kind'], x['sev']) for x in critic.analyse(data)['dissonance']]


def test_parallel_fifth_run_keeps_its_severity():
    # C4/G4 -> D4/A4 -> E4/B4 -> F4/C5: three consecutive beat-level fifths
    s = summary(score(quarters([67, 69, 71, 72]), quarters([60, 62, 64, 65])))
    assert s['parallels_error'] == 1, s
    assert s['parallels_error_transitions'] == 3, s
    assert s['doubling_runs'] == 0, s
    assert s['beat_parallels'] >= 1, s


def test_undeclared_octave_run_is_an_error():
    s = summary(score(quarters([72, 74, 76, 77]), quarters([60, 62, 64, 65])))
    assert s['parallels_error'] == 1 and s['doubling_runs'] == 0, s


def test_declared_octave_doubling_is_exempt():
    data = score(('Lead', quarters([72, 74, 76, 77])), ('Double', quarters([60, 62, 64, 65])),
                 meta={'doublings': [['Lead', 'Double']]})
    s = summary(data)
    assert s['parallels_error'] == 0 and s['doubling_runs'] == 1 and s['beat_parallels'] == 0, s
    # the same exemption through the voice-level field
    data = score(('Lead', quarters([72, 74, 76, 77])), ('Double', quarters([60, 62, 64, 65])),
                 Double={'doubles': 'Lead'})
    assert summary(data)['parallels_error'] == 0


def test_declared_doubling_does_not_excuse_fifths():
    data = score(('A', quarters([67, 69, 71, 72])), ('B', quarters([60, 62, 64, 65])),
                 meta={'doublings': [['A', 'B']]})
    assert summary(data)['parallels_error'] == 1


def test_second_followed_by_a_long_rest_is_unresolved():
    # C4/D4 at t=0, then D4/F4 only after 99 quarters of silence
    data = score([(0, 1, 62), (100, 1, 65)], [(0, 1, 60), (100, 1, 62)])
    kinds = dis_kinds(data)
    assert kinds[0][2] == 'error', kinds
    assert summary(data)['dissonance_unresolved'] >= 1


def test_parallel_seconds_are_not_a_resolution():
    # C4/D4 -> D4/E4: both voices step, the result is still a second
    data = score(quarters([62, 64, 65]), quarters([60, 62, 60]))
    first = dis_kinds(data)[0]
    assert first[2] != 'ok', first


def test_prepared_four_three_suspension_is_ok():
    # Upper F4 struck over D3 (consonant), held while the bass moves to C3
    # (a fourth over the bass, on beat 2), then falls to E4 (a third).
    data = score([(0, 2, 65), (2, 2, 64)], [(0, 1, 50), (1, 3, 48)])
    kinds = dis_kinds(data)
    assert ('b1.2', 'suspension', 'ok') in kinds, kinds
    assert summary(data)['dissonance_unresolved'] == 0


def test_unprepared_held_dissonance_is_marked():
    # Upper F4 struck against G3 (a seventh: no preparation), held over C3, falls to E4
    data = score([(0, 2, 65), (2, 2, 64)], [(0, 1, 55), (1, 3, 48)])
    kinds = dis_kinds(data)
    assert any(k[1] == 'suspension (unprepared)' for k in kinds), kinds


def test_reach_flags_three_far_registers():
    # Fugue XXIII b17.1: G#1, F#4, B#5 struck together (one hand needs 18 semitones)
    data = score([(0, 1, 84)], [(0, 1, 66)], [(0, 1, 32)], meta={'instrument': 'Piano'})
    R = critic.analyse(data)
    assert R['summary']['reach_errors'] == 1 and R['reach'][0]['span'] == 18, R['reach']
    assert R['summary']['solo_keyboard'] is True


def test_reach_accepts_a_wide_but_playable_chord_and_held_notes():
    # C2 struck with C4 E4 G4 C5: left hand takes C2, right hand spans an octave
    data = score([(0, 1, 72)], [(0, 1, 67)], [(0, 1, 64)], [(0, 1, 60)], [(0, 1, 36)])
    assert summary(data)['reach_errors'] == 0
    # a held low pedal note does not count against fresh attacks
    data = score([(1, 1, 84)], [(1, 1, 66)], [(0, 4, 32)])
    assert summary(data)['reach_errors'] == 0


def test_open_score_is_not_solo_keyboard():
    data = score([(0, 1, 60)], meta={'instrument': 'Twenty-five voices (open score)'})
    assert summary(data)['solo_keyboard'] is False


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
