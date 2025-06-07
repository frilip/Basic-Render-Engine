import numpy as np
import matplotlib.pyplot as plt
from Texture import render_object_w_texture

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
uvs = data_dict["uvs"]
face_uv_indices = data_dict["face_uv_indices"]


texture_map = plt.imread("cat_diff.png")

#image with phong shading and all lights
img_phong_all = render_object_w_texture(shader="phong",focal=focal, eye=cam_eye, lookat=cam_lookat, up=cam_up,
    bg_color=bg_color, M=M, N=N, H=H, W=W, verts=verts, faces=faces_id,
    ka=ka, kd=kd, ks=ks, n=n, lpos=light_pos, lint=light_int, lamb=Ia, uvs=uvs, 
    face_uv_indices=face_uv_indices, texture_map=texture_map)


#image with gouraud shading and only the first light
img_gou = render_object_w_texture(shader="gouraud",focal=focal, eye=cam_eye, lookat=cam_lookat, up=cam_up,
    bg_color=bg_color, M=M, N=N, H=H, W=W, verts=verts, faces=faces_id,
    ka=ka, kd=kd, ks=ks, n=n, lpos=light_pos, lint=light_int, lamb=Ia, uvs=uvs, 
    face_uv_indices=face_uv_indices, texture_map=texture_map)

#image with phong shading and only the first light
img_ph = render_object_w_texture(shader="phong",focal=focal, eye=cam_eye, lookat=cam_lookat, up=cam_up,
    bg_color=bg_color, M=M, N=N, H=H, W=W, verts=verts, faces=faces_id,
    ka=ka, kd=kd, ks=ks, n=n, lpos=light_pos, lint=light_int, lamb=Ia, uvs=uvs, 
    face_uv_indices=face_uv_indices, texture_map=texture_map)

plt.figure(1)
plt.imshow(img_phong_all)
plt.tight_layout()
plt.savefig("Texture_phong")

fig,axs = plt.subplots(1,2)
axs[0].imshow(img_gou)
axs[1].imshow(img_ph)
fig.savefig("Gou_vs_phong_texture")

plt.show()