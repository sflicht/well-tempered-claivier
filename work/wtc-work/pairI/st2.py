from cp import *
import sys
SUBJ=parse('C5:4 Db5:2 B4:2 D5:2 Bb4:2 Eb5:2 A4:2 Ab4:2 G4:2 F4:1 Eb4:1 D4:1 F4:1 Eb4:2 D4:2 C4:4')
lag,S,lead,k=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],int(sys.argv[4])
s=tr(SUBJ,k);i=mirror(SUBJ,S)
A,B=(s,i) if lead=='S' else (i,s)
print('lead ',' '.join(f"{n(p) if p else 'R'}:{d}" for p,d in A))
print('follow',' '.join(f"{n(p) if p else 'R'}:{d}" for p,d in B))
gA=grid(A+[(None,lag)]);gB=grid([(None,lag)]+B)
for x in range(0,len(gA),2):
    a=gA[x][0];b=gB[x][0]
    print(x, n(a) if a else '-', n(b) if b else '-', iv(a,b) if a and b else '')
