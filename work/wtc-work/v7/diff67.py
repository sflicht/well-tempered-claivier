import importlib.util,sys
def load(p,n):
    sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
a=load('../v6/fugue_v6_bars.py','a');b=load('fugue_v7_bars.py','b')
ch=[]
for i in range(len(a.S)):
    d=[v for v in 'S A T Br B'.split() if getattr(a,v)[i]!=getattr(b,v)[i]]
    if d: ch.append((i+1,d))
print(ch)
