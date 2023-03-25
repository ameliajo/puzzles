
import matplotlib.pyplot as plt
#from tile import Model, Shape
from geometry import *
import numpy as np

BLUE   = 0x477984
ORANGE = 0xEEAA4D
RED    = 0xC03C44
model = Model()
model.append(Shape(6, fill=RED))
a = model.add(0, range(6), 4, fill=ORANGE)
b = model.add(a, 1, 3, fill=BLUE)

c = model.add(a, 2, 6, fill=RED)
d = model.add(c, range(1,5), 4, fill=ORANGE)
e = model.add(d, 3, 3, fill=BLUE)

f = model.add(d, 2, 6, fill=RED)
#g = model.add(f, range(1,5), 4, fill=ORANGE)
#h = model.add(g, 3, 3, fill=BLUE)

#i = model.add(g, 2, 6, fill=RED)
#j = model.add(i, range(1,5), 4, fill=ORANGE)
#k = model.add(j, 3, 3, fill=BLUE)



if __name__=="__main__":
    plt.figure(figsize=(8,8))
    surface = model.render()
    surface.write_to_png('output.png')
