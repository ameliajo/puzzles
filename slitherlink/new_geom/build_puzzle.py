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
#from interactive import InteractivePlot
from write_results import write_results

matplotlib.rcParams['figure.figsize'] = (8, 8)



random.seed(1)
divisions = 3
base      = 5             
size      = 100



#from c import model
from a import model

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

b.plot(show=False)
plt.show()

write_results(b)



