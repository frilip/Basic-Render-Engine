import numpy as np
from Light import light
from Gouraud_shading import g_shading
from Line_Class import line
from BoundaryPoint_Class import BoundaryPoint
from vector_interpolation import double_vector_interp, double_vector_interp_normal
from Gouraud_shading import BoundaryPointSortx
import math


def calculate_normals(verts, faces):
    #verts, faces are (3xN)

    #array that contains the normal vector of every face
    normals_faces = np.empty((3,len(faces[0])))
    #array that contains the normal vector of every vertex
    #the normal of every face that has the vertex will be added to it, and then it will be divided by its norm
    normals_vertices = np.zeros((3,len(verts[0])))

    for i in range (len(faces[0])):
        vert_indxs = [faces[0][i], faces[1][i], faces[2][i]]

        vert1 = verts[:,vert_indxs[0]]
        vert2 = verts[:,vert_indxs[1]]
        vert3 = verts[:,vert_indxs[2]]

        #calculate the normal vector using the cross product
        A = vert2 - vert1
        B = vert3 - vert1

        normals_faces[0][i] = A[1]*B[2] - A[2]*B[1]
        normals_faces[1][i] = A[2]*B[0] - A[0]*B[2]
        normals_faces[2][i] = A[0]*B[1] - A[1]*B[0]

        #add it to every vertex's normal
        normals_vertices[:,vert_indxs[0]] += normals_faces[:,i]
        normals_vertices[:,vert_indxs[1]] += normals_faces[:,i]
        normals_vertices[:,vert_indxs[2]] += normals_faces[:,i]
    
    #divide every vector in normals_vertices by its norm
    for v in range (len(normals_vertices[0])):
        norm = np.linalg.norm(normals_vertices[:,v])
        normals_vertices[:,v] = normals_vertices[:,v]/norm
    

    return normals_vertices







def shade_gouraud(verts_p, verts_n, verts_c, bcoords, cam_pos, ka, kd, ks, n, lpos, lint, lamb, X):
    #transpose normals so they are horizontal
    verts_n = verts_n.T
    color_1 = light(bcoords, verts_n[0], verts_c[0], cam_pos, ka, kd, ks, n, lpos, lint, lamb)
    color_2 = light(bcoords, verts_n[1], verts_c[1], cam_pos, ka, kd, ks, n, lpos, lint, lamb)
    color_3 = light(bcoords, verts_n[2], verts_c[2], cam_pos, ka, kd, ks, n, lpos, lint, lamb)

    #add them on an array
    colors = np.vstack((color_1,color_2,color_3))
    #shade
    Y = g_shading(X, verts_p, colors)
    return Y




def shade_phong(verts_p, verts_n, verts_c, bcoords, cam_pos, ka, kd, ks, n, lpos, lint, lamb, X):
    #transpose normals so they are horizontal
    verts_n=verts_n.T


    #if any two vertices are the same then there is no triangle, and the function returns
    OneEqTwo = np.array_equal(verts_p[0], verts_p[1], equal_nan=False)
    OneEqThree = np.array_equal(verts_p[0], verts_p[2], equal_nan=False)
    TwoEqThree = np.array_equal(verts_p[1], verts_p[2], equal_nan=False)
    if OneEqTwo or OneEqThree or TwoEqThree:
        return 

    #creating the lines that form the triangle from the three points
    line_1 = line(verts_p[0],verts_p[1],verts_c[0],verts_c[1],1, verts_n[0], verts_n[1])
    line_2 = line(verts_p[0],verts_p[2],verts_c[0],verts_c[2],2, verts_n[0], verts_n[2])
    line_3 = line(verts_p[1],verts_p[2],verts_c[1],verts_c[2],3, verts_n[1], verts_n[2])
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
            x_value_of_boundary_points = [math.ceil(Active_boundary_points[0].point[0]) , math.ceil(Active_boundary_points[1].point[0])]
            x_value_of_boundary_points.sort()   #sorting them
        

            for x in range (x_value_of_boundary_points[0] , x_value_of_boundary_points[1]):
                #[y,x] is the pixel of the image that needs to be drawn

                #sort the boundary points with respect to x so that the first element is the leftmost
                BoundaryPointSortx(Active_boundary_points)  
                #find the normal vector with double vector interpolation 
                normal_vector = double_vector_interp_normal([x,y], Active_boundary_points[0], Active_boundary_points[1])

                #find color using double_vector_interp function
                color = double_vector_interp([x,y], Active_boundary_points[0], Active_boundary_points[1])
                #calculate lighting
                color_lighted = light(bcoords,normal_vector, color,cam_pos, ka, kd, ks, n, lpos, lint, lamb)
                #draw pixel
                X[y][x]= color_lighted
                

                
        else:
            return
            

            #--- calculating the next active boundary points: ---
        
        #If any line ends on current y (line.ymax==y), the boundary point that belongs to that line is removed.
        for l in lines:
            if y == l.ymax and y!=ymin:
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