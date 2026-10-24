from mini import *
import sys
sys.argv=['x']
from fugue_v5_bars import SUBJ,CSA,KSA
Bm=TD(SUBJ,-2); CSBm=TD(T(CSA,-4,-7),-2)
ANS=T(SUBJ,4,7); Fsm=TD(ANS,-2,KSA,KSA); CSFsm=TD(CSA,-2,KSA,KSA)
def rep(a,b,name):
    print(name)
    for oc in range(-3,4):
        R=check([(a,0),(T(b,7*oc,12*oc),0)])
        n=[len(R['beat_dissonance_both_attacking(unprepared)']),len(R['m2/M7_clash_list']),len(R['par16_list']),len(R['parallel_5ths_8ves(eighth grid, attack to attack)'])]
        print(' oct',oc,n,R['m2/M7_clash_list'][:3],R['beat_dissonance_both_attacking(unprepared)'][:3])
rep(Bm,CSBm,'Bm subj / CS_Bm'); rep(Fsm,CSFsm,'F#m ans / CS_F#m')
