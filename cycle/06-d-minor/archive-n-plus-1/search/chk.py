"""Quick check: rebuild fugue.json, print key critic numbers, flags, and attack stats.
Usage: chk.py [LO-HI for grid]"""
import json, subprocess, sys, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / 'tools'))
from critic import analyse
subprocess.run([sys.executable, str(HERE.parent / 'fugue.py')], check=True)
d = json.load(open(HERE.parent / 'fugue.json'))
R = analyse(d)
s = R['summary']
print({k: s[k] for k in ['stepwise_pct', 'leap_4th_plus_pct', 'parallels_error', 'beat_parallels',
                         'dissonance_unresolved', 'bad_doublings', 'pc_tripled_on_beats_pct',
                         'low_register_seconds', 'mean_moving_voices']})
for x in R['parallels'] + R['beat_parallels']:
    if x['sev'] in ('error', 'warn'):
        print('  PAR', x['sev'], x['loc'], x['voices'], x['kind'], x['what'])
for x in R['dissonance']:
    if 'UNRES' in x['kind'] or 'UNPREP' in x['kind']:
        print('  DIS', x['loc'], x['kind'], x.get('what', ''))
print('  bad doublings', R['sonority']['bad_doubling_examples'], 'low', R['sonority']['low_register_examples'])
bad = [t for t in R['themes'] if t.get('intervals_ok', '').split('/')[0] != t.get('intervals_ok', '').split('/')[-1]]
print('  themes', len(R['themes']), 'bad', bad)
# attack stats
att = collections.Counter()
for v in d['voices']:
    for e in v['events']:
        att[round(e['t'] * 4)] += 1
slots = len(att)
print(f"  onset slots {slots}, >=3 attacks {100 * sum(1 for c in att.values() if c >= 3) / slots:.0f}%, "
      f"16ths: {sum(1 for v in d['voices'] for e in v['events'] if e['d'] <= 0.25)}")
