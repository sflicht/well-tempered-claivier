from pk import *
CSAUG=AUG(CSD).replace('F#4:4 E4:4','F#4:6 E4:2').replace('D4:4 E4:4','D4:6 E4:2').replace('B4:4 A4:4','B4:6 A4:2')
Ts={'uni':(0,0),'5dn':(-4,-7),'4up':(3,5),'5up':(4,7),'4dn':(-3,-5)}
AS=OCT(AUG(SUBJ),-2); CSM=OCT(CSAUG,-2)
res=[]
for l1 in range(2,17):
  for n2 in Ts:
    for o1 in (-1,0,1):
     for o2 in (-1,0,1,2):
        a2=Ts[n2]
        s1=OCT(SUBJ,o1)
        s2=T(SUBJ,a2[0]+7*o2,a2[1]+12*o2)
        ents=[(AS,0),(CSM,0),(s1,0),(s2,l1)]
        order=sorted(ents,key=lambda e:-avg(e[0]))
        R=check(order); n=n_issues(R)
        res.append((sum(n),n,(l1,n2,o1,o2),len(R['xrel_list'])))
res.sort()
for r in res[:60]: print(r)
