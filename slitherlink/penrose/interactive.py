import matplotlib.pyplot as plt
import sys 
sys.path.append("../")
from edge import Edge

class InteractivePlot:
    def __init__(self, b):
        fig, ax = plt.subplots()
        b.plot(show=False)

        self.cidpress   = fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.point_to_drag = None
        self.point_to_make = None
        self.edge_of_interest = None
        self.b = b

    def on_press(self, event):
        point_click = tuple((round(event.xdata),round(event.ydata)))
        for point in self.b.points:
            if abs(point_click[0]-point[0]) < 2 and abs(point_click[1]-point[1]) < 2:
                plt.plot(point_click[0],point_click[1],'ro')
                self.point_to_drag = point

        if self.point_to_drag == None:
            # If we're not dragging a point, check to see if we should 
            # create a new point
            xp= point_click[0]
            yp= round(point_click[1])
            
            edge_of_interest = None
            newpoint = None
            for edge in self.b.edges():
                x0,y0 = edge.p1
                x1,y1 = edge.p2
 
                if edge.p2[0] == edge.p1[0] and abs(edge.p2[0]-xp) < 3:
                    if (yp > y0 and yp > y1) or (yp < y0 and yp < y1): continue

                    self.edge_of_interest = edge
                    new_x = edge.p1[0]
                    new_y = yp
                    self.point_to_make = tuple((new_x,new_y))
                    break
                else:
                    if edge.p2[0]-edge.p1[0] == 0: continue
                    m = (y1-y0)/(x1-x0)

                    if (xp > x0 and xp > x1) or (xp < x0 and xp < x1): continue

                    yi = round(m*(xp-x0)+y0)
                    if abs(yi-yp) < 3:
                        self.edge_of_interest = edge
                        self.point_to_make = tuple((round(xp),yi))
                        break

            if self.edge_of_interest:
                self.edge_of_interest.plot('c')
            if self.point_to_make:
                plt.plot(self.point_to_make[0],self.point_to_make[1],'go')

        self.b.initialize_points()
        plt.draw()



    def on_release(self, event):
        point_release = tuple((round(event.xdata),round(event.ydata)))
        plt.plot(point_release[0],point_release[1],'go')

        if self.point_to_drag in self.b.points_dict:
            relevant_edge_ids = self.b.points_dict[self.point_to_drag]
            for edge_id in relevant_edge_ids:
                edge = self.b.edges_dict[edge_id]
                if edge.p1 == self.point_to_drag:
                    edge.update(point_release,1)
                if edge.p2 == self.point_to_drag:
                    edge.update(point_release,2)
                for tile_id in edge.tiles:
                    self.b.tiles[tile_id].update_shape()

        if self.point_to_make != None:
            tile_ids = self.edge_of_interest.tiles
            max_id = max(self.b.edges_dict.keys())
            e1 = Edge(max_id+1,self.edge_of_interest.p1,self.point_to_make)
            self.b.edges_dict[max_id+1] = e1
            e2 = Edge(max_id+2,self.edge_of_interest.p2,self.point_to_make)
            self.b.edges_dict[max_id+2] = e2
            self.edge_of_interest.on = False
            e1.tiles = self.edge_of_interest.tiles
            e2.tiles = self.edge_of_interest.tiles
            for tile_id in tile_ids:
                self.b.tiles[tile_id].edges.remove(self.edge_of_interest)
                self.b.tiles[tile_id].edges_ids.remove(self.edge_of_interest.id)
                self.b.tiles[tile_id].edges.append(e1)
                self.b.tiles[tile_id].edges_ids.append(e1.id)
                self.b.tiles[tile_id].edges.append(e2)
                self.b.tiles[tile_id].edges_ids.append(e2.id)
                self.b.tiles[tile_id].update_shape()

            del self.b.edges_dict[self.edge_of_interest.id]
            self.b.initialize_tile_ids()
            self.b.initialize_points()



        # Show new geometry
        self.b.initialize_points()
        plt.clf()
        self.b.plot(show=False)
        plt.draw()

        self.point_to_make = None
        self.point_to_drag = None
        self.edge_of_interest = None


