# Fugue VIII v2 material. Pitches are semitones relative to the local tonic; chords are (beat, root_rel, quality).
MIN=(0,2,3,5,7,8,10); MAJ=(0,2,4,5,7,9,11)
# Subject (6 beats): Eb q, Bb q | Cb. Bb  Ab Gb | F D Eb q
S_m=[(0,1,0),(1,1,7),(2,.75,8),(2.75,.25,7),(3,.5,5),(3.5,.5,3),(4,.5,2),(4.5,.5,-1),(5,1,0)]
S_mc=[(0,0,'min'),(1,0,'min'),(2,5,'min'),(3,5,'min'),(4,7,'maj'),(5,0,'min')]
S_M=[(t,d,{3:4,8:9}.get(r,r)) for t,d,r in S_m]
S_Mc=[(0,0,'maj'),(1,0,'maj'),(2,5,'maj'),(3,2,'min'),(4,7,'maj'),(5,0,'maj')]
# tonal answer (relative to the SUBJECT's tonic): Bb Eb | Gb. F  Eb Db | C A Bb
A_m=[(0,1,7),(1,1,12),(2,.75,15),(2.75,.25,14),(3,.5,12),(3.5,.5,10),(4,.5,9),(4.5,.5,6),(5,1,7)]
A_mc=[(0,0,'min'),(1,0,'min'),(2,0,'min'),(3,8,'maj'),(4,5,'maj'),(5,7,'min')]
FORMS={'S':(S_m,S_mc),'SM':(S_M,S_Mc),'A':(A_m,A_mc)}
CS_m=[(.5,.25,19),(.75,.25,17),(1,.5,15),(1.5,.5,14),(2,1,12),(3,.5,20),(3.5,.5,19),(4,1,17),(5,.5,15),(5.5,.5,14)]
CS_M=[(t,d,{15:16,20:21}.get(r,r)) for t,d,r in CS_m]
CS_A=[(.5,.25,26),(.75,.25,24),(1,.5,27),(1.5,.5,26),(2,1,24),(3,.5,27),(3.5,.5,26),(4,1,24),(5,.5,22),(5.5,.5,21)]
FORMS.update({'CS':(CS_m,[]),'CSM':(CS_M,[]),'CSA':(CS_A,[])})
# head (first 3 beats) and tail figures for episodes
FORMS['H']=(S_m[:4],S_mc[:3]); FORMS['HM']=(S_M[:4],S_Mc[:3])
FORMS['T']=(CS_m[:5],[])
