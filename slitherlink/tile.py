from edge import Edge
import matplotlib.pyplot as plt
import numpy as np
from misc import get_angle_of_point


import math

class Tile:
    def __init__(self,idVal,edges,shape):
        self.id = idVal
        self.edges = edges
        self.edges_ids = sorted([edge.id for edge in edges])
        shape = tuple(set(shape))
        self.shape = shape
        self.status = 0
        self.approx_x = sum(i for i, j in shape)/len(shape)
        self.approx_y = sum(j for i, j in shape)/len(shape)
        self.tally = 0
        self.visible_tally = 0

        self.neighbors_edges = {}

    def update_shape(self):
        shape_list = []
        for edge in self.edges:
            shape_list.append(edge.p1)
            shape_list.append(edge.p2)
        self.shape = tuple(shape_list)
        self.approx_x = sum(i for i, j in self.shape)/len(self.shape)
        self.approx_y = sum(j for i, j in self.shape)/len(self.shape)


    """
    def plot(self,show=False,color='c'):
        if len(self.shape) == 3:
            triangle_x = [tupple[0] for tupple in self.shape]
            triangle_y = [tupple[1] for tupple in self.shape]

            plt.fill(triangle_x, triangle_y,alpha=0.2,color=color)
        if len(self.shape) == 4:
            points = [point for point in self.shape]
            origin = tuple((sum([point[0] for point in points])/len(points),
                            sum([point[1] for point in points])/len(points)))
            ordered = sorted(points, key=lambda point: get_angle_of_point(point, origin))
            x = [val[0] for val in ordered]
            y = [val[1] for val in ordered]
            plt.fill(x,y,alpha=0.2,color=color)

        if show:
            plt.show()
    """

    def plot(self,color='c',show=False):
        x = []
        y = []
        for point in self.shape:
            x.append(point[0])
            y.append(point[1])
        #plt.fill_between(x,y,0)#,color=color,alpha=0.4)
        #plt.fill_between(x,y,0,alpha=0.2,color='b')#,color=color,alpha=0.4)
        #facecolor=[1., alpha, alpha], interpolate=False
        alpha = 0.5
        plt.plot(x, y, 'o',markersize=3,  color=[1., alpha, alpha])
        plt.fill_between(x, 0, y, facecolor=[1., alpha, alpha], interpolate=False)

        if show:
            plt.show()



    def find_neighbors(self,tiles):
        for tile in tiles:
            if tile.id == self.id: continue
            for edge_id in tile.edges_ids:
                if edge_id in self.edges_ids:
                    self.neighbors_edges[tile.id] = edge_id

    def check_ensure_complete(self):
        points = []
        for edge in self.edges:
            points.append(edge.p1)
            points.append(edge.p2)

        points_needed = []
        for point in list(points):
            if point not in points: continue
            points.remove(point)
            if point in points:
                points.remove(point)
            else:
                points_needed.append(point)
        return points_needed



