# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 14:22:48 2016

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
Fx1 = 221680.
Fx2 = -391680.
Sx = 1.7*(10**5)

# shear and moment diagrams due to forces in y:
def diagramsx():
    #input data
    Vx = []
    Mx = []
    step = 0.1
    z0 = 0.
    z1 = L-Lf1-Lf2
    z2 = L-Lf1
    z3 = L + step
    int1, int2, int3 = 0.,0.,0.
    
    # working out the shear and moments in the three intervals
    int1 = np.arange(z0,z1,step)
    vlocal = np.ones(len(int1))*Sx
    mlocal = Sx*(2.8+int1)
    Vx = np.append(Vx,vlocal)
    Mx = np.append(Mx,mlocal)
    
    int2 = np.arange(z1,z2,step)
    vlocal = np.ones(len(int2))*(Sx + Fx2)
    mlocal = Sx*(2.8+int2) + Fx2*(int2-z1)
    Vx = np.append(Vx,vlocal)
    Mx = np.append(Mx,mlocal)
    
    int3 = np.arange(z2,30.00005,step)
    vlocal = np.ones(len(int3))*(Sx + Fx2 + Fx1)
    mlocal = Sx*(2.8+int3) + Fx2*(int3-z1) + Fx1*(int3-z2)
    Vx = np.append(Vx,vlocal)
    Mx = np.append(Mx,mlocal)
    
    # finding the max values and their location on the z axis:
    Vxmax = np.amax(abs(Vx))
    Vxpos = (np.argmax(abs(Vx)))*step
    Mxmax = np.amax(abs(Mx))
    Mxpos = (np.argmax(abs(Mx)))*step
    
    print "Vxmax =",Vxmax,"N", "at z =",Vxpos,"m"
    print "Mxmax =",Mxmax,"N*m", "at z =",Mxpos,"m"
    
    # plotting the diagrams
    x = np.arange(0,z3,step)
    y1 = Vx
    y2 = Mx
    plt.plot(x,y1,label='shear')
    plt.plot(x,y2,label='moment')
    plt.legend()
    plt.show()
    
    # return output
    return Vx, Mx, Vxmax, Vxpos, Mxmax, Mxpos
  
diagramsx() 