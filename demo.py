import numpy as np
from Render import render_object
import matplotlib.pyplot as plt

data = np.load("h3.npy", allow_pickle=True)
data_dict = data.item()

verts = data_dict["verts"]
v_colors = data_dict["vertex_colors"]
faces_id = data_dict["face_indices"]
cam_eye = data_dict["cam_eye"]
cam_up = data_dict["cam_up"]
cam_lookat = data_dict["cam_lookat"]
ka = data_dict["ka"]
kd = data_dict["kd"]
ks = data_dict["ks"]
n = data_dict["n"]
light_pos = data_dict["light_positions"]
light_int = data_dict["light_intensities"]
Ia = data_dict["Ia"]
M = data_dict["M"]
N = data_dict["N"]
W = data_dict["W"]
H = data_dict["H"]
bg_color = data_dict["bg_color"]
focal = data_dict["focal"]



#gouraud only ambient image (kd=ks=0)
img_g_amb = render_object("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, ka,0,0,n, light_pos, light_int, Ia)
#gouraud only diffuse image (ka=ks=0)
img_g_dif = render_object("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, 0,kd,0,n, light_pos, light_int, Ia)
#gouraud only specular image (kd=ks=0)
img_g_spec = render_object("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, 0,0,ks,n, light_pos, light_int, Ia)
#gauraud using all shadings image
img_g_all = render_object("gouraud", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, ka,kd,ks,n, light_pos, light_int, Ia)


#phing only ambient image (kd=ks=0)
img_p_amb = render_object("phong", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, ka,0,0,n, light_pos, light_int, Ia)
#phong only diffuse image (ka=ks=0)
img_p_dif = render_object("phong", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, 0,kd,0,n, light_pos, light_int, Ia)
#phong only specular image (kd=ks=0)
img_p_spec = render_object("phong", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, 0,0,ks, n, light_pos, light_int, Ia)
#phong using all shadings image
img_p_all = render_object("phong", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, ka,kd,ks,n, light_pos, light_int, Ia)

#gouraud shading graph
fig_g, axes_g = plt.subplots(2,2)
axes_g[0][0].imshow(img_g_amb)
axes_g[0][0].set_title("Gouraud Shading, only ambient")
axes_g[0][1].imshow(img_g_dif)
axes_g[0][1].set_title("Gouraud Shading, only diffuse")
axes_g[1][0].imshow(img_g_spec)
axes_g[1][0].set_title("Gouraud Shading, only specular")
axes_g[1][1].imshow(img_g_all)
axes_g[1][1].set_title("Gouraud Shading, all reflexions")
fig_g.tight_layout()
fig_g.savefig("Gouraud_shading_reflexion_modes")

#phong shading graph
fig_p, axes_p = plt.subplots(2,2)
axes_p[0][0].imshow(img_p_amb)
axes_p[0][0].set_title("Phong Shading, only ambient")
axes_p[0][1].imshow(img_p_dif)
axes_p[0][1].set_title("Phong Shading, only diffuse")
axes_p[1][0].imshow(img_p_spec)
axes_p[1][0].set_title("Phong Shading, only specular")
axes_p[1][1].imshow(img_p_all)
axes_p[1][1].set_title("Phong Shading, all reflexions")
fig_p.tight_layout()
fig_p.savefig("Phong_shading_reflexion_modes")

#different light sources
lpos_1 = [light_pos[0]]
lint_1 = [light_int[0]]
img_p_first_light = render_object("phong", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, ka,kd,ks,n, lpos_1, lint_1, Ia)

lpos_2 = [light_pos[1]]
lint_2 = [light_int[1]]
img_p_second_light = render_object("phong", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, ka,kd,ks,n, lpos_2, lint_2, Ia)

lpos_3 = [light_pos[2]]
lint_3 = [light_int[2]]
img_p_third_light = render_object("phong", focal, cam_eye, cam_lookat, cam_up, bg_color,
    M,N,H,W,verts,v_colors, faces_id, ka,kd,ks,n, lpos_3, lint_3, Ia)

#different light sources graph
fig_l, axes_l = plt.subplots(2,2)
axes_l[0][0].imshow(img_p_first_light)
axes_l[0][0].set_title("Phong Shading, all reflexions,\n first light source")
axes_l[0][1].imshow(img_p_second_light)
axes_l[0][1].set_title("Phong Shading, all reflexions,\n second light source")
axes_l[1][0].imshow(img_p_third_light)
axes_l[1][0].set_title("Phong Shading, all reflexions,\n third light source")
axes_l[1][1].imshow(img_p_all)
axes_l[1][1].set_title("Phong Shading, all reflexions,\n all light sources")
fig_l.tight_layout()
fig_l.savefig("Phong_Shading_different_light_sources")



plt.show()