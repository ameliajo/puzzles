import random
import matplotlib.pyplot as plt
import matplotlib
from geometry import *
import sys
sys.path.append('../')

from edge import Edge
from tile import Tile
from board import Board

matplotlib.rcParams['figure.figsize'] = (8, 8)


class PenroseBoard(Board):
    def __init__(self,divisions,base):
        edges,shape_list,tiles_list = setup_penrose_geometry(divisions,base)
        self.shape_list  = shape_list
        self.edges       = edges
        self.tiles       = tiles_list

        for tile in self.tiles:
            tile.find_neighbors(self.tiles)

        self.initialize_tile_ids()

    def plot(self,show=True):
        for edge in self.edges:
            edge.plot()
        for tile_id in self.tile_ids_on:
            self.tiles[tile_id].plot(color='k',show=False)
        for tile in self.tiles:
            #plt.text(tile.approx_x,tile.approx_y,str(tile.id),ha='center', va='center')
            plt.text(tile.approx_x,tile.approx_y,str(tile.tally),ha='center', va='center')
        if show:
            plt.show()



random.seed(6)
divisions = 2
base = 4             
b = PenroseBoard(divisions,base)

tile = b.tiles[10]
starting_tile = b.tiles[int(len(b.tiles)*0.5)]


b.initialize_board(starting_tile)
#b.plot(show=True)
b.solve_board()


surfaces = b.surface_edges
for tile in b.tiles:
    tile.tally = 0
    for edge in tile.edges_ids:
        if edge in surfaces:
            tile.tally += 1


b.plot(show=True)

plt.show()













