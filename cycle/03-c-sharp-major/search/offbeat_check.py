"""Off-beat dissonance audit (the critic checks beats only).

For every attack on a non-beat eighth or sixteenth, report dissonant intervals
(2nds, 7ths, tritones, 4ths against the bass) in which the dissonant note
neither arrives nor leaves by step (i.e. is not a passing/neighbour/suspension
figure).  Usage: offbeat_check.py score.json
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from critic import Score, TPQ
from chords import pname

S = Score(json.load(open(sys.argv[1])))
issues = []
for t in S.onsets:
    if S.strength(t) >= 2:
        continue
    snd = S.sounding(t)
    items = sorted((S.note(i, k)['p'], i, k, att) for i, (k, att) in snd.items())
    if len(items) < 2:
        continue
    bass = items[0][0]
    for x in range(len(items)):
        for y in range(x + 1, len(items)):
            lo, ilo, klo, alo = items[x]; hi, ihi, khi, ahi = items[y]
            c = (hi - lo) % 12
            diss = c in (1, 2, 10, 11, 6) or (c == 5 and x == 0)
            if not diss or not (alo or ahi):
                continue
            ok = False
            for (p, i, k, a) in ((lo, ilo, klo, alo), (hi, ihi, khi, ahi)):
                if not a:
                    continue
                prv, nxt = S.prev_note(i, k), S.next_note(i, k)
                if (prv and 1 <= abs(p - prv['p']) <= 2) or (nxt and 1 <= abs(nxt['p'] - p) <= 2):
                    ok = True
            if not ok:
                issues.append(f"{S.loc(t)} {S.names[ilo]}{pname(lo)}/{S.names[ihi]}{pname(hi)}")
print(len(issues), 'off-beat dissonances not explained by stepwise motion')
for s in issues:
    print('  ', s)
