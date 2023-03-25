import matplotlib.pyplot as plt
import numpy as np
import random
import time
random.seed(3)

 
class Edge:
    def __init__(self,idVal,p1,p2):
        self.id = idVal
        self.x1 = p1[0]
        self.x2 = p2[0]
        self.y1 = p1[1]
        self.y2 = p2[1]
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return "Edge extending ({x1},{y1}) --> ({x2},{y2})".format(
                x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2 )

    def plot(self,color='r'):
        plt.plot([self.x1,self.x2],[self.y1,self.y2],color=color,alpha=0.7)

    def contains_point(self,point):
        return point in [self.p1,self.p2]


    def common_point(self,edge2):
        if edge2.contains_point(self.p1):
            return self.p1 
        if edge2.contains_point(self.p2):
            return self.p1 
        return False

class Tile:
    def __init__(self,idVal,x,y,neighbor_ids):
        self.id = idVal
        self.center = tuple((x+0.5,y+0.5))
        self.x = x
        self.y = y
        self.neighbor_ids = neighbor_ids
        self.status = 0
        self.edges = {}
        self.edgesList = []

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
                    self.edgesList.append(self.edges[direction])
                    old_edges.append(self.edges[direction])
                    found_existing_edge = True
                    continue
            if not found_existing_edge:
                points = dir_stuff[direction] 
                p1 = tuple((points[0][0]+self.x,points[1][0]+self.y))
                p2 = tuple((points[0][1]+self.x,points[1][1]+self.y))
                idVal = k
                self.edges[direction] = Edge(idVal,p1,p2)
                self.edgesList.append(self.edges[direction])
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


class Board:
    def __init__(self,nx,ny):
        self.nx = nx
        self.ny = ny
        self.tiles = []
        self.edges     = {}
        self.edges_ids = []
        max_edge_id = 0
        self.loser_surface_edges = []
        k = 0
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
                for edge in new_edges:
                    self.edges[edge.id] = edge
                    edge.tiles = [tile.id]
                    max_edge_id = max(max_edge_id,edge.id)
                for edge in old_edges:
                    edge.tiles.append(tile.id)
                self.tiles.append(tile)
                k += 1

        self.edges_ids = self.edges.keys()
        self.tile_ids_on       = []
        self.tile_ids_off      = list(range(k))
        self.tile_ids_off_edge = [k for k in list(range(k)) if \
                (self.tiles[k].x == 0 or self.tiles[k].x == nx-1 or\
                 self.tiles[k].y == 0 or self.tiles[k].y == ny-1)]
        self.tile_ids_on_edge = []

    def plot_boundary(self):
        #surfaces = self.get_surface_area()
        surfaces = self.surface_edges
        for edge_id in surfaces:
            edge = self.edges[edge_id]
            edge.plot()


    def plot_grid(self):
        fig = plt.figure()
        plt.xlim([-0.5,self.nx+0.5])
        plt.ylim([-0.5,self.ny+0.5])
        for i in range(self.nx+1): plt.plot([i,i],[0,self.ny],'k--',alpha=0.2)
        for i in range(self.ny+1): plt.plot([0,self.nx],[i,i],'k--',alpha=0.2)
        return fig

    def plot_board(self,show=True):
        #if fig.get_axes():
        #    plt.show()
        fig = self.plot_grid()
        for tile in self.tiles:
            tile.plot()
            #plt.text(tile.center[0]+0.15,tile.center[1]+0.15,str(tile.id),alpha=0.4)
            #plt.text(tile.center[0]-0.25,tile.center[1]-0.25,str(tile.tally),color='r')
            #plt.text(tile.center[0]-0.25,tile.center[1]+0.15,str(tile.working_tally),color='g')

        for tile in self.tiles_to_check:
            plt.text(tile.center[0]+0.15,tile.center[1]-0.25,str(tile.tally),color='c')
        for tile_id in self.tile_ids_on:
            tile = self.tiles[tile_id]
            #for edge in tile.edges:
            #    tile.edges[edge].plot()
        self.plot_boundary()
        if show:
            plt.show()
        return fig

    def plot_path(self,path,show=True):
        self.plot_board(show=False)
        for edge_id in path:
            self.edges[edge_id].plot('r')
        if show:
            plt.show()


    def load_points_dict(self):
        # find all edges that go along with zero side guys
        self.no_go_edges = set()
        for tile in self.tiles_to_check:
            if tile.tally == 0:
                for direction in tile.edges: self.no_go_edges.add(tile.edges[direction])

        # Copy all the points that are NOT in no-go-edges, and populate dict
        self.points_dict = {}
        for edge_id in self.edges:
            #tile_tallies = [self.tiles[tile].tally for tile in self.edges[edge_id].tiles]
            #if tile_tallies == [3,3]:
            #    continue
            edge = self.edges[edge_id]
            if edge in self.no_go_edges:
                continue
            for p in [edge.p1,edge.p2]:
                if p not in self.points_dict: self.points_dict[p] = set()
                self.points_dict[p].add(edge_id)
                for edge2_id in self.edges:
                    edge2 = self.edges[edge2_id]
                    if edge_id != edge2_id:
                        if p in [edge2.p1,edge2.p2]:
                            self.points_dict[p].add(edge_id)

        # In case I had added in points that have dead ends (no good way to
        # circle back around, and only one valid edge connecting it), let's 
        # remove it 
        edges_to_remove = []
        for point in self.points_dict:
            if len(b.points_dict[point])==1:
                edges_to_remove.append(list(self.points_dict[point])[0])

        for point in list(self.points_dict.keys()):
            for edge in list(self.points_dict[point]):
                if edge in edges_to_remove:
                    self.points_dict[point].remove(edge)


        # Remove the corner edges from consideration, if they belong to a tile
        # with too low of a tally (so low that moving around a corner is 
        # impossible
        for tile in b.tiles_to_check:
            if len(tile.neighbor_ids) == 2: # Corner tile
                if tile.tally == 1:         # If tally > length to traverse corner
                    for direction in tile.edges: # Find the edges that constitute corner
                        if len(tile.edges[direction].tiles) == 1:
                            for point in b.points_dict:
                                for val in list(b.points_dict[point]):
                                    if val == tile.edges[direction].id:
                                        b.points_dict[point].remove(val)



