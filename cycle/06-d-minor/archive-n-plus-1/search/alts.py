"""Check alternatives for one note (checker only; the composer chooses and writes it).
Usage: alts.py score.json VOICE BAR.BEAT[.5] [pitch names...]
Reports, for each candidate pitch, the critic's parallel errors, beat-to-beat
parallels, unresolved dissonances and unisons in a window of two bars around."""
import sys, json, copy
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from critic import analyse
from chords import pname
import wtclib
data = json.load(open(sys.argv[1]))
abbr = sys.argv[2]
bb = sys.argv[3].split('.')
bar, beat = int(bb[0]), float('.'.join(bb[1:]))
t = (bar - 1) * 3 + (beat - 1)
vi = [v['abbr'] for v in data['voices']].index(abbr)
ev = [e for e in data['voices'][vi]['events'] if abs(e['t'] - t) < 1e-6]
assert ev, 'no note there'
e0 = ev[0]
cands = [wtclib.parse_tok(n + ':1')[0] for n in sys.argv[4:]] or list(range(e0['p'] - 7, e0['p'] + 8))
def score(d):
    R = analyse(d, (bar - 1, bar + 2))
    s = R['summary']
    par = sum(1 for x in R['parallels'] if x['sev'] == 'error')
    bpar = sum(1 for x in R['beat_parallels'] if x['sev'] != 'doubling')
    un = sum(1 for x in R['dissonance'] if x['sev'] == 'error')
    return par, bpar, un
uni = lambda d, p: sum(1 for j, v in enumerate(d['voices']) if j != vi for e in v['events']
                       if e['t'] <= t < e['t'] + e['d'] and e['p'] == p)
base = score(data)
print('current', pname(e0['p'], True), base, 'unison', uni(data, e0['p']))
for p in cands:
    d = copy.deepcopy(data)
    for e in d['voices'][vi]['events']:
        if abs(e['t'] - t) < 1e-6:
            e['p'] = p
    print(f'{pname(p, True):5s}', score(d), 'unison', uni(d, p))
