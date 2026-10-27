"""List beats where a pitch class sounds in 3+ voices, with the voices involved."""
import sys, json, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from critic import Score, TPQ
from chords import chord_candidates, pname, NAMES_FLAT
S = Score(json.load(open(sys.argv[1])))
lo, hi = (int(x) for x in sys.argv[2].split('-')) if len(sys.argv) > 2 else (1, S.nbars)
n = tot = 0
for t in range((lo - 1) * S.bar, hi * S.bar, S.beat):
    snd = S.sounding(t)
    ps = [(S.note(i, k)['p'], i) for i, (k, _) in snd.items()]
    if len(ps) < 3:
        continue
    tot += 1
    c = collections.Counter(p % 12 for p, _ in ps)
    pc, m = c.most_common(1)[0]
    if m >= 3:
        n += 1
        bass = min(ps)[0] % 12
        cands = chord_candidates(set(c), bass)
        role = '?'
        if cands:
            r, q = cands[0]
            iv = (pc - r) % 12
            role = {0: 'root', 7: '5th', 6: '5th', 3: '3rd', 4: '3rd', 10: '7th', 11: '7th', 9: '7th'}.get(iv, str(iv))
        who = ','.join(S.names[i] for p, i in ps if p % 12 == pc)
        print(f"{S.loc(t):>7} {NAMES_FLAT[pc]:3s} x{m} {role:4s} [{who}]")
print(f'{n}/{tot} = {100*n/max(1,tot):.1f}%')
