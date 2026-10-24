import json,sys,math
d=json.load(open(sys.argv[1])); V=d['voices']; ab=[v['abbr'] for v in V]
end=max(e['t']+e['d'] for v in V for e in v['events']); nb=math.ceil(end/4-1e-9)
rows=[]
for b in range(nb):
    n=0;who=[]
    for v in V:
        s=sum(max(0,min(e['t']+e['d'],b*4+4)-max(e['t'],b*4)) for e in v['events'])
        if s>=2-1e-9: n+=1;who.append(v['abbr'])
    rows.append((b+1,n,''.join(f'{w:>3}' if w in who else '  .' for w in ab)))
if len(sys.argv)>2:
    print('bar n  '+''.join(f'{a:>3}' for a in ab))
    for b,n,w in rows: print(f'{b:>3} {n:>2} {w}')
print('voices-per-bar:',' '.join(str(n) for b,n,w in rows))
import collections;print(sorted(collections.Counter(n for b,n,w in rows).items()))
