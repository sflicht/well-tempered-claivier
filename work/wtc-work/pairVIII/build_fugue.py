import json,sys
from fugue import *
import engine; from engine import realize,events; engine.SCALES.update(SC)
grid,theme,chords,labels=realize(NV,CENT,E,NB,KEY,PEDAL,ACT,final=(3,'min',[3,6,10]))
# final chord bar 22: whole notes all voices, Eb minor
FIN=[87,82,78,75,70,63,58,51,39]
s=(NB-1)*16
for v in range(NV):
    for x in range(s,s+16): grid[v][x]=(FIN[v],x==s)
DYN={1:60,2:62,3:64,4:66,5:69,6:71,7:73,8:66,9:68,10:70,11:72,12:74,13:78,14:82,15:90,16:92,17:62,18:64,19:76,20:80,21:84,22:86}
def vel(v,t,th):
    b=int(t//4)+1; x=DYN[b]+(6 if th else -6)
    if t%1==0: x+=3
    return max(30,min(112,x-(3 if v<6 else 0)))
V=events(grid,theme,NV,vel)
voices=[{'name':NAMES[i],'abbr':ABBR[i],'clef':'treble' if i<4 else 'bass','piano_pan':40+i*6,'events':V[i]} for i in range(NV)]
meta={'title':'The Well-Tempered clAIvier','subtitle':'Fugue VIII in E-flat minor - v1 (nine real voices, stretto style)','composer':'Recomposed by Claudia / Sam','instrument':'Piano','key':'Eb','mode':'minor','meter':[4,4],'bpm':60,'tempo_text':'Grave e pieno','movement_number':8,'piece_type':'fugue','edition':'v1','score_tagline':'Hand-planned, machine-realized v1 - Claudia / Sam',
 'markers':[{'t':0,'label':'mp'},{'t':32,'label':'Gb major stretto'},{'t':48,'label':'cresc.'},{'t':56,'label':'PEAK ff'},{'t':64,'label':'p, dominant pedal'},{'t':72,'label':'tonic pedal, final stretto'}]}
NM=['','','','']
json.dump({'metadata':meta,'voices':voices,'subject_entries':labels,'chords':[[c[0],c[1]] for c in chords]},open(sys.argv[1],'w'),indent=1)
