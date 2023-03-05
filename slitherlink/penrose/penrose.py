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


class PenroseBoard(Board):
    def __init__(self,divisions,base,size):
        edges,shape_list,tiles_list = setup_penrose_geometry(divisions,base,d=size)
        self.shape_list  = shape_list
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
            plt.plot(edge.p1[0],edge.p1[1],'ro')
            plt.plot(edge.p2[0],edge.p2[1],'ro')

        path_points = []
        for edge_id in self.surface_edges:
            self.edges_dict[edge_id].plot('r-')

        for tile in self.tiles_on:
            tile.plot(color='k',show=False)
        for tile in self.tiles:
            plt.text(tile.approx_x,tile.approx_y,str(tile.id),ha='center', va='center')
            #plt.text(tile.approx_x,tile.approx_y,str(tile.tally),ha='center', va='center')
        if show:
            plt.show()



random.seed(6)
divisions = 2
base      = 5             
size      = 100
b = PenroseBoard(divisions,base,size)


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
"""
"""













