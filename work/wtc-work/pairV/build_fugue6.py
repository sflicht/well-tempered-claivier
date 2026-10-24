import json,sys,importlib
from lit import events_for
P=importlib.import_module(sys.argv[2])
names=[('Soprano','S','treble',74),('Alto','A','treble',68),('Tenor','T','tenor',60),('Baritone','Br','bass',56),('Bass','B','bass',50),('Contrabass','Cb','bass',46)]
bars={n[0]:P.BARS[n[0]] for n in names}
nb=len(bars['Soprano']); assert all(len(v)==nb for v in bars.values()),{k:len(v) for k,v in bars.items()}
BASE={'Soprano':76,'Alto':72,'Tenor':70,'Baritone':68,'Bass':66,'Contrabass':64}
ENT=getattr(P,'ENT',[])
def lvlfun(name):
    def f(b,u,d,p):
        v=BASE[name]+getattr(P,'LEVEL',lambda b:0)(b)
        for (vn,b0,n) in ENT:
            if vn==name and b0-1<=b<b0-1+n: v+=6; break
        if u%16==0:v+=2
        elif u%4==0:v+=1
        if d==1:v-=2
        if p<48: v-=int((48-p)*0.8)
        return max(28,min(112,v))
    return f
gate=lambda d: .90 if d==1 else (.94 if d<=3 else .975)
bgate=lambda d: .80 if d==1 else (.86 if d<=3 else .92)
VOL=getattr(P,'VOL',{})
voices=[]
for name,abbr,clef,pan in names:
    voices.append({'name':name,'abbr':abbr,'clef':clef,'piano_pan':pan,'piano_vol':VOL.get(name,100),'events':events_for(bars[name],bar_units=16,vel=lvlfun(name),gate=(bgate if name in('Bass','Contrabass','Baritone') else gate))})
nmx=[n[0] for n in names]
entries=[{'voice':nmx.index(vn),'t':(b0-1)*4,'label':lab} for (vn,b0,n,lab) in getattr(P,'LAB',[])] 
meta={'title':'The Well-Tempered clAIvier','subtitle':'Fugue V in D major - v2 (hand-authored, six real voices)','composer':'Recomposed by Claudia / Sam','instrument':'Piano - six-voice study','key':'D','mode':'major','meter':[4,4],'bpm':getattr(P,'BPM',112),'tempo_text':'Allegro; bright, trumpet-and-dance','movement_number':5,'piece_type':'fugue','edition':'v2','score_tagline':'Hand-authored composition v2 - Claudia / Sam','markers':[{'t':(b-1)*4,'label':l} for b,l in getattr(P,'MARKS',[])]}
json.dump({'metadata':meta,'voices':voices,'subject_entries':entries,'literal_bars':{'bars':bars,'notes':getattr(P,'TAG',{})}},open(sys.argv[1],'w'),indent=1)
print('bars',nb)
