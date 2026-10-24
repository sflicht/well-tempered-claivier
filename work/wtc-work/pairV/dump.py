import sys,importlib
m=importlib.import_module(sys.argv[1])
for b in range(int(sys.argv[2]),int(sys.argv[3])+1):
    print('--',b)
    for v in m.NV:
        x=m.BARS[v][b-1] if isinstance(m.BARS[v],list) else m.BARS[v].get(b)
        if x and x.strip() and x.strip()!='R:16': print('  %-10s %s'%(v,x))
