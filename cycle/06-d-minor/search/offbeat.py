"""List off-beat (eighth/sixteenth) attacks forming a 2nd/7th/9th/tritone with another sounding voice,
where the attacked note is not approached AND left by step (i.e. not a passing/neighbour note)."""
import sys, json
from pathlib import Path
sys.path.insert(0, '/home/user/well-tempered-claivier/tools')
from critic import Score, TPQ
from chords import pname
d = json.load(open(str(Path(__file__).resolve().parents[1] / 'fugue.json')))
S = Score(d)
for i, v in enumerate(S.voices):
    for k, n in enumerate(v):
        t = n['s']
        if S.strength(t) >= 2:   # beats handled by the critic
            continue
        prv = S.prev_note(i, k); nxt = S.next_note(i, k)
        step_in = prv is not None and 1 <= abs(n['p'] - prv['p']) <= 2 and prv['e'] == t
        step_out = nxt is not None and 1 <= abs(nxt['p'] - n['p']) <= 2
        if step_in and step_out:
            continue
        for j, (kk, att) in S.sounding(t).items():
            if j == i: continue
            q = S.note(j, kk)['p']
            ic = abs(n['p'] - q) % 12
            if ic in (1, 2, 10, 11, 6):
                print(S.loc(t), S.names[i], pname(n['p'], True), 'vs', S.names[j], pname(q, True),
                      'in' if step_in else '', 'out' if step_out else '')
