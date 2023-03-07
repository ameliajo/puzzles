import matplotlib.pyplot as plt 

from edge import Edge
from tile import Tile
from board import Board

class PenroseBoard(Board):
    def __init__(self,edges,tiles_list):
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
            self.edges_dict[edge_id].plot('r-',thickness=4)

        for tile in self.tiles:
            #plt.text(tile.approx_x,tile.approx_y,str(tile.id),ha='center', va='center')
            plt.text(tile.approx_x,tile.approx_y,str(tile.tally),ha='center', va='center')
        if show:
            plt.show()



