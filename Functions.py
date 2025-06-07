import numpy as np
from Additional_Functions import Find_Depth, triangle_clipping


def world2view(pts:np.ndarray, R:np.ndarray, c0:np.ndarray) -> np.ndarray:
    # Implements a world-to-view transform, i.e. transforms the specified
    # points to the coordinate frame of a camera. The camera coordinate frame
    # is specified rotation (w.r.t. the world frame) and its point of reference
    # (w.r.t. to the world frame)
    #assuming pts is 3xN and c0 is vertical (3x1)

    R_tranp = R.transpose()
    mRTd = (-1)*np.dot(R_tranp,c0)
    tranformation_mat_top = np.concatenate((R_tranp, mRTd), axis=1)
    tranformation_mat = np.concatenate((tranformation_mat_top,[[0,0,0,1]]),axis=0)

    N=len(pts[0])
    #convert pts to homogenous coordinates
    N_ones = np.ones(N)
    pts_hom = np.append(pts,[N_ones],axis=0)
    #transform points
    points_transf = np.dot(tranformation_mat,pts_hom)
    #return the 3 dimensions of the transformed points
    return points_transf[0:3]






def lookat(eye:np.ndarray, up:np.ndarray, target:np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    # Calculate the camera's view matrix (i.e., its coordinate frame transformation specified
    # by a rotation matrix R, and a translation vector t).
    # :return a tuple containing the rotation matrix R (3 x 3) and a translation vector
    # t (3x1)
    #assuming eye,up,target are vertical (3x1)

    #vector representic (target-eye) i.e. from eye to target
    TargMinEye = target - eye
    #calculate its norm
    TargMinEyeNorm = np.linalg.norm(TargMinEye, axis=0)
    #zc camera unit vector is the above with norm 1:
    zc = TargMinEye/TargMinEyeNorm

    #calculate yc camera unit vector from up and zc
    vector_parallel_to_yc = up - (np.dot(up.T,zc))*zc
    vector_parallel_to_yc_norm = np.linalg.norm(vector_parallel_to_yc, axis=0)
    yc = vector_parallel_to_yc/vector_parallel_to_yc_norm

    #calculate xc camera unit vector as cross product of yc and zc
    #I use cross(zc,yc) to calculate -xc so that x will show from left to right
    xc = np.cross(zc.T,yc.T).T

    #generate R rotation matrix from xc,yc,zc
    R = np.concatenate((xc,yc,zc), axis=1)

    #return tuple containing R and translation vector=eye
    return (R,eye)





def perspective_project(pts:np.ndarray, focal:float, R:np.ndarray, t:np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    # Project the specified 3d points pts on the image plane, according to a pinhole
    # perspective projection model    

    #assuming pts is 3xN, R is 3x3, t is 3x1

    #first convert points from WCS to camera coordinates
    points_camera = world2view(pts,R,t)

    N = len(pts[0])
    #create 2xN array that will contain the coordinates of the projected points
    proj_pts_coord = np.empty((2,N))
    #create 1xN array that will contain the depth of every point
    depths = np.empty((N))

    for index in range (0,N):
        #index indexes every point(vertical) in points_camera

        #apply projection with equasion xq=xp*focal/zp , same for y
        #doesn't flip image, doesn't clip, still projects points behind the camera flipped
        zp = points_camera[2][index]
        proj_pts_coord[0][index] = points_camera[0][index]*focal/zp
        proj_pts_coord[1][index] = points_camera[1][index]*focal/zp

        depths[index] = zp

    #return both projected points and their depths as they will be needed in the render
    return (proj_pts_coord, depths)





def rasterize(pts_2d:np.ndarray, plane_w:int, plane_h:int, res_w:int, res_h:int) -> np.ndarray:
    # Rasterize the incoming 2d points from the camera plane to image pixel coordinates
    #assuming pts_2d is 2xN

    #pts_2d contains points in 2d coordinates according to the camera's coordinate system.
    #They will be rasterized to pixels (res_h x res_w) in a plane (plane_h x plane_w)
    #which the axis of the camera intersects in the center.
    
    #pixel lengths
    pixel_len_h = plane_h/res_h
    pixel_len_w = plane_w/res_w

    N = len(pts_2d[0])
    #create empty array that will contain the points after rasterization
    rasterized_pts = np.empty((2,N),dtype='int')

    for index in range (0,N):
        #index indexes every point(vertical) in pts_2d

        #add height/2 to y and width/2 to x so that (0,0) is the bottom left point
        #and perform integer division to find pixel number
        rasterized_pts[0][index] = (pts_2d[0][index]+plane_w/2)//pixel_len_w
        rasterized_pts[1][index] = (pts_2d[1][index]+plane_h/2)//pixel_len_h

    return rasterized_pts






def render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target) -> np.ndarray:
    #assuming v_pos is 3xN, v_clr is Nx3
    #assuming t_pos_idx is Fx3
    #assume every point is inside the canvas    (change later with clipping) <<<----

    image = np.ones((res_h,res_w,3))  #creates white canvas



    #calculate rotation matrix for camera coordinates
    R = lookat(eye,up,target)[0]
    #project points to camera plane
    (projected_points, depths) = perspective_project(v_pos,focal,R,eye)
    #rasterize them
    raster_points = rasterize(projected_points,plane_w,plane_h,res_w,res_h)
    raster_points_transposed = raster_points.T
    #raster_points is 2xN array with x,y pixel coordinates counting from bottom left
    # (contains every point, even those outside the plane, or behind the camera
    #with depth<0) 

    #calculate depth of every face 
    Depth_of_Faces = Find_Depth(t_pos_idx,depths)

  
    #Sorting the faces from biggest to smallest depth:
    depth_indexes = np.argsort(Depth_of_Faces,axis=0)[::-1]
    faces_sorted = t_pos_idx[depth_indexes]
    #sorting depths:
    Depth_of_Faces_sorted = Depth_of_Faces[depth_indexes]
    
    #total number of faces
    F = len(faces_sorted)

    for i in range (0,F):
        #accesing every face with order form farthest to closest

        #don't shade faces with negative depth (behind the camera):
        if (Depth_of_Faces_sorted[i]<=0):
            continue

        #vert variable contains the index of the coresponding vertex to the v_pos,v_clr arrays
        vert1 = faces_sorted[i][0] 
        vert2 = faces_sorted[i][1]
        vert3 = faces_sorted[i][2]

        #coordinates of the vertices
        triangle_vertices = [raster_points_transposed[vert1].tolist(), raster_points_transposed[vert2].tolist(), raster_points_transposed[vert3].tolist()] 
        #colors of the vertices
        triangle_vcolors = [v_clr[vert1].tolist(), v_clr[vert2].tolist(), v_clr[vert3].tolist()]  
        #shading
        triangle_clipping(image,triangle_vertices,triangle_vcolors,res_h,res_w)
   
    return image