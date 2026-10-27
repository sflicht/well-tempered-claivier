import sys, json
sys.path.insert(0,'.')
from xxiv import *
from conv_a import part_a
sc = Score(1)
part_a(sc, 1)
NB = 12
bars = sc.bars(NB)
voices = [(n, n, clef, 70) for n, long, clef in VOICES]
data = W.build_score('conv_test.json', {'meter':[4,4],'bpm':60,'key':'B','mode':'minor','title':'test'}, voices, bars,
   extra={'themes':[{'voice':v,'t':float(t/4),'label':l,'key':k,'scale':s,'semis':se,'inverted':inv} for v,t,l,k,s,se,inv in sc.entries]})
