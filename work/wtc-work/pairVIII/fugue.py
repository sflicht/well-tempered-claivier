import json,sys
from motifs import FORMS
NV=9
CENT=[82,77,72,67,62,57,52,46,38]
NAMES=['Soprano I','Soprano II','Alto I','Alto II','Tenor I','Tenor II','Baritone','Bass I','Bass II']
ABBR=['S1','S2','A1','A2','T1','T2','Bar','B1','B2']
SC={'ebm':[3,5,6,8,10,11,1,2],'bbm':[10,0,1,3,5,6,8,9],'gb':[6,8,10,11,1,3,5],'abm':[8,10,11,1,3,4,6,7],'db':[1,3,5,6,8,10,0],'fm':[5,7,8,10,0,1,3,4],'cb':[11,1,3,4,6,8,10]}
# entries: (bar, beat, voice, form, T)  T = semitone offset from Eb
B=lambda b,x=0:(b-1)*4+x
E=[]
def ent(b,x,v,f,T,oct=None): E.append((B(b,x),v,f,T,oct))
# --- exposition: accelerating entries
ent(1,0,4,'S',0)
ent(2,0,3,'S',7); ent(2,0,4,'CS',7)
ent(3,0,5,'S',0); ent(3,0,3,'CS',0)
ent(4,0,2,'S',7); ent(4,0,5,'CS',7)
ent(5,0,6,'S',0); ent(5,0,2,'CS',0); ent(5,1,1,'I',7)
ent(6,0,7,'S',7); ent(6,0,6,'CS',7); ent(6,1,0,'I',2)
ent(7,0,8,'S',0); ent(7,0,7,'CS',0); ent(7,1,3,'I',7); ent(7,0,1,'H',7+12)
# --- b8 episode: heads sequenced to Gb (subject head in quarter stagger)
ent(8,0,2,'HI',10); ent(8,1,5,'H',5); ent(8,2,0,'HI',13); ent(8,3,6,'H',8)
# --- b9-10 Gb major: tight stretto at 1 beat, fifth
ent(9,0,1,'M',3); ent(9,1,4,'M',10); ent(9,0,3,'CSM',3)
ent(10,0,6,'M',3); ent(10,2,0,'IM',6); ent(10,0,5,'CSM',3)
# --- b11-12 Ab minor: S + inversion at 1 beat
ent(11,0,2,'S',5); ent(11,1,5,'I',12); ent(11,0,7,'CS',5)
ent(12,0,4,'S',5); ent(12,1,0,'I',12); ent(12,0,8,'CS',5)
# --- b13-14 build: rising chain of entries every half bar (each a fifth higher)
ent(13,0,6,'S',8); ent(13,2,3,'S',15); ent(14,0,1,'S',22); ent(14,2,2,'S',29)
ent(13,0,2,'CS',8); ent(14,0,5,'CS',22)
# --- b15-16 PEAK: all nine, S + I at one beat, subject at the top
ent(15,0,0,'S',24); ent(15,1,4,'I',7); ent(15,0,6,'CS',0)
ent(16,0,1,'S',8); ent(16,1,3,'I',3); ent(16,0,5,'CS',8)
# --- b17-18 release over dominant pedal (thin)
ent(17,0,4,'S',7); ent(17,1,1,'I',2); ent(18,0,5,'S',7)
# --- b19-21 final tonic pedal: stretto, all voices
ent(19,0,1,'S',0); ent(19,1,4,'I',7)
ent(20,0,0,'S',0); ent(20,1,3,'I',7); ent(20,0,2,'CS',0)
ent(21,0,0,'H',12); ent(21,1,2,'HI',7)
NB=22
KEY={1:'ebm',2:'bbm',3:'ebm',4:'bbm',5:'ebm',6:'bbm',7:'ebm',8:'gb',9:'gb',10:'gb',11:'abm',12:'abm',13:'abm',14:'fm',15:'ebm',16:'cb',17:'ebm',18:'ebm',19:'ebm',20:'ebm',21:'ebm',22:'ebm'}
PEDAL={17:(8,46),18:(8,46),19:(8,39),20:(8,39),21:(8,39)}
# active free voices per bar (theme voices always active)
ACT={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[4,8],9:[0,8],10:[1,2,4],11:[0,3,4],12:[1,2,3,6],13:[0,4,5,8],14:[2,3,4,6,8],
     15:list(range(9)),16:list(range(9)),17:[4],18:[3],19:list(range(9)),20:list(range(9)),21:list(range(9)),22:list(range(9))}
