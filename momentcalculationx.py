# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 11:50:32 2016

@author: Gerjan
"""


import numpy as np
from numpy.linalg import solve
import matplotlib.pyplot as plt

Sx = 170000
Sxlgm = 391680
Mx = [0]*300

for i in range(1,300):

    moments = 0
    if i<135:
        Mx[i] = Sx*(i/10+2.8)

    if i>=135 and i<260:
        Mx[i] = Sx*(i/10+2.8) - Sxlgm*(i/10-13.5)

    if i>=260:
        Mx[i] = 0

        
plt.plot(Mx)
plt.show() 
