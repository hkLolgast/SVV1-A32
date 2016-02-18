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
        #Calculate stress without terms that will vanish
        stressBases[i] = My/Iyy*(x-Cx)+Mx/Ixx*(y-Cy)
        #Check how close this boom is to the floor attachment
        floorDist1[i] = ((x-floorAttach1[0])**2+(y-floorAttach1[1])**2)**0.5
        floorDist2[i] = ((x-floorAttach2[0])**2+(y-floorAttach2[1])**2)**0.5
    
    #Check which booms the floor should be connected to
    attach1 = floorDist1.index(min(floorDist1))
    attach2 = floorDist2.index(min(floorDist2))
    
    attachments = connections(booms, (attach1, attach2))
    
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
    return areas, (attach1, attach2)
    
def standardShearFlows(booms, Sx, Sy, floorAttachment):
    '''
    Calculates the basic shear flow q_s of a two-cell beam, without taking into account q_s0
    floorAttachment indicates the indices of the booms where the two cells intersect
    '''
    Ixx = main.idealMomentOfInertia("x", booms)
    Iyy = main.idealMomentOfInertia("y", booms)
    Ixy = main.idealMomentOfInertia("xy", booms)
    
    Cx, Cy = main.centroid(booms)
    
    deltaQ = [0]*len(booms)
    for i, (area, (x,y)) in enumerate(booms):
        #Calculate change in shear flow due to boom i
        deltaQ[i] = -(Ixx*Sx-Ixy*Sy)/(Ixx*Iyy-Ixy**2)*area*(x-Cx)\
                    -(Iyy*Sy-Ixy*Sy)/(Ixx*Iyy-Ixy**2)*area*(y-Cy)

    attachments = connections(booms, floorAttachment)
    
    #Store all the shear flows.
    #Element at index i gives the shear flow from boom i to boom (i-1)%n
    #Element at index n is the shear flow from attach1 to attach 2
    shearFlows = [0]*(len(booms)+1)
    
    shearFlows[len(booms)] = deltaQ[floorAttachment[0]]
    for i in range(floorAttachment[0],-1,-1):
        #              q from i+1 to i  + deltaQ
        shearFlows[i] = shearFlows[i+1] + deltaQ[i]
#     shearFlows[]

def connections(booms, floorAttachment):
    '''
    Checks which boom is connected to which
    '''
    attachments = []
    for i in range(len(booms)):
        attachments.append([])
        if i==0:
            attachments[i].append(len(booms)-1)
        else:
            attachments[i].append(i-1)
        attachments[i].append((i+1)%len(booms))
        if i==floorAttachment[0]:
            attachments[i].append(floorAttachment[1])
        if i==floorAttachment[1]:
            attachments[i].append(floorAttachment[0])
    return attachments
    
if __name__=="__main__":
    pass