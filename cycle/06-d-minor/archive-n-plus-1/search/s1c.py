from lab import *
import sys
shift, off = int(sys.argv[1]), int(sys.argv[2])
aug = notes(GROUND, 0, 0, 2)
up = []
for k in (-2, -1, 0, 1, 2):
    up += notes(GROUND, off + k * 96, shift)
up = [(s, d, p) for s, d, p in up if s + d > 0 and s < 192]
print(pair_cost(up, aug))
grid([up, aug], 0, 192, 4)
