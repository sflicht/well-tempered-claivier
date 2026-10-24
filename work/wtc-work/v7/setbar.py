import sys
f='fugue_v7_bars.py'
L=open(f).read().split('\n')
idx=[i for i,l in enumerate(L) if l.startswith('bar(')]
def put(n,line):
    L[idx[n-1]]=line
n=int(sys.argv[1]); put(n,sys.argv[2])
open(f,'w').write('\n'.join(L))
