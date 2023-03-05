
def adjacent_point(p1,p2):
    if p1[0] == p2[0] and abs(p1[1]-p2[1]) == 1:
        return True
    if p1[1] == p2[1] and abs(p1[0]-p2[0]) == 1:
        return True
    return False

def points_equal(p1,p2):
    diff = tuple(map(lambda i, j: abs(i - j), p1, p2))
    return diff[0] < 1e-8 and diff[1] < 1e-8


def is_new_edge_novel(edges_list,p1,p2):
    for edge in edges_list:
        if (points_equal(edge.p1,p1) and points_equal(edge.p2,p2)) or\
           (points_equal(edge.p2,p1) and points_equal(edge.p1,p2)):
            return False 
    return True

def find_edge_with_points(edges_list,p1,p2):
    for edge in edges_list:
        if (points_equal(edge.p1,p1) and points_equal(edge.p2,p2)) or\
           (points_equal(edge.p2,p1) and points_equal(edge.p1,p2)):
               return edge
    return False


