# -*- coding: utf-8 -*-
"""
Created on Thu May 19 13:32:14 2016

@author: gni
"""

import numpy as np
import matplotlib.pyplot as plt


def newton_sqrt(x, order):
    y0 = 1
    iterate_step = 0
    print "The %d steps: %f\n"%(iterate_step, y0)
    while 1:
        y1 = y0-(y0**order - x)/(order*y0**(order-1))
        iterate_step += 1
        print "The %d steps: %f\n"%(iterate_step, y1)
        if abs(y1 - y0) < 0.0001:
            break
        else:
            y0 = y1
