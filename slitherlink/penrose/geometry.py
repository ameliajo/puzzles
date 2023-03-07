import sys
sys.path.append('../')
from edge import Edge
from tile import Tile
from misc import points_equal, is_new_edge_novel, find_edge_with_points
import numpy as np

# Code modified from function penrose obtained from 
# http://github.com/samm00/penrose

def is_shape_novel(shape_list,p1,p2,p3):
    sorted_points = sorted([p1,p2,p3], key=lambda tup: tup[1])
    sorted_points = sorted(sorted_points, key=lambda tup: tup[0])

    for shape in shape_list:
        sorted_shape_points = sorted(shape, key=lambda tup: tup[1])
        sorted_shape_points = sorted(sorted_shape_points, key=lambda tup: tup[0])

        if points_equal(sorted_points[0],sorted_shape_points[0]) and \
           points_equal(sorted_points[1],sorted_shape_points[1]) and \
           points_equal(sorted_points[2],sorted_shape_points[2]):
               return False
    return True

def get_complex(d,increment,i):
    phi = increment * (2*i - 1)
    v1_imag = d * (np.cos(phi) + 1j*np.sin(phi)) 
    phi = increment * (2*i + 1)
    v2_imag = d * (np.cos(phi) + 1j*np.sin(phi)) 
    return v1_imag,v2_imag

class Triangle:
    def __init__(self,vertices,shape):
        self.vertices = vertices
        self.v1_imag  = vertices[0]
        self.v2_imag  = vertices[1]
        self.v3_imag  = vertices[2]
        self.v1 = self.get_vertex_tuple(1) 
        self.v2 = self.get_vertex_tuple(2) 
        self.v3 = self.get_vertex_tuple(3) 
        self.shape    = shape 

    def get_vertex_tuple(self,i):
        return tuple((int(self.vertices[i-1].real),int(self.vertices[i-1].imag)))

    def __repr__(self):
        return str((self.shape,self.v1_imag,self.v2_imag,self.v3_imag))

    def subdivide(self,i,j): 
        phi = (5 ** 0.5 + 1) / 2 # Golden ratio
        return self.vertices[i-1] + (self.vertices[j-1] - self.vertices[i-1]) / phi

    def add_edges_if_novel(self,k,edges_list):
        if is_new_edge_novel(edges_list,self.v1,self.v2):
            edges_list.append(Edge(k,self.v1,self.v2))
            k += 1
        if is_new_edge_novel(edges_list,self.v2,self.v3):
            edges_list.append(Edge(k,self.v2,self.v3))
            k += 1
        if is_new_edge_novel(edges_list,self.v1,self.v3):
            edges_list.append(Edge(k,self.v1,self.v3))
            k += 1

        return k,edges_list


def setup_penrose_geometry(divisions,base,d=100):
    increment = 0.5 * np.pi / base
    triangle_list = []
    for i in range(base * 2):
        if i%2 == 0:
            v3_imag,v2_imag = get_complex(d,increment,i)
        else:
            v2_imag,v3_imag = get_complex(d,increment,i)
       
        triangle_list.append(Triangle([0,v2_imag,v3_imag],"thin"))

    for i in range(divisions):
        new_triangle_list = []
        for triangle in triangle_list:
            v1,v2,v3 = triangle.vertices
            if triangle.shape == "thin":
                p1 = triangle.subdivide(1,2)
                new_triangle_list += [Triangle([v3,p1,v2],"thin"),
                                      Triangle([p1,v3,v1],"thick")]
            else:
                vA = triangle.subdivide(2,1)
                vB = triangle.subdivide(2,3)
                new_triangle_list+= [Triangle([vB,v3,v1],"thick"),
                                     Triangle([vA,vB,v2],"thick"),
                                     Triangle([vB,vA,v1],"thin")]

            triangle_list = new_triangle_list

    k1 = 0
    edges_list = []
    shape_list = []
    # Add the edges and shapes, package up and provide to board upstairs
    for triangle in triangle_list:
        k1,edges_list = triangle.add_edges_if_novel(k1,edges_list)
        if is_shape_novel(shape_list,triangle.v1,triangle.v2,triangle.v3):
            shape_list.append(tuple((triangle.v1,triangle.v2,triangle.v3)))

              
    tiles_list = []
    k2 = 0
    for shape in shape_list:
        p1,p2,p3 = shape
        e1 = find_edge_with_points(edges_list,p1,p2)
        e2 = find_edge_with_points(edges_list,p1,p3)
        e3 = find_edge_with_points(edges_list,p2,p3)
        tile = Tile(k2,[e1,e2,e3],shape)
        e1.tiles.append(k2)
        e2.tiles.append(k2)
        e3.tiles.append(k2)
        k2 += 1
        tiles_list.append(tile)


    return edges_list,tiles_list




