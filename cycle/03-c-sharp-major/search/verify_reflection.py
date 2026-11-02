"""Proof for the coda of Fugue III (bars 40-41, with the pickup in 39).

1. Soprano+alto of bars 40-41 are note-for-note Part 1's bars 9-10 (alto pickup in 8).
2. Tenor+bass of bars 40-41 are note-for-note Part 2's bars 23-24 (tenor pickup in 22).
3. Tenor = diatonic mirror of the alto, bass = diatonic mirror of the soprano, around
   E#4, with no time offset (C#<->G#, D#<->F#, E# fixed, A#<->B#).
4. The four lines extracted on their own are run through tools/critic.py analyse().
Usage: python3 verify_reflection.py ../fugue.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from critic import analyse  # noqa: E402

C_MAJ = [1, 3, 5, 6, 8, 10, 0]
d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / 'fugue.json'))
V = {v['name']: v['events'] for v in d['voices']}
BARQ = 6.0


def window(name, t0, t1):
    return [(round(e['t'] - t0, 4), round(e['d'], 4), e['p']) for e in V[name] if t0 <= e['t'] < t1]


def deg(p):
    return ((p - 1) // 12) * 7 + C_MAJ.index(p % 12)


ok = True
pick = 5.5  # quarters: the last eighth of the previous bar
END = 11.5  # the subject and countersubject end on the last beat of their second bar
src_up = {n: window(n, 8 * BARQ - 0.5, 8 * BARQ + END) for n in ('Soprano', 'Alto')}
src_lo = {n: window(n, 22 * BARQ - 0.5, 22 * BARQ + END) for n in ('Tenor', 'Bass')}
coda = {n: window(n, 39 * BARQ - 0.5, 39 * BARQ + END) for n in ('Soprano', 'Alto', 'Tenor', 'Bass')}
for n in ('Soprano', 'Alto'):
    same = src_up[n] == coda[n]
    ok &= same
    print(f'{n:8s} bars 40-41 == bars 9-10 : {same} ({len(coda[n])} notes)')
for n in ('Tenor', 'Bass'):
    same = src_lo[n] == coda[n]
    ok &= same
    print(f'{n:8s} bars 40-41 == bars 23-24: {same} ({len(coda[n])} notes)')
axis = deg(65)  # E#4
for lo, hi in (('Tenor', 'Alto'), ('Bass', 'Soprano')):
    a, b = coda[hi], coda[lo]
    mir = len(a) == len(b) and all(x[0] == y[0] and x[1] == y[1] and deg(y[2]) == 2 * axis - deg(x[2])
                                  for x, y in zip(a, b))
    ok &= mir
    print(f'{lo} is the E#4 mirror of {hi}, same rhythm, zero offset: {mir}')

extract = {'metadata': {'meter': [12, 8], 'bpm': 132, 'key': 'C#', 'mode': 'major'},
           'voices': [{'name': n, 'abbr': n[0], 'events': [{'t': t + BARQ - 0.5, 'd': dd, 'p': p} for t, dd, p in coda[n]]}
                      for n in ('Soprano', 'Alto', 'Tenor', 'Bass')]}
R = analyse(extract)
s = R['summary']
print('critic on the four extracted lines:',
      {k: s[k] for k in ('parallels_error', 'parallels_weak', 'beat_parallels', 'dissonance_unresolved',
                         'pc_tripled_on_beats_pct', 'low_register_seconds', 'crossings', 'keyboard_unplayable_pct',
                         'tertian_fit_pct')})
print('dissonance kinds:', s['dissonance_kinds'])
print('beat harmony (bar 40 | bar 41):', ' | '.join(str(x) for x in R['harmony']['labels'][4:12]))
R2 = analyse(d, (40, 41))
print('critic on the full score, bars 40-41:',
      {k: len([x for x in R2[k] if x.get('sev') not in ('note', 'ok')]) for k in ('parallels', 'beat_parallels', 'dissonance')})
print('ALL CHECKS PASS' if ok else 'CHECK FAILED')
