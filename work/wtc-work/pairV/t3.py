from mini import *
SUBJ='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
CSA='E5:2 D5:2 C#5:2 B4:2 A4:2 B4:2 C#5:2 D5:2 E5:3 F#5:1 A5:2 G#5:2 F#5:2 E5:2 D5:2 C#5:2'
CSD=T(CSA,-4,-7)
KSA={'F':1,'C':1,'G':1}
ANS=T(SUBJ,4,7)  # E5.. A major
Bm=TD(SUBJ,-2); CSBm=TD(CSD,-2)
print('Bm  ',Bm);print('CSBm',CSBm)
# answer in F#m: A-major notes shifted -2 steps
Fsm=TD(ANS,-2,KSA,KSA); CSFsm=TD(T(CSA,0,0),-2,KSA,KSA)
print('F#m ',Fsm);print('CSF#m',CSFsm)
import itertools
for lag in (4,5,6,7,8):
  for o2 in (-1,0,1):
    for oc in (-1,0,1,2):
      R=check([(Bm,0),(T(Fsm,7*o2,12*o2),lag),(T(CSBm,7*oc,12*oc),0)])
      n=[len(R['beat_dissonance_both_attacking(unprepared)']),len(R['m2/M7_clash_list']),len(R['par16_list']),len(R['parallel_5ths_8ves(eighth grid, attack to attack)'])]
      if sum(n)<=1: print(lag,o2,oc,n,R['beat_dissonance_both_attacking(unprepared)'][:2],R['m2/M7_clash_list'][:2])
print('--- no CS')
for lag in range(3,13):
  for o2 in (-1,0,1):
      R=check([(Bm,0),(T(Fsm,7*o2,12*o2),lag)])
      n=[len(R['beat_dissonance_both_attacking(unprepared)']),len(R['m2/M7_clash_list']),len(R['par16_list']),len(R['parallel_5ths_8ves(eighth grid, attack to attack)'])]
      if sum(n)==0: print(lag,o2,n)
print('--- both with Bm/Bm unison etc')
for lag in range(3,13):
  for name,s2 in [('Bm',Bm),('Bm5dn',TD(Bm,-4)),('Bm4up',TD(Bm,3))]:
   for o2 in (-1,0,1):
      R=check([(Bm,0),(T(s2,7*o2,12*o2),lag)])
      n=[len(R['beat_dissonance_both_attacking(unprepared)']),len(R['m2/M7_clash_list']),len(R['par16_list']),len(R['parallel_5ths_8ves(eighth grid, attack to attack)'])]
      if sum(n)==0: print(name,lag,o2,n)
