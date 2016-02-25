# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 09:49:19 2016

@author: Marc CB
"""

import matplotlib.pyplot as plt
import numpy as np
import main as mn

####input data:

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
T = Sx*(dlgy+dtaily)

def shearstressT():
    
    #### geom calculations
    Iyy = mn.realMomentOfInertia('y', R, ts, hf, tf, hst, wst, tst)
    Sfic = 20.
    d = 0.2
    step = 100.
    a = np.sqrt(R*R-d*d)
    alpha = np.arcsin(0.2/R)   
    
    ###################### SHEAR CENTER CALCULATION FOR REAL STRUCTURE
    
    ########## CELL 1
    
    int12 = np.linspace(0,2*a,step)
    qb12 = -(Sfic/Iyy)*tf*0.5*int12*int12
    
    int21 = np.linspace(0,np.pi+2*alpha,step)
    qb21 = qb12[-1] - (Sfic/Iyy)*ts*R*R*np.sin(int21)
    
    
    # qs0 = -int(qb*ds)/int(ds)
    term1 = (Sfic/Iyy)*(tf/2.)*((2*a)*(2*a)*(2*a)/3.) - qb12[-1]*R*(np.pi+2*alpha)
    term2 = (Sfic/Iyy)*ts*R*R*R*0.5*(-np.cos(3*np.pi+2*alpha)+np.cos(np.pi))
    qs0 = (term1 + term2)/(2*a + (np.pi+2*alpha)*R)
    
    q112 = qb12 + qs0
    q121 = qb21 + qs0
    
    ############ CELL 2
    
    int12 = np.linspace(0,np.pi-2*alpha,step)
    qb12 = - (Sfic/Iyy)*ts*R*R*np.sin(int12)
    
    int21 = np.linspace(0,2*a,step)
    qb21 = qb12[-1] -(Sfic/Iyy)*tf*0.5*int12*int12
    
    # qs0 = -int(qb*ds)/int(ds)
    term1 = -(Sfic/Iyy)*(ts*R*R*R*0.5)*(np.cos(-np.pi+4*alpha)-np.cos(np.pi))
    term2 = -qb12[-1]*2*a - (Sfic/Iyy)*tf*0.5*((2*a)*(2*a)*(2*a)/3.)
    qs0 = (term1 + term2)/(2*a + (np.pi-2*alpha)*R)
    
    q212 = qb12 + qs0
    q221 = qb21 + qs0
    
    ########### STRUCTURE
    q1 = q112
    q2 = q212
    qfl = q121 - q221[::-1]
    
    ########### MOMENT EQUIVALENCE AROUND CENTER
    sc_y = (R*sum(q1) + R*sum(q2) + d*sum(qfl))/Sfic
    #print sc_y
    
    ##############################################################
    
    
    
    ############ TORQUE CALCULATION AROUND Z
    
    '''
    T = Sx*(dlgy+dtailz-dy) torque at z=0 around shear center
    T2 = FyL*dx - FyR*dx - Fx2*dy
    T1 = Fx1*dy
    T - T1 - T2 = 0
    '''
    
    forces = mn.reactionForces(Lf1, Lf2, Lf3, L, R, W, Sx, dtailz, dtaily, dlgy)
    
    Fx1 = forces[0][0]
    Fx2 = forces[1][0] + forces[2][0]
    FyR = forces[2][1]
    FyL = forces[1][1]
    
    a = np.array([[1,1,Sx],[0,1,-Fx2],[1,0,-Fx1]])
    b = np.array([Sx*(dlgy+dtailz),  FyL*Lf3*0.5 - FyR*Lf3*0.5,0])
    x = np.linalg.solve(a, b)
    
    T1 = x[0]
    T2 = x[1]
    dy = x[2]
    
    T = Sx*(dlgy+dtailz-dy)
    
    step = 0.01
    z = np.arange(0,30+step,step)
    y1 = np.ones((13.5+step)/step)*(T)
    y2 = np.ones(12.5/step)*(T-T2)
    y3 = np.ones(4.0/step)*(T-T2-T1)
    y = np.append(y1,y2)
    y = np.append(y,y3)
    if __name__=="__main__":
        plt.plot(z,y)
        plt.show()
    
    shearT = []
    torques = (T, T-T2, T-T2-T1)
    for i in range(3):
        T = Sx*(dlgy+dtailz-dy)
        if i==1:
            T = T - T2
        if i==2:
            T = T - T2 - T1
            
        # geometrical parameters of the strucutre
        alpha = np.arccos((R-hf)/R)
        A2 = alpha*R*R - np.cos(alpha)*np.sin(alpha)*R*R
        A1 = np.pi*R*R - A2
        #print 'A1',A1,'A2',A2
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
        shearT.append((tau1,tau2,tau12))
    return shearT, torques

if __name__=="__main__":
    shearstressT()
