#!/usr/bin/env python3
"""Independent check of Fugue XVI's pedal canons and of every declared entry (reads only fugue.json).

`tools/critic.py` checks every entry against one subject (subject 1), so it reports mismatches for
the other nine subjects and the chorale lines.  This script holds its own literal copy of the
material (the chorale lines in G minor as fugue.py adapts them from BWV 267, the subjects, the
BWV 542 guest) and checks:

  * the pedal canons: for every line, each note of the leader (Pedal II, the line with its note
    values doubled) has a note in the follower (Pedal I) exactly `delay` later, an octave higher,
    with the same duration (the last note of each voice may be held longer); the delays must be
    the ladder 6 1/2, 5, 4 1/2, 4, 3 1/2, 3, 2 1/2, 1 1/2 beats; Pedal I plays nothing else, and
    the notes Pedal II plays outside the canons are listed;
  * every declared entry: the notes in that voice from the entry onwards against the subject it
    names, in rhythm (scaled for the pedal's augmentation) and in letter-name steps (inverted for
    the mirror).  Where the semitones differ from the model (a tonal answer, the mode) it is
    reported as 'tonal', not as an error.

    python3 check_canons.py           # exits 1 on any error
"""
import json
import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
LET = 'cdefgab'
NAT = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}

# "An Wasserfluessen Babylon", soprano of BWV 267 moved to G minor (lines 3-4 = 1-2), as in fugue.py
CHORALE = {
    1: 'D5:4 Eb5:4 D5:2 C5:2 Bb4:2 C5:2 D5:4 C5:2 Bb4:2 C5:4 Bb4:4',
    2: 'A4:4 Bb4:4 C5:4 D5:4 C5:2 Bb4:2 A4:2 G4:2 A4:4 G4:4',
    5: 'G4:4 A4:4 Bb4:4 C5:2 Bb4:2 A4:4 Bb4:4 A4:4 G4:4',
    6: 'G4:2 A4:2 Bb4:4 C5:4 D5:4 Eb5:4 Bb4:4 C#5:4 D5:4',
    7: 'Bb4:2 C5:2 D5:4 Eb5:4 D5:2 C5:2 Bb4:4 C5:8 Bb4:4',
    8: 'E5:4 E5:4 E5:4 A4:4 D5:4 C5:4 Bb4:4 A4:4',
    9: 'C5:4 Bb4:4 A4:4 G4:4 A4:2 G4:2 F4:4 Eb4:4 D4:4',
    10: 'D4:4 G4:4 A4:4 Bb4:6 C5:2 D5:4 C5:2 Bb4:2 A4:4 Bb4:2 C5:2 A4:8 G4:4',
}
CHORALE[3], CHORALE[4] = CHORALE[1], CHORALE[2]
SUBJECT = {
    1: CHORALE[1],
    2: 'A4:3 Bb4:1 C5:3 D5:1 C5:2 Bb4:2 A4:3 G4:1 A4:4 G4:4',
    5: 'G4:2 A4:4 Bb4:4 C5:2 Bb4:2 A4:4 Bb4:4 A4:4 G4:6',
    6: 'G4:1 A4:1 Bb4:1 C5:1 D5:2 Eb5:2 Bb4:2 C#5:2 D5:4',
    7: 'Bb4:4/3 C5:4/3 D5:4/3 Eb5:4 D5:4/3 C5:4/3 Bb4:4/3 C5:4 Bb4:4',
    8: 'E5:2 E5:2 E5:2 A4:2 D5:3 C5:1 Bb4:2 A4:2',
    9: 'C5:4 B4:2 Bb4:2 A4:4 G4:4 A4:2 G4:2 F4:2 E4:2 Eb4:4 D4:4',
    10: 'D4:2 G4:2 A4:2 Bb4:3 C5:1 D5:2 C5:1 Bb4:1 A4:2 Bb4:1 C5:1 A4:4 G4:4',
}
BWV542 = ('D5:2 Bb4:1 C5:1 A4:1 Bb4:1 G4:2 G5:2 F#5:1 G5:1 E5:1 F#5:1 D5:2 G5:1 D5:1 Eb5:2 C5:2 F4:2 '
          'F5:2 D5:1 Eb5:1 C5:1 D5:1 Bb4:2 Eb5:1 Bb4:1 C5:2 A4:2 D4:2 D5:2 Bb4:1 C5:1 A4:1 Bb4:1 G4:2')
LADDER = [Fr(13, 2), 5, Fr(9, 2), 4, Fr(7, 2), 3, Fr(5, 2), Fr(3, 2)]     # beats, lines 1 2 5-10


def toks(s):
    """'Eb5:4' tokens -> [(diatonic step, midi, duration in quarters)]."""
    out = []
    for t in s.split():
        name, d = t.rsplit(':', 1)
        m = re.fullmatch(r'([A-G])(#{0,2}|b{0,2})(-?\d)', name)
        L, acc, o = m.groups()
        alt = acc.count('#') - acc.count('b')
        out.append((LET.index(L.lower()) + 7 * int(o), 12 * (int(o) + 1) + NAT[L.lower()] + alt, Fr(d) / 4))
    return out


def ev(e):
    sp = e['spell']
    letter = sp[0]
    acc = sp[1:].count('is') - sp[1:].count('es')
    octave = (e['p'] - acc - NAT[letter]) // 12 - 1
    q = lambda x: Fr(x).limit_denominator(96)
    return q(e['t']), (LET.index(letter) + 7 * octave, e['p'], q(e['d']))


