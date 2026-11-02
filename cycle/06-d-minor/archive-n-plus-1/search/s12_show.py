import sys
from lab2 import *
AUG = ground(1, 0, 2); SOP = ground(5, 31)
lines = []
for spec in sys.argv[1:]:
    form, nm, b, beat = spec.split(',')
    from lab import wtclib
    p0 = wtclib.parse_tok(nm + ':1')[0]
    base = 69
    sh = p0 - base
    lines.append(subj(int(b), sh, int(beat)) if form == 'rect' else inv(int(b), sh, int(beat)))
lo = min(s for l in lines for s, _, _ in l); hi = max(s + d for l in lines for s, d, _ in l)
grid([SOP] + lines + [AUG], (lo // 12) * 12, hi, 4)
