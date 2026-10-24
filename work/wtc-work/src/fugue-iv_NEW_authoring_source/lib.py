import re, json
NAT={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def parse_tok(tok):
    name,d=tok.split(':')
    tie=False
    if d.endswith('~'): tie=True; d=d[:-1]
    d=int(d)
    if name=='R': return None,d,None,tie
    m=re.fullmatch(r'([A-G])(#{0,2}|b{0,2})(-?\d+)',name)
    if not m: raise ValueError(tok)
    L,acc,o=m.groups(); alter=acc.count('#')-acc.count('b')
    p=12*(int(o)+1)+NAT[L]+alter
    sp=L.lower()+('is'*alter if alter>=0 else 'es'*(-alter))
    return p,d,sp,tie
