import json,sys,importlib
sys.path.insert(0,'.')
from lit import events_for
from cp import tobars,length
def build(mod,out,title,edition):
    P=importlib.import_module(mod)
    tot=max(max(s+length(l) for s,l in P.U),max(s+length(l) for s,l in P.L))
    tot=((tot+15)//16)*16
    def line_of(V):
        V=sorted(V,key=lambda z:z[0]);out=[];t=0
        for s,l in V:
            assert s>=t,(s,t)
            if s>t: out.append((None,s-t))
            out+=l;t=s+length(l)
        if t<tot: out.append((None,tot-t))
        return out
    KS=getattr(P,'KEYSP',{})
    from cp import SPELL
    def spf(b):
        d=dict(SPELL);d.update(KS.get(b+1,{}));return d
    bars={'Upper':tobars(line_of(P.U),spf),'Lower':tobars(line_of(P.L),spf)}
    extra=getattr(P,'EXTRA',[])
    voices=[]
    def vel(name):
        def f(b,u,d,p):
            v=getattr(P,'LEVEL',lambda b:72)(b)+(2 if name=='Upper' else 0)
            if u%16==0:v+=3
            elif u%4==0:v+=1
            if d==1:v-=2
            if p<45:v-=int((45-p)*0.6)
            return max(30,min(115,v))
        return f
    gate=lambda d: .90 if d==1 else (.93 if d<=3 else .97)
    for name,clef,pan in(('Upper','treble',66),('Lower','bass',58)):
        voices.append({'name':name,'abbr':'U' if name=='Upper' else 'L','clef':clef,'piano_pan':pan,'events':events_for(bars[name],vel=vel(name),gate=gate)})
    for name,bb in extra:
        voices.append({'name':name,'abbr':'Ped','clef':'bass','piano_pan':54,'events':events_for(bb,vel=vel('Lower'),gate=gate)})
    meta={'title':'The Well-Tempered clAIvier','subtitle':title,'composer':'Recomposed by Claudia / Sam','instrument':'Piano','key':'C','mode':'minor','meter':[4,4],'bpm':getattr(P,'BPM',66),'tempo_text':getattr(P,'TEMPO','Moderato'),'movement_number':1,'piece_type':'fugue','edition':edition,'score_tagline':'Hand-authored composition v1 - Claudia / Sam','markers':[{'t':(b-1)*4,'label':l} for b,l in getattr(P,'MARKS',[])]}
    ents=[{'voice':v,'t':(b-1)*4,'label':lab} for v,b,lab in getattr(P,'LAB',[])]
    json.dump({'metadata':meta,'voices':voices,'subject_entries':ents,'literal_bars':{'bars':bars}},open(out,'w'),indent=1)
    return bars
if __name__=='__main__':
    b=build(sys.argv[1],sys.argv[2],'Fugue I in C minor - v1 (two voices, wedge subject)','v1')
    for i,(u,l) in enumerate(zip(b['Upper'],b['Lower'])): print(i+1,'U',u);print(i+1,'L',l)
