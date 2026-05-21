import math
from PIL import Image
import numpy as np

#Sakralprodukt
def dot(v1, v2): 
    res = 0
    for i in range(len(v1)):
        res+= v1[i] * v2[i]
    return res

def cross(v1, v2):
    res= []
    res.append(v1[1]*v2[2] - v1[2]*v2[1])
    res.append(v1[2]*v2[0] - v1[0]*v2[2])
    res.append(v1[0]*v2[1] - v1[1]*v2[0])
    return res



height = 1000
width = 1000

sphere_center = [0,0,5] #zentrum von Kugel
sphere_radius = 1 #radius von Kugel

img = Image.new('RGB', (width, height), 'black') #schwarzes bild kreieren

pixel = img.load()

for y in range (height):
    v = 1 - y/height * 2
    for x in range (width):
        u = x/width * 2 + - 1
        lst = [u,v,1]
        D_vectr = np.array(lst)
        length_D = math.sqrt(sum(k**2 for k in D_vectr))

        norm_x = u / length_D
        norm_y = v / length_D
        norm_z = 1.0 / length_D


        P = [0.0, 0.0, 0.0]

        V = [norm_x, norm_y, norm_z]

        r_vec = []

        dt = 0.005
        max_steps = 10/dt
        step = 0
        hit = False # Ein Schalter, der sich merkt, ob wir getroffen haben

        while hit == False and step < max_steps:
            r_vec = []
            r_vec.append(P[0] - sphere_center[0])
            r_vec.append(P[1] - sphere_center[1])
            r_vec.append(P[2] - sphere_center[2])
            #d = math.sqrt((P[0] -sphere_center[0])**2 + (P[1] -sphere_center[1])**2 + (P[2] -sphere_center[2])**2) #Distanz von Position zu Kugelmitte
            r = math.sqrt(dot(r_vec, r_vec)) #Distanz von Position zur Kugelmitte

            if r < sphere_radius:
                hit = True
            
            else:
                h_vec = cross(r_vec, V)
                h2 = dot(h_vec, h_vec) #länge im Quadrat vom Vektor
                factor = -1.5 * sphere_radius * h2 / r**5
                a = []
                for i in range(3):
                    a.append(r_vec[i] * factor)
                
                for i in range (3):
                    V[i] += a[i] * dt
                
                V_laenge = math.sqrt(V[0]**2 + V[1]**2 + V[2]**2)

                for i in range (3):
                    V[i] = V[i] / V_laenge

                for i in range(3):
                    P[i] += V[i] * dt
                #P[1] += V[1] * dt
                #P[2] += V[2] * dt

            step +=1
        
        if hit == True:
            red_num = 0
            green_num = 0
            blue_num = 0

        else:
            phi = math.atan2(V[0], V[2])
            theta = math.acos(V[1])
            check_x = int(phi * (16.0 / math.pi))
            check_y = int(theta * (8.0 / math.pi))
            if (check_x + check_y) % 2 == 0:
                red_num = 255
                green_num = 255
                blue_num = 255

            else: 
                red_num = 60
                green_num = 60
                blue_num = 60

        #D_norm = [norm_x, norm_y, norm_z]
        #L = [-sphere_center[0], -sphere_center[1], -sphere_center[2]]
        #b = 2.0 * dot(D_norm, L)
        #c = dot(L, L) - (sphere_radius * sphere_radius)
        #discriminant = (b * b) - (4.0 * 1.0 * c)

        #if discriminant >= 0:
        #    red_num = 0
        #    green_num = 0
        #    blue_num = 0
        
        #else:
        #    red_num = int((norm_x + 1)* 0.5 * 255)
        #    green_num = int((norm_y + 1)* 0.5 * 255)
        #    blue_num = int((norm_z + 1)* 0.5 * 255)

        pixel[x, y] = (red_num, green_num, blue_num)

img.save('mein_erstes_bild.png')
