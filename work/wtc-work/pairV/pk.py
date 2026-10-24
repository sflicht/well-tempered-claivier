from mini import *
import itertools,sys
SUBJ='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
CSA='E5:2 D5:2 C#5:2 B4:2 A4:2 B4:2 C#5:2 D5:2 E5:3 F#5:1 A5:2 G#5:2 F#5:2 E5:2 D5:2 C#5:2'
CSD=T(CSA,-4,-7)
def AUG(s): return ' '.join(t.split(':')[0]+':'+str(int(t.split(':')[1].rstrip('~'))*2) for t in toks(s))
ped=' '.join(['A1:16~']*3+['A1:16'])
def avg(s):
    ps=[midi(t.split(':')[0]) for t in toks(s) if not t.startswith('R')]; return sum(ps)/len(ps)
def n_issues(R):
    return (len(R['beat_dissonance_both_attacking(unprepared)']),len(R['m2/M7_clash_list']),len(R['par16_list'])+len(R.get('parallel_5ths_8ves(eighth grid, attack to attack)',[])),len(R['crossing_list']))
if __name__=='__main__':
    for aoct in (-2,-1):
      for coct in (-1,0):
        base=[(OCT(AUG(SUBJ),aoct),0),(OCT(AUG(CSD),coct),0),(ped,0)]
        R=check(base); print('aug base',aoct,coct,n_issues(R))
    for aoct,coct in ((-2,-2),(-1,-1),(-2,-3),(-3,-3)):
        base=[(OCT(AUG(SUBJ),aoct),0),(OCT(AUG(CSD),coct),0),(ped,0)]
        R=check(base); print('aug base',aoct,coct,n_issues(R)); print(R['beat_dissonance_both_attacking(unprepared)'],R['crossing_list'][:3])
