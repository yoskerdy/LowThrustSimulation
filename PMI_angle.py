# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 19:19:27 2021

@author: YoSke
"""

from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

#-----------------------Données------------------------------------------------
#Célérité dans le vide (m/s)
c = 299792458

#Positions des lasers/capteurs 1, 2 et 3 (m)
x1 = 0
y1 = 0
z1 = 0

x2 = 0
y2 = 0.1
z2 = 0

x3 = 0
y3 = (1/2)*0.1
z3 = (sqrt(3)/2)*0.1

#-----------------------Temps de réponse du laser------------------------------
t1 = 0.0000178014
t2 = 0.0000306043
t3 = 0.0000376025

#-----------------------Calculs------------------------------------------------
#Calcul des distances et positions points satellite cible
d1 = t1*c
d2 = t2*c
d3 = t3*c

x4 = x1+d1
y4 = y1
z4 = z1

x5 = x2+d2
y5 = y2
z5 = z2

x6 = x3+d3
y6 = y3
z6 = z3

#différence de distance entre les points 2D mesurés
diff2D = d2-d1

#-----------------------Affichage----------------------------------------------
"""
print("distance 1 : ",int(d1/1000),"km et ",1000*((d1/1000)-int(d1/1000)),"m")
print("distance 2 : ",int(d2/1000),"km et ",1000*((d2/1000)-int(d2/1000)),"m")
print("distance 3 : ",int(d3/1000),"km et ",1000*((d3/1000)-int(d3/1000)),"m")
"""

fig2 = plt.figure()
ax2 = fig2.add_subplot(projection='3d')

#PLOT POINTS
ax2.scatter(x1,y1,z1,c='b')
ax2.scatter(x2,y2,z2,c='b')
ax2.scatter(x3,y3,z3,c='b')

ax2.scatter(x4,y4,z4,c='r')
ax2.scatter(x5,y5,z5,c='r')
ax2.scatter(x6,y6,z6,c='r')

#PLOT LIGNES SATELLITE TIREUR
lx1 = np.linspace(0,0,100)
ly1 = np.linspace(0,y2,100)
lz1 = np.linspace(0,0,100)

lx2 = np.linspace(0,0,100)
ly2 = np.linspace(y2,y2/2,100)
lz2 = np.linspace(0,z3,100)

lx3 = np.linspace(0,0,100)
ly3 = np.linspace(y2/2,0,100)
lz3 = np.linspace(z3,0,100)

ax2.plot(lx1,ly1,lz1,c='b')
ax2.plot(lx2,ly2,lz2,c='b')
ax2.plot(lx3,ly3,lz3,c='b')

#PLOT LIGNES SATELLITE CIBLE
lx1 = np.linspace(x4,x5,100)
ly1 = np.linspace(y4,y5,100)
lz1 = np.linspace(z4,z5,100)

lx2 = np.linspace(x5,x6,100)
ly2 = np.linspace(y5,y6,100)
lz2 = np.linspace(z5,z6,100)

lx3 = np.linspace(x6,x4,100)
ly3 = np.linspace(y6,y4,100)
lz3 = np.linspace(z6,z4,100)

ax2.plot(lx1,ly1,lz1,c='r')
ax2.plot(lx2,ly2,lz2,c='r')
ax2.plot(lx3,ly3,lz3,c='r')

plt.show()