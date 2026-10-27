#!/usr/bin/env python3
"""Audit the critic's UNRESOLVED / UNPREPARED dissonance flags: for each flag, show both notes
(attacked or held) and what each does next, so the composer can decide which line to re-voice.
Usage: audit.py score.json [a-b]"""
import json, sys, collections
sys.path.insert(0, '/home/user/well-tempered-claivier/tools')
import critic
from chords import pname
d = json.load(open(sys.argv[1]))
a, b = (int(x) for x in sys.argv[2].split('-')) if len(sys.argv) > 2 else (1, 999)
S = critic.Score(d)
R = critic.analyse(d)
cnt = collections.Counter()
per_bar = collections.Counter()
for x in R['dissonance']:
    if not x['kind'].startswith('UN'):
        continue
    bar = int(x['loc'][1:].split('.')[0])
    per_bar[bar] += 1
    if not (a <= bar <= b):
        continue
    t = x['t']
    snd = S.sounding(t)
    info = []
    for i, (k, att) in snd.items():
        nm = S.names[i]
        if nm in x['what']:
            n = S.note(i, k); nx = S.next_note(i, k)
            info.append(f"{nm}:{pname(n['p'])}{'*' if att else '~'}->{pname(nx['p']) if nx else '-'}")
    print(x['loc'], x['kind'], x['what'], ' | ', ' '.join(info))
    cnt[x['what'].split('/')[0]] += 1; cnt[x['what'].split('/')[1]] += 1
print('per bar:', dict(sorted(per_bar.items())))
print('total UN*:', sum(per_bar.values()))
