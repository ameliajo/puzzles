from misc import points_equal
import math, cmath, cairo, random, re

class Board(object):

    def find_edge_with_points(self,p1,p2):
        for edge in self.edges():
            if (points_equal(edge.p1,p1) and points_equal(edge.p2,p2)) or\
               (points_equal(edge.p2,p1) and points_equal(edge.p1,p2)):
                   return edge
        return False

    def flip_tile(self,tile_id):
        self.tiles[tile_id].status = 1

        tile = self.tiles[tile_id]
        self.tiles_off.remove(tile)
        self.tiles_on.append(tile)
        if tile in self.tiles_off_edge:
            self.tiles_on_edge.append(tile)
            self.tiles_off_edge.remove(tile)

        self.get_surface_area()

    def revert_tile(self,tile_id):
        self.tiles[tile_id].status = 0

        tile = self.tiles[tile_id]
        self.tiles_on.remove(tile)
        self.tiles_off.append(tile)
        if tile in self.tiles_on_edge:
            self.tiles_on_edge.remove(tile)
            self.tiles_off_edge.append(tile)

        self.get_surface_area()

    def initialize_points(self):    
        self.points = set()
        self.points_dict = {}
        for edge in self.edges():
            self.points.add(edge.p1)
            self.points.add(edge.p2)
            if edge.p1 in self.points_dict:
                self.points_dict[edge.p1].add(edge.id)
            else:
                self.points_dict[edge.p1] = {edge.id}
            if edge.p2 in self.points_dict:
                self.points_dict[edge.p2].add(edge.id)
            else:
                self.points_dict[edge.p2] = {edge.id}

    def get_surface_area(self):
        surfaces = []
        for tile in self.tiles_on:
            for edge_id in tile.edges_ids:
                if edge_id in surfaces:
                    surfaces.remove(edge_id)
                else:
                    surfaces.append(edge_id)

        self.surface_edges = surfaces
        self.winner_surface_edges = [s for s in surfaces if s not in self.loser_surface_edges]

        #print(surfaces) 

        self.landlocked_tiles = []
        for tile in self.tiles_on:
            has_opening = False
            for edge_id in tile.edges_ids:
                if edge_id in surfaces:
                    # Currently setting this so that "landlocked" means only 
                    # those that are surrounded on all sides by filled in tiles
                    # If you take the "True" thing off of here, then you'll 
                    # make it so that the tiles on the edge of the board that 
                    # are otherwise surrounded by tiles also count as landlocked.
                    if len(self.edges_dict[edge_id].tiles) > 1 or True:
                        has_opening = True
                        break
            if not has_opening:
                self.landlocked_tiles.append(tile.id)


        self.surfaces     = surfaces
        self.surface_area = len(surfaces)
        self.area         = len(self.tiles_on)
        self.ratio        = self.surface_area/self.area

    def solve_board(self):
        for i in range(int(len(self.tiles)*0.5)):
            best_ratio, best_option = 0, None
            for j in range(5):
                num_illegal_moves = 0
                found_legal_move = False
                num_landlocked = len(self.landlocked_tiles)
                while not found_legal_move:
                    tiles_on_this_edge = []
                    while len(tiles_on_this_edge) != 2:
                        if len(self.winner_surface_edges)>3:
                            surf_edge_id = random.sample(self.winner_surface_edges,1)[0]
                        else:
                            surf_edge_id = random.sample(self.surface_edges,1)[0]
                        tiles_on_this_edge = self.edges_dict[surf_edge_id].tiles
                        if len(tiles_on_this_edge) < 2:
                            self.loser_surface_edges.append(surf_edge_id)
                    tile_to_flip = [t for t in tiles_on_this_edge if self.tiles[t] in self.tiles_off][0]
                    self.flip_tile(tile_to_flip)
                    found_legal_move = self.check_legal()
                    if not found_legal_move:
                        self.loser_surface_edges.append(surf_edge_id)
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

                self.revert_tile(tile_to_flip)

            self.flip_tile(best_option)

    def initialize_board(self,starting_tile):
        self.flip_tile(starting_tile.id)
        for i in range(2):
            flipped = False
            while not flipped:
                # sample surface
                surf_edge_id = random.sample(self.surface_edges ,1)[0]
                tiles_on_this_edge = self.edges_dict[surf_edge_id].tiles
                if len(tiles_on_this_edge) > 2:
                    print('\noh god something is wrong\n',tiles_on_this_edge,'\n')
                if len(tiles_on_this_edge) == 2:
                    tile_to_flip = [t for t in tiles_on_this_edge if self.tiles[t] in self.tiles_off][0]
                    self.flip_tile(tile_to_flip)
                    flipped = True
 
    def check_legal(self):
        if len(self.tiles_off_edge) < self.number_original_surface_tiles*0.2:
            return False

        points_chosen = {}
        for edge_id in self.surfaces:
            edge = self.edges_dict[edge_id]
            if edge.p1 in points_chosen:
                points_chosen[edge.p1] += 1
            else: 
                points_chosen[edge.p1] =  1
            if edge.p2 in points_chosen:
                points_chosen[edge.p2] += 1
            else: 
                points_chosen[edge.p2] =  1

        for point in points_chosen:
            if points_chosen[point] > 2:
                return False



        added = set([tile.id for tile in self.tiles_off_edge])
        reachable = set(added)
        while len(added) > 0:

            added_new = set()
            for tile_id in added:
                tile = self.tiles[tile_id]
                for neighbor_id in tile.neighbors_edges:
                    neighbor_tile = self.tiles[neighbor_id] 
                    if neighbor_tile.status == 0 and neighbor_tile.id not in reachable:
                        added_new.add(neighbor_tile.id)
            added = added_new
            reachable.update(added_new)

        return len(reachable) == len(self.tiles_off)

    def initialize_tile_ids(self):

        self.tiles_off      = [t for t in self.tiles]
        self.tiles_on       = []
        self.tiles_on_edge  = []
        self.tiles_off_edge  = []

        for tile in self.tiles_off:
            edges_from_neighbors = [tile.neighbors_edges[neighbor] for \
                                    neighbor in tile.neighbors_edges]
            edges_in_total = tile.edges_ids
            if len(edges_from_neighbors) < len(edges_in_total):
                self.tiles_off_edge.append(tile)



        self.loser_surface_edges = []
        self.number_original_surface_tiles = len(self.tiles_off_edge)


