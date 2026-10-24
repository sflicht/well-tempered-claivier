from piece import *
gU=G(U)
Ab={8,0,3};Fm={5,8,0};Dd={2,5,8,0};G7={7,11,2,5}
pl=[Ab,Ab,Fm,Dd,G7,G7,G7,G7]
t0=26*16
ch=lambda t: pl[(t-t0)//4] if t0<=t<t0+32 else None
for seed in range(3):
    r=gen(gU,[2]*16,t0,{0,2,3,5,7,8,11},(36,56),above=False,chords=ch,target=interp([(t0,44),(t0+12,38),(t0+16,43),(t0+31,43)]),seed=seed,prev0=44)
    print(round(r[1],1),tobars(r[0]))
