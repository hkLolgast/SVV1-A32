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
import numpy.linalg as linalg

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

#     attachments = connections(booms, floorAttachment)
    
    #Store all the shear flows.
    #Element at index i gives the shear flow from boom i to boom (i-1)%n
    #Element at index n is the shear flow from attach1 to attach 2
    shearFlows = [0]*(len(booms)+1)
    
    def calcShearFlow(i):
        return shearFlows[(i+1)%len(booms)] + deltaQ[i] #Shear flow from previous beam + delta
    
    shearFlows[len(booms)] = deltaQ[floorAttachment[0]]
    for i in range(floorAttachment[0]-1,-1,-1):
        shearFlows[i] = calcShearFlow(i)
    
    for i in range(len(booms)-1,floorAttachment[1],-1):
        shearFlows[i] = calcShearFlow(i)
        
    shearFlows[floorAttachment[1]] = shearFlows[floorAttachment[1]+1]+shearFlows[len(booms)]+deltaQ[floorAttachment[1]]
    
    for i in range(floorAttachment[1]-1, floorAttachment[0], -1):
        shearFlows[i] =calcShearFlow(i)
        
    return shearFlows

def shearCenter(booms, Sx, Sy, floorAttachment, floorHeight, R, tf, ts):
    qs = standardShearFlows(booms, Sx, Sy, floorAttachment)
    
    #Areas
    A2 = R**2*np.arccos((R-floorHeight)/R)-(R-floorHeight)*np.sqrt(2*R*floorHeight-floorHeight**2)        #Reference: Wolfram
    A1 = np.pi*R**2-A2
    
    A = np.array([[0,0,0,0],      #(dtheta/dz)_I=0
                  [0,0,0,0],      #(dtheta/dz)_II=0
                  [2*A1,2*A2,0,Sy],   #Sum(M) = 0 for Cx
                  [2*A1,2*A2,Sx,0]])  #Sum(M) = 0 for Cy
    
    #Row 1: 1/(2A1*G)*integral(qs/t*ds over area 1) = 0 (G = constant)
    #Row 2: 1/(2A2*G)*integral(qs/t*ds over area 2) = 0
    # --> integral = 0
    #Row 3: 2A1*qs01+2A2*qs02+Sy*Cx = integral(qb*d*r)+qf*lf*df
    #Row 3: 2A1*qs01+2A2*qs02+Sx*Cy = integral(qb*d*r)+qf*lf*df
    
    B = np.array([[0],[0],[0],[0]])
    
    floorAngle = np.arccos((R-floorHeight)/R)
    floorLength = R*np.sin(floorAngle)
    
    A[0,1] = A[1,0] = floorLength/tf
    
    #qb goes to the other side
    B[0] = -1/tf*qs[-1]*floorLength       #Sign convention
    B[1] =  1/tf*qs[-1]*floorLength
    
    #Calculate moments due to shear flow
    B[2] = B[3] = qs[-1]*floorLength*(R-floorHeight)
    for i,(boomArea1, (x1,y1)) in enumerate(booms):
        boomArea2, (x2, y2) = booms[(i-1)%len(booms)]
        d = ((x1-x2)**2+(y1-y2)**2)**0.5
        midpoint = ((x1+x2)/2,(y1+y2)/2)
        r = (midpoint[0]**2+midpoint[1]**2)**0.5
#         print d, r
        if floorAttachment[0]<i<=floorAttachment[1]:    #lower segment
            A[1,1]+=1/ts*d
            B[1]+=qs[i]*d/ts
        else:
            A[0,0]+=1/ts*d
            B[0]+=qs[i]*d/ts
        B[2]+=qs[i]*d*r
        B[3]+=qs[i]*d*r
        
    print A
    print "-"
    print B
    qs01, qs02, dx, dy = linalg.solve(A,B)
    
    return dx, dy, qs01, qs02

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