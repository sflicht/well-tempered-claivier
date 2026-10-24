import os
from fugue_v5_bars import *
ls,sm=-4,-7
BASE=25
def stretto3(BASE,ls,sm,vS3='S',vS1='A',vCS='T',vS2='B',lag1=6,lag2=8):
    S1=T(SUBJ,ls,sm)
    S2=T(SUBJ,ls-3-7,sm-5-12)
    S3=T(SUBJ,ls+7,sm+12)
    CS=T(CSA,ls-4,sm-7)
    putseq(vS1,BASE,S1); putseq(vCS,BASE,CS)
    putseq(vS2,BASE,'R:%d '%lag1+S2)
    putseq(vS3,BASE,'R:%d '%(lag1+lag2)+S3)
stretto3(25,-4,-7)

