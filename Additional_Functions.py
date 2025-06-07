import numpy as np
from vector_interpolation import vector_interp
from Gouraud_shading import g_shading


'''function that finds the depth of every face in the Faces array based on the center of mass of 
its points.'''
def Find_Depth(Faces, Depth):
    #create empty numpy array
    #assuming Faces is Kx3
    Depth_Of_Faces = np.empty((len(Faces)))   
    for i in range (0,len(Faces)):
        #calculate the depth of each face
        Depth_Of_Faces[i] = (Depth[Faces[i][0]]+Depth[Faces[i][1]]+Depth[Faces[i][2]])/3 
    return Depth_Of_Faces



def is_point_outside_plane(x,y,H,W):
    if (x<0 or x>=W or y<0 or y>=H):
        return True
    else:
        return False





def find_segment_intersection(in_point, out_point, H, W):
    #find points where the plane HxW intersects the line segment in_point-out_point

    x1, y1 = in_point
    x2, y2 = out_point
    
    # Calculate the slope (m) and y-intercept (b) of the line segment
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    
        
    # Function to check if a point is on the line segment
    def is_on_segment(x, y):
        return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)
    
    # Check intersection with top boundary
    y_bottom = 0
    if (m):
        x_bottom = (y_bottom - b) / m
        if 0 <= x_bottom < W and is_on_segment(x_bottom, y_bottom):
            return [int(x_bottom),int(y_bottom)]
    
    # Check intersection with bottom boundary
    y_top = H - 1
    if(m):
        x_top = (y_top - b) / m
        if 0 <= x_top < W and is_on_segment(x_top, y_top):
            return [int(x_top),int(y_top)]
    
    # Check intersection with left boundary
    x_left = 0
    y_left = m * x_left + b
    if 0 <= y_left < H and is_on_segment(x_left, y_left):
        return [int(x_left),int(y_left)]
    
    # Check intersection with right boundary
    x_right = W - 1
    y_right = m * x_right + b
    if 0 <= y_right < H and is_on_segment(x_right, y_right):
        return [int(x_right),int(y_right)]




def find_corner_point (p1,p2,H,W):
    #finds the corner point of the plane HxW where the lines of p1,p2 intersect
    #assuming p1 and p2 are on attached edges 
    #corner point will have the value of x that is either 0 or W-1, and y 0 or H-1
    corner = [-1,-1]
    if (p1[0]==0 or p2[0]==0):
        corner[0]=0
    elif (p1[0]==W-1 or p2[0]==W-1):
        corner[0]=W-1
    
    if (p1[1]==0 or p2[1]==0):
        corner[1]=0
    elif(p1[1]==H-1 or p2[1]==H-1):
        corner[1]=H-1
    
    if (corner[0]==-1 or corner[1]==-1):
        raise Exception("p1 or p2 are not edge points")




