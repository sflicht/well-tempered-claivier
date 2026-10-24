import json,sys,importlib
from lit import events_for
P=importlib.import_module(sys.argv[2])
n=len(P.U); assert len(P.L)==n
def lvl(b):   # 0-based bar -> base velocity
    segs=[(0,4,76),(4,8,80),(8,12,70),(12,16,76),(16,20,82),(20,24,78),(24,28,84),(28,29,92),(29,31,98),(31,32,100),(32,36,80),(36,38,84),(38,39,88),(39,40,80)]
    for a,z,v in segs:
        if a<=b<z:return v
    return 76
def make_vel(voice):
    def f(b,u,d,p):
        v=lvl(b)+{'U':2,'L':-4}[voice]
        if u%4==0: v+=3
        elif u%2==0: v+=1
        if d==1: v-=2
        if d>=8: v+=2
        if p<48: v-=int((48-p)*0.9)
        return max(30,min(118,v))
    return f
gate=lambda d: .90 if d==1 else (.94 if d<=3 else .975)
voices=[{'name':'Upper line','abbr':'R.H.','clef':'treble','piano_pan':68,'events':events_for(P.U,vel=make_vel('U'),gate=gate)},
        {'name':'Lower line','abbr':'L.H.','clef':'bass','piano_pan':60,'events':events_for(P.L,vel=make_vel('L'),gate=gate)}]
marks=[(1,'Allegro; bright, fanfare-like'),(9,'A major: compound line'),(17,'Development: tattoo cell'),(21,'7th-chord chain'),(25,'A pedal: climb'),(30,'PEAK: G#dim7 / E7 apex'),(32,'Arrival on D'),(33,'Return (shortened)')]
meta={'title':'The Well-Tempered clAIvier','subtitle':'Prelude V in D major - v1 (hand-authored, continuous sixteenths in both hands)','composer':'Recomposed by Claudia / Sam','instrument':'Piano','key':'D','mode':'major','meter':[4,4],'bpm':getattr(P,'BPM',104),'tempo_text':'Allegro; bright, extroverted','movement_number':5,'piece_type':'prelude','edition':'v1','score_tagline':'Hand-authored composition v1 - Claudia / Sam',
 'markers':[{'t':(b-1)*4,'label':l} for b,l in marks]}
json.dump({'metadata':meta,'voices':voices,'literal_bars':{'unit':'sixteenth','upper':P.U,'lower':P.L,'notes':P.TAG}},open(sys.argv[1],'w'),indent=1)
print('bars',n)
