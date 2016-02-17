'''
Created on Feb 17, 2016

@author: Rick
'''
'''
B_n = sum([t_D*b/6*(2+sig_m/sig_n) for n in adjacent_booms]

s1/s2 = (My/Iyy*x1+Mx/Ixx*y1)/(My/Iyy*x2+Mx/Ixx*Iyy)
'''

import main
import numpy as np

def boomAreas(Mx, My, booms, R, ts, floorHeight, tf, hst, wst, tst):
    Ixx = main.realMomentOfInertia("x", R, ts, floorHeight, tf, hst, wst, tst)
    Iyy = main.realMomentOfInertia("y", R, ts, floorHeight, tf, hst, wst, tst)
    stressBases = [0]*len(booms)
    floorDist1 = [0]*len(booms)
    floorDist2 = [0]*len(booms)
    
    floorAngle = np.arccos((R-floorHeight)/R)
    floorLength = R*np.sin(floorAngle)
    floorAttach1 = (floorLength, floorHeight - R)
    floorAttach2 = (-floorLength, floorHeight - R)
    
    Cx, Cy = main.realCentroid(R, ts, floorHeight, tf, hst, wst, tst)
    
    for i,(x,y) in enumerate(booms):
        stressBases[i] = My/Iyy*(x-Cx)+Mx/Ixx*(y-Cy)
        floorDist1[i] = ((x-floorAttach1[0])**2+(y-floorAttach1[1])**2)**0.5
        floorDist2[i] = ((x-floorAttach2[0])**2+(y-floorAttach2[1])**2)**0.5
    
    attach1 = floorDist1.index(min(floorDist1))
    attach2 = floorDist2.index(min(floorDist2))
    
    attachments = []
    for i in range(len(booms)):
        attachments.append([])
        if i==0:
            attachments[i].append(len(booms)-1)
        else:
            attachments[i].append(i-1)
        attachments[i].append((i+1)%len(booms))
        if i==attach1:
            attachments[i].append(attach2)
        if i==attach2:
            attachments[i].append(attach1)
    
    areas = []
    for n in range(len(booms)):
        A = 0.
        for m in attachments[n]:
            if (n==attach1 and m==attach2) or (n==attach2 and m==attach1):
                t_D = tf 
            else:
                t_D = ts
            
            d = ((booms[n][0]-booms[m][0])**2+(booms[n][1]-booms[m][1])**2)**0.5
            A+=t_D*d/6.*(2+stressBases[m]/stressBases[n])
        areas.append(A)
    return areas
    
if __name__=="__main__":
    pass