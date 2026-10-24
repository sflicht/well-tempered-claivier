from v2.comp import *
f=dinv(0,74)
S=ln('C5:4 B4:2 D5:2 Ab4:2 Eb5:2 G4:2 F5:2 Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 G4:2')
A=[(f(p),d) for p,d in S]
oth=G([(0,A)])
rh=[1]*14+[2,2]+[1]*6+[2,2,2]
ch=chords(['Cm','Do','G7','Cm','Cm','Cm','Fm','G7'],1)
tgt=lambda t: 74+ (3 if t<12 else 0) - (t-12)//8
best=None
for seed in range(6):
  try:
    line,c=gen(oth,rh,2,CMIN,(65,82),above=True,chords=ch,seed=seed,target=tgt,tw=.15,beam=800)
  except RuntimeError as e: print(e);continue
  if best is None or c<best[1]: best=(line,c)
print(best[1]); print('CS = R:2 '+nm_line(best[0])); print('ANS=',nm_line(A))
