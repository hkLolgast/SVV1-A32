'''
Created on Feb 15, 2016

@author: Rick
'''
try:
    import numpy as np
except ImportError:
    import os
    try:
        os.system("pip install numpy")
        import numpy as np
    except:
        print "Please, be so kind to install pip if you want to do anything useful with python"
        os.system("pause")
        quit()
from numpy.linalg import solve
try:
    import matplotlib.pyplot as plt
except ImportError:
    import os
    os.system("pip install matplotlib")
    import matplotlib.pyplot as plt
from matplotlib import cm


import structuralAnalysis
import forces_x, forces_y, Torque

np.set_printoptions(edgeitems=10)

def centroid(objects):
    '''
    objects: list of (area, (x, y))
    '''
    sumAdx = 0.
    sumAdy = 0.
    sumA = 0.
    for o in objects:
        sumAdx+=o[0]*o[1][0]
        sumAdy+=o[0]*o[1][1]
        sumA+=o[0]
    return (sumAdx/sumA, sumAdy/sumA)

def neutralLine(axis, objects):
    '''
    Calculates the distance of the neutral line to axis
    '''
    if axis not in ("x", "y"):
        raise ValueError, "axis must be either x or y"
    naxis = 1 if axis=="x" else 0       #Distance to x-axis is Cy
    c = centroid(objects)
    return c[naxis]

def reactionForces(Lf1, Lf2, Lf3, L, R, W, Sx, dtailz, dtaily, dlgy):
    '''
    Calculate the reaction forces on the aircraft using the parameters
    '''
    '''
    RLx      FLx    RL1y    RL2y    FLy
Fx  1        1      0       0       0     = Sx
Fy  0        0      1       1       1     = 3*W*9.81
Fz  0        0      0       0       0     = 0
Mx  0        0      0       0       Lf2   = 3*W*9.81*(Lf1+Lf2-0.5*L)
My  0        LF2    0       0       0     = -Sx*(L-(Lf1+Lf2)+dtailz)
Mz  0        0      -0.5Lf3 0.5Lf3  0     = Sx*(dlgy+dtaily)
    '''
    a = np.matrix([[1,       1,     0,      0,      0,     ],                     
                   [0,       0,     1,      1,      1,     ],  
                   [0,       0,     0,      0,      Lf2,   ],
                   [0,       Lf2,   0,      0,      0,     ],
                   [0,       0,     Lf3/2., -Lf3/2.,0,     ]])
    
    b = np.array([[Sx,                     
    3*W*9.81,               
    3*W*9.81*(Lf1+Lf2-0.5*L),      
    -Sx*(L-(Lf1+Lf2)+dtailz),
    Sx*(dlgy+dtaily),]]).T       
    [RLx, FLx, RL1y, RL2y, FLy] = solve(a, b)
    RL1x = RL2x = RLx/2.
    Ffront = (FLx[0], FLy[0])
    Frear1 = (RL1x[0], RL1y[0])
    Frear2 = (RL2x[0], RL2y[0])
    
    return [Ffront, Frear1, Frear2]

def idealMomentOfInertia(axis, booms):
    '''
    Calculates the moment of inertia about axis of the idealised structure
    booms: list of boom tuples
    boom: (area, (x, y))
    '''
    I = 0
    if axis not in ("x", "y", "xy"):
        raise ValueError, "axis must be either x or y or xy"
    naxis1 = 1 if axis=="x" else 0
    naxis2 = naxis1 if axis!="xy" else int(not naxis1)
    neutral1 = neutralLine("y" if axis!="x" else "x", booms)
    neutral2 = neutralLine("x" if axis!="y" else "y", booms)
    
    for (area, pos) in booms:
        I+=area*(pos[naxis1]-neutral1)*(pos[naxis2]-neutral2)
    
    return I

def realMomentOfInertia(axis, R, ts, floorHeight, tf, hst, wst, tst):
    I = 0
    if axis=="xy":
        pass
    elif axis=="x":
        floorAngle = np.arccos((R-floorHeight)/R)
        floorLength = 2*R*np.sin(floorAngle)
        
        Cx, Cy = realCentroid(R, ts, floorHeight, tf, hst, wst, tst)
        
        I+=np.pi*R**3*ts+np.pi*2*R*ts*(0-Cy)**2
        I+=1/12.*floorLength*tf**3+floorLength*tf*(-(R-floorHeight)-Cy)**2
        stiffenerArea = hst*tst+wst*tst
        
        for (x,y) in boomLocations(36, R, False, floorHeight):
            I+=stiffenerArea*(y-Cy)**2
        
    elif axis=="y":
        I+=np.pi*R**3*ts
        floorAngle = np.arccos((R-floorHeight)/R)
        floorLength = 2*R*np.sin(floorAngle)
        I+=1/12.*floorLength**3*tf
        stiffenerArea = hst*tst+wst*tst
        for (x,y) in boomLocations(36, R, False, floorHeight):
            I+=stiffenerArea*x**2
    
    else:
        raise ValueError, "axis must be either x or y or xy"

    return I

