import sys,re
# usage: python3 setbars.py file.txt  ; each line: N|key=val|key=val ... (replaces whole bar N voice strings; keys s a t br b tag)
f='fugue_v3_bars.py'
lines=open(f).read().split('\n')
idx=[i for i,l in enumerate(lines) if l.startswith('bar(')]
for ln in open(sys.argv[1]):
    ln=ln.strip()
    if not ln or ln.startswith('#'): continue
    p=ln.split('|'); n=int(p[0]); d=dict(x.split('=',1) for x in p[1:])
    tag=d.pop('tag','')
    order=['s','a','t','br','b']
    parts=[f"{k}='{d[k]}'" for k in order if k in d and d[k]!='R:12']
    if tag: parts.append(f"tag='{tag}'")
    lines[idx[n-1]]="bar("+', '.join(parts)+")"
open(f,'w').write('\n'.join(lines))
