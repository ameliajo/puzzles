
import matplotlib.pyplot as plt
from model_builder import Model, Shape
import numpy as np

import sys
sys.path.append('../')
from edge import Edge
from tile import Tile
from misc import is_new_edge_novel, find_edge_with_points

BLUE   = 0x477984
ORANGE = 0xEEAA4D
RED    = 0xC03C44

plt.figure(figsize=(8,8))


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


#model.repeat(c)
surface = model.render()
surface.write_to_png('output.png')

def unique_shape(points,tiles_list):
    for tile in tiles_list:
        tile_points = tile.shape
        if points[0] in tile_points and \
           points[1] in tile_points and \
           points[2] in tile_points:
               return False
    return True

    

def setup_hex_sq_geometry(model):
    edges_list = []
    tiles_list = []
    k1 = 0
    k2 = 0
    for shape in model.shapes:
        these_edges = []
        points = [tuple((round(p[0]*100),round(p[1]*100))) for p in shape.points()]
        for i in range(1,len(points)):
            opx,opy = points[i-1] 
            npx,npy = points[i  ] 
            p1 = tuple((round(points[i-1][0]),round(points[i-1][1])))
            p2 = tuple((round(points[i  ][0]),round(points[i  ][1])))
            if is_new_edge_novel(edges_list,p1,p2):
                e = Edge(k1,p1,p2)
                edges_list.append(e)
                these_edges.append(e)
                k1 += 1
            else:
                e = find_edge_with_points(edges_list,p1,p2)
                edges_list.append(e)
                these_edges.append(e)

        if unique_shape(points,tiles_list):
            t = Tile(k2,these_edges,points)
            tiles_list.append(t)
            k2 += 1

    for edge in edges_list:
        for tile in tiles_list:
            if edge in tile.edges:
                if tile.id not in edge.tiles:
                    edge.tiles.append(tile.id)

    return edges_list,tiles_list


