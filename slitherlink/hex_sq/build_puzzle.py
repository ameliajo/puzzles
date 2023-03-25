import random
import matplotlib.pyplot as plt
import matplotlib
from geometry import *
import sys
sys.path.append('../')

from edge import Edge
from tile import Tile
from board import Board
from hex_sq import HexSqBoard
from interactive import InteractivePlot
from write_results import write_results

matplotlib.rcParams['figure.figsize'] = (8, 8)



random.seed(5)
divisions = 3
base      = 5             
size      = 100

model = Model()
model.append(Shape(6, fill=RED))
a = model.add(0, range(6), 4, fill=ORANGE)
b = model.add(a, 1, 3, fill=BLUE)

c = model.add(a, 2, 6, fill=RED)
d = model.add(c, range(1,5), 4, fill=ORANGE)
#e = model.add(d, 3, 3, fill=BLUE)

#f = model.add(d, 2, 6, fill=RED)
#g = model.add(f, range(1,5), 4, fill=ORANGE)
#h = model.add(g, 3, 3, fill=BLUE)

#i = model.add(g, 2, 6, fill=RED)
#j = model.add(i, range(1,5), 4, fill=ORANGE)
#k = model.add(j, 3, 3, fill=BLUE)




edges,tiles_list = setup_hex_sq_geometry(model)
b = HexSqBoard(edges,tiles_list)
#b = HexSqBoard(model)

#b.plot(show=False)

### Alter geometry, if desired
#b.initialize_points()
#iplot = InteractivePlot(b)
#plt.show()


tile = b.tiles[10]
starting_tile = b.tiles[int(len(b.tiles)*0.5)]
b.initialize_board(starting_tile)
b.solve_board()

surfaces = b.surface_edges
for tile in b.tiles:
    tile.tally = 0
    for edge in tile.edges_ids:
        if edge in surfaces:
            tile.tally += 1

b.plot(show=True)

plt.show()

write_results(b)