def check_tallies(b,path):
    for tile in b.tiles:
        if tile in b.tiles_to_check:
            if tile.tally < tile.working_tally:
                return False
        else: 
            if tile.working_tally == 4:
                return False

    #for tile in b.tiles_to_check:
    #    #print('\t\t',tile.x,tile.y,'\t\t',tile.tally,tile.working_tally)
    #    if tile.tally < tile.working_tally:
    #        return False
    return True


def move(b,path,last_point):
    #print('Starting at ',last_point)
    chosen_edge = path[-1]
    #print()
    #print("Chosen edge ",chosen_edge,b.edges[chosen_edge])
    last_point = b.edges[chosen_edge].p1 if b.edges[chosen_edge].p1 != last_point \
            else b.edges[chosen_edge].p2
    #print("Last point ", last_point)


    if len(path) > 2 and chosen_edge in b.three_sider_edges:
        #print('here we go buddy!')
        #print('we want to by cycling around',b.three_sider_edges[chosen_edge],b.three_sider_edges[chosen_edge].working_tally)
        tile_to_cycle = b.three_sider_edges[chosen_edge]
        if tile_to_cycle.working_tally == 3:
            possible_edges_for_movement = b.points_dict[last_point]
            possible_edges_for_movement = set(v for v in possible_edges_for_movement if v not in path)
        else:
            for next_edge in tile_to_cycle.edgesList:
                if next_edge.contains_point(last_point) and next_edge != b.edges[chosen_edge]:
                    possible_edges_for_movement = [next_edge.id]
                    break
    else:
        if last_point in b.three_sider_points and len(path) > 2:
            #print('HERE I SHOULD BE CIRCLING')
            possible_edges_for_movement2 = b.points_dict[last_point]
            possible_edges_for_movement2 = set(v for v in possible_edges_for_movement2 if v not in path)
            possible_edges_for_movement = []
            for edge in possible_edges_for_movement2:
                for tile in b.edges[edge].tiles:
                    if b.tiles[tile].tally == 3:
                        possible_edges_for_movement.append(edge)
 
        else:
            possible_edges_for_movement = b.points_dict[last_point]
            possible_edges_for_movement = set(v for v in possible_edges_for_movement if v not in path)

    #print("Possible edges for move ")
    #for val in possible_edges_for_movement:
    #    print("\t\t",b.edges[val])

    #b.plot_path(path,show=True)

    #plt.show()
    for chosen_edge in possible_edges_for_movement:
        #print(b.edges[path[0]].p1,[b.edges[chosen_edge].p1,b.edges[chosen_edge].p2])
        if b.edges[path[0]].p1 in [b.edges[chosen_edge].p1,b.edges[chosen_edge].p2]: 
            #print('here! :-)')
            success = True
            # Update sanity check
            for tile in b.edges[chosen_edge].tiles:
                b.tiles[tile].working_tally += 1
            for tile in b.tiles_to_check:
                if tile.tally != tile.working_tally:
                    #print("failed somehow :'-(")
                    success = False
                    for tile in b.edges[chosen_edge].tiles:
                        b.tiles[tile].working_tally -= 1
                    break
            if success:
                #print(b.edges[chosen_edge])
                path.append(chosen_edge)
                b.winning_path = path
                #b.plot_path(path,show=True)
                return True


        path.append(chosen_edge)

        # Update sanity check
        for tile in b.edges[chosen_edge].tiles:
            b.tiles[tile].working_tally += 1

        passed = check_tallies(b,path)
        #print('Passed? ',passed)
        #print(path)
        #b.plot_path(path,show=True)
        if not passed:
            path.pop(-1)
            for tile in b.edges[chosen_edge].tiles:
                b.tiles[tile].working_tally -= 1
            continue
        else:
            #next_last_point = b.edges[chosen_edge].p1 if b.edges[chosen_edge].p2 != last_point \
            #        else b.edges[chosen_edge].p2
            next_last_point = b.edges[chosen_edge].p1 if b.edges[chosen_edge].p1 != last_point \
                    else b.edges[chosen_edge].p2

            #b.plot_path(path,show=True)

            worked = move(b,path,last_point)
            if not worked:
                path.pop(-1)
                for tile in b.edges[chosen_edge].tiles:
                    b.tiles[tile].working_tally -= 1
            else:
                return True
    return False

