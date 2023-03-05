import random
import matplotlib.pyplot as plt
import matplotlib
from geometry import *
import sys
sys.path.append('../')

from edge import Edge
from tile import Tile
from board import Board
from interactive import InteractivePlot

matplotlib.rcParams['figure.figsize'] = (8, 8)


class HexSqBoard(Board):
    def __init__(self,model):
        edges,tiles_list = setup_hex_sq_geometry(model)
        self.edges_dict  = dict()
        for edge in edges:
            self.edges_dict[edge.id] = edge

        self.tiles       = tiles_list
        self.surface_edges = []

        for tile in self.tiles:
            tile.find_neighbors(self.tiles)

        self.initialize_tile_ids()

    def edges(self):
        return [self.edges_dict[key] for key in self.edges_dict]

    def plot(self,show=True):
        for edge in self.edges():
            edge.plot('k-.')
            plt.plot(edge.p1[0],edge.p1[1],'ro',markersize=1)
            plt.plot(edge.p2[0],edge.p2[1],'ro',markersize=1)

        path_points = []
        for edge_id in self.surface_edges:
            self.edges_dict[edge_id].plot('r-')

        for tile in self.tiles_on:
            tile.plot(color='k',show=False)
        for tile in self.tiles:
            #plt.text(tile.approx_x,tile.approx_y,str(tile.id),ha='center', va='center')
            plt.text(tile.approx_x,tile.approx_y,str(tile.tally),ha='center', va='center')
        if show:
            plt.show()



random.seed(6)

model = Model()
model.append(Shape(6, fill=RED))
a = model.add(0, range(6), 4, fill=ORANGE)
b = model.add(a, 1, 3, fill=BLUE)

c = model.add(a, 2, 6, fill=RED)
d = model.add(c, range(1,5), 4, fill=ORANGE)
e = model.add(d, 3, 3, fill=BLUE)

f = model.add(d, 2, 6, fill=RED)
g = model.add(f, range(1,5), 4, fill=ORANGE)
h = model.add(g, 3, 3, fill=BLUE)

i = model.add(g, 2, 6, fill=RED)
j = model.add(i, range(1,5), 4, fill=ORANGE)
k = model.add(j, 3, 3, fill=BLUE)




b = HexSqBoard(model)
#b.plot(show=False)
#print(b.tiles[50].edges)
#print(b.tiles[51].edges)
#plt.show()

#### Alter geometry, if desired
#b.initialize_points()
#iplot = InteractivePlot(b)
#plt.show()


b.initialize_points()
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
"""
"""













