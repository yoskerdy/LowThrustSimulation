# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 01:11:27 2021

@author: Houssen Zbairi
"""

#%%------------------------Import packages & tools-----------------------------
from tletools import TLE
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.optimize import fsolve
from math import asin, atan, tan, cos, sin, pi, sqrt

#%%---------------Extracting orbital parameters from TLE-----------------------
tle_string = """
NSS-9
1 33749U 09008A   21309.77806091  .00000079  00000-0  00000-0 0  9992
2 33749   0.0228   1.3579 0002100 218.9799 288.0653  1.00271016 46643
"""
tle_lines = tle_string.strip().splitlines()
tle = TLE.from_lines(*tle_lines)
print(tle)

name = tle.name
i = tle.inc
e = tle.ecc
n = (tle.n*(2*pi))/24/60/60
#M0 = tle.M * pi/180
M0 = 0

#%%----------------------------Other variables---------------------------------
mu = 3.98600441*10**14
Rt = 6378.135*10**3

a = (mu/n**2)**(1/3)
b = sqrt(1-e**2)*a
p = a*(1-e**2)
c = e*a
rp = a*(1-e)
ra = a*(1+e)
tp = 0
targetAltitude = 30000*10**3+Rt
speed = 100
timediff = -30

a3 = a
b3 = b
p3 = p
c3 = c
rp3 = rp
ra3 = ra
e3 = e
n3 = n

tf_ra = ra
tf_rp = targetAltitude
tf_a = (a+tf_rp)/2
tf_e = (tf_ra-tf_rp)/(tf_ra+tf_rp)
tf_b = sqrt(1-tf_e**2)*tf_a
tf_p = tf_a*(1-tf_e**2)
tf_n = sqrt(mu/tf_a**3)
t_compense = 0

"""
tg_ra = targetAltitude
tg_rp = targetAltitude
tg_a = targetAltitude
tg_e = 0
tg_b = targetAltitude
tg_p = targetAltitude
"""

J = 0
H = 0
Min = 0

distance = 0

#%%-----------------What we want to draw on the animation----------------------
drawLaserSatellite = True
drawExcentricCircle = False
drawMeanAnomaly = False
drawEarth = True
drawFixedPoints = True
drawTargetOrbit = True

fig, ax = plt.subplots()
ax.axis([-1.2*a,1.2*a,-1.2*a,1.2*a])
ax.set_aspect("equal")
fig.suptitle('Trajectoire du satellite '+name)

if drawExcentricCircle == True:
    circle = plt.Circle((0,0),a,fill=False)
    ax.add_patch(circle)

if drawMeanAnomaly == True:
    point2, = ax.plot(0,1, marker="o",c='orange')

if drawEarth == True:
    earth = plt.Circle((c,0),Rt,fill='b')
    ax.add_patch(earth)
    
if drawTargetOrbit == True:
    targetOrbit = plt.Circle((c,0),targetAltitude,fill=False)
    ax.add_patch(targetOrbit)
    
#Target satellite
point1, = ax.plot(0,1, marker="o",c='black')

#Laser satellite
if drawLaserSatellite == True:
    point3, = ax.plot(0,1, marker="s",c='red',markerfacecolor=None)

#Fixed points (center of excentric circle and focuses)
if drawFixedPoints == True:
    plt.scatter(0,0,c='r')
    plt.scatter(c,0,c='m')
    plt.scatter(-c,0,c='m')

#%%------------------------Start of the Algorithm------------------------------
def ellipse(t):
    
    global a
    global b
    global p
    global e
    global rp
    global n
    
    t = speed*t+tp
    
    M = n*(t-tp) + M0
    M = M%(2*pi)
    
    M3 = n3*(t-timediff-tp) + M0
    M3 = M3%(2*pi)
    
    """
    J = int(t/60/60/24)
    H = (int(t/60/60) - J ) %24
    Min = int(t/60) %60
    print("time +")
    print(J,'jours')
    print(H,'heures')
    print(Min,'min\n')
    """
    #print('Time (s) :',t)
    
    fct = lambda x: x-e*sin(x)-M
    fct3 = lambda x: x-e3*sin(x)-M3
    
    if t == 43200:
        a = tf_a
        b = tf_b
        p = tf_p
        e = tf_e
        rp = tf_rp
        n = tf_n
    
    """
    if t  == 86400:
        a = tg_a
        b = tg_b
        p = tg_p
        e = tg_e
        rp = tg_rp
    """
        
    E = fsolve(fct,M)[0]
    E3 = fsolve(fct3,M3)[0]
    
    nu = 2*atan( sqrt((1+e)/(1-e))*tan(E/2) )
    nu3 = 2*atan( sqrt((1+e3)/(1-e3))*tan(E3/2) )
    
    r =  a*(1-e*cos(E))
    r2 = a
    r3 = a3*(1-e3*cos(E3))
    
    x1 = r*cos(nu)+c
    y1 = r*sin(nu)
    x2 = r2*cos(M)
    y2 = r2*sin(M)
    x3 = r3*cos(nu3)+c
    y3 = r3*sin(nu3)
    
    distance = sqrt( (x1-x3)**2 + (y1-y3)**2 )
    print('distance (km) :',distance/1000)
    
    return np.array([x1, y1, x2, y2, x3, y3])
    

def update(t):
    
    x1,y1,x2,y2,x3,y3 = ellipse(t)
    
    point1.set_data([x1],[y1])
    
    if drawLaserSatellite == True and drawMeanAnomaly == True:
        point2.set_data([x2],[y2])
        point3.set_data([x3],[y3])
        return point1, point2, point3
    elif drawLaserSatellite == True and drawMeanAnomaly == False:
        point3.set_data([x3],[y3])
        return point1, point3
    elif drawLaserSatellite == False and drawMeanAnomaly == True:
        point2.set_data([x2],[y2])
        return point1, point2
    elif drawLaserSatellite == False and drawMeanAnomaly == False:
        return point1,

#%%-------------------Animation function and display---------------------------
#For real time diplay :
#ani = FuncAnimation(fig, update, interval=1000, blit=True, repeat=True)

#For accelerated simulation
ani = FuncAnimation(fig, update, interval=10, blit=True, repeat=True)
