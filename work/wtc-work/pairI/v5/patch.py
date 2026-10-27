# hand rewrite of b24.3-b29 (applied after s5.py)
L=open('v5/lit.txt').read().splitlines()
def rep(prefix,new):
    global L
    idx=[i for i,l in enumerate(L) if l.startswith(prefix)]
    assert len(idx)==1,(prefix,idx); L[idx[0]]=new
rep("put(U,24,","put(U,24,'C5:2 Ab4:1 Bb4:1 C5:2 G4:2',8)")
rep("put(U,25,","put(U,25,'Eb5:2 G5:2 D5:2 G5:2 C5:1 F5:1 Ab5:1 C6:1 B5:1 G5:1 D5:1 G5:1 F5:1 Ab5:1 C6:1 Ab5:1 A5:1 C6:1 Eb6:1 C6:1 D6:1 G6:1 D6:1 Eb6:1 D6:1 C6:1 B5:1 D6:1',0)")
rep("put(L,25,","put(L,25,'C3:4 Bb2:4 Ab2:4 G2:4 F2:4 F#2:4 G2:4 G2:2 F2:2',0)")
rep("put(L,27,'G2","put(L,27,'G2:4 C3:2 F2:2 C3:2 Eb2:2 C3:2 B2:2 C3:4 Ab2:4 G2:4',4)")
rep("put(U,29,'G6","put(U,29,'Eb6:4',0)")
rep("put(U,29,'D6","put(U,29,'C6:1 Eb6:1 C6:1 Ab5:1 Db6:2 Ab5:2 F5:1 Ab5:1 Db6:1 Ab5:1',4)")
open('v5/lit.txt','w').write('\n'.join(L)+'\n')
