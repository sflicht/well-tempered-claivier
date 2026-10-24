from mini import *
from pk import SUBJ,CSA,avg,n_issues
import itertools
Ts={'uni':(0,0),'5dn':(-4,-7),'4up':(3,5)}
ped='D2:64'
res=[]
for l1 in (5,6,7,8,9):
 for l2 in (2,3,4,5,6):
  for n2 in ('uni','5dn','4up'):
   for n3 in ('uni','5dn','4up'):
    for o2 in (-1,0,1):
     for o3 in (-2,-1,0,1,2):
      for ocs in (-2,-1,0,1):
        a2=Ts[n2];a3=Ts[n3]
        s2=T(SUBJ,a2[0]+7*o2,a2[1]+12*o2); s3=T(SUBJ,a3[0]+7*o3,a3[1]+12*o3)
        cs=T(CSA,-4+7*ocs,-7+12*ocs)
        ents=[(SUBJ,0),(s2,l1),(s3,l1+l2),(cs,0)]
        order=sorted(ents,key=lambda e:-avg(e[0]))
        if avg(order[-1][0])<50: continue
        R=check(order+[(ped,0)])
        n=sum(n_issues(R))
        if n==0: res.append((l1,l2,n2,o2,n3,o3,ocs,len(R['xrel_list'])))
print(len(res))
for r in res: print(r)
