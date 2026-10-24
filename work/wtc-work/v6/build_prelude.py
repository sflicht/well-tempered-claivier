import json,sys
from lit import events_for
import prelude_v6_bars as P
n=len(P.U); assert len(P.L)==n
# authored dynamics: base level per bar (MIDI velocity for the voice carrying the line)
def lvl(b):
    # b is 0-based bar
    segs=[(0,4,74),(4,8,72),(8,14,70),(14,18,72),(18,20,62),(20,21,90),(21,23,96),(23,25,90),(25,26,80),(26,31,76),(31,34,78),(34,36,84),(36,37,74),(37,38,62)]
    for a,z,v in segs:
        if a<=b<z:return v
    return 72
def make_vel(voice):
    def f(b,u,d,p):
        v=lvl(b)
        if (b+1) in (5,10,16,29): v+= {'U':-6,'L':+5}[voice]   # HAND SWITCH bars: L states M, U plays the 16th figuration
        # a voice carrying the motif head/tail gets +3; accompanying voice -4; upper line at least as present as lower
        v+= {'U':2,'L':-3}[voice]
        if u%4==0: v+=2
        if d==1: v-=3
        if d>=6: v-=2
        # low register compensation for the soundfont: attenuate below C3, never boost
        if p<48: v-= int((48-p)*0.9)
        return max(30,min(118,v))
    return f
gate=lambda d: .90 if d==1 else (.94 if d<=3 else .975)
voices=[{'name':'Upper line','abbr':'R.H.','clef':'treble','piano_pan':68,'events':events_for(P.U,vel=make_vel('U'),gate=gate)},
        {'name':'Lower line','abbr':'L.H.','clef':'bass','piano_pan':60,'events':events_for(P.L,vel=make_vel('L'),gate=gate)}]
meta={'title':'The Well-Tempered clAIvier','subtitle':'Prelude IV in C-sharp minor - v6 (hand-authored, sixteenth-note broken-chord accompaniment, no pause: held-dominant arrival of 1.5 beats then straight into the drop, shortened return)','composer':'Recomposed by Claudia / Sam','instrument':'Piano','key':'C#','mode':'minor','meter':[3,4],'bpm':96,'tempo_text':'Allegro inquieto; lightly sprung','movement_number':4,'piece_type':'prelude','edition':'v6','score_tagline':'Hand-authored recomposition v6 - Claudia / Sam',
 'markers':[{'t':0,'label':'Allegro inquieto'},{'t':(8*12)/4,'label':'E major'},{'t':(14*12)/4,'label':'Development: A major (bVI)'},{'t':(18*12)/4,'label':'V pedal; augmentation'},{'t':(20*12)/4,'label':'Arrival: held dominant 7th, no pause'},{'t':(21*12)/4,'label':'Drop'},{'t':(23*12)/4,'label':'Hemiola'},{'t':(26*12)/4,'label':'Return (shortened)'}]}
score={'metadata':meta,'voices':voices,'literal_bars':{'unit':'sixteenth','upper':P.U,'lower':P.L,'notes':P.TAG}}
json.dump(score,open(sys.argv[1],'w'),indent=1)
print('bars',n,'notes',sum(len(v['events']) for v in voices))
