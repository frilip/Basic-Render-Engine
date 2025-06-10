import numpy as np
import math
from Line_Class import line
from BoundaryPoint_Class import BoundaryPoint

'''f_shading is the function responsible for the flat shading of a triangle given the coordinates of its vertices,
   their color and an image on which the triangle will be projected'''

def f_shading(img, vertices, vcolors):
    
    #if any two vertices are the same then there is no triangle, and the function returns
    OneEqTwo = np.array_equal(vertices[0], vertices[1], equal_nan=False)
    OneEqThree = np.array_equal(vertices[0], vertices[2], equal_nan=False)
    TwoEqThree = np.array_equal(vertices[1], vertices[2], equal_nan=False)
    if OneEqTwo or OneEqThree or TwoEqThree:
        return 


    #creating the lines that form the triangle from the three points
    line_1 = line(vertices[0],vertices[1],vcolors[0],vcolors[1],1)
    line_2 = line(vertices[0],vertices[2],vcolors[0],vcolors[2],2)
    line_3 = line(vertices[1],vertices[2],vcolors[1],vcolors[2],3)
    lines = [line_1 , line_2 , line_3]  #adding the lines in an array to access them easily

    #ymin and ymax are the min and max of every line's ymin and ymax respectively 
    ymin = min(line_1.ymin , line_2.ymin , line_3.ymin)
    ymax = max(line_1.ymax , line_2.ymax , line_3.ymax)

    '''Finding the initial active boundary points:
       The active boundary points are the points where any non horizontal line intersects the axis ymin.
       The code below checks for lines that have the above property, then creates an object of the class 
       BoundaryPoint where it stores the coordinates of the point together with the characteristics of 
       the line it belongs to.'''
    Active_boundary_points = []
    for l in lines:
        if l.ymin == ymin and l.slope!=0:
            boundary_point = BoundaryPoint(l.pointmin,l.slope,l.number,l)
            Active_boundary_points.append(boundary_point)
    #Active_boundary_points now cointains two objects of the class BoundaryPoint 
    
    for y in range (ymin,ymax+1):  #for every y where the triangle lies
        
        '''if Active_boundary_points contains two points, then we start drawing from the ceiling of the leftmost one 
           and stop before the ceiling of the rightmost one. If it contains any different amount of points the function
           returns.'''
        if len(Active_boundary_points)==2: 
            #storing the x values of the active boundary points:
            x_value_of_boundary_points=[math.ceil(Active_boundary_points[0].point[0]) , math.ceil(Active_boundary_points[1].point[0])] 
            x_value_of_boundary_points.sort()   #sorting them 
            for x in range (x_value_of_boundary_points[0] , x_value_of_boundary_points[1]):
                #in flat shading we color the whole triangle with the average of the colors of its vertices
                img[y][x]=[(vcolors[0][0]+vcolors[1][0]+vcolors[2][0])/3,  
                        (vcolors[0][1]+vcolors[1][1]+vcolors[2][1])/3,
                        (vcolors[0][2]+vcolors[1][2]+vcolors[2][2])/3]     
        else:
            return
            

            #--- calculating the next active boundary points: ---
        
        #If any line ends on current y (line.ymax==y), the boundary point that belongs to that line is removed.
        for l in lines:
            if y == l.ymax:
                for b in Active_boundary_points:
                    if b.line_number == l.number:
                        Active_boundary_points.remove(b)
            #Boundary points that belong to a non horizontal line that begins on current y (line.ymin==y) are appended.
            #This doesn't happen on the first iteration as these points are already in the array.
            elif y == l.ymin and l.slope!=0 and y!=ymin:
                boundary_point = BoundaryPoint(l.pointmin,l.slope,l.number,l)
                Active_boundary_points.append(boundary_point)   

        #The active boundary points get updated according to their slope.
        new_active_boundary_points = []
        for p in Active_boundary_points:
            if p.slope != float('inf'):
                new_x = p.point[0] + 1/p.slope
                new_point = [new_x, y+1]
            else:
                new_point = [p.point[0], y+1]
            new_boundary_point = BoundaryPoint(new_point, p.slope, p.line_number, p.line)
            new_active_boundary_points.append(new_boundary_point)
        Active_boundary_points = new_active_boundary_points
