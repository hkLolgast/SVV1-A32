# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 09:49:19 2016

@author: Marc CB
"""
import numpy as np

#input data:
hf = 1.8
R = 2.0
ts = 0.003
tf = 0.02
T = 344.0

def shearstressT():
    # geometrical parameters of the strucutre
    alpha = np.arccos((R-hf)/R)
    A2 = alpha*R*R - np.cos(alpha)*np.sin(alpha)*R*R
    A1 = np.pi*R*R - A2
    
    # lengths calculations
    s1 = 2*np.pi*R - 2*alpha*R
    s2 = 2*np.pi*R - s1
    s12 = 2*np.sin(alpha)*R
    
    # using equality of rates of twist and simplifying:
    term1 = s1/(A1*ts) + s12/(A1*tf) + s12/(A2*tf)
    term2 = s2/(A2*ts) + s12/(A2*tf) + s12/(A1*tf)
    
    # solving for q1 and q2
    a = np.array([[term1,-term2], [2*A1,2*A2]])
    b = np.array([0,T])
    x = np.linalg.solve(a, b)
    q1 = x[0]
    q2 = x[1]
    tau1 = q1/ts
    tau2 = q2/ts
    tau12 = (q1-q2)/tf
    return tau1, tau2, tau12

shearstressT()
    