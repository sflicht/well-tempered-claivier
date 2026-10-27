import sys, json
sys.path.insert(0, '.')
from xxiv import *
import build1, build2
NB = int(sys.argv[1]) if len(sys.argv) > 1 else 12
sc = Score(1)
build1.wave1(sc)
build2.wave2(sc)
bars = sc.bars(NB)
voices = [(n, n, clef, 70) for n, long, clef in VOICES]
B, C, Cs, D, Ds, E, F, Fs, G, Gs, A, As = 11, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
def sub_plan(o, k):     # harmony implied by the subject starting at beat o, transposed by k semitones
    rows = [(0, 1.5, [B, D, Fs]), (1.5, 2, [B, D, Fs, Cs]), (2, 3.5, [Cs, F, Gs, B]), (3.5, 4, [Fs, As, Cs]), (4, 5.5, [B, Ds, Fs, A]),
            (5.5, 6, [E, G, B]), (6, 7, [C, E, G]), (7, 8, [B, Ds, Fs, A]), (8, 8.5, [E, G, B]),
            (8.5, 9, [F, Gs, B, D]), (9, 9.5, [D, Fs, A, Cs]), (9.5, 10, [Fs, As, Cs, E])]
    return [[o + a, o + b, sorted((x + k) % 12 for x in pcs), 'S-harm%+d' % k] for a, b, pcs in rows]
def rows(o, rr): return [[o + a, o + b, pcs, lab] for a, b, pcs, lab in rr]
plan = sub_plan(0, 0) + sub_plan(10, -5) + sub_plan(20, 0) + sub_plan(30, -5)
plan += rows(40, [(0, 1, [Fs, A, Cs], 'F#m'), (1, 2, [B, D, Fs], 'Bm/F#'), (2, 4, [B, D, Fs], 'Bm'), (4, 6, [E, Gs, B, D], 'E7/G#'), (6, 8, [A, Cs, E, G], 'A7')])
plan += sub_plan(48, 3)
plan += rows(58, [(0, 2, [D, F, A], 'Dm'), (2, 4, [G, B, D, F], 'G7'), (4, 6, [C, E, G], 'C'), (6, 8, [Fs, A, C, E], 'F#o7'), (8, 10, [B, Ds, Fs, A], 'B7'), (10, 14, [E, G, B], 'Em')])
W.build_score('btest.json', {'meter':[4,4],'bpm':63,'key':'B','mode':'minor','title':'test'}, voices, bars,
   extra={'harmonic_plan': plan, 'themes':[{'voice':v,'t':float(t/4),'label':l,'key':k,'scale':s,'semis':se,'inverted':inv} for v,t,l,k,s,se,inv in sc.entries]})
