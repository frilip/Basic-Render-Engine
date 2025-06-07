import numpy as np
from Functions import perspective_project, rasterize
from Functions import lookat as lookat_funct
from Additional_Functions import Find_Depth
from Shading import calculate_normals, shade_gouraud
from BoundaryPoint_Class import BoundaryPoint
from Line_Class import line
from Gouraud_shading import BoundaryPointSortx
import math
from vector_interpolation import double_vector_interp_uv, double_vector_interp_normal
from Light import light
from Gouraud_shading import g_shading

def bilerp(uv, texture_map):
    #assume uv is [x,y] floats in [0,1]
    H, W = len(texture_map), len(texture_map[0])

    x, y  = int(uv[0]*W), int(uv[1]*H)

    # Ensure x, y are within the valid range
    if (x<0 or x>W-1 or y<0 or y>H-1):
        return [0,0,0]
    elif (x==W-1 or y==H-1):
        return texture_map[y][x]
    else:
        # Get the values from the corners and interpolate 
        Q11 = texture_map[y, x]
        Q12 = texture_map[y, x + 1]
        Q21 = texture_map[y + 1, x]
        Q22 = texture_map[y + 1, x + 1]
        return Q11/4+Q12/4+Q21/4+Q22/4




def shade_phong_w_texture(verts_p, verts_n, bcoords, cam_pos, ka, kd, ks, n,
    lpos, lint, lamb, X, verts_uvs, texture_map):
    #function to shade using the texture_map, using the phong reflexion model

    #transpose normals so they are horizontal
    verts_n=verts_n.T


    #if any two vertices are the same then there is no triangle, and the function returns
    OneEqTwo = np.array_equal(verts_p[0], verts_p[1], equal_nan=False)
    OneEqThree = np.array_equal(verts_p[0], verts_p[2], equal_nan=False)
    TwoEqThree = np.array_equal(verts_p[1], verts_p[2], equal_nan=False)
    if OneEqTwo or OneEqThree or TwoEqThree:
        return 

    #creating the lines that form the triangle from the three points
    line_1 = line(verts_p[0],verts_p[1],[],[],1, verts_n[0], verts_n[1] ,verts_uvs[0], verts_uvs[1])
    line_2 = line(verts_p[0],verts_p[2],[],[],2, verts_n[0], verts_n[2] ,verts_uvs[0], verts_uvs[2])
    line_3 = line(verts_p[1],verts_p[2],[],[],3, verts_n[1], verts_n[2] ,verts_uvs[1], verts_uvs[2])
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

                #find the uv coordinates using double_vector_interp_uv
                uv_coords = double_vector_interp_uv([x,y],Active_boundary_points[0], Active_boundary_points[1])

                #find color using bilerp
                color = bilerp(uv_coords, texture_map)

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











def render_object_w_texture(shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, faces, 
    ka, kd, ks, n, lpos, lint, lamb, uvs, face_uv_indices, texture_map):
    #almost identical to the render_object function, but the color is gotten from the texture map

    normals = calculate_normals(verts, faces)
    #transpose faces, colors matrix so that it is compatible with the functions from the previous assignment
    faces = faces.T
    face_uv_indices = face_uv_indices.T
    

    image = np.ones((M,N,3))
    image = bg_color*image

    #calculate rotation matrix for camera coordinates
    R = lookat_funct(np.atleast_2d(eye).T, np.atleast_2d(up).T, np.atleast_2d(lookat).T)[0]
    #project points to camera plane (in 2xN output)
    projected_verts, depths = perspective_project(verts, focal, R, np.atleast_2d(eye).T)
    #rasterize them
    raster_verts = rasterize(projected_verts, W, H, N, M)
    raster_verts_transp = raster_verts.T
    #calculate depth of every face
    Depth_of_Faces = Find_Depth(faces, depths)
    #Sorting the faces from biggest to smallest depth:
    depth_indexes = np.argsort(Depth_of_Faces,axis=0)[::-1]
    faces_sorted = faces[depth_indexes]
    faces_uv_sorted = face_uv_indices[depth_indexes]
    #sorting depths:
    Depth_of_Faces_sorted = Depth_of_Faces[depth_indexes]
    
    #total number of faces
    F = len(faces_sorted)

    for i in range (F):
        #accesing every face with order form farthest to closest

        #don't shade faces with negative depth (behind the camera):
        if (Depth_of_Faces_sorted[i]<=0):
            continue
        
        #vert variable contains the index of the coresponding vertex to the verts,vert_colors arrays
        vert1 = faces_sorted[i][0] 
        vert2 = faces_sorted[i][1]
        vert3 = faces_sorted[i][2]

        #coordinates of the vertices
        triangle_vertices = np.array([raster_verts_transp[vert1], raster_verts_transp[vert2], raster_verts_transp[vert3]] )
        #invert vertices from bottom to top -> top to botton, to shade correctly 
        triangle_vertices[:,1] = np.array([H,H,H]) - triangle_vertices[:,1]
        #uvs of the vertices
        uv_coords = uvs[:,faces_uv_sorted[i,:]].T

        #normals of the vertices
        triangle_normals = np.concatenate((np.atleast_2d(normals[:,vert1]),np.atleast_2d(normals[:,vert2]),np.atleast_2d(normals[:,vert3])),axis=0).T
        #bcoords:
        center_of_mass = (verts[:,vert1]+verts[:,vert2]+verts[:,vert3])/3

        #shade
        if shader == "gouraud":
            triangle_colors = np.array([bilerp(u, texture_map) for u in uv_coords])
            shade_gouraud(triangle_vertices, triangle_normals, triangle_colors, center_of_mass,
                eye, ka,kd,ks,n, lpos, lint, lamb, image)
        elif shader == "phong":
            shade_phong_w_texture(triangle_vertices, triangle_normals, center_of_mass, eye, ka,kd,ks,n,
            lpos, lint, lamb, image, uv_coords, texture_map)
        else:
            raise Exception ("Non valid arguement for shader")

        

        
            

    return image