#!/usr/bin/env python3
"""Independent check of every canon in Fugue XIII (reads only fugue.json).

For each canon the table below gives the dux and comes voices, the interval (a diatonic shift in
the F-sharp-major key signature, or a mirror that maps one note onto another and negates the
accidental), the delay in bars, and the span of dux bars that the comes copies.  The check is:

  * every dux note that starts inside the span has a comes note exactly `delay` bars later with
    the same duration (cut at the end of the span, where a tie is released) and the transformed
    pitch, spelled with the transformed letter;
  * every comes note that starts inside the copied span has such a dux note (so the comes holds
    nothing of its own while the canon runs).

The two quodlibet canons are checked over the stretch where they are strict (the end of each
tune is free, as in Bach's Var. 30).

    python3 check_canons.py
"""
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
BAR = Fr(3)                                   # quarters per 3/4 bar
LET = 'cdefgab'
NAT = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}
KEYACC = {'f': 1, 'c': 1, 'g': 1, 'd': 1, 'a': 1, 'e': 1, 'b': 0}     # F-sharp major


def parse(e):
    """(onset, duration, diatonic step, accidental relative to the key, midi) of one event."""
    sp = e['spell']
    letter, rest = sp[0], sp[1:]
    acc = rest.count('is') - rest.count('es') - (1 if rest in ('s',) else 0)
    natural = e['p'] - acc
    octave = (natural - NAT[letter]) // 12 - 1
    step = LET.index(letter) + 7 * octave
    q = lambda x: Fr(x).limit_denominator(96)          # times are stored as floats (triplets)
    return q(e['t']), q(e['d']), step, acc - KEYACC[letter], e['p']


def midi(step, rel):
    letter = LET[step % 7]
    octave = step // 7
    return 12 * (octave + 1) + NAT[letter] + KEYACC[letter] + rel


def step_of(name):                            # 'F#5' -> diatonic step
    letter, octave = name[0].lower(), int(name[-1])
    return LET.index(letter) + 7 * octave


def shift(k):
    return lambda s, r: (s + k, r)


def mirror(a, b):
    sa, sb = step_of(a), step_of(b)
    return lambda s, r: (sa + sb - s, -r)


#  name, dux, comes, transform, delay (bars), first dux bar, last dux bar, label
CANONS = [
    ('I',   'Canon I dux',   'Canon I comes (unison)',               shift(0),   2,  9, 62, 'unison'),
    ('II',  'Canon II dux',  'Canon II comes (2nd above)',           shift(1),   1, 17, 63, '2nd above'),
    ('III', 'Canon III dux', 'Canon III comes (3rd above)',          shift(2),   2, 25, 62, '3rd above'),
    ('IV',  'Canon IV dux',  'Canon IV comes (4th below, inverted)', mirror('F#5', 'C#5'), 4, 33, 60,
     '4th below by inversion (F#<->C#)'),
    ('V',   'Canon V dux',   'Canon V comes (5th below, inverted)',  mirror('F#5', 'B4'), 3, 41, 60,
     '5th below by inversion (F#<->B)'),
    ('VI',  'Canon VI dux',  'Canon VI comes (6th below)',           shift(-5),  8, 49, 60, '6th below'),
]
# Quodlibet canons, checked from the upbeat (in quarters) to the end of the strict stretch.
QUODLIBET = [
    ('Ich bin (var. 9)', 'Canon I dux', 'Canon I comes (unison)', shift(7), 2, 63 * 3 + Fr(9, 4), 68 * 3,
     'octave above'),
    ('Kraut (var. 9)', 'Canon II dux', 'Canon II comes (2nd above)', shift(-6), 1, 68 * 3, 71 * 3,
     '7th below'),
    ('Ich bin (var. 10)', 'Canon I comes (unison)', 'Canon I dux', shift(-7), 2, 71 * 3 + Fr(9, 4), 76 * 3,
     'octave below'),
]


def check(voices, label, dux, comes, f, delay, t0, t1, interval):
    D = [parse(e) for e in voices[dux]['events']]
    C = {(t, p): (d, s, r) for t, d, s, r, p in (parse(e) for e in voices[comes]['events'])}
    lag = delay * BAR
    bad, n = [], 0
    for t, d, s, r, p in D:
        if not (t0 <= t < t1):
            continue
        n += 1
        s2, r2 = f(s, r)
        q = midi(s2, r2)
        want_d = min(d, t1 - t)
        got = C.get((t + lag, q))
        if got is None or got[0] != want_d or got[1] != s2:
            bad.append(f'dux {t}q p{p} -> wanted comes {t + lag}q p{q} d{want_d}, got {got}')
    dux_onsets = {t for t, *_ in D}
    extra = [f'comes {t}q p{p}' for (t, p) in C if t0 + lag <= t < t1 + lag and t - lag not in dux_onsets]
    ok = not bad and not extra
    span = f'{float(t0 / BAR) + 1:g}-{float(t1 / BAR):g}'
    print(f'  {label:<18} {interval:<34} delay {delay} bar(s), dux bars {span:<11} '
          f'{n:4d} notes  {"OK" if ok else "FAILED"}')
    for x in (bad + extra)[:8]:
        print('      ', x)
    return ok


def main():
    data = json.loads((HERE / 'fugue.json').read_text())
    voices = {v['name']: v for v in data['voices']}
    good = True
    print('Fugue XIII: the six canons of the tower')
    for name, dux, comes, f, delay, b0, b1, interval in CANONS:
        good &= check(voices, f'Canon {name}', dux, comes, f, delay, (b0 - 1) * BAR, b1 * BAR, interval)
    print('Quodlibet canons (strict stretch)')
    for label, dux, comes, f, delay, t0, t1, interval in QUODLIBET:
        good &= check(voices, label, dux, comes, f, delay, Fr(t0), Fr(t1), interval)
    print('ALL CANONS EXACT' if good else 'CHECK FAILED')
    return 0 if good else 1


if __name__ == '__main__':
    sys.exit(main())
