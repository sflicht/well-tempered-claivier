"""Inspect a built score: per-beat (or per-eighth) grid of all voices with chord labels,
plus the critic's problems in the range.  Usage: look.py score.json 9-16 [8]"""
import sys, json, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from critic import Score, analyse, TPQ
from chords import name_chord, pname
data = json.load(open(sys.argv[1]))
lo, hi = (int(x) for x in sys.argv[2].split('-'))
step = TPQ * 4 // int(sys.argv[3]) if len(sys.argv) > 3 else TPQ
S = Score(data)
print('     ' + ' '.join(f'{n:>5}' for n in S.names))
for t in range((lo - 1) * S.bar, hi * S.bar, step):
    snd = S.sounding(t)
    cells = []
    pcs = set(); low = None
    for i in range(len(S.voices)):
        if i in snd:
            k, att = snd[i]
            p = S.note(i, k)['p']
            pcs.add(p % 12); low = p if low is None or p < low else low
            cells.append(f"{pname(p, True):>4}{'*' if att else ' '}")
        else:
            cells.append('    .')
    nm = name_chord(pcs, low % 12 if low is not None else None, True) if pcs else ''
    print(f"{S.loc(t):>7} " + ' '.join(cells) + f"  {nm or ''}")
R = analyse(data, (lo, hi))
for k in ('parallels', 'beat_parallels'):
    for x in R[k]:
        if x['sev'] in ('error', 'warn', 'doubling'):
            print('  PAR', x['sev'], x['loc'], x['voices'], x['kind'], x['what'])
for x in R['dissonance']:
    if x['sev'] != 'ok':
        print('  DIS', x['loc'], x['kind'], x['what'])
for x in R['melody']:
    if x['sev'] == 'warn':
        print('  MEL', x['loc'], x['kind'], x['what'])
for x in R['direct']:
    print('  DIR', x['loc'], x['what'])
low = [l for l in R['sonority']['low_register_examples'] if lo <= int(l[1:].split('.')[0]) <= hi]
if low:
    print('  LOW', low)
print('  texture', ' '.join(str(r['moving']) for r in R['texture'][lo - 1:hi]))
