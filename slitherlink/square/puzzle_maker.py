import matplotlib.pyplot as plt
import numpy as np
import random
import sys
sys.path.append('../')
from edge import Edge
from tile import Tile
from misc import adjacent_point


"""
class Tile:
    def __init__(self,idVal,x,y,neighbor_ids):
        self.id = idVal
        self.center = tuple((x+0.5,y+0.5))
        self.x = x
        self.y = y
        self.neighbor_ids = neighbor_ids
        self.status = 0
        self.edges = {}

    def add_edges(self,edges_to_borrow,max_edge_id):
        dir_stuff = {'r':[[1,1],[0,1]], 
                     't':[[0,1],[1,1]],
                     'l':[[0,0],[0,1]],
                     'b':[[0,1],[0,0]]}
        k = max_edge_id+1
        new_edges,old_edges = [],[]
        for direction in dir_stuff:
            found_existing_edge = False
            for edge_to_borrow in edges_to_borrow:
                if direction == edge_to_borrow[0]:
                    self.edges[direction] = edge_to_borrow[1]
                    old_edges.append(self.edges[direction])
                    found_existing_edge = True
                    continue
            if not found_existing_edge:
                points = dir_stuff[direction] 
                p1 = tuple((points[0][0]+self.x,points[1][0]+self.y))
                p2 = tuple((points[0][1]+self.x,points[1][1]+self.y))
                idVal = k
                self.edges[direction] = Edge(idVal,p1,p2)
                k += 1
                new_edges.append(self.edges[direction])
        return new_edges,old_edges


    def plot(self):
        #plt.plot(self.center[0],self.center[1],'ro')
        x,y = self.x,self.y
        if self.status == 0: # off
            plt.fill_between([x,x+1],[y,y],[y+1,y+1],color='orange',alpha=0.2)
        if self.status == 1: # on
            plt.fill_between([x,x+1],[y,y],[y+1,y+1],color='blue',alpha=0.2)

    def plot_individual(self):
        x,y = self.x,self.y
        plt.fill_between([x,x+1],[y,y],[y+1,y+1],color='green',alpha=0.2)
"""


