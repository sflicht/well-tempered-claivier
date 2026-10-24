"""Builder: literal bar-by-bar authorship. Each token = PITCH:SIXTEENTHS ('R' = rest, trailing '~' ties into the next same-pitch token).
No pitch is generated, searched or repaired by code."""
import json,sys,importlib
from lib import parse_tok
VOICES=[('Soprano','S','treble',70),('Alto','A','treble',66),('Tenor','T','tenor',62),('Baritone','Br','bass',58),('Bass','B','bass',54)]
BASEV={'Soprano':74,'Alto':70,'Tenor':68,'Baritone':66,'Bass':70}
def build(BARS,ENTRIES,LEVEL,meta_extra,out):
    nbars=max(len(v) for v in BARS.values())
    voices=[];nnotes=0
    for name,abbr,clef,pan in VOICES:
        bars=BARS[name]; assert len(bars)==nbars,(name,len(bars),nbars)
        events=[]
        for b,bar in enumerate(bars):
            u=0
            for tok in bar.split():
                p,d,sp,tie=parse_tok(tok)
                if p is not None:
                    lvl=LEVEL[b] if b<len(LEVEL) else 0
                    v=BASEV[name]+lvl
                    for (vi,b0,nb,lab) in ENTRIES:
                        if vi==name and b0-1<=b<b0-1+nb: v+=9; break
                    v+= 4 if u%4==0 and u%12==0 else (2 if u%4==0 else (-2 if d==1 else 0))
                    ev={'t':b*3+u/4,'d':d/4,'p':p,'spell':sp,'v':max(30,min(120,v)),'gate':.93 if d<=2 else .97,'bar':b+1,'tie':tie}
                    events.append(ev)
                else:
                    events.append({'t':b*3+u/4,'d':d/4,'p':None,'rest':True})
                u+=d
            assert u==12,(name,b+1,u,bar)
        # merge ties
        merged=[];i=0;ev=[e for e in events if not e.get('rest')]
        for e in ev:
            if merged and merged[-1].get('_tie') and merged[-1]['p']==e['p'] and abs(merged[-1]['t']+merged[-1]['d']-e['t'])<1e-9:
                merged[-1]['d']+=e['d']; merged[-1]['_tie']=e['tie']; continue
            e=dict(e); e['_tie']=e['tie']; merged.append(e)
        for e in merged:
            e.pop('_tie',None); e.pop('tie',None); nnotes+=1
            e['gate']=.98 if e['d']>=1.5 else e['gate']
        voices.append({'name':name,'abbr':abbr,'clef':clef,'piano_pan':pan,'events':merged})
    entries=[]
    for vi,b0,nb,lab in ENTRIES:
        if lab.startswith('Subject') or lab.startswith('Answer'):
            idx=[v[0] for v in VOICES].index(vi)
            entries.append({'voice':idx,'t':(b0-1)*3,'label':lab})
    meta=dict(title='The Well-Tempered clAIvier',subtitle='IV. Fugue in C-sharp minor — recomposition (hand-authored first pass)',composer='Recomposed by Claudia / Sam',
      instrument='Piano — five-voice study',key='C#',mode='minor',meter=[3,4],bpm=92,tempo_text='Allegro inquieto; lightly sprung')
    meta.update(meta_extra)
    score={'metadata':meta,'voices':voices,'subject_entries':entries,'literal_bars':BARS}
    json.dump(score,open(out,'w'),indent=1)
    return nbars,nnotes
