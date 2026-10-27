import json,sys,re
sys.path.insert(0,'..')
import chk
d=json.load(open(sys.argv[1]));R=chk.run(sys.argv[1])
ab={v['abbr']:v for v in d['voices']}
def th(a,t):
    for e in ab[a]['events']:
        if e['t']<=t<e['t']+e['d']: return e.get('th','free')
    return '-'
from collections import Counter
C=Counter()
for s in R['parallel_5ths_8ves(eighth grid, attack to attack)']:
    m=re.match(r'b(\d+)\.(\S+) (\S+?)(S1|S2|A1|A2|T1|T2|Bar|B1|B2) ',s)
    b,pos,a1,a2=m.groups(); a1=re.match(r'(S1|S2|A1|A2|T1|T2|Bar|B1|B2)',s.split()[1]).group(1); pair=s.split()[1]; a2=pair[len(a1):]
    t=(int(b)-1)*4+float(pos)-1
    k=(th(a1,t)!='free',th(a2,t)!='free'); C[k]+=1
    if k==(True,True) or '-v' in sys.argv: print(s,th(a1,t),th(a2,t))
print(C)