class Board:
    def __init__(self,nx,ny):
        self.nx = nx
        self.ny = ny


        #self.plot_grid()
        points = []
        for i in range(0,nx+1):
            for j in range(0,ny+1):
                points.append(tuple((i,j)))
        #for point in points:
        #    plt.plot(point[0],point[1],'ro')
        #plt.show()
        k = 0
        edges = []
        for p1 in points:
            for p2 in points:
                if adjacent_point(p1,p2):
                    edges.append(Edge(k,p1,p2))
                    k += 1

        self.edges = edges

        self.tiles = []
        k = 0
        for i in range(nx):
            for j in range(ny):
                bl = tuple((i  ,j  ))
                br = tuple((i+1,j  ))
                tl = tuple((i  ,j+1))
                tr = tuple((i+1,j+1))
                el = [edge for edge in edges if edge.contains_point(bl) and \
                                                edge.contains_point(tl)][0]
                er = [edge for edge in edges if edge.contains_point(br) and \
                                                edge.contains_point(tr)][0]
                et = [edge for edge in edges if edge.contains_point(tl) and \
                                                edge.contains_point(tr)][0]
                eb = [edge for edge in edges if edge.contains_point(bl) and \
                                                edge.contains_point(br)][0]
                self.tiles.append(Tile(k,[el,er,et,eb],[bl,tl,tr,br]))
                k += 1

        for tile in self.tiles:
            tile.find_neighbors(self.tiles)

        """
        #self.edges = {}
        max_edge_id = 0
        self.loser_surface_edges = []
        for i in range(nx):
            for j in range(ny):
                if j == 0:
                    neighbors = [k-ny,k+ny,k+1]
                elif j == ny-1:
                    neighbors = [k-ny,k+ny,k-1]
                else:
                    neighbors = [k-ny,k+ny,k-1,k+1]

                neighbors = [n for n in neighbors if n >= 0 and n < nx*ny]
                edges_to_borrow = []
                if i != 0:  edges_to_borrow.append(['l',self.tiles[k-ny].edges['r']])
                if j != 0:  edges_to_borrow.append(['b',self.tiles[k-1 ].edges['t']])
                tile = Tile(k,i,j,neighbors)
                new_edges,old_edges = tile.add_edges(edges_to_borrow,max_edge_id)
                #print('Made new edges ')
                for edge in new_edges:
                    self.edges[edge.id] = edge
                    edge.tiles = [tile.id]
                    #print('\t\t',edge.id)
                    max_edge_id = max(max_edge_id,edge.id)
                for edge in old_edges:
                    #self.edges[edge.id] = edge
                    edge.tiles.append(tile.id)
                self.tiles.append(tile)
                k += 1
        """

        self.tile_ids_off      = list(range(len(self.tiles)))
        self.tile_ids_on       = []
        self.tile_ids_on_edge  = []
        self.tile_ids_off_edge  = []
        for tile_id in self.tile_ids_off:
            tile = self.tiles[tile_id]
            edges_from_neighbors = [tile.neighbors_edges[neighbor] for \
                                    neighbor in tile.neighbors_edges]
            edges_in_total = tile.edges_ids
            if len(edges_from_neighbors) < len(edges_in_total):
                self.tile_ids_off_edge.append(tile_id)

        self.loser_surface_edges = []
        self.number_original_surface_tiles = len(self.tile_ids_off_edge)


        """
        self.tile_ids_on       = []
        self.tile_ids_off      = list(range(k))
        self.tile_ids_off_edge = [k for k in list(range(k)) if \
                (self.tiles[k].x == 0 or self.tiles[k].x == nx-1 or\
                 self.tiles[k].y == 0 or self.tiles[k].y == ny-1)]
        self.tile_ids_on_edge = []

        self.checkpoint = {}
        """



    def get_surface_area(self):
        surfaces = []
        for tile_id in self.tile_ids_on:
            edges = self.tiles[tile_id].edges
            for edge in edges:
                edge_id = edge.id
                if edge_id in surfaces:
                    surfaces.remove(edge_id)
                else:
                    surfaces.append(edge_id)

        self.surface_edges = surfaces
        self.winner_surface_edges = [s for s in surfaces if s not in self.loser_surface_edges]
        #print(len(self.winner_surface_edges))
        self.landlocked_tiles = []
        for tile_id in self.tile_ids_on:
            edges = self.tiles[tile_id].edges
            has_opening = False
            for edge in edges:
                edge_id = edge.id
                if edge_id in surfaces:
                    has_opening = True
            if not has_opening:
                self.landlocked_tiles.append(tile_id)
        self.surface_area = len(surfaces)
        self.area         = len(self.tile_ids_on)
        self.ratio        = self.surface_area/self.area
        return surfaces

    
    def plot_boundary(self):
        #surfaces = self.get_surface_area()
        surfaces = self.surface_edges
        for edge_id in surfaces:
            edge = self.edges[edge_id]
            edge.plot()



    def flip_tile(self,tile_id):
        self.tiles[tile_id].status = 1
        self.tile_ids_off.remove(tile_id)
        self.tile_ids_on.append(tile_id)
        if tile_id in self.tile_ids_off_edge:
            self.tile_ids_on_edge.append(tile_id)
            self.tile_ids_off_edge.remove(tile_id)
        self.tile_ids_on.sort()
        self.tile_ids_off.sort()
        self.get_surface_area()

    def revert_tile(self,tile_id):
        self.tiles[tile_id].status = 0
        self.tile_ids_on.remove(tile_id)
        self.tile_ids_off.append(tile_id)
        if tile_id in self.tile_ids_on_edge:
            self.tile_ids_on_edge.remove(tile_id)
            self.tile_ids_off_edge.append(tile_id)
        self.tile_ids_on.sort()
        self.tile_ids_off.sort()
        self.get_surface_area()


    def plot_grid(self):
        fig = plt.figure()
        plt.xlim([-0.5,self.nx+0.5])
        plt.ylim([-0.5,self.ny+0.5])
        for i in range(self.nx+1): plt.plot([i,i],[0,self.ny],'k--',alpha=0.2)
        for i in range(self.ny+1): plt.plot([0,self.nx],[i,i],'k--',alpha=0.2)
        return fig

    def check_legal(self):

        if len(self.tile_ids_off_edge) < 2*self.nx+2*self.ny*0.2:
            return False
        # START WITH BOUNDARY
        off_tiles_seeing_end = set(self.tile_ids_off_edge)
        for i in range(1,self.nx*self.ny):
            if self.nx*self.ny-i == self.tile_ids_off[-i]:
                off_tiles_seeing_end.add(self.tile_ids_off[-i])
                #print(self.tile_ids_off[-i-1])
            else:
                break


        # NOW START CREEPING IN TOWARDS THE CENTER
        while True:
            to_add = set()
            for tile in off_tiles_seeing_end:
                neighbors = self.tiles[tile].neighbor_ids
                for neighbor in neighbors:
                    if neighbor in self.tile_ids_off and neighbor not in off_tiles_seeing_end:
                        to_add.add(neighbor)
            if len(to_add) == 0:
                break
            off_tiles_seeing_end.update(to_add)
        # IF THERES ANY NOT-LOOPED VALUES THAT CANT SEE THE BOUNDARY,
        # THEN I MUST HAVE LAKES POPPING UP
        return len(off_tiles_seeing_end) == len(self.tile_ids_off)


    def plot_board(self,show=True):
        #if fig.get_axes():
        #    plt.show()
        fig = self.plot_grid()
        for tile in self.tiles:
            tile.plot()
            #plt.text(tile.center[0],tile.center[1],str(tile.id))
        for tile_id in self.tile_ids_on:
            tile = self.tiles[tile_id]
            #for edge in tile.edges:
            #    tile.edges[edge].plot()
        #self.plot_boundary()
        if show:
            plt.show()
        return fig


    def initialize_board(self,starting_tile):
        self.flip_tile(starting_tile.id)

        # starting out
        for i in range(2):
            flipped = False
            while not flipped:
                # sample surface
                surf_edge_id = random.sample(self.surface_edges ,1)[0]
                print(surf_edge_id)
                tiles_on_this_edge = self.edges[surf_edge_id].tiles
                print(tiles_on_this_edge)
                break
                if len(tiles_on_this_edge) > 2:
                    print('\noh god something is wrong\n',tiles_on_this_edge,'\n')
                if len(tiles_on_this_edge) == 2:
                    tile_to_flip = [t for t in tiles_on_this_edge if t in self.tile_ids_off][0]
                    self.flip_tile(tile_to_flip)
                    flipped = True

        #fig = self.plot_board()
        #print('Done setting up!')

    def solve_board(self):
        for i in range(int(self.nx*self.ny*0.6)):
            best_ratio, best_option  = 0, None
            for j in range(5):
                num_illegal_moves = 0
                found_legal_move = False
                num_landlocked   = len(self.landlocked_tiles)
                while not found_legal_move:
                    tiles_on_this_edge = []
                    while len(tiles_on_this_edge) != 2:
                        if len(self.winner_surface_edges)>3:
                            surf_edge_id = random.sample(self.winner_surface_edges ,1)[0]
                        else:
                            surf_edge_id = random.sample(self.surface_edges ,1)[0]
                        tiles_on_this_edge = self.edges[surf_edge_id].tiles
                        if len(tiles_on_this_edge) < 2:
                            self.loser_surface_edges.append(surf_edge_id)

                    tile_to_flip = [t for t in tiles_on_this_edge if t in self.tile_ids_off][0]
                    self.flip_tile(tile_to_flip)
                    found_legal_move = self.check_legal()

                    if not found_legal_move:
                        self.loser_surface_edges.append(surf_edge_id)
                    #print(i,num_landlocked,len(b.landlocked_tiles))
                    if len(self.landlocked_tiles) > num_landlocked and found_legal_move:
                        if random.random() > 0.1:
                            found_legal_move = False

                    if not found_legal_move:
                        self.revert_tile(tile_to_flip)
                        num_illegal_moves += 1
                        if num_illegal_moves > 50: 
                            #fig = self.plot_board()
                            return
                if self.ratio > best_ratio:
                    best_ratio = self.ratio
                    best_option = tile_to_flip

                #if num_illegal_moves > 50: break
                self.revert_tile(tile_to_flip)
            #if num_illegal_moves > 50: break
            self.flip_tile(best_option)




