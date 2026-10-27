import sys, time
from ladder import *
seeds = {
 's1': (14, "G4:2 C5:4 G4:2 A4:1 B4:1 C5:2 D5:2 E5:2 F5:3 E5:1 D5:2 C5:2 B4:2 C5:2 D5:2"),
 's2': (14, "G4:2 C5:2 C5:1 D5:1 E5:2 C5:2 G5:4 F5:1 E5:1 D5:1 C5:1 B4:2 G4:2 A4:2 B4:2 C5:2 D5:2"),
 's3': (2, "C4:2 D4:2 E4:2 F4:3 G4:1 F4:2 E4:2 A4:2 D4:2 G4:3 F4:1 E4:2"),
}
for k,(p0,s) in seeds.items():
    n = parse(s)
    t=time.time()
    L = ladder(n, p0)
    print(k, s, 'len16', sum(d for d,_ in n), 'mel', melodic_penalty(n,p0), f'{time.time()-t:.2f}s')
    for d,c in L.items(): print('  d',d, c)
