import random
import matplotlib.pyplot as plt
import matplotlib
from geometry import *
import sys,os
sys.path.append('../')

from edge import Edge
from tile import Tile
from board import Board
from penrose_board import PenroseBoard
#from interactive import InteractivePlot
from write_results import write_results

from solver import *

matplotlib.rcParams['figure.figsize'] = (8, 8)

def mkdir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)



seed      = 1
divisions = 4
base      = 5             
size      = 100

random.seed(seed)
edges,tiles_list = setup_penrose_geometry(divisions,base,d=size)
num_puzzles_to_make = 5
starting_tiles = random.sample(tiles_list,num_puzzles_to_make)
#num_ambiguous_tiles,num_starting_edges = 16, 20 # base = 5, divisions = 2
num_ambiguous_tiles,num_starting_edges = 32, len(edges) # base = 5, divisions = 2

dirname = 'Divisions'+str(divisions)+'_'+'Base'+str(base)+'_'+'Seed'+str(seed)+\
                                     '_'+'Ambiguous'+str(num_ambiguous_tiles)

mkdir('output_files/'+dirname)


for i,starting_tile in enumerate(starting_tiles):

    subdir = 'output_files/'+dirname+'/'+str(i+1)
    mkdir(subdir)

    edges,tiles_list = setup_penrose_geometry(divisions,base,d=size)
    b = PenroseBoard(edges,tiles_list)
    b.initialize_board(starting_tile)
    b.solve_board()

    for tile in b.tiles:
        tile.status = 0
        tile.tally  = 0
        for edge in tile.edges_ids:
            if edge in b.surface_edges:
                tile.tally += 1

    #b.plot(show=True)

    write_results(b,directory=subdir)

    #b = PenroseBoard(edges_list,tiles_list)
    for edge in b.edges(): edge.tiles = []

    solution_edges = [b.edges_dict[idVal] for idVal in b.surface_edges]
    tiles_to_make_ambiguous = sweep_for_unique_solutions(b,num_ambiguous_tiles,
                                            num_starting_edges,solution_edges )
    if tiles_to_make_ambiguous:
        with open(subdir+'/ambiguous_tiles.dat','w') as f:
            for tile in tiles_to_make_ambiguous:
                f.write(str(tile.id)+' ')
            f.write('\n')


    for tile in b.tiles:    del tile
    for edge in b.edges():  del edge
    del b


