# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 17:15:16 2016

@author: gni
"""


import numpy as np
import matplotlib.pyplot as plt


R=1
L=1
dt = 0.1
E=10

A = np.matrix([[1/R,-1/R,1],[-1/R, 1/R + dt/L,0],[1,0,0]])
x = np.matrix([[0],[0],[0]])
b = np.matrix([[0],[0],[E]])
x_coord = []
v_coord = []
i_coord = []
for i in np.arange(50):
    x_coord.append(i)
    v_coord.append(x.tolist()[1][0])
    i_coord.append(x.tolist()[2][0])
    x = A.I*b
    b[1] = -b[1]
   
plt.plot(x_coord, v_coord, 'r')
plt.plot(x_coord, i_coord, 'g')  