import random
import matplotlib.pyplot as plt
import matplotlib
from geometry import *
import sys
sys.path.append('../')

from edge import Edge
from tile import Tile
from board import Board
from penrose_board import PenroseBoard
from interactive import InteractivePlot
from write_results import write_results

matplotlib.rcParams['figure.figsize'] = (8, 8)



random.seed(6)
divisions = 2
base      = 4             
size      = 100
edges,tiles_list = setup_penrose_geometry(divisions,base,d=size)
b = PenroseBoard(edges,tiles_list)

#b.plot(show=False)

### Alter geometry, if desired
b.initialize_points()
iplot = InteractivePlot(b)
plt.show()


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



