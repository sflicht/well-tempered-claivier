"""Build a throw-away multi-voice JSON from (token-string, start_unit) pairs and run chk on it."""
import json,io,contextlib,sys,tempfile,os
from lib5 import *
from lit import parse_tok
import chk
def mk(voices,fname='/tmp/mini.json',total=None):
    V=[];end=0
    for i,(s,st) in enumerate(voices):
        u=st;ev=[]
        for tok in toks(s):
            p,d,sp,tie=parse_tok(tok)
            if p is not None: ev.append({'t':u/4,'d':d/4,'p':p,'spell':sp,'v':80,'gate':.95})
            u+=d
        end=max(end,u)
        V.append({'name':f'v{i}','abbr':f'v{i}','clef':'treble','events':ev})
    # merge ties crudely ignored
    nb=(end+15)//16
    meta={'meter':[4,4],'bpm':112}
    json.dump({'metadata':meta,'voices':V},open(fname,'w'))
    return fname
def check(voices,verbose=False):
    f=mk(voices)
    R=chk.run(f,True)
    return R
def summary(R):
    return dict(aa=R['beat_dissonance_both_attacking(unprepared)'],clash=R['m2/M7_clash_list'],par=R.get('par16_list'),xr=R.get('xrel_list'),cross=R.get('crossing_list'))
