import sys
from lab2 import *
from lab import wtclib
AUG = ground(49, 0, 2); SOP = ground(53, 31)
TAIL = [x for x in subj(47, -17) if x[0] >= 48 * 12]
lines = [SOP]
for spec in sys.argv[1:]:
    form, nm, b, beat = spec.split(',')
    sh = wtclib.parse_tok(nm + ':1')[0] - 69
    lines.append(subj(int(b), sh, int(beat)) if form == 'rect' else inv(int(b), sh, int(beat)))
lines += [TAIL, AUG]
lo = min(s for l in lines[1:-2] for s, _, _ in l); hi = max(s + d for l in lines[1:-2] for s, d, _ in l)
grid(lines, (lo // 12) * 12, hi, 4)
