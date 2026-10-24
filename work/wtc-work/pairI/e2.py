from piece import *
gU=G(U)
Gm={7,10,2};Cm={0,3,7};Fm={5,8,0};C7={0,4,7,10}
pl=[Gm,Gm,Cm,Cm,Fm,Fm,C7,C7]
ch=lambda t: pl[(t-160)//4] if 160<=t<192 else None
for seed in range(3):
    r=gen(gU,[2]*16,160,{0,2,3,5,7,8,10,11,4,9,1,6},(40,58),above=False,chords=ch,target=interp([(160,55),(176,48),(191,48)]),seed=seed)
    print(r[1] if isinstance(r,tuple) else '',tobars(r[0] if isinstance(r,tuple) else r))
