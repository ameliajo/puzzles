import matplotlib.pyplot as plt 

class Edge:
    def __init__(self,idVal,p1,p2):
        self.id = idVal
        self.x1 = p1[0]
        self.x2 = p2[0]
        self.y1 = p1[1]
        self.y2 = p2[1]
        self.p1 = p1
        self.p2 = p2
        self.tiles = []

    def update(self,point,i):
        if i == 1:
            self.p1 = point
            self.x1 = point[0]
            self.y1 = point[1]
        if i == 2:
            self.p2 = point
            self.x2 = point[0]
            self.y2 = point[1]



    def get_length(self):
        return ((self.p1[0]-self.p2[0])**2+(self.p1[1]-self.p2[1])**2)**0.5

    def __repr__(self):
        return "Edge extending ({x1},{y1}) --> ({x2},{y2})".format(
                x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2 )
        

    def plot(self,color='r'):
        plt.plot([self.x1,self.x2],[self.y1,self.y2],color,alpha=0.7)

    def contains_point(self,point):
        return point in [self.p1,self.p2]


    def common_point(self,edge2):
        if edge2.contains_point(self.p1):
            return self.p1 
        if edge2.contains_point(self.p2):
            return self.p1 
        return False


