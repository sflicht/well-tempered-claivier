#!/usr/bin/env python3
"""Independent check of every canon in Fugue XIII (reads only fugue.json).

For each canon the table below gives the dux and comes voices, the key whose signature the
transform uses, the transform (a diatonic shift by letter names, or a mirror that maps one note
onto another and negates the accidental relative to the key signature), the delay and the span of
dux music that the comes copies.  The check is:

  * every dux note that starts inside the span has a comes note exactly `delay` later, with the
    same duration (cut at the end of the span, where a tie is released), the transformed letter
    name and the transformed pitch;
  * every comes note that starts inside the copied span has such a dux note (so the comes holds
    nothing of its own while the canon runs);
  * the only pitch differences allowed are the declared accidentals of the minor mode (FICTA):
    the letter and the rhythm stay strict, the note is raised a semitone to the leading tone of
    the chord it sounds against.  Each one is listed by bar and spelling, and reported.

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
SIX = dict(f=1, c=1, g=1, d=1, a=1, e=1, b=0)
FIVE = dict(f=1, c=1, g=1, d=1, a=1, e=0, b=0)
KEYS = {'F#': SIX, 'B': FIVE, 'G#m': FIVE, 'C#': dict.fromkeys(LET, 1),
        'F#m': dict(f=1, c=1, g=1, d=0, a=0, e=0, b=0)}


def parse(e, ks):
    """(onset, duration, diatonic step, accidental relative to key signature ks, midi, spelling)."""
    sp = e['spell']
    letter, rest = sp[0], sp[1:]
    acc = rest.count('is') - rest.count('es')
    natural = e['p'] - acc
    octave = (natural - NAT[letter]) // 12 - 1
    step = LET.index(letter) + 7 * octave
    q = lambda x: Fr(x).limit_denominator(96)          # times are stored as floats (triplets)
    return q(e['t']), q(e['d']), step, acc - ks[letter], e['p'], sp


def midi(step, rel, ks):
    letter = LET[step % 7]
    octave = step // 7
    return 12 * (octave + 1) + NAT[letter] + ks[letter] + rel


def step_of(name):                            # 'F#5' -> diatonic step
    letter, octave = name[0].lower(), int(name[-1])
    return LET.index(letter) + 7 * octave


def shift(k):
    return lambda s, r: (s + k, r)


def mirror(a, b):
    sa, sb = step_of(a), step_of(b)
    return lambda s, r: (sa + sb - s, -r)


def spelled(step, p):
    """LilyPond-style spelling of midi p on the letter of diatonic step (for the report)."""
    letter = LET[step % 7]
    octave = step // 7
    acc = p - (12 * (octave + 1) + NAT[letter])
    return letter + ('is' * acc if acc > 0 else 'es' * -acc)


#  name, dux, comes, key, transform, delay (quarters), span start, span end (quarters), label
Q = lambda bar, beat=0: (bar - 1) * BAR + Fr(beat)
CANONS = [
    ('I', 'Soprano', 'Alto', 'F#', shift(0), 2 * BAR, Q(3), Q(7), 'unison'),
    ('II', 'Soprano', 'Alto', 'B', shift(-1), 1 * BAR, Q(12), Q(16), '2nd below'),
    ('III', 'Soprano', 'Alto', 'G#m', shift(-2), 2 * BAR, Q(19), Q(23), '3rd below'),
    ('IV', 'Soprano', 'Tenor', 'C#', mirror('C#5', 'G#3'), 1 * BAR, Q(29), Q(34),
     '4th below by inversion (C#<->G#)'),
    ('V', 'Alto', 'Tenor', 'F#', mirror('A#4', 'D#4'), 2 * BAR, Q(39), Q(45),
     '5th below by inversion (A#<->D#)'),
    ('VI', 'Alto', 'Soprano', 'F#m', shift(5), 2 * BAR, Q(47), Q(51), '6th above'),
    ('Ich bin', 'Tenor', 'Alto', 'F#', shift(7), 2 * BAR, Q(54, Fr(9, 4)), Q(59), 'octave above'),
]
# Declared accidentals of the minor mode in a comes: (canon, comes bar, spelling there).
FICTA = {('III', 22, 'fisis'), ('VI', 50, 'eis')}


def check(voices, name, dux, comes, key, f, lag, t0, t1, interval):
    ks = KEYS[key]
    D = [parse(e, ks) for e in voices[dux]['events']]
    C = {}
    for e in voices[comes]['events']:
        t, d, s, r, p, sp = parse(e, ks)
        C[t] = (d, s, p, sp)
    bad, ficta, n = [], [], 0
    for t, d, s, r, p, sp in D:
        if not (t0 <= t < t1):
            continue
        n += 1
        s2, r2 = f(s, r)
        want_p = midi(s2, r2, ks)
        want_d = min(d, t1 - t)
        got = C.get(t + lag)
        bar = int((t + lag) // BAR) + 1
        if got is None or got[0] != want_d or got[1] != s2:
            bad.append(f'dux {float(t)}q {sp} -> wanted comes {float(t + lag)}q '
                       f'{spelled(s2, want_p)} d{want_d}, got {got}')
        elif got[2] != want_p:
            if (name, bar, got[3]) in FICTA and got[2] - want_p == 1:
                ficta.append(f'b{bar} {spelled(s2, want_p)} -> {got[3]}')
            else:
                bad.append(f'dux {float(t)}q {sp} -> comes b{bar} {got[3]}, wanted {spelled(s2, want_p)}')
    dux_onsets = {t for t, *_ in D}
    extra = [f'comes {float(t)}q {v[3]}' for t, v in C.items()
             if t0 + lag <= t < t1 + lag and t - lag not in dux_onsets]
    ok = not bad and not extra
    span = f'{float(t0 / BAR) + 1:g}-{float(t1 / BAR):g}'
    print(f'  Canon {name:<8} {interval:<34} {dux:>7} -> {comes:<7} delay {float(lag / BAR):g} bar(s), '
          f'dux bars {span:<10} {n:3d} notes  {"OK" if ok else "FAILED"}'
          + (f'   (minor-mode accidentals: {", ".join(ficta)})' if ficta else ''))
    for x in (bad + extra)[:8]:
        print('      ', x)
    return ok


def main():
    data = json.loads((HERE / 'fugue.json').read_text())
    voices = {v['name']: v for v in data['voices']}
    good = True
    print('Fugue XIII: the canons')
    for c in CANONS:
        good &= check(voices, *c)
    print('ALL CANONS EXACT' if good else 'CHECK FAILED')
    return 0 if good else 1


if __name__ == '__main__':
    sys.exit(main())
