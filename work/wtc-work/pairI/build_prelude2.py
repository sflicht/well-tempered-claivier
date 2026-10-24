import json,sys,importlib
from lit import events_for
P=importlib.import_module(sys.argv[2])
n=len(P.U); assert len(P.L)==n
def lvl(b):   # 0-based bar -> base velocity
    segs=[(0,4,70),(4,11,74),(11,12,82),(12,18,76),(18,24,74),(24,25,86),(25,27,78),(27,28,68)]
    for a,z,v in segs:
        if a<=b<z:return v
    return 76
def make_vel(voice):
    ACC=P.ACCU if voice=='U' else P.ACCL
    def f(b,u,d,p):
        v=lvl(b)+{'U':2,'L':-4}[voice]
        if b*16+u in ACC: v+=8
        if u==0 and b in (0,11,24,27): v+=6
        if d==1: v-=2
        if d>=8: v+=2
        if p<48: v-=int((48-p)*0.9)
        return max(30,min(118,v))
    return f
gate=lambda d: .90 if d==1 else (.94 if d<=3 else .975)
voices=[{'name':'Upper line','abbr':'R.H.','clef':'treble','piano_pan':68,'events':events_for(P.U,vel=make_vel('U'),gate=gate)},
        {'name':'Lower line','abbr':'L.H.','clef':'bass','piano_pan':60,'events':events_for(P.L,vel=make_vel('L'),gate=gate)}]
marks=[(1,'C minor: groups of four'),(5,'Groups of three, dotted-quarter bass: hemiola toward E-flat'),(12,'E-flat: downbeat regained'),(13,'Groups of five over syncopated bass: E-flat to F minor'),(19,'Dominant implied by re-struck G: irregular 3/5 groups, top rises G-Ab-A-Bb-B'),(25,'C minor: downbeat regained'),(28,'Plain close')]
meta={'title':'The Well-Tempered clAIvier','subtitle':'Prelude I in C minor - v2 (losing the beat)','composer':'Recomposed by Claudia / Sam','instrument':'Piano','key':'C','mode':'minor','meter':[4,4],'bpm':getattr(P,'BPM',72),'tempo_text':'Andante; even sixteenths, accents follow the groups','movement_number':1,'piece_type':'prelude','edition':'v2','score_tagline':'Hand-authored composition v2 - Claudia / Sam',
 'markers':[{'t':(b-1)*4,'label':l} for b,l in marks]}
json.dump({'metadata':meta,'voices':voices,'literal_bars':{'unit':'sixteenth','upper':P.U,'lower':P.L,'notes':P.TAG}},open(sys.argv[1],'w'),indent=1)
print('bars',n)