"""
b = Board(20,10) 
#b = Board(10,10) 
#b = Board(8,5) 
b = Board(25,25) 
b = Board(20,20) 
#fig = b.plot_board()
b = Board(15,15) 
b = Board(3,5) 
b = Board(8,5) 
b = Board(6,12) 
"""
b = Board(3,5) 

random.seed(4)
random.seed(6)
b.plot_board(show=False)

tile = random.sample(b.tiles,1)[0]
approx_center_tile = b.tiles[int(len(b.tiles)*0.5)-int(0.5*b.ny)]
approx_center_tile = b.tiles[int(b.ny*0.5)]
b.initialize_board(approx_center_tile)
#b.plot_board(show=False)
plt.show()
"""
b.solve_board()
fig = b.plot_board()



fig = b.plot_board(show=False)
surfaces = b.surface_edges
for t in b.tiles:
    t.tally = 0
    edges_ids = [t.edges[k].id for k in t.edges]
    for edge in edges_ids:
        if edge in surfaces:
            t.tally += 1
    plt.text(t.x+0.5,t.y+0.5,str(t.tally))

puzzle = []
k = 0
for i in range(b.nx):
    this_chunk = []
    for j in range(b.ny):
        this_chunk.append(b.tiles[k].tally)
        k += 1
    puzzle.append(this_chunk)
puzzle_to_write = np.array(puzzle).T[::-1] # Pretty view, like how it is on plot
puzzle_to_write = np.array(puzzle)         # Easier view, like how I read it in
np.savetxt('puzzle.dat',puzzle_to_write,fmt='%i')

plt.show()



points = [tuple((b.edges[s].p1,b.edges[s].p2)) for s in surfaces]

solution = [points[0]]
points.remove(solution[-1])
while len(points)>0:
    this_point = [p for p in points if (p[0] in solution[-1] or p[1] in solution[-1])][0]
    points.remove(this_point)
    if this_point[0] != solution[-1][-1]:
        this_point = tuple((this_point[1],this_point[0]))
    solution.append(this_point)

with open('solution.dat','w') as f:
    for val in solution:
        f.write(str(val[0])+' --> '+str(val[1])+'\n')
    

"""

#if fig.get_axes():
#    plt.show()


