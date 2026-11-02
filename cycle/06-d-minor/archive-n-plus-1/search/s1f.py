from lab import *
import sys
shift, offb = int(sys.argv[1]), int(sys.argv[2])
aug = notes(GROUND, 0, 0, 2)
up = notes(GROUND, offb * 12, shift)
print(pair_cost(up, aug))
grid([up, aug], 0, 192, 4)
