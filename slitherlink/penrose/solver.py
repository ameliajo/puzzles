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
from read_results import read_info, read_solution

from tqdm import tqdm

import time


def misc_solving_setup(b):
    # Make a counter to count the number of times we attempt a move
    b.counter = 0
    # Make sure each edge knows its corresponding tiles 
    for edge in b.edges():
        for tile in b.tiles:
            if edge in tile.edges:
                edge.tiles.append(tile)

    # Make a tally of all the tiles that are nearly complete
    # (e.g., each square that has three sides to be filled in, each
    #  triangle with two sides to be filled in, etc.)
    b.high_fill_tiles = []
    for tile in b.tiles:
        if tile.visible_tally == len(tile.edges)-1:
            b.high_fill_tiles.append(tile)

    # Make sure each point knows the edges to which it can connect
    b.initialize_points()

    # Make a list of the edges that are ajecent to a tile that's listed to have 
    # zero sides filled (i.e., these are the edges we know are right out)
    b.no_go_edges = set()
    for tile in b.tiles:
        if tile.visible_tally == 0:
            for edge in tile.edges:
                b.no_go_edges.add(edge.id)

    return b

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
        #plt.text(tile.approx_x,tile.approx_y,str(tile.tally),ha='center', va='center')
        if tile.visible_tally:
            plt.text(tile.approx_x,tile.approx_y,str(tile.visible_tally),ha='center', va='center')
        #plt.text(tile.approx_x+4,tile.approx_y,str(tile.working_tally),ha='center', va='center',color='r')
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
        if tile.visible_tally:
            if tile.working_tally > tile.visible_tally:
                return False
    return True

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


def explore_loops_around_nearly_filled_tile(b,high_fill,this_point,path):
    loops = get_loops_for_high_fill(b,this_point,high_fill)
    for loop in loops:
        for edge in loop:
            point = edge.p1 if edge.p1 not in path['points'] else edge.p2
            path = add_to_path(path,edge,point)
            update_working_tallies(b,edge.id,add=True)

        # We amy have accidentally added in duplicate points in this 
        # nonsense. Check for that ahead of time
        valid_option = True
        for point in path['points']:
            if path['points'].count(point) > 1:
                valid_option = False

        if valid_option:
            movement(b,path,path['points'][-2],path['points'][-1])
        if b.winning_path:
            return b
        else:
            for edge in loop[::-1]:
                update_working_tallies(b,path['edges'][-1].id,add=False)
                path = remove_last_entry_from_path(path)
    return b



def solve(b,starting_edge):
    for tile in b.tiles: tile.working_tally = 0
    b.winning_path = None

    last_point,this_point = starting_edge.p1,starting_edge.p2

    path = {'ids'   : [starting_edge.id],
            'edges' : [starting_edge],
            'points': [last_point,this_point]}

    update_working_tallies(b,starting_edge.id,add=True)

    return movement(b,path,last_point,this_point)


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
    random.shuffle(possible_edges_for_movement)

    for edge_id in possible_edges_for_movement:
        edge = b.edges_dict[edge_id]
        new_point = edge.p1 if edge.p1 != this_point else edge.p2

        # Check to see if we won
        if new_point == path['points'][0]: 
            path = add_to_path(path,edge,new_point)
            update_working_tallies(b,edge_id,add=True)
            winner = True
            for tile in b.tiles:
                if tile.visible_tally:
                    if tile.visible_tally != tile.working_tally:
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
            #plot_working_tallies(b,path['edges'],show=True)
            #plt.ion()
            #plot_working_tallies(b,path['edges'],show=False)
            #plt.draw(); plt.pause(0.001); plt.clf()
            if passed:
                movement(b,path,last_point=this_point,this_point=new_point)
                if b.winning_path:
                    return b

            path = remove_last_entry_from_path(path)
            update_working_tallies(b,edge_id,add=False)

    return b 
    

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

def sweep_for_unique_solutions(b,num_ambiguous_tiles,num_starting_edges,solution_edges,fail_immediately=True):

    tiles_to_make_ambiguous = [b.tiles[t.id] for t in random.sample(b.tiles,num_ambiguous_tiles)]
    for tile in b.tiles:
        if tile in tiles_to_make_ambiguous:
            tile.visible_tally = None
        else:
            tile.visible_tally = tile.tally
    b = misc_solving_setup(b)

    these_ids = [idVal for idVal in list(b.edges_dict.keys()) if idVal not in b.no_go_edges]
    starting_ids = random.sample(these_ids, min(num_starting_edges,int(len(these_ids)*0.5)))

    num_success     = 0
    num_indifferent = 0
    num_failed      = 0

    for starting_id in tqdm(starting_ids):
        starting_edge  = b.edges()[starting_id] 
        b = solve(b,starting_edge)
        if b.winning_path:
            A = sorted(b.winning_path['ids'])
            B = sorted([edge.id for edge in solution_edges])

            if A==B:
                num_success += 1
            else:
                num_failed += 1
                break
        else:
            num_indifferent += 1


    print('# Success:                   \t',num_success)
    print('# Idle (no solution reached):\t',num_indifferent)
    print('# Fails:                     \t',num_failed)

    return tiles_to_make_ambiguous if num_failed == 0 else None


if __name__=="__main__":

    matplotlib.rcParams['figure.figsize'] = (8, 8)
    random.seed(4)

    edges_list,tiles_list = read_info()
    b = PenroseBoard(edges_list,tiles_list)

    num_ambiguous_tiles,num_starting_edges = 16, 20 # base = 5, divisions = 2
    #num_ambiguous_tiles,num_starting_edges = 33, 20 # base = 5, divisions = 3



    solution_edges = read_solution(b)
    tiles_to_make_ambiguous = sweep_for_unique_solutions(b,num_ambiguous_tiles,num_starting_edges,solution_edges)
    if tiles_to_make_ambiguous:
        with open('output_files/ambiguous_tiles.dat','a') as f:
            for tile in tiles_to_make_ambiguous:
                f.write(str(tile.id)+' ')
            f.write('\n')


















