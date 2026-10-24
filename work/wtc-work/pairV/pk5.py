from pk import *
CSAUG=AUG(CSD).replace('F#4:4 E4:4','F#4:6 E4:2').replace('D4:4 E4:4','D4:6 E4:2').replace('B4:4 A4:4','B4:6 A4:2')
Ts={'uni':(0,0),'5dn':(-4,-7),'4up':(3,5),'5up':(4,7),'4dn':(-3,-5)}
AS=OCT(AUG(SUBJ),-2); CSM=OCT(CSAUG,-2)
res=[]
for (l1,n2,o1,o2) in [(9,'uni',0,1),(9,'uni',-1,1),(9,'uni',1,-1),(9,'uni',0,2),(7,'4up',0,1),(7,'5dn',-1,1),(9,'5up',0,1)]:
 a2=Ts[n2]
 s1=OCT(SUBJ,o1); s2=T(SUBJ,a2[0]+7*o2,a2[1]+12*o2)
 for l3 in range(2,40):
  for n3 in Ts:
   for o3 in (-1,0,1,2):
    a3=Ts[n3]; s3=T(SUBJ,a3[0]+7*o3,a3[1]+12*o3)
    ents=[(AS,0),(CSM,0),(s1,0),(s2,l1),(s3,l3)]
    order=sorted(ents,key=lambda e:-avg(e[0]))
    R=check(order); n=n_issues(R)
    if sum(n)==0: res.append(((l1,n2,o1,o2),(l3,n3,o3),len(R['xrel_list'])))
print(len(res))
for r in res[:80]: print(r)
