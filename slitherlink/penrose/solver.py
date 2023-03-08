import random
import matplotlib.pyplot as plt
import matplotlib
from geometry import *
import sys
sys.path.append('../')

from edge import Edge
from tile import Tile
from board import Board
from penrose_board import PenroseBoard
from interactive import InteractivePlot
from read_results import read_info


import time

def plot_working_tallies(b,path_edges,show=True):
    for edge in b.edges():
        edge.plot('k-.')
        plt.plot(edge.p1[0],edge.p1[1],'ro')
        plt.plot(edge.p2[0],edge.p2[1],'ro')

    path_points = []
    for edge in path_edges:
        edge.plot('r-',thickness=4)

    for tile in b.tiles:
        #plt.text(tile.approx_x,tile.approx_y,str(tile.id),ha='center', va='center')
        plt.text(tile.approx_x,tile.approx_y,str(tile.tally),ha='center', va='center')
        plt.text(tile.approx_x+4,tile.approx_y,str(tile.working_tally),ha='center', va='center',color='r')
    if show:
        plt.show()


def update_working_tallies(b,edge_id,add):
    for tile in b.edges_dict[edge_id].tiles:
        if add:
            tile.working_tally += 1
        else:
            tile.working_tally -= 1


def check_tallies(b):
    b.counter += 1
    for tile in b.tiles:
        if tile.working_tally > tile.tally:
            return False
    return True

def solve(b,starting_edge):
    b.no_go_edges = set()
    for tile in b.tiles:
        if tile.tally == 0:
            for edge in tile.edges:
                b.no_go_edges.add(edge.id)

    k = 0
    for tally in b.tiles: tally.working_tally = 0
    path_edges_ids  = [starting_edge.id]
    path_edges  = [starting_edge]
    chosen_edge = starting_edge
    last_point = starting_edge.p1
    this_point = starting_edge.p2
    path_points = [last_point,this_point]
    update_working_tallies(b,starting_edge.id,add=True)
    path = {'ids':path_edges_ids,'edges':path_edges,'points':path_points}
    b.winning_path = None

    return movement(b,path,last_point,this_point)

def explore_loops_around_nearly_filled_tile(b,high_fill,this_point,path):
    loops = get_loops_for_high_fill(b,this_point,high_fill)
    for loop in loops:
        for edge in loop:
            point = edge.p1 if edge.p1 not in path['points'] else edge.p2
            path = add_to_path(path,edge,point)
            update_working_tallies(b,edge.id,add=True)
        movement(b,path,path['points'][-2],path['points'][-1])
        if b.winning_path:
            return b
        else:
            for edge in loop[::-1]:
                update_working_tallies(b,path['edges'][-1].id,add=False)
                path = remove_last_entry_from_path(path)
    return b

def add_to_path(path,edge,new_point):
    path['ids'].append(edge.id)
    path['edges'].append(edge)
    path['points'].append(new_point)
    return path

def remove_last_entry_from_path(path):
    path['ids'].pop(-1)
    path['edges'].pop(-1)
    path['points'].pop(-1)
    return path



def movement(b,path,last_point,this_point):

    # If I approach a square that is supposed to have three sides filled in,
    # automatically loop around it both clockwise and counterclockwise and 
    # see if that works. Same for shapes of other sizes
    high_fill = check_for_high_tally(b,this_point)
    if high_fill:
        return explore_loops_around_nearly_filled_tile(b,high_fill,this_point,path)

    possible_edges_for_movement = []
    for edge_id in b.points_dict[this_point]:
        if edge_id not in path['ids'] and edge_id not in b.no_go_edges:
            possible_edges_for_movement.append(edge_id)

    for edge_id in possible_edges_for_movement:
        edge = b.edges_dict[edge_id]
        new_point = edge.p1 if edge.p1 != this_point else edge.p2

        # Check to see if we won
        if new_point == path['points'][0]: 
            path = add_to_path(path,edge,new_point)
            update_working_tallies(b,edge_id,add=True)
            winner = True
            for tile in b.tiles:
                if tile.tally != tile.working_tally:
                   winner = False
            if winner:
                b.winning_path = path
                return b
            else:
                update_working_tallies(b,edge_id,add=False)
                path = remove_last_entry_from_path(path)
                continue

        if new_point not in path['points']:
            path = add_to_path(path,edge,new_point)
            update_working_tallies(b,edge_id,add=True)
            passed = check_tallies(b)
            ##plot_working_tallies(b,path['edges'],show=True)
            #plt.ion()
            #plot_working_tallies(b,path['edges'],show=False)
            #plt.draw(); plt.pause(0.001); plt.clf()
            if passed:
                movement(b,path,last_point=this_point,this_point=new_point)
                if b.winning_path:
                    return b

            path = remove_last_entry_from_path(path)
            update_working_tallies(b,edge_id,add=False)

    return False
    



matplotlib.rcParams['figure.figsize'] = (8, 8)

random.seed(4)

edges_list,tiles_list = read_info()


b = PenroseBoard(edges_list,tiles_list)
b.counter = 0

for edge in b.edges():
    for tile in b.tiles:
        if edge in tile.edges:
            edge.tiles.append(tile)



b.high_fill_tiles = []
for tile in b.tiles:
    if tile.tally == len(tile.edges)-1:
        b.high_fill_tiles.append(tile)

def check_for_high_tally(b,this_point):
    possible_edge_ids = b.points_dict[this_point]
    for edge_id in possible_edge_ids:
        edge = b.edges_dict[edge_id]
        for tile in edge.tiles:
            if tile.working_tally == 0:
                if tile in b.high_fill_tiles:
                    return tile
    return None

def get_loops_for_high_fill(b,this_point,high_fill):
    starters = [edge for edge in high_fill.edges if edge.contains_point(this_point)]
    edges_loops = []
    for starter in starters:
        edges_loop = []
        pA = this_point
        pB = starter.p1 if starter.p1 != this_point else starter.p2
        edges_loop.append(starter)
        
        for i in range(1,len(high_fill.edges)-1):
            for edge in high_fill.edges:
                if edge not in edges_loop and edge.contains_point(pB):
                    edges_loop.append(edge)
        edges_loops.append(edges_loop)
    return edges_loops





#b.plot()
#starting_edge = b.edges_dict[20]
#starting_edge = b.edges_dict[42]
starting_edge = b.edges_dict[107]
starting_edge = b.edges_dict[272]

#b.plot(show=False)
#starting_edge.plot('c',3)
b.initialize_points()


b = solve(b,starting_edge)
print(b.counter)
plot_working_tallies(b,b.winning_path['edges'])


solution_edges = []
with open('./output_files/solution.dat','r') as f:
   solution_edges = [b.edges_dict[int(val)] for val in f.readlines()[1].split()]
b.plot(show=False)
for edge in solution_edges:
    edge.plot('c',3)
plt.show()























