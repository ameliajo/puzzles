import numpy as np
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

def get_angle_of_point(point,origin):
    if point == origin: return -np.pi,0
    start_dir = np.array([1,0])
    vec = np.array([point[0]-origin[0], point[1]-origin[1]])
    vec_magnitude= (sum((np.array(point)-np.array(origin))**2))**0.5
    normalized = vec/vec_magnitude
    dot = sum(normalized*start_dir)
    dif = start_dir[1]*normalized[0] - start_dir[0]*normalized[1]     # x1*y2 - y1*x2
    angle = np.arctan2(dif, dot)
    return angle,vec_magnitude if angle >= 0 else 2*np.pi+angle, vec_magnitude


