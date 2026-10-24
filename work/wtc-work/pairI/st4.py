from st3 import *
import sys
lag,S,lead,k,key=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
s=tr(SUBJ,k);i=tinv(s,S,key=key)
A,B=(s,i) if lead=='S' else (i,s)
print('lead  ',' '.join(f"{n(p)}:{d}" for p,d in A));print('follow',' '.join(f"{n(p)}:{d}" for p,d in B))
gA=grid(A+[(None,lag)]);gB=grid([(None,lag)]+B)
print(' '.join(f"{x}:{n(gA[x][0]) if gA[x][0] else '-'}/{n(gB[x][0]) if gB[x][0] else '-'}={iv(gA[x][0],gB[x][0]) if gA[x][0] and gB[x][0] else ''}" for x in range(0,len(gA),2)))
