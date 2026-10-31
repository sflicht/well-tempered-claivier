from lab import *
import sys
exec(open('summit_inner_critic.py').read().split("alto_c = []")[0])
from wtclib import parse_tok
def place(form, lvl, bar, beat):
    tok, base = (SUBJECT, 69) if form == 'subj' else (INV, 74)
    sh = parse_tok(lvl + ':1')[0] - base
    return notes(tok, (bar - 1) * 12 + (beat - 1) * 4, sh)
combos = [(('subj','D4',47,1),('inv','D4',49,3)), (('subj','C4',48,1),('inv','D4',49,3)),
          (('subj','D4',48,3),('inv','D4',49,3)), (('subj','E4',49,2),('inv','E4',51,3)),
          (('subj','D4',47,1),('inv','A4',50,1)), (('subj','D4',47,1),('inv','D4',50,1)),
          (('inv','A4',48,3),('subj','D4',49,1)), (('inv','D5',48,1),('subj','A3',49,1)),
          (('subj','D4',47,1),('inv','G4',49,3)), (('subj','D4',47,1),('inv','E4',50,1))]
for a, t in combos:
    A = place(*a); T = place(*t)
    lo = min(A[0][0], T[0][0]); hi = max(A[-1][0] + A[-1][1], T[-1][0] + T[-1][1])
    pe, bp, un, R = crit([SOP, A, T, AUG], lo, hi)
    c, bad = cons_cost([SOP, A, T, AUG], lo, hi)
    cross = len(R['crossing'])
    errs = [ (x['loc'], x['voices'], x['what']) for x in R['parallels'] if x['sev']=='error']
    uns = [(x['loc'], x['kind'], x['what']) for x in R['dissonance'] if x['sev']=='error']
    print(a, t, 'par', pe, 'bpar', bp, 'unres', un, 'cross', cross, 'cost', round(c,1), errs[:3], uns[:3])
