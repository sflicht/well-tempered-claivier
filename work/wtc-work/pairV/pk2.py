from pk import *
for aoct,coct in ((-2,-2),(-1,-1)):
    base=[(OCT(AUG(SUBJ),aoct),0),(OCT(AUG(CSD),coct),0)]
    R=check(base); print(aoct,coct,n_issues(R)); print(R['beat_dissonance_both_attacking(unprepared)'])
print(OCT(AUG(SUBJ),-2)); print(OCT(AUG(CSD),-2))
