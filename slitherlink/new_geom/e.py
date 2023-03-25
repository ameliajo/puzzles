
import matplotlib.pyplot as plt
#from tile import Model, Shape
from geometry import *
import numpy as np

BLUE   = 0x477984
ORANGE = 0xEEAA4D
RED    = 0xC03C44
GREEN  = 0x069869
PINK   = 0xff737e
model = Model()
model.append(Shape(6, fill=GREEN))

sq1a = model.add(0,    range(6), 4, fill=RED)

hex2 = model.add(sq1a, [2],      6, fill=GREEN)
tr1a = model.add(sq1a, [1],      3, fill=ORANGE)
sq1b = model.add(tr1a, [2],      4, fill=RED)
s12  = model.add(sq1b, [2],     12, fill=BLUE)
sq1c = model.add(s12 , [2],      4, fill=RED)

tr2a = model.add(sq1c, [3],      3, fill=ORANGE)
tr2b = model.add(tr2a, [1],      3, fill=ORANGE)
tr2c = model.add(tr2a, [2],      3, fill=ORANGE)
sq2a = model.add(tr2b, [2],      4, fill=RED)
sq2b = model.add(tr2c, [1],      4, fill=RED)

sq2cA= model.add(s12 , [5],      4, fill=RED)
sq2cB= model.add(s12 , [7],      4, fill=RED)
s12bA= model.add(sq2cA,[2],     12, fill=BLUE) # LEFT of hex
s12bB= model.add(sq2cB,[2],     12, fill=BLUE) # RIGHT of hex
tr2d = model.add(s12 , [4,8],    3, fill=ORANGE)
sq2d = model.add(sq2a, [2],      4, fill=RED)
sq2e = model.add(sq2b, [2],      4, fill=RED)

hex3 = model.add(s12 , [6],      6, fill=GREEN)
tr2e = model.add(s12bA,[1],      3, fill=ORANGE)
tr2f = model.add(sq2d ,[1],      3, fill=ORANGE)
tr2g = model.add(sq2cB,[3],      3, fill=ORANGE)
tr2h = model.add(sq2cA,[1],      3, fill=ORANGE)

tr2i = model.add(sq2d, [2],      3, fill=ORANGE)
tr2j = model.add(sq2e, [2],      3, fill=ORANGE)

sq2f = model.add(s12bA,[10],     4, fill=RED) # HEX
sq2g = model.add(s12bA,[3],      4, fill=RED)# NOT HEX
tr2k = model.add(sq2g, [1],      3, fill=ORANGE)


hex4 = model.add(sq2g, [3],      6, fill=GREEN) # hex side
tr3a = model.add(sq2f, [1],      3, fill=ORANGE) # tri/sq side
tr3c = model.add(tr3a,[1],      3, fill=ORANGE)
tr3d = model.add(tr3a,[2],      3, fill=ORANGE)
sq3a = model.add(tr3c,[2],      4, fill=RED)
sq3b = model.add(tr3d,[1],      4, fill=RED)

sq_on_hex = model.add(hex4,[2,4],4,fill=RED)
sq_on_hex2= model.add(hex4,[3]  ,4,fill=RED)
tr3e = model.add(sq_on_hex2,[1,3],3,fill=ORANGE)

hex7 = model.add(sq_on_hex2,[2],6,fill=GREEN)

sq_start_again = model.add(hex7, range(1,6),4,fill=RED)
hex_new = model.add(sq_start_again,[2],6,fill=GREEN)
tr4a = model.add(sq_start_again ,[3],3,fill=ORANGE)
sq_again = model.add(hex_new,[1],4,fill=RED)
sq_4 = model.add(s12bA,[7],4,fill=RED)
tr_4a = model.add(sq_4,[3],3,fill=ORANGE)
tr_4b = model.add(s12bA,[8],3,fill=ORANGE)
sq_5 = model.add(s12bB,[5],4,fill=RED)
tr_5a = model.add(sq_5,[1],3,fill=ORANGE)
tr_5b = model.add(s12bB,[4],3,fill=ORANGE)


sq_newa= model.add(sq3a,[2],4,fill=RED)
sq_newb= model.add(sq3b,[2],4,fill=RED)

tr_newc= model.add(sq_newa,[1],3,fill=ORANGE)
tr_newd= model.add(sq_newb,[3],3,fill=ORANGE)

tr_newe= model.add(sq_newa,[2],3,fill=ORANGE)
tr_newd= model.add(sq_newb,[2],3,fill=ORANGE)
tr_newf= model.add(tr_newe,[2],3,fill=ORANGE)

big_again = model.add(sq_4,[2],12,fill=BLUE)
big_again2= model.add(sq_5,[2],12,fill=BLUE)

