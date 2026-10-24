import json,sys,importlib
from lit import events_for
P=importlib.import_module(sys.argv[2])
n=len(P.U); assert len(P.L)==n
def lvl(b):   # 0-based bar -> base velocity
    segs=[(0,8,70),(8,14,76),(14,20,74),(20,23,72),(23,26,80),(26,29,88),(29,33,72),(33,34,66)]
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
marks=[(1,'C minor: rocking broken chords'),(9,'Wedge hint: outer voices spread by half steps'),(15,'Circle of fifths toward E-flat'),(21,'Return to C minor'),(24,'Dominant pedal: the wedge widens'),(30,'Tonic pedal, Picardy close')]
meta={'title':'The Well-Tempered clAIvier','subtitle':'Prelude I in C minor - v1 (broken-chord sixteenths over an eighth-note bass)','composer':'Recomposed by Claudia / Sam','instrument':'Piano','key':'C','mode':'minor','meter':[4,4],'bpm':getattr(P,'BPM',72),'tempo_text':'Moderato; legato, veiled','movement_number':1,'piece_type':'prelude','edition':'v1','score_tagline':'Hand-authored composition v1 - Claudia / Sam',
 'markers':[{'t':(b-1)*4,'label':l} for b,l in marks]}
json.dump({'metadata':meta,'voices':voices,'literal_bars':{'unit':'sixteenth','upper':P.U,'lower':P.L,'notes':P.TAG}},open(sys.argv[1],'w'),indent=1)
print('bars',n)
