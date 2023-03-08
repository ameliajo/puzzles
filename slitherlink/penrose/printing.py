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
from interactive import InteractivePlot
from read_results import read_info, read_solution, read_ambiguous_tiles

from tqdm import tqdm

import time

def plot(b,solution_edges,show_solution=True,show=True):

    for edge in b.edges():
        edge.plot('k-.',0.5)

    if show_solution:
        for edge in solution_edges:
            edge.plot('c',3)

    for tile in b.tiles:
        if tile.visible_tally:
            plt.text(tile.approx_x,tile.approx_y,str(tile.visible_tally),ha='center', va='center')
    if show:
        plt.show()



matplotlib.rcParams['figure.figsize'] = (8, 8)


#directory = 'output_files/Divisions3_Base5_Seed1_Ambiguous16'
directory = 'output_files/Divisions4_Base5_Seed1_Ambiguous32'
subdirs = os.popen("ls "+directory).read().split()
for subdir in subdirs:
    edges_list,tiles_list = read_info(directory+'/'+subdir)
    b = PenroseBoard(edges_list,tiles_list)
    solution_edges = read_solution(b,directory+'/'+subdir)

    ambiguous_tiles = read_ambiguous_tiles(b,directory+'/'+subdir)
    #b.plot(show)
    for tile in b.tiles:
        tile.visible_tally = 0
        for edge in tile.edges:
            if edge in solution_edges:
                tile.visible_tally += 1
    for tile in b.tiles:
        if tile in ambiguous_tiles:
            tile.visible_tally = None

    #plot(b,solution_edges,show_solution=False,show=True)
    #plot(b,solution_edges,show_solution=True,show=True)

    plot(b,solution_edges,show_solution=False,show=False)
    plt.grid(False)
    plt.axis('off')
    plt.savefig(directory+'/'+subdir+'/'+'no_solution_'+str(subdir)+'.pdf')
    plot(b,solution_edges,show_solution=True,show=False)
    plt.grid(False)
    plt.axis('off')
    plt.savefig(directory+'/'+subdir+'/'+'with_solution_'+str(subdir)+'.pdf')
    plt.clf()
    del b
    del solution_edges



