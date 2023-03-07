import sys
sys.path.append('../')

from edge import Edge
from tile import Tile

def read_info():
    edges_list = []
    with open('./output_files/edges.dat','r') as f:
        for line in f.readlines()[1:]:
            idVal, x1, y1, x2, y2 = line.split()
            edges_list.append(Edge(int(idVal), tuple((int(x1),int(y1))),
                                               tuple((int(x2),int(y2)))))

    def replace_str(string,chars):
        for char in chars:
            string = string.replace(char,'')
        return string

    def string_to_list(string):
        new_string = replace_str(string,'[]\t,')
        new_string = new_string.split()
        return [int(val) for val in new_string]

    def string_to_tup_of_tup(string):
        list_tuples = []
        tuple_chunks = string.split('),')
        for chunk in tuple_chunks:
            chunk = replace_str(chunk,'()\t')
            x = int(chunk.split(',')[0])
            y = int(chunk.split(',')[1])
            list_tuples.append(tuple((x,y)))
        return tuple(list_tuples)

    tiles_list = []
    with open('./output_files/tiles.dat','r') as f:
        lines = f.readlines()[1:]
        for i in range(len(lines)):
            line = lines[i].split()
            idVal,numSides = int(line[0]), int(line[1])
            edges_ids  = string_to_list(lines[i].split(':')[1])
            tile_shape = string_to_tup_of_tup(lines[i].split(':')[2])
            tile_tally = int(replace_str(lines[i].split(':')[3],'\t'))
            t = Tile(idVal,[edge for edge in edges_list if edge.id in edges_ids],tile_shape)
            t.tally = tile_tally
            tiles_list.append(t)


    return edges_list,tiles_list

