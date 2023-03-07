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




matplotlib.rcParams['figure.figsize'] = (8, 8)

random.seed(6)

edges_list,tiles_list = read_info()


b = PenroseBoard(edges_list,tiles_list)

for edge in b.edges():
    for tile in b.tiles:
        if edge in tile.edges:
            edge.tiles.append(tile)

def update_working_tallies(b,edge_id,add):
    for tile in b.edges_dict[edge_id].tiles:
        if add:
            tile.working_tally += 1
        else:
            tile.working_tally -= 1


def check_tallies(b):
    for tile in b.tiles:
        if tile.working_tally > tile.tally:
            return False
    return True


#b.plot()
starting_edge = b.edges_dict[42]
#starting_edge = b.edges_dict[20]

#b.plot(show=False)
#starting_edge.plot('c',3)
b.initialize_points()

def solve(b,starting_edge):
    k = 0
    for tally in b.tiles: tally.working_tally = 0
    path_edges_ids  = [starting_edge.id]
    path_edges  = [starting_edge]
    chosen_edge = starting_edge
    last_point = starting_edge.p1
    this_point = starting_edge.p2
    path_points = [last_point,this_point]
    print('Starting at ',last_point)
    print('Moving to   ',this_point)
    update_working_tallies(b,starting_edge.id,add=True)
    path = {'ids':path_edges_ids,'edges':path_edges,'points':path_points}
    b.winning_path = None
    #plot_working_tallies(b,path['edges'],show=True)

    return movement(b,path,last_point,this_point)

def movement(b,path,last_point,this_point):

    possible_edges_for_movement = b.points_dict[this_point]
    possible_edges_for_movement = [edge for edge in possible_edges_for_movement if edge not in path['ids']]


    for edge_id in possible_edges_for_movement:
        edge = b.edges_dict[edge_id]
        print('considering edge: ',edge)
        path['ids'].append(edge.id)
        path['edges'].append(edge)
        new_point = edge.p1 if edge.p1 != this_point else edge.p2
        if new_point == path['points'][0]: 
            update_working_tallies(b,edge_id,add=True)
            winner = True
            for tile in b.tiles:
                if tile.tally != tile.working_tally:
                   winner = False
            if winner:
                #print('\t\there')
                #print('\t\t',edge.id)
                #print('\t\t',path['ids'])
                b.winning_path = path
                return b
            else:
                update_working_tallies(b,edge_id,add=False)
                print('REALLY THOUGHT I WAS GONNA WIN THERE!')
                path['ids'].pop(-1)
                path['edges'].pop(-1)
                continue

        if new_point not in path['points']:
            path['points'].append(new_point)
            update_working_tallies(b,edge_id,add=True)
            passed = check_tallies(b)
            print('Did it pass? ',passed)

            #plot_working_tallies(b,path['edges'],show=True)

            #plt.ion()
            #plot_working_tallies(b,path['edges'],show=False)
            #plt.draw()
            #plt.pause(0.001)
            #plt.clf()

            if passed:
                last_point2 = this_point
                this_point2 = new_point
                movement(b,path,last_point2,this_point2)
                print('now were back here')
                if b.winning_path:
                    return b
                else:
                    path['ids'].pop(-1)
                    path['edges'].pop(-1)
                    path['points'].pop(-1)
                    update_working_tallies(b,edge_id,add=False)
            else:
                path['ids'].pop(-1)
                path['edges'].pop(-1)
                path['points'].pop(-1)
                update_working_tallies(b,edge_id,add=False)

        else:
            #print(':-(')
            #plot_working_tallies(b,path['edges'])
            path['ids'].pop(-1)
            path['edges'].pop(-1)
            #plot_working_tallies(b,path['edges'])
    return False
    


b = solve(b,starting_edge)

#plt.show()



plot_working_tallies(b,b.winning_path['edges'])




solution_edges = []
with open('./output_files/solution.dat','r') as f:
   solution_edges = [b.edges_dict[int(val)] for val in f.readlines()[1].split()]























