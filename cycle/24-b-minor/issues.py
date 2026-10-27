#!/usr/bin/env python3
"""Diagnostics in one listing (reports only; it never changes a note):
parallels, beat parallels, the critic's UNRESOLVED/UNPREPARED dissonances (with what each note
does next), doubled sevenths / leading tones (with the voices that double them), low-register
seconds.  Usage: issues.py score.json [a-b] [--voices S1,A2]"""
import argparse, json, sys, collections
sys.path.insert(0, '/home/user/well-tempered-claivier/tools')
import critic
from critic import chord_candidates
from chords import pname

ap = argparse.ArgumentParser(); ap.add_argument('score'); ap.add_argument('bars', nargs='?', default='1-999')
ap.add_argument('--voices', default=''); ap.add_argument('--quiet', action='store_true')
a = ap.parse_args()
lo, hi = (int(x) for x in a.bars.split('-'))
want = set(x for x in a.voices.split(',') if x)
d = json.load(open(a.score))
S = critic.Score(d)
R = critic.analyse(d)
bar_of = lambda loc: int(loc[1:].split('.')[0])
inr = lambda loc: lo <= bar_of(loc) <= hi
hit = lambda names: not want or any(n in want for n in names)
un = [x for x in R['dissonance'] if x['kind'].startswith('UN')]
bad = []
for t in range(0, S.end, S.beat):
    snd = S.sounding(t)
    ps = [(S.note(i, k)['p'], S.names[i]) for i, (k, _) in snd.items()]
    if len(ps) < 3:
        continue
    cnt = collections.Counter(p % 12 for p, _ in ps)
    c = chord_candidates(set(cnt), min(p for p, _ in ps) % 12)
    if not c:
        continue
    root, q = c[0]
    sev = {'7': 10, 'm7': 10, 'ø7': 10, 'o7': 9, 'maj7': 11, '7(no5)': 10, 'm(no5)7': 10}.get(q)
    if sev is not None and cnt[(root + sev) % 12] >= 2:
        bad.append((S.loc(t), '7th', [n + pname(p) for p, n in ps if p % 12 == (root + sev) % 12]))
    if q in ('7', '7(no5)') and cnt[(root + 4) % 12] >= 2:
        bad.append((S.loc(t), 'LT', [n + pname(p) for p, n in ps if p % 12 == (root + 4) % 12]))
s = R['summary']
print(f"TOTAL parallels {s['parallels_error']}/{s['parallels_weak']}  beatpar {s['beat_parallels']}  unresolved {len(un)}  "
      f"bad_doublings {len(bad)}  low {s['low_register_seconds']}  stepwise {s['stepwise_pct']}  moving {s['mean_moving_voices']}")
print('MOVING', ' '.join(f"{r['bar']}:{r['moving']}" for r in R['texture'] if lo <= r['bar'] <= hi))
if a.quiet:
    sys.exit()
for x in R['parallels']:
    if x['sev'] in ('error', 'warn', 'doubling') and inr(x['loc']) and hit(x['voices']):
        print('PAR', x['sev'], x['loc'], x['voices'], x['kind'], x['what'])
for x in R['beat_parallels']:
    if inr(x['loc']) and hit(x['voices']):
        print('BEATPAR', x['loc'], x['voices'], x['kind'], x['what'])
for x in un:
    if not inr(x['loc']):
        continue
    t = x['t']; info = []; names = []
    for i, (k, att) in S.sounding(t).items():
        nm = S.names[i]
        if x['what'].startswith(nm) or ('/' + nm) in x['what']:
            n = S.note(i, k); nx = S.next_note(i, k)
            info.append(f"{nm}:{pname(n['p'])}{'*' if att else '~'}->{pname(nx['p']) if nx else '-'}"); names.append(nm)
    if hit(names):
        print('DISS', x['loc'], x['kind'], ' '.join(info))
for loc, k, who in bad:
    if inr(loc) and hit([w.rstrip('0123456789#b').rstrip('ABCDEFG') for w in who] + [w[:2] for w in who] + [w[:3] for w in who]):
        print('DOUBLE', loc, k, who)
for loc in R['sonority']['low_register_examples']:
    if inr(loc):
        print('LOW', loc)
