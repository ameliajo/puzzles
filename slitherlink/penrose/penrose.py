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
divisions = 4
base      = 6             
size      = 100
b = PenroseBoard(divisions,base,size)


class InteractivePlot:
    def __init__(self, line,b):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cidpress   = line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = line.figure.canvas.mpl_connect('button_release_event', self.on_release)

        self.point_to_drag = None
        self.point_to_make = None
        self.edge_of_interest = None

    def on_press(self, event):
        point_click = tuple((round(event.xdata),round(event.ydata)))
        for point in b.points:
            if abs(point_click[0]-point[0]) < 2 and abs(point_click[1]-point[1]) < 2:
                plt.plot(point_click[0],point_click[1],'ro')
                self.point_to_drag = point

        if self.point_to_drag == None:
            # If we're not dragging a point, check to see if we should 
            # create a new point
            xp= point_click[0]
            yp= round(point_click[1])
            
            edge_of_interest = None
            newpoint = None
            for edge in b.edges():
                x0,y0 = edge.p1
                x1,y1 = edge.p2
 
                if edge.p2[0] == edge.p1[0] and abs(edge.p2[0]-xp) < 3:
                    if (yp > y0 and yp > y1) or (yp < y0 and yp < y1): continue

                    self.edge_of_interest = edge
                    new_x = edge.p1[0]
                    new_y = yp
                    self.point_to_make = tuple((new_x,new_y))
                    break
                else:
                    if edge.p2[0]-edge.p1[0] == 0: continue
                    m = (y1-y0)/(x1-x0)

                    if (xp > x0 and xp > x1) or (xp < x0 and xp < x1): continue

                    yi = round(m*(xp-x0)+y0)
                    if abs(yi-yp) < 3:
                        self.edge_of_interest = edge
                        self.point_to_make = tuple((round(xp),yi))
                        break

            if self.edge_of_interest:
                self.edge_of_interest.plot('c')
            if self.point_to_make:
                plt.plot(self.point_to_make[0],self.point_to_make[1],'go')

        self.line.figure.canvas.draw()

    def on_release(self, event):
        point_release = tuple((round(event.xdata),round(event.ydata)))
        plt.plot(point_release[0],point_release[1],'go')

        if self.point_to_drag in b.points_dict:
            relevant_edge_ids = b.points_dict[self.point_to_drag]
            for edge_id in relevant_edge_ids:
                edge = b.edges_dict[edge_id]
                if edge.p1 == self.point_to_drag:
                    edge.update(point_release,1)
                if edge.p2 == self.point_to_drag:
                    edge.update(point_release,2)
                for tile_id in edge.tiles:
                    b.tiles[tile_id].update_shape()

        if self.point_to_make != None:
            tile_ids = self.edge_of_interest.tiles
            max_id = max(b.edges_dict.keys())
            e1 = Edge(max_id+1,self.edge_of_interest.p1,self.point_to_make)
            b.edges_dict[max_id+1] = e1
            e2 = Edge(max_id+2,self.edge_of_interest.p2,self.point_to_make)
            b.edges_dict[max_id+2] = e2
            self.edge_of_interest.on = False
            e1.tiles = self.edge_of_interest.tiles
            e2.tiles = self.edge_of_interest.tiles
            for tile_id in tile_ids:
                b.tiles[tile_id].edges.remove(self.edge_of_interest)
                b.tiles[tile_id].edges_ids.remove(self.edge_of_interest.id)
                b.tiles[tile_id].edges.append(e1)
                b.tiles[tile_id].edges_ids.append(e1.id)
                b.tiles[tile_id].edges.append(e2)
                b.tiles[tile_id].edges_ids.append(e2.id)
                b.tiles[tile_id].update_shape()

            del b.edges_dict[self.edge_of_interest.id]
            b.initialize_tile_ids()
            b.initialize_points()



        # Show new geometry
        b.initialize_points()
        plt.clf()
        b.plot(show=False)
        plt.draw()

        self.point_to_make = None
        self.point_to_drag = None
        self.edge_of_interest = None

### Alter geometry, if desired
b.initialize_points()
fig, ax = plt.subplots()
b.plot(show=False)
line, = ax.plot([0], [0])  # empty line
linebuilder = InteractivePlot(line,b)
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













