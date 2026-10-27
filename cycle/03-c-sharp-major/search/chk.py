"""Build the current draft and report: critic summary/issues for a bar range, and a grid."""
import sys, json, importlib
sys.argv = sys.argv
from asm import *
import draft
from wtclib import build_score
from critic import analyse
from lib import grid as lgrid

OUT = '/tmp/claude-0/-home-user-well-tempered-claivier/9e003b56-0315-515e-a129-a5b629d0f3cb/scratchpad/fdraft.json'
nb = int(sys.argv[1]); lo = int(sys.argv[2]); hi = int(sys.argv[3])
showgrid = len(sys.argv) > 4
bars = {k: assemble(v, nb) for k, v in draft.V.items()}
names = {'S': 'Soprano', 'A': 'Alto', 'T': 'Tenor', 'B': 'Bass'}
meta = {'meter': [12, 8], 'bpm': 150, 'key': 'C#', 'mode': 'major', 'subtitle': 'draft'}
data = build_score(OUT, meta, [(names[k], k, 'treble', 70) for k in 'SATB'], {names[k]: bars[k] for k in 'SATB'})
R = analyse(data, (lo, hi))
s = R['summary']
print({k: s[k] for k in ('parallels_error', 'parallels_weak', 'beat_parallels', 'pc_tripled_on_beats_pct', 'dissonance_unresolved', 'keyboard_unplayable_pct', 'crossings', 'low_register_seconds')})
for x in R['parallels']:
    if x['sev'] != 'note': print('  par', x['loc'], x['voices'], x['kind'], x['what'])
for x in R['beat_parallels']: print('  bpar', x['loc'], x['voices'], x['kind'], x['what'])
for x in R['dissonance']:
    if x['sev'] != 'ok': print('  dis', x['loc'], x['kind'], x['what'])
for x in R['melody']:
    if x['sev'] == 'warn': print('  mel', x['loc'], x['kind'], x['what'])
for x in R['crossing']: print('  cross', x['loc'], x['what'])
kb = R['keyboard']
bad = [e for e in kb['examples']]
print('  kb', [(e['loc'], e['what']) for e in bad if lo <= int(e['loc'][1:].split('.')[0]) <= hi][:8])
labs = R['harmony']['labels']
for b in range(lo, hi + 1):
    print(f'  b{b}', ' | '.join(str(x) for x in labs[(b - 1) * 4:(b) * 4]))
if showgrid:
    lines = [(' '.join(bars[k]), 0) for k in 'SATB']
    lgrid(lines, start=(lo - 1) * 24, end=hi * 24)
import collections
from critic import Score
from chords import pname
Sx = Score(data)
trip = []
for t in range(0, Sx.end, Sx.beat):
    if not (lo <= t // Sx.bar + 1 <= hi):
        continue
    ps = [Sx.note(i, k)['p'] for i, (k, _) in Sx.sounding(t).items()]
    if len(ps) >= 3:
        c = collections.Counter(p % 12 for p in ps)
        if max(c.values()) >= 3:
            trip.append(Sx.loc(t) + ' ' + ' '.join(pname(p) for p in sorted(ps)))
print('  tripled:', trip)
