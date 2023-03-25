
import matplotlib.pyplot as plt
#from tile import Model, Shape
from geometry import *
import numpy as np

BLUE   = 0x477984
ORANGE = 0xEEAA4D
RED    = 0xC03C44



model = Model()
model.append(Shape(3, fill=ORANGE))
a1 = model.add(0, 0, 3, fill=ORANGE)
a2 = model.add(0, 2, 3, fill=ORANGE)
b1 = model.add(a1, 1, 3, fill=ORANGE)
b2 = model.add(a2, 2, 3, fill=ORANGE)
b3 = model.add(b2, 2, 3, fill=ORANGE)
d1 = model.add(b1, 2, 4, fill=RED)
d2 = model.add(b2, 1, 4, fill=RED)
d3 = model.add(b3, 1, 4, fill=RED)
d4 = model.add(a1, 2, 4, fill=RED)
d5 = model.add(a2, 1, 4, fill=RED)
d6 = model.add(0 , 1, 4, fill=RED)
for d in [d1,d2,d3,d4,d5,d6]:
    t = model.add(d,2,3,fill=ORANGE)
    t2 = model.add(d,3,3,fill=BLUE)
    t3 = model.add(t2,1,3,fill=BLUE)
    s2 = model.add(t,[1,2],4,fill=RED)
    t4 = model.add(s2,2,3,fill=ORANGE)
    t5a = model.add(s2,3,3,fill=BLUE)
    t5b = model.add(s2,1,3,fill=BLUE)
    s3a = model.add(t5a,1,4,fill=RED)
    s3b = model.add(t5b,2,4,fill=RED)
    t5a = model.add(s3a,1,3,fill=ORANGE)
    t5b = model.add(s3b,3,3,fill=ORANGE)
    t6a = model.add(t5a,2,3,fill=ORANGE)
    t6b = model.add(t5b,1,3,fill=ORANGE)
    s4a = model.add(t6a,2,4,fill=RED)
    s4b = model.add(t6b,1,4,fill=RED)
    t7 = model.add(s3a,2,3,fill=ORANGE)
    t7 = model.add(s3a,3,3,fill=ORANGE)
    t7 = model.add(s3b,2,3,fill=ORANGE)
    t7 = model.add(s4a,1,3,fill=BLUE)
#d3 = model.add(b3, 2, 4, fill=RED)
#b = model.add(a, [1,2], 3, fill=ORANGE)
#b = model.add(a, 1, 3, fill=RED)
#c = model.add(a, 2, 6, fill=RED)
#d = model.add(b,[2,4],6,fill=RED)
#a = model.add(0, range(6), 4, fill=ORANGE)
#b = model.add(a, 1, 3, fill=RED)
#c = model.add(a, 2, 6, fill=RED)
#model.repeat(c)

if __name__=="__main__":
    plt.figure(figsize=(8,8))
    surface = model.render()
    surface.write_to_png('output.png')
