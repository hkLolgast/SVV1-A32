# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 12:08:03 2016

@author: Marc CB
"""

import numpy as np
import matplotlib.pyplot as plt
#import structuralAnalysis as sa

# input data
L = 30.0
Lf1 = 4.0
Lf2 = 12.5
Lf3 = 5.2
W = 65000.
q = (3*W*9.81)/30.
Fy1 = 226856.
Fy2 = 1686094.

# shear and moment diagrams due to forces in y:
def diagramsy():
    #input data
    V = []
    M = []
    step = 0.1
    z0 = 0.
    z1 = L-Lf1-Lf2
    z2 = L-Lf1
    z3 = L + step
    int1, int2, int3 = 0.,0.,0.
    
    # working out the shear and moments in the three intervals
    int1 = np.arange(z0,z1,step)
    vlocal = -q*int1
    mlocal = -q*int1*int1/2.
    V = np.append(V,vlocal)
    M = np.append(M,mlocal)
    
    int2 = np.arange(z1,z2,step)
    vlocal = -q*int2 + Fy2
    mlocal = -q*int2*int2/2. + Fy2*(int2-z1)
    V = np.append(V,vlocal)
    M = np.append(M,mlocal)
    
    int3 = np.arange(z2,30.000009,step)
    vlocal = -q*int3 + Fy2 + Fy1
    mlocal = -q*int3*int3/2. + Fy2*(int3-z1) + Fy1*(int3-z2)
    V = np.append(V,vlocal)
    M = np.append(M,mlocal)
    
    # finding the max values and their location on the z axis:
    Vmax = np.amax(abs(V))
    Vpos = (np.argmax(abs(V)))/10.
    Mmax = np.amax(abs(M))
    Mpos = (np.argmax(abs(M)))/10.
    
    print "Vmax =",Vmax,"N", "at z =",Vpos,"m"
    print "Mmax =",Mmax,"N*m", "at z =",Mpos,"m"
    
    # plotting the diagrams
    x = np.arange(0,z3,step)
    y1 = V
    y2 = M
    plt.plot(x,y1)
    plt.plot(x,y2)
    plt.show()
    
    # return output
    return V,M, Vmax, Vpos, Mmax, Mpos
  
diagramsy()

    
