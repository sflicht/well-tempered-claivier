"""Authoring helpers for Pair V (literal score notation, bars of 16 sixteenth-units in 4/4).
Tokens: PITCH:DUR (DUR in sixteenths, '~' tie), 'R' rest.  Nothing here chooses a pitch:
T() is exact transposition of an already-written motif (letter-steps + semitones), nothing else."""
import re
NAT={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
LET='CDEFGAB'
NAMES=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def midi(n):
    m=re.fullmatch(r'([A-G])(#{0,2}|b{0,2})(-?\d+)',n)
    L,acc,o=m.groups(); return 12*(int(o)+1)+NAT[L]+acc.count('#')-acc.count('b')
def nm(p): return NAMES[p%12]+str(p//12-1)
def toks(s): return s.replace('|',' ').split()
def parse(s):
    out=[]
    for t in toks(s):
        n,d=t.split(':'); tie=d.endswith('~'); d=int(d.rstrip('~'))
        out.append((n,d,tie))
    return out
def S(s):
    """sixteenth-note string: bare tokens get ':1'"""
    return ' '.join(t if ':' in t else t+':1' for t in toks(s))
def tn(name,ls,semi):
    """transpose one note name by ls letter-steps and semi semitones"""
    m=re.fullmatch(r'([A-G])(#{0,2}|b{0,2})(-?\d+)',name)
    L,acc,o=m.groups(); o=int(o)
    p=midi(name)+semi
    li=LET.index(L)+ls; no=o+li//7; nl=LET[li%7]
    alt=p-(12*(no+1)+NAT[nl])
    if abs(alt)>2: raise ValueError(f'cannot spell {name} {ls},{semi}')
    return nl+('#'*alt if alt>0 else 'b'*(-alt))+str(no)
def T(s,ls,semi):
    out=[]
    for t in toks(s):
        n,d=t.split(':')
        out.append((n if n=='R' else tn(n,ls,semi))+':'+d)
    return ' '.join(out)
def OCT(s,k=1): return T(s,7*k,12*k)
def units(s): return sum(int(t.split(':')[1].rstrip('~')) for t in toks(s))
def grid(s,n=None):
    """expand to per-sixteenth list of (midi or None, attack?)"""
    g=[]
    for t in toks(s):
        nme,d=t.split(':'); d=int(d.rstrip('~'))
        for i in range(d): g.append((None if nme=='R' else midi(nme), i==0))
    return g
def rests(n): return f'R:{n}'

# ---- diatonic transposition (exact scale-step shift, chromatic inflections kept relative to the key signature)
KS_D={'F':1,'C':1}
def TD(s,steps,ks_from=None,ks_to=None):
    ks_from=KS_D if ks_from is None else ks_from; ks_to=ks_from if ks_to is None else ks_to
    out=[]
    for t in toks(s):
        n,d=t.split(':')
        if n=='R': out.append(t); continue
        m=re.fullmatch(r'([A-G])(#{0,2}|b{0,2})(-?\d+)',n)
        L,acc,o=m.groups(); o=int(o)
        alt=acc.count('#')-acc.count('b')
        delta=alt-ks_from.get(L,0)
        li=LET.index(L)+steps; no=o+li//7; nl=LET[li%7]
        newalt=ks_to.get(nl,0)+delta
        if abs(newalt)>2: raise ValueError('spell')
        out.append(nl+('#'*newalt if newalt>0 else 'b'*(-newalt))+str(no)+':'+d)
    return ' '.join(out)
