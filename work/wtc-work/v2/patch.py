import sys,re
# usage: patch.py N key=val ... (bar number 1-indexed) : replaces voice strings for that bar in fugue_v2_bars.py
f='fugue_v2_bars.py'
lines=open(f).read().split('\n')
idx=[i for i,l in enumerate(lines) if l.startswith('bar(')]
def setbar(n,**kw):
    i=idx[n-1]
    l=lines[i]
    m=re.match(r"bar\((.*?)(,tag='.*')?\)\s*(#.*)?$",l)
    body=m.group(1); tag=m.group(2) or ''
    d=dict(re.findall(r"(\w+)='([^']*)'",body))
    d.update(kw)
    order=['s','a','t','br','b']
    parts=[f"{k}='{d[k]}'" for k in order if k in d and d[k]!='R:12']
    lines[i]="bar("+', '.join(parts)+tag+")"
if __name__=='__main__':
    n=int(sys.argv[1]); kw=dict(a.split('=',1) for a in sys.argv[2:])
    setbar(n,**kw); open(f,'w').write('\n'.join(lines))
