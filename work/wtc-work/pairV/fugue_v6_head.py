from lib5 import *
NV=['Soprano','Alto','Tenor','Baritone','Bass','Contrabass']
N=59
BARS={v:['R:16']*N for v in NV}
def put(b,**kw):
    ab={'S':'Soprano','A':'Alto','T':'Tenor','Br':'Baritone','B':'Bass','Cb':'Contrabass'}
    for k,v in kw.items():
        v=v.strip()
        assert units(v)==16,(b,k,units(v),v)
        BARS[ab[k]][b-1]=v
def putseq(v,b,s):
    ab={'S':'Soprano','A':'Alto','T':'Tenor','Br':'Baritone','B':'Bass','Cb':'Contrabass'}
    for i,bs in enumerate(splitbars(s)): BARS[ab[v]][b-1+i]=bs
def splitbars(s):
    """cut a token string into 16-unit bars; notes crossing a barline are tied; a short last bar is padded with rest"""
    out=[];cur=[];u=0
    for t in toks(s):
        p_,d=t.split(':'); tie=d.endswith('~'); d=int(d.rstrip('~'))
        while d>0:
            room=16-u; take=min(d,room)
            rest_=(take<d)
            cur.append(f"{p_}:{take}"+('~' if (p_!='R' and (rest_ or tie)) else ''))
            u+=take; d-=take
            if u==16: out.append(' '.join(cur));cur=[];u=0
    if cur: out.append(' '.join(cur+[f"R:{16-u}"]))
    return out
SUBJ1='A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4'
SUBJ2='A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2'
SUBJ=SUBJ1+' '+SUBJ2
CSA1='E5:2 D5:2 C#5:2 B4:2 A4:2 B4:2 C#5:2 D5:2'
CSA2='E5:3 F#5:1 A5:2 G#5:2 F#5:2 E5:2 D5:2 C#5:2'
CSA=CSA1+' '+CSA2
def subj(oct_=0): return splitbars(OCT(SUBJ,oct_) if oct_ else SUBJ)
def ans(oct_=0): return splitbars(T(SUBJ,4+7*oct_,7+12*oct_))   # E5 start for oct_=0
def csA(o=0): return splitbars(T(CSA,7*o,12*o))
def csD(o=0): return splitbars(T(CSA,-4+7*o,-7+12*o))
# --- exposition entries (fan): A subj A4 | T ans E3 | B subj A2 | S ans E5 | Br subj A3 | Cb ans E2
SA4=subj(0); AE3=ans(-2); SA2=subj(-2); AE5=ans(0); SA3=subj(-1); AE2=ans(-3)
