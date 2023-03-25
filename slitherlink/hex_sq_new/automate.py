import random
import matplotlib.pyplot as plt
import matplotlib
from geometry import *
import os
import sys
sys.path.append('../')

from edge import Edge
from tile import Tile
from board import Board
from hex_sq import HexSqBoard
from interactive import InteractivePlot
from write_results import write_results
from new_solver import *
from tqdm import tqdm

matplotlib.rcParams['figure.figsize'] = (8, 8)



random.seed(1)
divisions = 3
base      = 5             
size      = 100

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


def mkdir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)

for i_puzzle in range(1,15):
    print(i_puzzle)
    #dirname = './output_files/'+str(i_puzzle)
    dirname = './B/'+str(i_puzzle)
    mkdir(dirname)

    edges,tiles_list = setup_hex_sq_geometry(model)
    b = HexSqBoard(edges,tiles_list)

    tile = b.tiles[10]
    starting_tile = b.tiles[int(len(b.tiles)*0.5)]
    b.initialize_board(starting_tile)
    b.solve_board()

    for tile in b.tiles:
        tile.tally = 0
        for edge in tile.edges_ids:
            if edge in b.surface_edges:
                tile.tally += 1

    #b.plot(show=True)

    write_results(b,directory=dirname)



    edges_list,tiles_list = read_info(directory=dirname)
    b1 = HexSqBoard(edges_list,tiles_list)

    solution_edges = read_solution(b1,directory=dirname)
    solution_ids   = sorted([e.id for e in solution_edges])

    num_ambiguous_tiles = 1

    ambiguous_tile_ids = [t.id for t in random.sample(b1.tiles,num_ambiguous_tiles)]
    non_ambiguous_tile_ids = [t.id for t in b1.tiles if t.id not in ambiguous_tile_ids]

    can_be_solved = solvable(ambiguous_tile_ids,solution_ids,dirname )

    #print(can_be_solved)
    if can_be_solved:
        for new_ambiguous in tqdm(non_ambiguous_tile_ids):
            ambiguous_tile_ids.append(new_ambiguous)
            can_be_solved = solvable(ambiguous_tile_ids,solution_ids,dirname )
            if not can_be_solved:
                ambiguous_tile_ids.remove(new_ambiguous)
        edges_list,tiles_list = read_info(directory=dirname)
        b = HexSqBoard(edges_list,tiles_list)
        for tile in b.tiles:
            if tile.id in ambiguous_tile_ids: tile.visible_tally = None
            else: tile.visible_tally = tile.tally
        b = misc_solving_setup(b)

        print('DONE')
        #b.plot()
    
        with open(dirname+'/ambiguous_tiles.dat','w') as f:
            for tile_id in ambiguous_tile_ids:
                f.write(str(tile_id)+' ')
            f.write('\n')



