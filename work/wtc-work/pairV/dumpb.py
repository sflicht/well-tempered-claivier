import importlib,sys
P=importlib.import_module(sys.argv[1])
for b in range(int(sys.argv[2]),int(sys.argv[3])+1):
  print('--',b)
  for v in P.NV: print(f'{v[:3]:4}',P.BARS[v][b-1])
