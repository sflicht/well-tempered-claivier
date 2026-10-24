import sys,re,ast
f='fugue_v5_bars.py'
lines=open(f).read().split('\n')
idx=[i for i,l in enumerate(lines) if l.startswith('bar(')]
for ln in open(sys.argv[1]):
    ln=ln.strip()
    if not ln or ln.startswith('#'): continue
    p=ln.split('|'); n=int(p[0]); upd=dict(x.split('=',1) for x in p[1:])
    src=lines[idx[n-1]]
    d=ast.literal_eval('dict('+src[4:-1]+')') if False else eval('dict('+src[4:-1]+')')
    d.update(upd)
    order=['s','a','t','br','b','tag']
    parts=[f"{k}='{d[k]}'" for k in order if k in d and d[k]!='R:12']
    lines[idx[n-1]]="bar("+', '.join(parts)+")"
open(f,'w').write('\n'.join(lines))