def spec(label):
    """(model tokens, rhythm scale, mirror?, last note free?) for a declared entry."""
    m = re.match(r'cantus line (\d+)', label)
    if m:
        return toks(CHORALE[int(m.group(1))]), 2, False, True
    m = re.match(r'line (\d+): the chorale', label)
    if m:
        return toks(CHORALE[int(m.group(1))]), 1, False, False
    if 'echo of "an Zion"' in label:                    # the close of line 3 (= line 1)
        return toks(CHORALE[3])[-5:], 1, False, False
    if 'echo of "von Herzen"' in label:                 # the close of line 4 (= line 2)
        return toks(CHORALE[4])[-6:], 1, False, False
    if label.startswith('guest'):
        return toks(BWV542), 1, False, False
    if label.startswith('coda'):                        # line 1, notes 2-7 (E-flat D C B-flat C D)
        return toks(CHORALE[1])[1:7], 1, False, False
    if label.startswith('summit'):
        return toks(SUBJECT[10]), 1, False, False
    m = re.match(r'line (\d+) Vorimitation', label)
    if m:
        return toks(SUBJECT[int(m.group(1))]), 1, 'mirror' in label, False
    raise ValueError(label)


def main():
    data = json.loads((HERE / 'fugue.json').read_text())
    voices = [sorted(ev(e) for e in v['events'] if e.get('p') is not None) for v in data['voices']]
    names = [v['name'] for v in data['voices']]
    errors = 0

    def loc(t):
        b, beat = divmod(t, 4)
        return f'b{int(b) + 1}.{float(beat + 1):g}'

    # ---- declared entries
    print('entries (rhythm and letter steps against their own subject):')
    for e in data['subject_entries']:
        model, scale, mirror, free_last = spec(e['label'])
        t0 = Fr(e['t']).limit_denominator(96)
        vs = voices[e['voice']]
        k = next((i for i, (t, _) in enumerate(vs) if t == t0), None)
        if k is None or k + len(model) > len(vs):
            print(f'   ERROR {loc(t0)} {e["label"]}: no notes'); errors += 1
            continue
        got = vs[k:k + len(model)]
        ok, tonal = True, 0
        for i in range(len(model)):
            dur_ok = got[i][1][2] == model[i][2] * scale or (free_last and i == len(model) - 1)
            ok &= dur_ok
            if i:
                ds = model[i][0] - model[i - 1][0]
                dp = model[i][1] - model[i - 1][1]
                gs = got[i][1][0] - got[i - 1][1][0]
                gp = got[i][1][1] - got[i - 1][1][1]
                if mirror:
                    ds, dp = -ds, -dp
                ok &= gs == ds
                tonal += gp != dp
        # the onsets must follow each other without gaps (scaled rhythm)
        for i in range(1, len(model)):
            ok &= got[i][0] == got[i - 1][0] + model[i - 1][2] * scale
        tag = 'ok' if ok else 'ERROR'
        errors += not ok
        extra = f', tonal at {tonal} step(s)' if tonal and ok else ''
        print(f'   {tag:5} {loc(t0):9} {names[e["voice"]]:9} {len(model):2} notes{extra}  {e["label"]}')

    # ---- pedal canons
    print('pedal canons (Pedal II leads, Pedal I an octave higher):')
    P1, P2 = voices[names.index('Pedal I')], voices[names.index('Pedal II')]
    lead = {}
    fol = {}
    for e in data['subject_entries']:
        m = re.match(r'cantus line (\d+) \(Pedal (II|I),', e['label'])
        if m:
            (lead if m.group(2) == 'II' else fol)[int(m.group(1))] = Fr(e['t']).limit_denominator(96)
    used1, used2, delays = set(), set(), []
    for line in sorted(lead):
        n = len(toks(CHORALE[line]))
        d0, c0 = lead[line], fol[line]
        delay = c0 - d0
        delays.append(delay)
        i = next(i for i, (t, _) in enumerate(P2) if t == d0)
        j = next(j for j, (t, _) in enumerate(P1) if t == c0)
        bad = []
        for k in range(n):
            (td, (sd, pd, dd)), (tc, (sc, pc, dc)) = P2[i + k], P1[j + k]
            if tc - td != delay or pc != pd + 12 or sc != sd + 7 or (dd != dc and k < n - 1):
                bad.append(loc(td))
            used2.add(i + k)
            used1.add(j + k)
        errors += bool(bad)
        print(f'   {"ok" if not bad else "ERROR":5} line {line:2}: leader {loc(d0)}, follower {loc(c0)}, '
              f'{float(delay):g} beats, {n} notes' + (f'  mismatches at {bad}' if bad else ''))
    ladder_ok = delays == LADDER and all(a > b for a, b in zip(delays, delays[1:]))
    errors += not ladder_ok
    print(f'   {"ok" if ladder_ok else "ERROR":5} delays {[float(d) for d in delays]} '
          f'(the ladder 6.5 5 4.5 4 3.5 3 2.5 1.5, strictly shrinking)')
    own1 = [loc(t) for k, (t, _) in enumerate(P1) if k not in used1]
    own2 = [loc(t) for k, (t, _) in enumerate(P2) if k not in used2]
    errors += bool(own1)
    print(f'   {"ok" if not own1 else "ERROR":5} Pedal I plays only the canons' + (f': also {own1}' if own1 else ''))
    print(f'   note  Pedal II outside the canons: {len(own2)} notes {own2}')
    print('OK' if not errors else f'{errors} ERROR(S)')
    return errors


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
