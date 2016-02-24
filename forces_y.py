# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 12:08:03 2016

@author: Marc CB
"""

import numpy as np
import matplotlib.pyplot as plt
import main as mn
#import structuralAnalysis as sa

# input data
hf = 1.8
R = 2.0
ts = 0.003
tf = 0.02
hst = 0.015
wst = 0.02
tst = 0.0012
L = 30.
Lf1 = 4.0
Lf2 = 12.5
Lf3 = 5.2
W = 65000.0
Sx = 170000.0
dtailz = 2.8
dtaily = 5.0
dlgy = 1.8
q = (3*W*9.81)/30.

forces = mn.reactionForces(Lf1, Lf2, Lf3, L, R, W, Sx, dtailz, dtaily, dlgy)
Fy1 = forces[0][1]
Fy2 = forces[1][1] + forces[2][1]

# shear and moment diagrams due to forces in y:
def diagramsy():
    #input data
    Vy = []
    My = []
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
    Vy = np.append(Vy,vlocal)
    My = np.append(My,mlocal)
    
    int2 = np.arange(z1,z2,step)
    vlocal = -q*int2 + Fy2
    mlocal = -q*int2*int2/2. + Fy2*(int2-z1)
    Vy = np.append(Vy,vlocal)
    My = np.append(My,mlocal)
    
    int3 = np.arange(z2,30.000009,step)
    vlocal = -q*int3 + Fy2 + Fy1
    mlocal = -q*int3*int3/2. + Fy2*(int3-z1) + Fy1*(int3-z2)
    Vy = np.append(Vy,vlocal)
    My = np.append(My,mlocal)
    
    # finding the max values and their location on the z axis:
    Vymax = np.amax(abs(Vy))
    Vypos = (np.argmax(abs(Vy)))*step
    Mymax = np.amax(abs(My))
    Mypos = (np.argmax(abs(My)))*step
    
    print "Vymax =",Vymax,"N", "at z =",Vypos,"m"
    print "Mymax =",Mymax,"N*m", "at z =",Mypos,"m"
    
    # plotting the diagrams
    x = np.arange(0,z3,step)
    y1 = Vy
    y2 = My
    if __name__=="__main__":
        plt.plot(x,y1,label='shear')
        plt.plot(x,y2,label='moment')
        plt.legend()
        plt.show()
    
    # return output
    return Vy,My, Vymax, Vypos, Mymax, Mypos
  
if __name__=="__main__":
    diagramsy()   

    
