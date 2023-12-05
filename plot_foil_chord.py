import sys
import numpy as np

foilfile = sys.argv[1]
chord = float(sys.argv[2])

dat = np.loadtxt(foilfile,delimiter=',')

print("spline")

for adat in dat:
    x = adat[0]*chord
    y = adat[1]*chord
    print(str(x)+","+str(y))

print("")
print("")
print("")