def triangle_clipping(img, vertices, vcolors,H,W):
    #shades the triangle, if it's outside, it clips it and then shades it
    #vertices is 3x2 where a point is horizontal, vcolors 3x3 where a color is horizontal
    


    verts_inside = vertices.copy()
    verts_outside = []
    cols_inside = vcolors.copy()
    cols_outside = []
    for i in range (0,3):
        if ( is_point_outside_plane(vertices[i][0], vertices[i][1], H,W )):
            #point ver is outside the plane
            verts_outside.append(vertices[i])
            cols_outside.append(vcolors[i])
            verts_inside.remove(vertices[i])
            cols_inside.remove(vcolors[i])
    #verts inside and outside contain the inside and outside points
    #cols inside and outside contain the inside and outside colors

    if (len(verts_outside)==0):
        #all the points are inside the plane, continue with shading
        g_shading(img,vertices,vcolors)

    elif (len(verts_outside)==1):
        #perform clipping -------------

        #one outside point

        #out and in points in the format [x,y]
        out = verts_outside[0]
        in_1 = verts_inside[0]
        in_2 = verts_inside[1]
        #their colors
        out_col = cols_outside[0]
        in_1_col = cols_inside[0]
        in_2_col = cols_inside[1]

        
        #Find intersection points p1,p2
        p1 = find_segment_intersection(in_1,out,H,W)
        p2 = find_segment_intersection(in_2,out,H,W)

        #Find colors of p1,p2
        if (out[0]-in_1[0]!=0):
            #x coord
            p1_col = vector_interp(in_1, out, in_1_col, out_col, p1[0],1)
        elif (out[1]-in_1[1]!=0):
            #y coord
            p1_col = vector_interp(in_1, out, in_1_col, out_col, p1[1],2)
        else:
            raise Exception("Division by zero at vector_interp")

        if (out[0]-in_2[0]!=0):
            #x coord
            p2_col = vector_interp(in_2, out, in_2_col, out_col, p2[0],1)
        elif (out[1]-in_2[1]!=0):
            #y coord
            p2_col = vector_interp(in_2, out, in_2_col, out_col, p2[1],2)
        else:
            raise Exception("Division by zero at vector_interp")




        if (p1[0]==p2[0] or p1[1]==p2[1]):
            #p1 and p2 are on the same edge
            #shade the two triangles that those points create (p1,p2,i1), (i1,i2,p2) where i=in
            triangle1_pts = [p1,p2,in_1]
            triangle1_cols = [p1_col,p2_col,in_1_col]
            g_shading(img,triangle1_pts,triangle1_cols)
            triangle2_pts = [in_1,in_2,p2]
            triangle2_cols = [in_1_col,in_2_col,p2_col]
            g_shading(img,triangle2_pts,triangle2_cols)
        else:   
            '''shouldnt run'''
            #p1 and p2 are on different edges but attached, so there are 3 triangles in the plane:
            #(c,p1,p2), (p1,p2,i1), (p2,i1,i2) where c=corner point

            #find corner point
            corner_pt= find_corner_point(p1,p2,H,W)

            #find triangle coordinates and colors
            triangle1_pts = [corner_pt, p1, p2]
            triangle1_cols = []

            #shade 
    

    elif (len(verts_outside)==2):
        #perform clipping, two outside points

        #out and in points in the format [x,y]
        out_1=verts_outside[0]
        out_2=verts_outside[1]
        in_0 = verts_inside[0]
        #their colors
        out_1_col = cols_outside[0]
        out_2_col = cols_outside[1]
        in_col = cols_inside[0]


        #Find intersection points p1,p2
        p1 = find_segment_intersection(in_0,out_1,H,W)
        p2 = find_segment_intersection(in_0,out_2,H,W)


        #Find colors of p1,p2
        if (out_1[0]-in_0[0]!=0):
            #x coord
            p1_col = vector_interp(in_0, out_1, in_col, out_1_col, p1[0],1)
        elif (out_1[1]-in_0[1]!=0):
            #y coord
            p1_col = vector_interp(in_0, out_1, in_col, out_1_col, p1[1],2)
        else:
            raise Exception("Division by zero at vector_interp")

        if (out_2[0]-in_0[0]!=0):
            #x coord
            p2_col = vector_interp(in_0, out_2, in_col, out_2_col, p2[0],1)
        elif (out_2[1]-in_0[1]!=0):
            #y coord
            p2_col = vector_interp(in_0, out_2, in_col, out_2_col, p2[1],2)
        else:
            raise Exception("Division by zero at vector_interp")

        if (p1[0]==p2[0] or p1[1]==p2[1]):
            #p1 and p2 are on the same edge
            #shade the one triangle that is created: (i,p1,p2)

            triangle_pts = [in_0,p1,p2]
            triangle_cols = [in_col,p1_col,p2_col]
            g_shading(img,triangle_pts,triangle_cols)
        else: 
            '''shoudnt run'''
            #p1 and p2 are on different edges
            #find corner points and shade the triangles that are created

            print("kill error")


    else:
        #the whole triangle is outside
        return