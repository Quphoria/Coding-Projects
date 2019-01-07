import math
xmin = 1
xmax = 5
ymin = 1
ymax = 17

idxmin = 0
idxmax = 65
for idx in range(idxmin,idxmax):
    xcalc = (idx % 5) + 1
    ycalc = math.floor(idx / 5) + 1
    print(idx)
    print(xcalc)
    print(ycalc)
    print()