def setup_solver(b,starting_edge):
    k = 0
    for i in range(b.nx):
        for j in range(b.ny): 
            b.tiles[k].working_tally = 0 
            k += 1

    path = [starting_edge]
    for tile in b.edges[starting_edge].tiles:
        b.tiles[tile].working_tally += 1
    last_point = b.edges[starting_edge].p1
    b.winning_path = []

    b.three_siders = [tile for tile in b.tiles_to_check if tile.tally == 3]
    b.three_sider_edges = {}
    b.three_sider_points = []
    for tile in b.three_siders:
        for edge in tile.edgesList:
            b.three_sider_edges[edge.id] = tile
            b.three_sider_points.append(edge.p1)
            b.three_sider_points.append(edge.p2)


    b.load_points_dict()
    return path,last_point





board = np.loadtxt('puzzle.dat',dtype='i')
b = Board(len(board),len(board[0]))
b.surface_edges = []

k = 0
for i in range(len(board)):
    for j in range(len(board[0])): 
        b.tiles[k].tally = board[i][j]
        k += 1




# Load solution
solution = []
with open('solution.dat','r') as f:
    for line in f.readlines():
        # find ID with these points
        p1,p2 = line.split('-->')
        p1 = p1.replace('(','').replace(')','')
        p1 = tuple((int(p1.split(',')[0]),int(p1.split(',')[1])))
        p2 = p2.replace('(','').replace(')','')
        p2 = tuple((int(p2.split(',')[0]),int(p2.split(',')[1])))
        #print(p1,p2)
        for id_edge in b.edges:
            #print("           ",b.edges[id_edge])
            if p1 in [b.edges[id_edge].p1,b.edges[id_edge].p2] and\
               p2 in [b.edges[id_edge].p1,b.edges[id_edge].p2]:
                solution.append(id_edge)


#starting_edge = 74
#starting_edge = 19
#starting_edge = 9

starting_edges = list(range(1,len(b.edges)))
#starting_edges = random.sample(starting_edges,min(10,len(starting_edges)))


b.tiles_to_check = []
for tile in b.tiles:
    b.tiles_to_check.append(tile)

num_to_remove = 12
num_to_remove = 18
for _ in range(num_to_remove):
    i = random.randint(0,len(b.tiles_to_check)-1)
    b.tiles_to_check.pop(i)

num_winners = 0
for starting_edge in starting_edges:
    path,last_point = setup_solver(b,starting_edge)
    valid_starting_edge = False
    for point in b.points_dict:
        if starting_edge in b.points_dict[point]:
            valid_starting_edge = True
            break
    #print(b.edges[starting_edge],valid_starting_edge)
    if not valid_starting_edge: continue
    #print('Finished Initializing :-)')
    t1 = time.time()
    move(b,path,last_point)
    t2 = time.time()
    if len(b.winning_path) > 0:
        success = sorted(b.winning_path) == sorted(solution)
        #print(success)
        #b.plot_path(b.winning_path,show=True)
        if success:
            #print(':-)')
            num_winners += 1
            print(num_winners,len(b.winning_path))
        else:
            print('OH NO WE FAILED AND ARE NO LONGER IN A UNIQUE SOLUTION')
            b.plot_path(b.winning_path,show=True)
            break

            #b.plot_path(b.winning_path,show=True)
    #print(b.winning_path)
    #print('TIME: ',t2-t1)
    #break




"""
for _ in range(1):
    k = 0
    for i in range(len(board)):
        for j in range(len(board[0])): 
            #b.tiles[k].tally = board[i][j]
            b.tiles[k].working_tally = 0 
            k += 1

    starting_edge = 19
    path = [starting_edge]
    for tile in b.edges[starting_edge].tiles:
        b.tiles[tile].working_tally += 1
    last_point = b.edges[starting_edge].p1
    b.winning_path = []

    move(b,path,last_point)
    success = sorted(b.winning_path) == sorted(solution)
    print(success)

    b.plot_path(b.winning_path,show=True)

    if not success:
        print("oh no!")
        break

"""

#if fig.get_axes():
#    plt.show()



