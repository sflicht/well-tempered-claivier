"""Literal-score builder: tokens PITCH:SIXTEENTHS ('R' rest, trailing ~ ties into next same-pitch token).
No pitch is chosen, searched or repaired by code. Bars in 3/4 = 12 sixteenths."""
import re,json
NAT={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def parse_tok(tok):
    name,d=tok.split(':');tie=d.endswith('~');d=int(d.rstrip('~'))
    if name=='R':return None,d,None,tie
    m=re.fullmatch(r'([A-G])(#{0,2}|b{0,2})(-?\d+)',name)
    if not m:raise ValueError(tok)
    L,acc,o=m.groups();alter=acc.count('#')-acc.count('b')
    return 12*(int(o)+1)+NAT[L]+alter,d,L.lower()+('is'*alter if alter>=0 else 'es'*(-alter)),tie
def events_for(bars,bar_units=12,vel=None,gate=None):
    """vel(bar_index, unit, dur, pitch)->velocity ; authored per call."""
    evs=[]
    for b,bar in enumerate(bars):
        u=0
        for tok in bar.split():
            p,d,sp,tie=parse_tok(tok)
            if p is not None:
                evs.append({'t':(b*bar_units+u)/4,'d':d/4,'p':p,'spell':sp,'v':vel(b,u,d,p) if vel else 80,'gate':(gate(d) if gate else .95),'bar':b+1,'_tie':tie})
            else: evs.append({'t':(b*bar_units+u)/4,'d':d/4,'p':None,'_rest':True})
            u+=d
        if u!=bar_units:raise ValueError(f'bar {b+1} has {u} units: {bar}')
    out=[]
    for e in evs:
        if e.get('_rest'):continue
        if out and out[-1].get('_tie') and out[-1]['p']==e['p'] and abs(out[-1]['t']+out[-1]['d']-e['t'])<1e-9:
            out[-1]['d']+=e['d'];out[-1]['_tie']=e['_tie'];out[-1]['gate']=.985;continue
        out.append(dict(e))
    for e in out:
        e.pop('_tie',None);e.pop('_rest',None)
    return out
