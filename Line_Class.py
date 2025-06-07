
'''class that describes the lines of a triangle. It it instances by taking as parameters the two points that define the line,
   (point1, point2) the colors of those points respectively (col1, col2) and a number that is specific to this line for 
   identification perposes (i.e. 1,2,3..)'''

'''from the two points, the properties of the line are deduced (xmin, xmax, ymin, ymax, slope) and stored as attributes'''

'''pointmin and pointmax are the lowest and highest with respect to y points of the line, if the line is horizontal they
   are arbitrary'''

class line:
    def __init__(self,point1,point2,col1,col2,number,norm1=[],norm2=[],uv1=[],uv2=[]):
        self.number = number
        self.point1=point1
        self.point2=point2
        self.col1=col1
        self.col2=col2
        self.norm1=norm1
        self.norm2 = norm2
        self.uv1 = uv1
        self.uv2 = uv2
        self.xmin = min(point1[0],point2[0])
        self.xmax = max(point1[0],point2[0])
        self.ymin = min(point1[1],point2[1])
        self.ymax = max(point1[1],point2[1])
        
        if point1[0]-point2[0]:    #if there is division by zero, the value float('inf') is stored as the slope
            self.slope = (point1[1]-point2[1])/(point1[0]-point2[0])
        else:
            self.slope = float('inf')

        if point1[1] == self.ymin:    #if y value of the first point is the minimum value then that point is the minimum 
            self.pointmin = point1
            self.pointmax = point2
        else:
            self.pointmin = point2
            self.pointmax = point1