def realCentroid(R, ts, floorHeight, tf, hst, wst, tst):
    floorAngle = np.arccos((R-floorHeight)/R)
    floorLength = 2*R*np.sin(floorAngle)
    
    sumAd = 0
    sumA = 0
    
    #fuselage
    sumAd+=np.pi*2*R*ts*0
    sumA +=np.pi*2*R*ts
    
    #floor
    sumAd+=floorLength*tf*(-(R-floorHeight))
    sumA +=floorLength*tf
    
    #stiffeners
    stiffenerArea = hst*tst+wst*tst
    for (x,y) in boomLocations(36, R, False, floorHeight):
        sumAd+=stiffenerArea*y
        sumA +=stiffenerArea
    
    
    Cy = sumAd/sumA
    return (0,Cy)               #Symmetry -> Cx = 0

def boomLocations(nBooms,R,addFloor = False, floorHeight = None):
    '''
    addFloor: Whether to add two booms at the end of the floor
    '''
    angles = np.linspace(0,2*np.pi,nBooms+1)[:-1]
    if addFloor:
        angle1 = np.arccos(-(R-floorHeight)/R)
        angle2 = 2*np.pi-angle1
        i = 0
        while i<len(angles):
            if angles[i]<=angle1<angles[(i+1)%len(angles)]:
                angles = np.insert(angles,i+1,angle1)
                i+=1
            elif angles[i]<=angle2<angles[(i+1)%len(angles)]:
                angles = np.insert(angles, i+1,angle2)
                break
            i+=1
        
    locations = zip(R*np.sin(angles), R*np.cos(angles))
    return locations

def polygonArea(n, R):
    return 1./2*n*R**2*np.sin(2*np.pi/n)

if __name__=="__main__":
    fh = 1.8
    R = 2.
    boomLocs = boomLocations(36, R, True, fh)
    ts = 0.003
    tf = 0.02
    hst = 0.015
    wst = 0.02
    tst = 0.012
    lf = 2*(fh*(2*R-fh))**0.5
    L = 30.
    Lf1 = 4.
    Lf2 = 12.5
    Lf3 = 5.2
    W = 65000.
    Sx = 1.7*10**5
    dtailz = 2.8
    dtaily = 5.0
    dlgy = 1.8
    
    
    Vx, Mx = forces_x.diagramsx()[:2]
    Vy, My = forces_y.diagramsy()[:2]
    qs0, T = Torque.shearstressT()
    results = np.zeros(shape=(len(Vx)*(len(boomLocs)+1),6))
    n = 0
    Ff, Fr1, Fr2 = reactionForces(Lf1, Lf2, Lf3, L, R, W, Sx, dtailz, dtaily, dlgy)
    for el in range(len(Vx)):
        Sx, mx = Vx[el], Mx[el]
        Sy, my = Vy[el], My[el]
        z = L*el/len(Vx)
        if z<L-Lf1-Lf2:
            Mz = T[0]
        elif z<L-Lf1:
            Mz = T[1]
        else:
            Mz = T[2]
        areas, floorAttachment = structuralAnalysis.boomAreas(mx, my, boomLocs, R, ts, fh, tf, hst, wst, tst)
        booms = []
        for i,boom in enumerate(boomLocs):
            booms.append((areas[i], boom))
    
        qs = structuralAnalysis.totalShearFlow(booms, Sx, Sy, -Mz, floorAttachment, fh, R, tf, ts)
        for i, (x1,y1) in enumerate(boomLocs):
            (x2, y2) = boomLocs[(i-1)%len(booms)]
            (x,y) = ((x1+x2)/2,(y1+y2)/2)
            results[n] = [x,y,z,qs[i], qs[i]/ts, qs[i]/ts*3**0.5]   #x,y,z,qs, tau, von mises
            n+=1
        results[n] = [0, fh-R, z, qs[-1], qs[-1]/tf, qs[-1]/tf*3**0.5]  #x,y,z,qs, tau, von mises
        n+=1
    v = results[np.argmax(results[:,4])]
    print v
    fig = plt.figure()
    from mpl_toolkits.mplot3d import Axes3D
    ax = fig.gca(projection="3d")
    x = results[:,0]
    y = results[:,1]
    z = results[:,2]
    S = ax.scatter(x,y,z, c = results[:,5])
#     plt.show()
