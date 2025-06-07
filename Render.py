import numpy as np
from Functions import perspective_project, rasterize
from Functions import lookat as lookat_funct
from Additional_Functions import Find_Depth
from Shading import shade_gouraud, shade_phong, calculate_normals

def render_object(shader, focal, eye, lookat, up, bg_color, M, N, H, W, verts, vert_colors, faces, ka, kd, ks, n, lpos, lint, lamb):
    
    normals = calculate_normals(verts, faces)

    #transpose faces, colors matrix so that it is compatible with the functions from the previous assignment
    faces = faces.T
    colors_transp = vert_colors.T

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
        #colors of the vertices
        triangle_vcolors = np.array([colors_transp[vert1], colors_transp[vert2], colors_transp[vert3]]  )
        #normals of the vertices
        triangle_normals = np.concatenate((np.atleast_2d(normals[:,vert1]),np.atleast_2d(normals[:,vert2]),np.atleast_2d(normals[:,vert3])),axis=0).T
        center_of_mass = (verts[:,vert1]+verts[:,vert2]+verts[:,vert3])/3

        '''    <<<<<<------change later
        for v in triangle_vertices:
            #don't shade faces with a vertex outside the camera plane
            if (v[0]<0 or v[0]>=W or v[1]<0 or v[1]>=H):
                continue'''
        
        #shade
        if shader=="gouraud":
            shade_gouraud(triangle_vertices, triangle_normals, triangle_vcolors, center_of_mass, eye, ka,kd,ks,n,
                lpos, lint, lamb, image)
        elif shader == "phong":
            shade_phong(triangle_vertices, triangle_normals, triangle_vcolors, center_of_mass, eye, ka,kd,ks,n,
                lpos, lint, lamb, image)
        else:
            raise Exception ("Non valid shader arguement.")
        


    return image

