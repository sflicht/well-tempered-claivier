#!/usr/bin/env python3
"""Organ check for Pair XVI: is every attack playable by two hands and two feet?

`tools/critic.py` checks a score for one keyboard: its `reach_errors` count fresh attacks that no
split between two hands can strike (> 16 semitones in a hand).  XVI is organ music (the fugue has
three manual voices and double pedal, the prelude three manual voices and pedal), so this script
(reads only the JSON) applies the organ's rules instead:

  * every voice whose name starts with 'Pedal' is played by the feet.  Its notes must lie in the
    pedal compass; with two pedal voices each foot takes one, so they must not cross, and the
    widest interval between them is reported;
  * the manual voices are played by two hands.  On an organ nothing sustains a key that is let go,
    so the check is stricter than the critic's: at every onset, *all* sounding manual notes (held
    ones too) must split between two hands with at most 16 semitones (a major tenth) and five
    notes per hand;
  * the attacks the critic reports as unreachable on one keyboard are listed with their split.

    python3 check_organ.py            # exits 1 if any attack is unplayable
"""
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPAN = 16                    # semitones per hand (the critic's limit: a major tenth)
PEDAL = (36, 67)             # C2-G4: the 32-note pedalboard of a modern organ
PERIOD_PEDAL_TOP = 62        # d' (D4): the usual top of Bach's pedal parts
MANUAL = (36, 96)            # C2-C7: a 61-note manual
PERIOD_MANUAL_TOP = 84       # c''' (C6): the usual top of a manual in Bach's time
NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']


def nm(p):
    return f'{NAMES[p % 12]}{p // 12 - 1}'


def loc(t, bar=4):
    t = Fr(t).limit_denominator(96)
    b, beat = divmod(t, bar)
    return f'b{int(b) + 1}.{float(beat + 1):g}'


def split(ps):
    """Best two-hand split of the pitches ps: (largest hand span, left, right)."""
    ps = sorted(ps)
    best = None
    for k in range(len(ps) + 1):
        L, R = ps[:k], ps[k:]
        if len(L) > 5 or len(R) > 5:
            continue
        m = max(L[-1] - L[0] if L else 0, R[-1] - R[0] if R else 0)
        if best is None or m < best[0]:
            best = (m, L, R)
    return best


def check(path):
    data = json.loads(path.read_text())
    voices = data['voices']
    q = lambda x: Fr(x).limit_denominator(96)
    notes = [[(q(e['t']), q(e['t']) + q(e['d']), e['p']) for e in v['events'] if e.get('p') is not None]
             for v in voices]
    ped = [i for i, v in enumerate(voices) if v['name'].startswith('Pedal')]
    man = [i for i in range(len(voices)) if i not in ped]
    onsets = sorted({s for v in notes for s, _, _ in v})

    def sounding(i, t):
        return [p for s, e, p in notes[i] if s <= t < e]

    bad, worst, ped_gap, crossings, wide = [], (0, None), (0, None), [], []
    for t in onsets:
        m = [p for i in man for p in sounding(i, t)]
        if m:
            span, L, R = split(m)
            if span > worst[0]:
                worst = (span, t)
            if span > SPAN:
                bad.append((t, m))
        if len(ped) == 2:
            a, b = sounding(ped[0], t), sounding(ped[1], t)
            if a and b:
                upper, lower = max(a[0], b[0]), min(a[0], b[0])
                if a[0] < b[0]:
                    crossings.append(t)
                if upper - lower > ped_gap[0]:
                    ped_gap = (upper - lower, t)
                if upper - lower > 12:
                    wide.append(loc(t))
    ped_notes = [p for i in ped for _, _, p in notes[i]]
    man_notes = [p for i in man for _, _, p in notes[i]]
    above = sorted({(loc(s), nm(p)) for i in ped for s, _, p in notes[i] if p > PERIOD_PEDAL_TOP})
    high = sorted({(loc(s), nm(p)) for i in man for s, _, p in notes[i] if p > PERIOD_MANUAL_TOP})

    print(f'== {path.name}: {len(onsets)} onsets; manuals: '
          f'{", ".join(voices[i]["name"] for i in man)}; pedal: {", ".join(voices[i]["name"] for i in ped)}')
    ok = True
    lo, hi = min(ped_notes), max(ped_notes)
    inr = PEDAL[0] <= lo and hi <= PEDAL[1]
    ok &= inr
    print(f'pedal compass: {nm(lo)}-{nm(hi)} ({"inside" if inr else "OUTSIDE"} C2-G4); '
          f'above d\' (D4): {len(above)} attacks' + (f' {above}' if above else ''))
    if len(ped) == 2:
        print(f'double pedal: Pedal I above Pedal II at every shared onset: {"yes" if not crossings else "NO " + str([loc(t) for t in crossings])}; '
              f'widest interval between the feet {ped_gap[0]} semitones at {loc(ped_gap[1])}; '
              f'wider than an octave at {len(wide)} onsets (e.g. {", ".join(wide[:6])})')
        ok &= not crossings
    lo, hi = min(man_notes), max(man_notes)
    print(f'manual compass: {nm(lo)}-{nm(hi)} (inside C2-C7: {MANUAL[0] <= lo and hi <= MANUAL[1]}); '
          f'above c\'\'\' (C6): {len(high)} attacks' + (f' {high}' if high else ''))
    print(f'hands: widest hand at any onset (held notes included) {worst[0]} semitones at {loc(worst[1])}; '
          f'onsets over {SPAN}: {len(bad)}')
    for t, m in bad:
        print(f'   UNPLAYABLE {loc(t)}: {" ".join(nm(p) for p in sorted(m))}')
    ok &= not bad
    # the critic's one-keyboard reach errors, shown with the organ split
    by_t = {}
    for v in notes:
        for s, _, p in v:
            by_t.setdefault(s, set()).add(p)
    for t in sorted(by_t):
        if split(by_t[t])[0] > SPAN:
            f = [p for i in ped for p in sounding(i, t)]
            m = [p for i in man for p in sounding(i, t)]
            span, L, R = split(m)
            print(f'   one-keyboard reach error {loc(t)} {" ".join(nm(p) for p in sorted(by_t[t]))}: '
                  f'feet {" ".join(nm(p) for p in sorted(f)) or "-"} | LH {" ".join(nm(p) for p in L) or "-"}'
                  f' | RH {" ".join(nm(p) for p in R) or "-"} (widest hand {span})')
    return ok


if __name__ == '__main__':
    results = [check(HERE / f) for f in ('prelude.json', 'fugue.json')]
    print('OK: playable by two hands and pedal' if all(results) else 'FAIL')
    sys.exit(0 if all(results) else 1)
