'''class that describes the boundary points for the shading process. The coordinates of the point as well as the slope 
   of the line it belongs to, the line number and the line itself are stored as attributes.'''


class BoundaryPoint:
    def __init__(self,point,slope,line_number,line):
        self.point=point
        self.slope=slope
        self.line_number = line_number
        self.line = line