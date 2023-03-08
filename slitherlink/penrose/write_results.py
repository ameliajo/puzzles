
def tuple_list_to_string(tup):
    string = ''
    for val in tup:
        string += str(val)+' '
    return string

def write_results(b,directory='./output_files'):
    with open(directory+'/edges.dat','w') as f:
        f.write('#ID\tx0\ty0\t\tx1\ty1\n')
        for edge_id in b.edges_dict:
            egde = b.edges_dict[edge_id]
            f.write( str(edge_id) + '\t' +\
                     tuple_list_to_string(b.edges_dict[edge_id].p1)+'\t\t'+
                     tuple_list_to_string(b.edges_dict[edge_id].p2)+'\n')


    with open(directory+'/tiles.dat','w') as f:
        f.write('#ID\t#Sides\t:\tEdge IDs\t:\tShape\t:\tTally\n')
        for tile in b.tiles:
            f.write(str(tile.id)+'\t'+str(len(tile.edges))+'\t:\t')
            f.write(str([e.id for e in tile.edges])+'\t:\t')
            f.write(str(tile.shape)+'\t:\t')
            f.write(str(tile.tally)+'\n')



    with open(directory+'/solution.dat','w') as f:
        f.write('# Edge ids indicating the winning path\n')
        f.write(tuple_list_to_string(b.surface_edges)+'\n')