sq_final = model.add(tr_newf,[1],4,fill=RED)
#tr3e = model.add(s12bA,[9],      3, fill=ORANGE)
#tr3f = model.add(s12bB,[8],      3, fill=ORANGE)

#sq3a = model.add(tr3c ,[2],      4, fill=RED)
#sq3b = model.add(tr3d ,[2],      4, fill=RED)
#sq3c = model.add(tr3e ,[1],      4, fill=RED)
#sq3d = model.add(tr3f ,[1],      4, fill=RED)

#sq1b = model.add(sq1a, [2]     , 4, fill=RED)
#tri1a= model.add(sq1a, [3]     , 3, fill=ORANGE)
#tri1b= model.add(tri1a,[1]     , 3, fill=BLUE)
#tri1c= model.add(sq1b, [1,3]   , 3, fill=ORANGE)

#hex2 = model.add(sq1b, [2]     , 6, fill=GREEN)
#sq2a = model.add(hex2, [1,5]   , 4, fill=RED)
#tri2a = model.add(sq2a, [1]   , 3, fill=ORANGE)
#tri2b = model.add(sq2a, [3]   , 3, fill=ORANGE)
#tri2c = model.add(tri2b,[1]   , 3, fill=BLUE)
#sq2b = model.add(hex2, [2]    , 4, fill=RED)
#sq2c = model.add(sq2b, [2]    , 4, fill=RED)
#tri2d = model.add(sq2c,[1]    , 3, fill=ORANGE)
#sq2d = model.add(hex2, [4]    , 4, fill=RED)
#sq2e = model.add(sq2d, [2]    , 4, fill=RED)

#sq2f = model.add(hex2, [3]    , 4, fill=RED)
#sq2g = model.add(sq2f, [2]    , 4, fill=RED)

#hex3 = model.add(sq2c, [2]     , 6, fill=GREEN)
#hex3b= model.add(sq2g, [2]     , 6, fill=GREEN)

#tri3a = model.add(sq2f, [1]   , 3, fill=ORANGE)
#tri3b = model.add(tri3a,[2]   , 3, fill=BLUE)
#tri3c = model.add(sq2f, [3]   , 3, fill=ORANGE)
#tri3d = model.add(tri3c,[1]   , 3, fill=BLUE)

#tri3e = model.add(sq2g, [1,3] , 3, fill=ORANGE)
#tri3f = model.add(tri3b,[1]   , 3, fill=ORANGE)
#tri3g = model.add(tri3d,[2]   , 3, fill=ORANGE)
#

#sq4a = model.add(hex3, [2,5]  , 4, fill=RED)
#sq4b = model.add(hex3b,[1,5]  , 4, fill=RED)

#sq2b = model.add(hex2, [2,3]   , 4, fill=RED)
#sq2c = model.add(sq2b, [2]     , 4, fill=RED)
#hex3 = model.add(sq2c, [2]     , 6, fill=GREEN)
#tri2a= model.add(sq2b , [1,3]  , 3, fill=ORANGE)
#tri2b= model.add(tri2a, [2]    , 3, fill=BLUE)

#hex3 = model.add(sq2b, [2]     , 6, fill=GREEN)
#connecting_sq3 = model.add(hex2, [1,2,5] , 4, fill=BLUE)


"""
b = model.add(a, [2], 4, fill=RED)
c = model.add(a, [3], 3, fill=ORANGE)
d = model.add(c, [1], 3, fill=BLUE)
e = model.add(d, [1,2], 3, fill=ORANGE)


z  = model.add(b, [2], 6, fill=GREEN)
b2 = model.add(z, [1,5], 4, fill=RED)
f  = model.add(z, [2,3,4], 4, fill=RED)
g  = model.add(f, [2], 4, fill=RED)
h  = model.add(b2, [1,3], 3, fill=ORANGE)
i1 = model.add(f, [1], 3, fill=ORANGE)
i2 = model.add(f, [3], 3, fill=ORANGE)
j  = model.add(g, [1,3], 3, fill=ORANGE)
k  = model.add(i1, [2], 3, fill=BLUE)



z2  = model.add(g, [2], 6, fill=GREEN)
sq_new  = model.add(z2, [1,2,3,4], 4, fill=RED)
sq_new2 = model.add(sq_new, [2], 4, fill=RED)
tri_new = model.add(sq_new,[1,3],3,fill=ORANGE)
tri_newb= model.add(sq_new2,[3],3,fill=ORANGE)
tri_new2= model.add(sq_new2,[1],3,fill=BLUE)
"""



if __name__=="__main__":
    plt.figure(figsize=(8,8))
    surface = model.render()
    surface.write_to_png('output.png')
