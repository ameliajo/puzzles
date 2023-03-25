
import matplotlib.pyplot as plt
#from tile import Model, Shape
from geometry import *
import numpy as np

BLUE   = 0x477984
ORANGE = 0xEEAA4D
RED    = 0xC03C44
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

#i = model.add(g, 2, 6, fill=RED)
#j = model.add(i, range(1,5), 4, fill=ORANGE)
#k = model.add(j, 3, 3, fill=BLUE)



if __name__=="__main__":
    plt.figure(figsize=(8,8))
    import sys
    sys.path.append('../')
    from tile import Tile
    from edge import Edge
    from misc import is_new_edge_novel

    edges_list,tiles_list = setup_hex_sq_geometry(model)
    tile = tiles_list[0]
    for t in tiles_list:
        t.find_neighbors(tiles_list)

    new_tiles_list = []
    new_edges_list = []

    hex_tiles = [t for t in tiles_list if len(t.shape) == 6]
    for tile in hex_tiles:
        for point in tile.shape:
            these_tiles = [t for t in tiles_list if point in t.shape]
            tile_points = [tuple((rt.approx_x,rt.approx_y)) for rt in these_tiles]
            for t in these_tiles:
                pairing_tile = [t1 for t1 in these_tiles if (t1!=t and t1.id in t.neighbors_edges)]
                p1 = tuple((t.approx_x,t.approx_y))
                p2 = tuple((pairing_tile[0].approx_x,pairing_tile[0].approx_y))
                if is_new_edge_novel(new_edges_list,p1,p2):
                    e_new = Edge(len(new_edges_list),p1,p2)
                    new_edges_list.append(e_new)
                p2 = tuple((pairing_tile[1].approx_x,pairing_tile[1].approx_y))
                if is_new_edge_novel(new_edges_list,p1,p2):
                    e_new = Edge(len(new_edges_list),p1,p2)
                    new_edges_list.append(e_new)
            relevant_edges = [e for e in new_edges_list if e.p1 in tile_points and e.p2 in tile_points]
            new_tile = Tile(len(new_tiles_list),relevant_edges,tuple(tile_points))
            new_tiles_list.append(new_tile)

    #for edge in edges_list:
    #    edge.plot('r',2)
    for tile in new_tiles_list:
        for edge in tile.edges:
            edge.plot('g')
    print(len(new_tiles_list))
    print(len(new_edges_list))
    plt.show()

    #surface = model.render()
    #surface.write_to_png('output.png')
