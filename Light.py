import numpy as np

def light(point,normal,vcolor,cam_pos,ka,kd,ks,n,lpos,lint,lamb):


	#ambient light intensities for each color
	Ia = ka*lamb*vcolor
	#total illumination 
	Illumin = Ia

	for i in range (len(lpos)):
		#position and intensity of every light source
		light_position = lpos[i]
		light_intensity = lint[i]


		#calculate distance from point to light source
		point_light_difference = light_position - point
		#Vector from point to light
		L_vect = point_light_difference/np.linalg.norm(point_light_difference)
		#dot product of L,N 
		L_N_dot = np.dot(L_vect,normal)
		#diffuse intensity
		Id =  kd  * light_intensity * L_N_dot * vcolor
		Id = np.where(Id > 0, Id, 0)

		

		#calculate vector from camera to point
		cam_pt_diff = cam_pos - point
		V_vect = cam_pt_diff/np.linalg.norm(cam_pt_diff)
		#Reflection vector
		R = 2*np.dot(normal,L_vect)*normal - L_vect
		#R = R/np.linalg.norm(R)
		#dot product of R,V
		R_V_dot = np.dot(R, V_vect )
		#raise it to the nth power
		R_V_nth = R_V_dot**n
		#specular intensity
		Is = ks * light_intensity * R_V_nth * vcolor
		Is = np.where(Is > 0, Is, 0)


		#add them to total illumination
		Illumin = Illumin + Id + Is

	#clip illumination
	Illumin = np.clip(Illumin,0,1)
	return Illumin