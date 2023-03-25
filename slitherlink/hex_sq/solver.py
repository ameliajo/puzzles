import random
import matplotlib.pyplot as plt
import matplotlib
from geometry import *
import sys
sys.path.append('../')

from edge import Edge
from tile import Tile
from board import Board
from hex_sq import HexSqBoard
from interactive import InteractivePlot
from read_results import read_info, read_solution

#from tqdm import tqdm

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
    #b.initialize_no_go_edges()
    b.initialize_points()
    b.remove_undesirable_edges_from_point_dict()

    return b

def plot_working_tallies(b,path_edges,show=True):
    for edge in b.edges():
        edge.plot('k-.')
        #plt.plot(edge.p1[0],edge.p1[1],'ro')
        #plt.plot(edge.p2[0],edge.p2[1],'ro')
    for point in b.points_dict:
        for edge_id in b.points_dict[point]:
            b.edges_dict[edge_id].plot('c',2)


    path_points = []
    for edge in path_edges:
        edge.plot('r-',thickness=4)

    for tile in b.tiles:
        #plt.text(tile.approx_x,tile.approx_y,str(tile.id),ha='center', va='center')
        #plt.text(tile.approx_x,tile.approx_y,str(tile.tally),ha='center', va='center')
        if tile.visible_tally != None:
            plt.text(tile.approx_x,tile.approx_y,str(tile.visible_tally),ha='center', va='center')
        else:
            plt.plot(tile.approx_x,tile.approx_y,'ro',markersize=5)
        #plt.text(tile.approx_x+4,tile.approx_y,str(tile.working_tally),ha='center', va='center',color='r')
    if show:
        plt.show()


def update_working_tallies(b,edge_id,add):
    okay = True
    for tile in b.edges_dict[edge_id].tiles:
        if add:
            tile.working_tally += 1
            if tile.visible_tally != None:
                if tile.working_tally > tile.visible_tally:
                    okay = False
        else:
            tile.working_tally -= 1
    return okay

def check_tallies(b,edge_id):
    b.counter += 1
    #for tile in b.tiles:
    for tile in b.tiles:
        if tile.visible_tally != None:
            if tile.working_tally > tile.visible_tally:
                #if tile not in b.edges_dict[edge_id].tiles:
                #    print('here',tile,b.edges_dict[edge_id].tiles)
                return False
    return True

def add_to_path(b,edge,new_point):
    b.path['ids'].append(edge.id)
    b.path['edges'].append(edge)
    b.path['points'].append(new_point)
    #return path

def remove_last_entry_from_path(b):
    b.path['ids'].pop(-1)
    b.path['edges'].pop(-1)
    b.path['points'].pop(-1)
    #return path


def explore_loops_around_nearly_filled_tile(b,high_fill,this_point):
    loops = get_loops_for_high_fill(b,this_point,high_fill)
    for loop in loops:
        movement_of_loop_legal = True
        for i,edge in enumerate(loop):
            point = edge.p1 if edge.p1 not in b.path['points'] else edge.p2
            add_to_path(b,edge,point)
            update_valid = update_working_tallies(b,edge.id,add=True)
            if not update_valid:
                for j in range(i+1):
                    update_working_tallies(b,b.path['edges'][-1].id,add=False)
                    remove_last_entry_from_path(b)
                movement_of_loop_legal = False
                break
        if not movement_of_loop_legal: 
            continue

        # We amy have accidentally added in duplicate points in this 
        # nonsense. Check for that ahead of time
        valid_option = True
        #for point in b.path['points']:
        #    if b.path['points'].count(point) > 1:
        #        valid_option = False

        if valid_option:
            movement(b,b.path['points'][-2],b.path['points'][-1])
        if b.winning_path:
            return b
        else:
            for edge in loop[::-1]:
                update_working_tallies(b,b.path['edges'][-1].id,add=False)
                remove_last_entry_from_path(b)
                #plot_working_tallies(b,path['edges'],show=True)
    return b



def solve(b,starting_edge):
    for tile in b.tiles: tile.working_tally = 0
    b.winning_path = None

    last_point,this_point = starting_edge.p1,starting_edge.p2

    b.path = {'ids'   : [starting_edge.id],
            'edges' : [starting_edge],
            'points': [last_point,this_point],
            'times' : {'A':0,'B':0,
                       'C':0,'D':0,
                       'E':0,'F':0,
                       'G':0,'H':0}
            }

    update_working_tallies(b,starting_edge.id,add=True)

    return movement(b,last_point,this_point)


