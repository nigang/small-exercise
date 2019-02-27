# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 15:58:58 2016

@author: gni
"""

import numpy as np
import matplotlib.pyplot as plt


R=1
C=1
dt = 0.1
E=10
time = 8
steps = time/dt
# MNA stamping method
A = np.matrix([[1/R,-1/R,1],[-1/R, 1/R + C/dt,0],[1,0,0]])
x = np.matrix([[0],[0],[0]])
b = np.matrix([[0],[C/dt * x[1]],[E]])

x_coord = []
u1 = []
i_cur = []
u1_real = []
i_real = []
for i in np.arange(steps):    
    x = A.I*b
    b[1] = C/dt * x[1]
    x_coord.append(i+1)
    u1.append(x.tolist()[1][0])
    i_cur.append(x.tolist()[2][0])
    u1_real.append((1-np.exp(-(i+1)*dt/(R*C)))*E)
    i_real.append((np.exp(-(i+1)*dt/(R*C)))*-E)
plt.figure()
plt.text(50,60,"dfdd")
p1 = plt.subplot(211)
p2 = plt.subplot(212)
p1.plot(x_coord, u1, 'g^', label= "u1 calculated charging voltage")
p1.plot(x_coord, u1_real, 'g', label= "u1 authentic charging voltage")
p1.grid(True)
p1.legend()
p2.plot(x_coord, i_cur, 'b^', label= "calculated charging current")
p2.plot(x_coord, i_real, 'b', label= "authentic charging current")

p2.legend()
#plt.plot(x_coord, i, 'g')  

# NA stamping method
#plt.figure(2)
#Gs = 10e6 #huge conductance
#A = np.matrix([[1/R+Gs,-1/R],[-1/R, 1/R + C/dt]])
#x = np.matrix([[0],[0]])
#b = np.matrix([[E*Gs],C/dt*x[1]])
#x_coord = []
#v_coord = []
#for i in np.arange(50):
#    x_coord.append(i)
#    v_coord.append(x.tolist()[1][0])
#    x = A.I*b
#    b[1] = C/dt * x[1]
#   
#plt.plot(x_coord, v_coord, 'r')
#plt.plot(x_coord, i, 'g')  