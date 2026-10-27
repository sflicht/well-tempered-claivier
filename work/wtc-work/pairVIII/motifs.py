# (t, d, rel semitones from tonic Eb4=63)
S=[(0,1,0),(1,.5,3),(1.5,.25,2),(1.75,.25,0),(2,.5,-1),(2.5,.5,0),(3,.5,2),(3.5,.5,-5)]
M=[(t,d,4 if r==3 else r) for t,d,r in S]        # major-mode subject
I=[(0,1,0),(1,.5,-3),(1.5,.25,-2),(1.75,.25,0),(2,.5,2),(2.5,.5,0),(3,.5,-2),(3.5,.5,5)]
IM=[(t,d,-4 if r==-3 else (-1 if r==-2 else r)) for t,d,r in I]
CS=[(.5,.5,7),(1,1,12),(2,.5,19),(2.5,.5,17),(3,.25,14),(3.25,.25,12),(3.5,.5,11)]
CSM=[(t,d,r) for t,d,r in CS]
H=S[:4]; HM=M[:4]; HI=I[:4]
FORMS=dict(S=S,M=M,I=I,IM=IM,CS=CS,CSM=CSM,H=H,HM=HM,HI=HI)