def movement(b,last_point,this_point):

    # If I approach a square that is supposed to have three sides filled in,
    # automatically loop around it both clockwise and counterclockwise and 
    # see if that works. Same for shapes of other sizes
    ta = time.time()
    high_fill = check_for_high_tally(b,this_point)
    if high_fill:
        return explore_loops_around_nearly_filled_tile(b,high_fill,this_point)
    tb = time.time()
    b.path['times']['A'] += tb-ta


    ta = time.time()
    possible_edges_for_movement = []
    for edge_id in b.points_dict[this_point]:
        if edge_id != b.path['ids'][-1]:
            possible_edges_for_movement.append(edge_id)
    tb = time.time()
    b.path['times']['B'] += tb-ta
    #random.shuffle(possible_edges_for_movement)

    for edge_id in possible_edges_for_movement:
        edge = b.edges_dict[edge_id]
        new_point = edge.p1 if edge.p1 != this_point else edge.p2

        # Check to see if we won
        if new_point == b.path['points'][0]: 

            ta = time.time()
            add_to_path(b,edge,new_point)
            tb = time.time()
            b.path['times']['C'] += tb-ta

            ta = time.time()
            update_working_tallies(b,edge_id,add=True)
            #plot_working_tallies(b,path['edges'],show=True)
            tb = time.time()
            b.path['times']['D'] += tb-ta

            winner = True
            #plot_working_tallies(b,path['edges'],show=True)
            for tile in b.tiles:
                if tile.visible_tally != None:
                    if tile.visible_tally != tile.working_tally:
                        winner = False
            if winner:
                if b.winning_path != None:
                    b.winning_path = 'Duplicate'
                    print('Duplicates')
                    return b
                else:
                    b.winning_path = b.path
                #return b
            else:
                ta = time.time()
                update_working_tallies(b,edge_id,add=False)
                remove_last_entry_from_path(b)
                #plot_working_tallies(b,path['edges'],show=True)
                tb = time.time()
                b.path['times']['E'] += tb-ta

                continue

        if new_point not in b.path['points']:
            ta = time.time()
            add_to_path(b,edge,new_point)
            #update_working_tallies(b,edge_id,add=True)
            update_valid = update_working_tallies(b,edge.id,add=True)

            passed = update_valid#check_tallies(b,edge_id)
            #passed = check_tallies(b,edge_id)
            tb = time.time()
            b.path['times']['F'] += tb-ta

            #plot_working_tallies(b,b.path['edges'],show=True)
            #plot_working_tallies(b,path['edges'],show=True)
            #plt.ion()
            #plot_working_tallies(b,b.path['edges'],show=False)
            #plt.draw(); plt.pause(0.001); plt.clf()
            if passed:
                movement(b,last_point=this_point,this_point=new_point)
                if b.winning_path:
                    return b

            ta = time.time()
            remove_last_entry_from_path(b)
            update_working_tallies(b,edge_id,add=False)
            tb = time.time()
            b.path['times']['G'] += tb-ta


    return b 
    

def check_for_high_tally(b,this_point):
    possible_edge_ids = b.points_dict[this_point]
    for edge_id in possible_edge_ids:
        edge = b.edges_dict[edge_id]
        for tile in edge.tiles:
            if tile.visible_tally != None:
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

def sweep_for_unique_solutions(b,tiles_to_make_ambiguous,num_starting_edges,solution_edges,fail_immediately=True):

    for tile in b.tiles:
        if tile in tiles_to_make_ambiguous:
            tile.visible_tally = None
        else:
            tile.visible_tally = tile.tally
    b = misc_solving_setup(b)

    these_ids = [idVal for idVal in list(b.edges_dict.keys()) if idVal not in b.no_go_edges]
    #starting_ids = random.sample(these_ids, min(num_starting_edges,int(len(these_ids)*0.5)))
    starting_ids = random.sample(list(b.edges_dict.keys()), min(num_starting_edges,len(these_ids)))

    num_success     = 0
    num_indifferent = 0
    num_failed      = 0

    #for starting_id in tqdm(starting_ids):
    for starting_id in starting_ids:
        starting_edge  = b.edges()[starting_id] 

        b = solve(b,starting_edge)
        if b.winning_path:
            if b.winning_path == 'Duplicate':
                num_failed += 1
                break
            else:
                num_success += 1
            #A = sorted(b.winning_path['ids'])
            #B = sorted([edge.id for edge in solution_edges])
            #if A==B:
            #    num_success += 1
            #else:
            #    num_failed += 1
            #    break
        else:
            num_indifferent += 1


    print('# Success:                   \t',num_success)
    print('# Idle (no solution reached):\t',num_indifferent)
    print('# Fails:                     \t',num_failed)

    return tiles_to_make_ambiguous if num_failed == 0 else None


