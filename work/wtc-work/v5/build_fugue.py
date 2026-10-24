import json,sys
from lit import events_for
import importlib
P=importlib.import_module(sys.argv[2] if len(sys.argv)>2 else 'fugue_v5_bars')
names=[('Soprano','S','treble',70),('Alto','A','treble',64),('Tenor','T','tenor',58),('Baritone','Br','bass',54),('Bass','B','bass',50)]
bars={'Soprano':P.S,'Alto':P.A,'Tenor':P.T,'Baritone':P.Br,'Bass':P.B}
nb=len(P.S); assert all(len(v)==nb for v in bars.values())
BASE={'Soprano':74,'Alto':71,'Tenor':70,'Baritone':69,'Bass':66}
ENT=getattr(P,'ENT',[])
def lvlfun(name):
    def f(b,u,d,p):
        v=BASE[name]+getattr(P,'LEVEL',lambda b:0)(b)
        for (vn,b0,n) in ENT:
            if vn==name and b0-1<=b<b0-1+n: v+=6; break
        if u%12==0:v+=2
        elif u%4==0:v+=1
        if d==1:v-=2
        # register compensation (soundfont: low piano notes are much louder in the mix): lower the lowest octaves
        return max(28,min(110,v))
    return f
gate=lambda d: .90 if d==1 else (.94 if d<=3 else .975)
bgate=lambda d: .80 if d==1 else (.86 if d<=3 else .92)   # lighter, more detached bass
VOL=getattr(P,'VOL',{})
voices=[]
for name,abbr,clef,pan in names:
    voices.append({'name':name,'abbr':abbr,'clef':clef,'piano_pan':pan,'piano_vol':VOL.get(name,100),'events':events_for(bars[name],vel=lvlfun(name),gate=(bgate if name=='Bass' else gate))})
entries=[{'voice':[n[0] for n in names].index(vn),'t':(b0-1)*3,'label':'subject'} for (vn,b0,n) in ENT]
meta={'title':'The Well-Tempered clAIvier','subtitle':'Fugue IV in C-sharp minor - v5 (hand-authored)','composer':'Recomposed by Claudia / Sam','instrument':'Piano - five-voice study','key':'C#','mode':'minor','meter':[3,4],'bpm':93,'tempo_text':'Allegro inquieto; lightly sprung','movement_number':4,'piece_type':'fugue','edition':'v5','score_tagline':'Hand-authored recomposition v5 - Claudia / Sam'}
json.dump({'metadata':meta,'voices':voices,'subject_entries':entries,'literal_bars':{'bars':{k:v for k,v in bars.items()},'notes':P.TAG}},open(sys.argv[1],'w'),indent=1)
print('bars',nb)
