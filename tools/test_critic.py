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


def permuted(data):
    """The score with its voices listed in every order."""
    import itertools
    for perm in itertools.permutations(range(len(data['voices']))):
        yield dict(data, voices=[data['voices'][k] for k in perm])


def order_free_report(data):
    """Dissonance and direct-motion rows, keyed by voice names rather than voice indices."""
    R = critic.analyse(data)
    dis = sorted((x['loc'], x['kind'], tuple(sorted(x['what'].split('/')))) for x in R['dissonance'])
    return dis, sorted((x['loc'], x['what']) for x in R['direct'])


def test_unison_bass_is_order_independent():
    # A and B share the bass C3 while C strikes F3 (a fourth against the bass) and resolves to E3;
    # whichever bass voice is listed first, the classification is the same.
    data = score(('A', [(0, 2, 48), (2, 2, 48)]), ('B', [(1, 1, 48), (2, 2, 43)]),
                 ('C', [(0, 1, 55), (1, 1, 53), (2, 2, 52)]))
    reports = [order_free_report(d) for d in permuted(data)]
    assert all(r == reports[0] for r in reports), reports
    # the fourth is judged against both bass voices
    pairs = {k[2] for k in reports[0][0] if k[0] == 'b1.2'}
    assert pairs == {('AC3', 'CF3'), ('BC3', 'CF3')}, reports[0]


def test_direct_octave_with_a_unison_top_is_order_independent():
    # A and B share the top E4, then A leaps to C5 while the bass rises G2 -> C3: a direct
    # octave A/Bass.  It used to be found only when A was listed after B.
    data = score(('A', [(0, 1, 64), (1, 1, 72)]), ('B', [(0, 1, 64), (1, 1, 60)]),
                 ('Bass', [(0, 1, 43), (1, 1, 48)]))
    reports = [order_free_report(d)[1] for d in permuted(data)]
    assert all(r == [('b1.2', 'direct 8ve A/Bas top leaps +8')] for r in reports), reports


def test_rootless_dominant_seventh_in_first_inversion():
    # B-D-F over D (vii6 in C = a rootless G7) going to C: B3 rises to C4, F4 falls to E4.
    # The seventh is F (it resolves); B is the leading tone.  It used to be read as
    # D-F-Ab-B with B as the "seventh", flagged for rising.
    good = score(('S', [(0, 1, 65), (1, 1, 64)]), ('A', [(0, 1, 59), (1, 1, 60)]),
                 ('B', [(0, 1, 50), (1, 1, 48)]))
    kinds = dis_kinds(good)
    assert kinds and all(k[1] == 'chord' for k in kinds if k[0] == 'b1.1'), kinds
    # the same chord with the seventh F rising to G is flagged
    bad = score(('S', [(0, 1, 65), (1, 1, 67)]), ('A', [(0, 1, 59), (1, 1, 60)]),
                ('B', [(0, 1, 50), (1, 1, 48)]))
    assert any(k[1] == 'chord (7th not resolved down)' for k in dis_kinds(bad)), dis_kinds(bad)


def test_diminished_seventh_root_is_its_rising_leading_tone():
    # B-D-F-Ab over D (vii-o6/5 in C): B3 rises to C4, Ab4 (the seventh) falls to G4.
    good = score(('S', [(0, 1, 68), (1, 1, 67)]), ('A', [(0, 1, 65), (1, 1, 64)]),
                 ('T', [(0, 1, 59), (1, 1, 60)]), ('B', [(0, 1, 50), (1, 1, 48)]))
    kinds = dis_kinds(good)
    assert kinds and all(k[1] == 'chord' for k in kinds if k[0] == 'b1.1'), kinds
    bad = score(('S', [(0, 1, 68), (1, 1, 70)]), ('A', [(0, 1, 65), (1, 1, 64)]),
                ('T', [(0, 1, 59), (1, 1, 60)]), ('B', [(0, 1, 50), (1, 1, 48)]))
    assert any(k[1] == 'chord (7th not resolved down)' for k in dis_kinds(bad)), dis_kinds(bad)


def test_two_pitch_classes_get_an_interval_label():
    # C4 under E4, with a passing G4 sixteenth: two pitch classes sound together, so the beat
    # is the dyad C-E, not a C major chord made up with the passing note.
    data = score([(0, 0.75, 64), (0.75, 0.25, 67), (1, 1, 65)], [(0, 2, 60)])
    H = critic.analyse(data)['harmony']
    assert H['labels'][0] == 'C-E (M3)', H['labels']
    assert H['dyad_beats_pct'] == 100.0, H
    # a third voice makes it a chord again
    data = score([(0, 1, 67)], [(0, 1, 64)], [(0, 1, 60)])
    assert critic.analyse(data)['harmony']['labels'][0] == 'C'


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
