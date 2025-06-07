import numpy as np


'''Vector interpolation function. Returns the vector interpolation according to the equation
   explained in the report.'''
def vector_interp(p1,p2,V1,V2,coord,dim):
    if dim==1:   #x
        lamda = (coord-p1[0])/(p2[0]-p1[0])
    elif dim==2:
        lamda = (coord-p1[1])/(p2[1]-p1[1])
    else:
        raise Exception('dim must be either 1 or 2')
    return np.multiply(lamda,V2) + np.multiply((1-lamda),V1)





'''This function is used to find the color of a pixel in the gouraud shading using three vector interpolations.
   It takes as parameters the point we want to color and its left and right boundary points and returns
   the color V.'''
def double_vector_interp(point,boundleft,boundright):
    #Left and Right lines from the boundary points
    LeftLine = boundleft.line
    RightLine = boundright.line

    '''LeftLine.point1 or point2 are the two points that define the line, if they are equal the divisor in vector_interp will be zero
    So the code checks to see if the interpolation will be calculated with respect to x or y '''

    #Vector Interpolation to find the color of boundleft
    if LeftLine.point1[0]!=LeftLine.point2[0]:
        V1 = vector_interp(LeftLine.point1,LeftLine.point2,LeftLine.col1,LeftLine.col2,boundleft.point[0],1)  #with respect to x
    elif LeftLine.point1[1]!=LeftLine.point2[1]:
        V1 = vector_interp(LeftLine.point1,LeftLine.point2,LeftLine.col1,LeftLine.col2,boundleft.point[1],2)  #with respect to y 
    else:
        raise Exception('division by zero at left line')
    
    #Vector Interpolation to find the color of boundright
    if RightLine.point1[0]!=RightLine.point2[0]:
        V2 = vector_interp(RightLine.point1, RightLine.point2, RightLine.col1, RightLine.col2, boundright.point[0], 1)  #with respect to x
    elif RightLine.point1[1]!=RightLine.point2[1]:
        V2 = vector_interp(RightLine.point1, RightLine.point2, RightLine.col1, RightLine.col2, boundright.point[1], 2)  #with respect to y
    else:
        raise Exception('division by zero at right line')
    
    #Vector Interpolation to find the color of point
    if boundleft.point[0]!=boundright.point[0]:
        V = vector_interp(boundleft.point, boundright.point, V1, V2, point[0],1) #with respect to x
    elif boundleft.point[1]!=boundright.point[1]:
        V = vector_interp(boundleft.point, boundright.point, V1, V2, point[1],2) #with respect to y
    else:
        raise Exception('division by zero at center line')

    return V


def double_vector_interp_normal(point,boundleft,boundright):
    #Left and Right lines from the boundary points
    LeftLine = boundleft.line
    RightLine = boundright.line

    '''LeftLine.point1 or point2 are the two points that define the line, if they are equal the divisor in vector_interp will be zero
    So the code checks to see if the interpolation will be calculated with respect to x or y '''

    #Vector Interpolation to find the normals of boundleft
    if LeftLine.point1[0]!=LeftLine.point2[0]:
        V1 = vector_interp(LeftLine.point1,LeftLine.point2,LeftLine.norm1,LeftLine.norm2,boundleft.point[0],1)  #with respect to x
    elif LeftLine.point1[1]!=LeftLine.point2[1]:
        V1 = vector_interp(LeftLine.point1,LeftLine.point2,LeftLine.norm1,LeftLine.norm2,boundleft.point[1],2)  #with respect to y 
    else:
        raise Exception('division by zero at left line')
    
    #Vector Interpolation to find the normals of boundright
    if RightLine.point1[0]!=RightLine.point2[0]:
        V2 = vector_interp(RightLine.point1, RightLine.point2, RightLine.norm1, RightLine.norm2, boundright.point[0], 1)  #with respect to x
    elif RightLine.point1[1]!=RightLine.point2[1]:
        V2 = vector_interp(RightLine.point1, RightLine.point2, RightLine.norm1, RightLine.norm2, boundright.point[1], 2)  #with respect to y
    else:
        raise Exception('division by zero at right line')
    
    #Vector Interpolation to find the normal of point
    if boundleft.point[0]!=boundright.point[0]:
        V = vector_interp(boundleft.point, boundright.point, V1, V2, point[0],1) #with respect to x
    elif boundleft.point[1]!=boundright.point[1]:
        V = vector_interp(boundleft.point, boundright.point, V1, V2, point[1],2) #with respect to y
    else:
        raise Exception('division by zero at center line')

    return V




def double_vector_interp_uv(point,boundleft,boundright):
    #Left and Right lines from the boundary points
    LeftLine = boundleft.line
    RightLine = boundright.line

    '''LeftLine.point1 or point2 are the two points that define the line, if they are equal the divisor in vector_interp will be zero
    So the code checks to see if the interpolation will be calculated with respect to x or y '''

    #Vector Interpolation to find the uvs of boundleft
    if LeftLine.point1[0]!=LeftLine.point2[0]:
        V1 = vector_interp(LeftLine.point1,LeftLine.point2,LeftLine.uv1,LeftLine.uv2,boundleft.point[0],1)  #with respect to x
    elif LeftLine.point1[1]!=LeftLine.point2[1]:
        V1 = vector_interp(LeftLine.point1,LeftLine.point2,LeftLine.uv1,LeftLine.uv2,boundleft.point[1],2)  #with respect to y 
    else:
        raise Exception('division by zero at left line')
    
    #Vector Interpolation to find the uvs of boundright
    if RightLine.point1[0]!=RightLine.point2[0]:
        V2 = vector_interp(RightLine.point1, RightLine.point2, RightLine.uv1, RightLine.uv2, boundright.point[0], 1)  #with respect to x
    elif RightLine.point1[1]!=RightLine.point2[1]:
        V2 = vector_interp(RightLine.point1, RightLine.point2, RightLine.uv1, RightLine.uv2, boundright.point[1], 2)  #with respect to y
    else:
        raise Exception('division by zero at right line')
    
    #Vector Interpolation to find the uv of point
    if boundleft.point[0]!=boundright.point[0]:
        V = vector_interp(boundleft.point, boundright.point, V1, V2, point[0],1) #with respect to x
    elif boundleft.point[1]!=boundright.point[1]:
        V = vector_interp(boundleft.point, boundright.point, V1, V2, point[1],2) #with respect to y
    else:
        raise Exception('division by zero at center line')

    return V