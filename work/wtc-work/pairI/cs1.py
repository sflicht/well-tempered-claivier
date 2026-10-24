from gen import *
ANS=parse('G3:4 F#3:2 Ab3:2 F3:2 A3:2 E3:2 Bb3:2 B3:2 C4:2 D4:1 Eb4:1 F4:1 D4:1 Eb4:2 F4:2 G4:4')
other=G([(0,ANS)])
CH={0:{0,3,7},4:{2,0,8,5,3,6,9},8:{2,5,0,9},12:{0,7,10,4},16:{7,11,2,5},20:{7,11,2,5},24:{0,3,7},28:{7,11,2}}
ch=lambda x:CH.get(x%32 - (x%32)%4)
R=[2,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1,  1,1,1,1, 2,2, 1,1,1,1, 1,1,2]
pcs={0,2,3,5,7,8,10,11}
tg=interp([(0,79),(8,72),(14,76),(20,79),(26,72),(31,74)])
for seed in range(4):
    line,c=gen(other,R,0,pcs,(65,84),above=True,chords=ch,seed=seed,target=tg,tw=0.3)
    print(round(c,1),' '.join(tobars(line)))
