"""For each tripled beat, try moving ONE non-theme note (that starts on that beat) to a
nearby pitch; keep alternatives that remove the tripling and add no parallel error,
beat-to-beat parallel, unresolved dissonance, unison or new tripling nearby.  Checker
only: it prints options; the composer chooses and edits the source by hand."""
import sys, json, copy, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'tools'))
from critic import analyse, Score
from chords import pname
data = json.load(open(sys.argv[1]))
# theme note spans: (voice, t0, t1) from subject_entries (approx: entry start + its length)
def theme_spans(d):
    L = {}
    lens = {'Ground': 24, 'Ground augm.': 48}
    out = []
    for e in d['subject_entries']:
        lab = e['label']
        n = 48 if 'augm' in lab else (24 if lab.startswith('Ground') else 12)
        out.append((e['voice'], e['t'], e['t'] + n))
    return out
TH = theme_spans(data)
def is_theme(vi, t):
    return any(v == vi and a - 1e-6 <= t < b - 1e-6 for v, a, b in TH)
def metrics(d, lo, hi):
    R = analyse(d, (lo, hi))
    par = sum(1 for x in R['parallels'] if x['sev'] in ('error', 'doubling'))
    bpar = sum(1 for x in R['beat_parallels'] if x['sev'] != 'doubling')
    un = sum(1 for x in R['dissonance'] if x['sev'] == 'error')
    S = Score(d)
    trip = 0; uni = 0
    for t in range((lo - 1) * S.bar, hi * S.bar, S.beat):
        ps = [S.note(i, k)['p'] for i, (k, _) in S.sounding(t).items()]
        c = collections.Counter(p % 12 for p in ps)
        if len(ps) >= 3 and max(c.values()) >= 3: trip += 1
        cc = collections.Counter(ps)
        uni += sum(v - 1 for v in cc.values())
    return par, bpar, un, trip, uni
S = Score(data)
lo_bar, hi_bar = (int(x) for x in sys.argv[2].split('-'))
for t in range((lo_bar - 1) * S.bar, hi_bar * S.bar, S.beat):
    snd = S.sounding(t)
    ps = [(S.note(i, k)['p'], i, k) for i, (k, _) in snd.items()]
    c = collections.Counter(p % 12 for p, _, _ in ps)
    if len(ps) < 3 or max(c.values()) < 3: continue
    pc = c.most_common(1)[0][0]
    bar = t // S.bar + 1
    base = metrics(data, bar - 1, bar + 1)
    opts = []
    for p, i, k in ps:
        n = S.note(i, k)
        if p % 12 != pc or n['s'] != t or is_theme(i, n['s'] / 48): continue
        for q in range(p - 5, p + 6):
            if q == p: continue
            d = copy.deepcopy(data)
            for e in d['voices'][i]['events']:
                if abs(e['t'] * 48 - t) < 1: e['p'] = q
            m = metrics(d, bar - 1, bar + 1)
            if m[0] <= base[0] and m[1] <= base[1] and m[2] <= base[2] and m[3] < base[3] and m[4] <= base[4]:
                opts.append(f"{S.names[i]}:{pname(p, True)}->{pname(q, True)}")
    print(S.loc(t), pname(pc + 60, True)[:-1], 'base', base, '|', ' '.join(opts) if opts else '-- no single-note fix')
