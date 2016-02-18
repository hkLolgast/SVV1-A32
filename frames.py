# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:52:45 2016

@author: Marc CB
"""
import numpy as np
import scipy.integrate as integrate

# input data:
R = 2.0
ts = 0.003
Fx1 = 1.
Fx2 = 1.
Fy1 = 1.
Fy2 = 1.
A = np.pi*R*R

Ixx = np.pi*R*R*R*ts
Iyy = Ixx
Ixy = 0.


fx = lambda x: R*np.cos(x)
fy = lambda y: R*np.sin(y)

part1 = - Fx1/Ixx*ts*integrate.quad(fx,0,2*np.pi)
part2 = - Fy1/Iyy*ts*integrate.quad(fy,0,2*np.pi)

qb =  part1 + part2
q0 = Fx1*R/2*A
qtot = qb - q0


    