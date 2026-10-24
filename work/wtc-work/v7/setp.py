import sys
f='prelude_v5_bars.py'
lines=open(f).read().split('\n')
idx=[i for i,l in enumerate(lines) if l.startswith('bar(')]
for ln in open(sys.argv[1]):
    ln=ln.strip()
    if not ln or ln.startswith('#'): continue
    p=ln.split('|'); n=int(p[0]); upd=dict(x.split('=',1) for x in p[1:])
    src=lines[idx[n-1]]
    d=eval('dict(u=%s)'%src[4:-1].replace(",'",",l='",1) if False else 'None') if False else None
    # parse tuple-style
    t=eval('('+src[4:-1]+',)')
    u,l,tag=(list(t)+[''])[:3]
    if 'u' in upd:u=upd['u']
    if 'l' in upd:l=upd['l']
    if 'tag' in upd:tag=upd['tag']
    lines[idx[n-1]]="bar(%r,%r,%r)"%(u,l,tag)
open(f,'w').write('\n'.join(lines))