if __name__=="__main__":

    matplotlib.rcParams['figure.figsize'] = (8, 8)
    random.seed(4)
#
    edges_list,tiles_list = read_info()
    b = HexSqBoard(edges_list,tiles_list)

    #num_ambiguous_tiles,num_starting_edges = 15, 20 # base = 5, divisions = 2
    num_ambiguous_tiles,num_starting_edges = 0,0 # base = 5, divisions = 3
    #num_ambiguous_tiles,num_starting_edges = 5,0 # base = 5, divisions = 3



    solution_edges = read_solution(b)

    tiles_to_make_ambiguous = [b.tiles[t.id] for t in random.sample(b.tiles,num_ambiguous_tiles)]


    for tile in b.tiles:
        if tile in tiles_to_make_ambiguous:
            tile.visible_tally = None
        else:
            tile.visible_tally = tile.tally

    b = misc_solving_setup(b)


    for tile in b.tiles:
        tile.preliminary_tally = 0

    for tile in b.tiles:
        tile.possible_edges = set()
    for point in b.points_dict:
        for edge_id in b.points_dict[point]:
            edge = b.edges_dict[edge_id]
            edge.plot('r',3)
            for tile in edge.tiles:
                tile.possible_edges.add(edge)

    certain_edges = set()
    for tile in b.tiles:
        if tile.visible_tally != None:
            if len(tile.possible_edges) == tile.visible_tally:
                for edge in tile.possible_edges:
                    certain_edges.add(edge)
                    for tile in edge.tiles:
                        tile.preliminary_tally += 1

    def plot_temp(b,certain_edges,show=True):
        b.plot(show=False)
        for point in b.points_dict:
            for edge_id in b.points_dict[point]:
                b.edges_dict[edge_id].plot('r',3)
        for edge in certain_edges:
            edge.plot('c',3)
        if show:
            plt.show()

    def remove_nonsense(b,certain_edges):
        # REMOVE NONSENSE ONES FROM LIST 
        for tile in b.tiles:
            if tile.visible_tally != None:
                if tile.preliminary_tally == tile.visible_tally:
                    for edge in tile.edges:
                        if edge in certain_edges: continue
                        for point in b.points_dict:
                            if edge.id in b.points_dict[point]:
                                b.points_dict[point].remove(edge.id)

    def add_new_certain_edges(b,certain_edges):
        # ADD NEW CERTAIN EDGES
        to_add = set()
        for point in b.points_dict:
            for edge_id in b.points_dict[point]:
                if b.edges_dict[edge_id] in list(certain_edges):
                    certain_edge = b.edges_dict[edge_id]
                    if len(b.points_dict[point]) == 2:
                        adding_this = [b.edges_dict[e] for e in b.points_dict[point] if b.edges_dict[e] != certain_edge]
                        for tile in adding_this[0].tiles:
                            if adding_this[0] not in to_add and adding_this[0] not in certain_edges:
                                tile.preliminary_tally += 1
                        to_add.add(adding_this[0])
        certain_edges = certain_edges.union(to_add)
        return certain_edges

    def add_tiles_based_on_tally_count(b,certain_edges):
        possible_edges = set()
        to_add = set()
        for point in b.points_dict:
            for edge_id in b.points_dict[point]:
                possible_edges.add(b.edges_dict[edge_id])
        for tile in b.tiles:
            possible_edges_this_tile = [e for e in possible_edges if e in tile.edges]
            if len(possible_edges_this_tile) == tile.tally:
                for edge in possible_edges_this_tile:
                    if edge not in certain_edges:
                        to_add.add(edge)
        for tile in b.tiles:
            for edge in to_add:
                if edge in tile.edges:
                    tile.preliminary_tally += 1
        certain_edges = certain_edges.union(to_add)
        return certain_edges

    def remove_edges_that_are_dead_ends(b,certain_edges):
        for point in b.points_dict:
            connecting_edges = [b.edges_dict[edge_id] for edge_id in b.points_dict[point]]
            num_in_certain_edges = 0
            for edge in connecting_edges:
                if edge in certain_edges:
                    num_in_certain_edges += 1
            if num_in_certain_edges > 1:
                for edge in connecting_edges:
                    if edge not in certain_edges:
                        p1 = point
                        p2 = edge.other_point(p1)
                        b.points_dict[p1].remove(edge.id)
                        b.points_dict[p2].remove(edge.id)
        return certain_edges

    def remove_vshape_tally1_edgecase(b):
        #plot_temp(b,certain_edges,show=False)
        for tile in b.tiles:
            if tile.tally == 1:
                possible_edges_this_tile = []
                for point in tile.shape:
                    for edge_id in b.points_dict[point]:
                        possible_edges_this_tile.append(b.edges_dict[edge_id])

                to_remove = set()
                for point in tile.shape:
                    num_this_point = 0
                    edges_this_point = set()
                    for edge in possible_edges_this_tile:
                        if edge.contains_point(point):
                            num_this_point += 1
                            edges_this_point.add(edge)
                    if num_this_point == 2 and len(b.points_dict[point]) == 2:
                        to_remove = to_remove.union(edges_this_point)
                for point in b.points_dict:
                    for edge in list(b.points_dict[point]):
                        if b.edges_dict[edge] in to_remove:
                            b.points_dict[point].remove(edge)




    #plot_temp(b,certain_edges)
    thin_ice = False
    for i in range(30):
        print('thin ice',thin_ice)
        n_certain_edges = len(certain_edges)
        print(i)
        print('\t\tAdding based off of path requirements')
        certain_edges = add_new_certain_edges(b,certain_edges)
        #plot_temp(b,certain_edges)

        print('\t\tRemoving based off of options')
        remove_nonsense(b,certain_edges)
        #plot_temp(b,certain_edges)

        print('\t\tAdding based off of path requirements')
        certain_edges = add_new_certain_edges(b,certain_edges)
        #plot_temp(b,certain_edges)

        print('\t\tRemoving based off of options')
        remove_nonsense(b,certain_edges)
        #plot_temp(b,certain_edges)

        print('\t\tAdding based off of tally count')
        certain_edges = add_tiles_based_on_tally_count(b,certain_edges)
        #plot_temp(b,certain_edges)

        print('\t\tRemoving based off of options')
        remove_nonsense(b,certain_edges)
        #plot_temp(b,certain_edges)

        print('\t\tRemoving undesirable ones')
        b.remove_undesirable_edges_from_point_dict()
        #plot_temp(b,certain_edges)

        print('\t\tRemoving edges at a vertex')
        certain_edges = remove_edges_that_are_dead_ends(b,certain_edges)
        #plot_temp(b,certain_edges)


        n_added = len(certain_edges) - n_certain_edges
        print('# Gained: ',n_added)

        if n_added == 0:
            if thin_ice == True:
                break
            remove_vshape_tally1_edgecase(b)
            certain_edges = add_new_certain_edges(b,certain_edges)
            remove_nonsense(b,certain_edges)
            thin_ice = True

        else:
            plot_temp(b,certain_edges)
            thin_ice = False



    plot_temp(b,certain_edges)

                


        #points_to_remove = set()
        #for point in b.points_dict:
        #    for edge_id in b.points_dict[point]:
        #        edge = b.edges_dict[edge_id]
        #        if len(b.points_dict[edge.p1]) > 1 and len(b.points_dict[edge.p2]) > 1:
        #            continue
        #        else:
        #            points_to_remove.add(point)
        #for point in points_to_remove:
        #    b.points_dict[point] = set()

    #plot_temp(b,[]) 
    #remove_nonsense(b,certain_edges)
    #plot_temp(b,certain_edges)
    #certain_edges = add_new_certain_edges(b,certain_edges)
    #plot_temp(b,certain_edges)


    #t0 = time.time()
    #solve(b,solution_edges[0])
    #t1 = time.time()
    #print(t1-t0)
    #plot_working_tallies(b,b.winning_path['edges'],show=True)
    #print(b.winning_path['times'])





    #tiles_to_make_ambiguous = sweep_for_unique_solutions(b,num_ambiguous_tiles,num_starting_edges,solution_edges)

    #if tiles_to_make_ambiguous:
    #    with open('output_files/ambiguous_tiles.dat','a') as f:
    #        for tile in tiles_to_make_ambiguous:
    #            f.write(str(tile.id)+' ')
    #        f.write('\n')


















