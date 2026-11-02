"""Grid view of fugue.json: per beat (or eighth) with chord labels and critic flags.
Usage: look.py LO-HI [8]"""
import sys, json, subprocess
from pathlib import Path
ROOT = Path('/home/user/well-tempered-claivier')
sys.path.insert(0, str(ROOT / 'tools'))
from critic import Score, analyse, TPQ
from chords import name_chord, pname
F = Path(__file__).resolve().parents[1] / 'fugue.json'
data = json.load(open(F))
lo, hi = (int(x) for x in sys.argv[1].split('-'))
step = TPQ * 4 // int(sys.argv[2]) if len(sys.argv) > 2 else TPQ
S = Score(data)
print('        ' + ' '.join(f'{n[:5]:>5}' for n in S.names))
for t in range((lo - 1) * S.bar, hi * S.bar, step):
    snd = S.sounding(t)
    cells, pcs, low = [], set(), None
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
so = R['sonority']
print('  bad doublings', [b for b in so['bad_doubling_examples'] if lo <= int(b[1:].split('.')[0]) <= hi])
print('  low', [l for l in so['low_register_examples'] if lo <= int(l[1:].split('.')[0]) <= hi])
print('  crossings', [c for c in R['crossing']] if isinstance(R['crossing'], list) else R['crossing'])
kb = R['keyboard']
print('  keyboard', kb['unplayable_onsets'], '/', kb['onsets'], kb['examples'][:6])
