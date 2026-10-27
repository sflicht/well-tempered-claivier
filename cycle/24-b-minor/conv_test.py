import sys, json
sys.path.insert(0,'.')
from xxiv import *
from conv_a import part_a, plan_a
from conv_b import part_b, plan_b
from conv_c import part_c, plan_c
sc = Score(1)
part_a(sc, 1)
part_b(sc, 1)
part_c(sc, 1)
NB = 14
bars = sc.bars(NB)
voices = [(n, n, clef, 70) for n, long, clef in VOICES]
data = W.build_score('conv_test.json', {'meter':[4,4],'bpm':60,'key':'B','mode':'minor','title':'test'}, voices, bars,
   extra={'harmonic_plan': plan_a(0) + plan_b(20) + plan_c(36), 'themes':[{'voice':v,'t':float(t/4),'label':l,'key':k,'scale':s,'semis':se,'inverted':inv} for v,t,l,k,s,se,inv in sc.entries]})
