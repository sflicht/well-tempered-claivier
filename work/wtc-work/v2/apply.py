import sys
import patch
def run(d):
    for n,kw in d.items(): patch.setbar(n,**kw)
    open(patch.f,'w').write('\n'.join(patch.lines))
