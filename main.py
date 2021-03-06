'''
Created on Feb 15, 2016

@author: Rick
'''

fh = 1.8
R = 3.0
ts = 0.003
tf = 0.04
hst = 0.15
wst = 0.04
tst = 0.012
L = 30.
Lf1 = 4.0
Lf2 = 12.5
Lf3 = 5.2
W = 65000.0
Sx = 170000.0
dtailz = 2.8
dtaily = 5.0
dlgy = 1.8

'''
Normal:
    x: 1.99498743711
    y: -0.1
    z: 13.3554817276
    Von Mises stress: 1.331594e+08
Higher Sx:
    x: -1.14278760969
    y: 1.6320698469
    z: 13.4551495017
    Von Mises stress: 1.747969e+08
Higher weight:
    x: 1.99498743711
    y: -0.1
    z: 13.3554817276
    Von Mises stress: 2.464144e+08
Higher tf:
    x: 1.99498743711
    y: -0.1
    z: 13.3554817276
    Von Mises stress: 1.268518e+08
Higher ts:
    x: 1.99498743711
    y: -0.1
    z: 13.3554817276
    Von Mises stress: 8.807580e+07
Lower Lf2:
    x: 1.99498743711
    y: -0.1
    z: 15.3488372093
    Von Mises stress: 1.560959e+08
Higher R:
    x: 2.8867505607
    y: -0.773502481489
    z: 13.3554817276
    Von Mises stress: 9.623139e+07
'''

import plotfunctions
from datafunctions import VonMises_with_Floor, VonMises_without_Floor
try:
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError:
    import os
    try:
        print "Updating pip..."
        os.system("python -m pip install -U pip")
        print "Installing libraries..."
        os.system("pip install numpy")
        os.system("pip install matplotlib")
        import numpy as np
        import matplotlib.pyplot as plt
        print "Libraries successfully installed and loaded"
    except:
        print "Please, be so kind to install pip if you want to do anything useful with python"
        os.system("pause")
        quit()
from numpy.linalg import solve
from matplotlib import cm


import structuralAnalysis
import forces_x, forces_y, Torque

np.set_printoptions(edgeitems=40)

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
    boomLocs = boomLocations(36, R, True, fh)

        
    step = 0.1
    Vx, Mx = forces_x.diagramsx(step)[:2]
    Vy, My = forces_y.diagramsy(step)[:2]
    qs0, T = Torque.shearstressT()
    results = np.zeros(shape=(len(Vx)*(len(boomLocs)+1),7))
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
        
        Ixx = idealMomentOfInertia("x", booms)
        Iyy = idealMomentOfInertia("y", booms)
        Ixy = idealMomentOfInertia("xy", booms)
        
#         if 6.4<z<=6.7:
#             print z, el, n
#             plt.plot(qs)
#             plt.title("qs (z=%.2f)" % z)
#             plt.show()
#             plt.clf()
        for i, (x1,y1) in enumerate(boomLocs):
            (x2, y2) = boomLocs[(i-1)%len(booms)]
            (x,y) = ((x1+x2)/2,(y1+y2)/2)
            sigma = (Ixx*my-Ixy*mx)/(Ixx*Iyy-Ixy**2)*x+(Iyy*mx-Ixy*my)/(Ixx*Iyy-Ixy**2)*y
            results[n] = [x,y,z,qs[i], qs[i]/ts, (sigma**2+(qs[i]/ts)**2*3)**0.5, sigma]   #x,y,z,qs, tau, von mises
            n+=1
        
        sigma = (Ixx*my-Ixy*mx)/(Ixx*Iyy-Ixy**2)*x+(Iyy*mx-Ixy*my)/(Ixx*Iyy-Ixy**2)*y
#         if 11700<=n<11739:
#             print my, mx, sigma, z
        results[n] = [0, fh-R, z, qs[-1], qs[-1]/tf, (sigma**2+(qs[-1]/tf)**2*3)**0.5, sigma]  #x,y,z,qs, tau, von mises, normal stress
        n+=1
        
#     print Mx[np.argmax(Mx)], np.argmax(Mx), My[np.argmax(abs(My))], np.argmax(abs(My))
    
    
# #     plt.subplot(121)
#     th = np.linspace(0,2*np.pi, 38)
#     x = np.append(2000*np.cos(-th+0.5*np.pi), [0])
#     y = np.append(2000*np.sin(-th+0.5*np.pi), [-200.])
#     
# #     plt.scatter(x, y,c=10**-6*results[5265:5304,5],s=80, vmin=0, vmax=150)
#     plt.scatter(x, y,c=10**-6*results[2574:2613,5],s=80, vmin=0, vmax=150)
#     plt.title("Numerical simulation (z=6.625)")
#     plt.xlabel("x-location [mm]")
#     plt.ylabel("y-location [mm]")
#     plt.colorbar(label="[MPa]")
#     plt.savefig("Numerical_von_mises_6625.png")
# #     plt.show()
#     plt.clf()
#     
# #     plt.subplot(122)
#     plotfunctions.vonMises_colour_mapping(6625, VonMises_with_Floor('Fuselage_Boeing_737_Combined_Loads.rpt'))
#     plt.title("Validation (z=6.625)")
#     plt.savefig("Validation_von_mises_6625.png")
# #     plt.show()
#     plt.clf()
# #     plt.show()
    
            
    
    x = results[:,0]
    y = results[:,1]
    z = results[:,2]
    r = results[:,5]
    
    #From the graphs, it can be seen that the sensible maximum lies between 13.4 and 13.5 meters - the attachment of the main landing gear
    limx = x[np.where(6<z)]
    limy = y[np.where(6<z)]
    limz = z[np.where(6<z)]
    limr = r[np.where(6<z)]
    
    limx = limx[np.where(limz<24)]
    limy = limy[np.where(limz<24)]
    limz = limz[np.where(limz<24)]
    limr = limr[np.where(limz<24)]
    
#     v = results[np.where(np.all(13.4<z,z<13.5))][np.argmax(r[np.where(np.all(13.4<z,z<13.5))])]
    i = np.argmax(abs(limr))
    v = (limx[i], limy[i], limz[i], limr[i])
    print "Maximum:"
    print '''    x: {}
    y: {}
    z: {}
    Von Mises stress: {:e}'''.format(*v)


#     for j in range(39):
#         if x[j]==v[0]:
#             break
#     for i in range(len(boomLocs)+1):
#     for i in (0,20):
    
    
    wantedX, wantedY = (0,2)
    diffs = [0]*39
    for j in range(39):
        diffs[j] = ((x[j]-wantedX)**2+(y[j]-wantedY)**2)**0.5
    j = diffs.index(min(diffs))
    #j = 0
#     print x[j], y[j]
    
    for i in (j,):
        plt.plot(z[np.where(x==x[i])], r[np.where(x==x[i])], label="(%.2f, %.2f)" % (x[i], y[i]))
#     plt.legend()
#     S = ax.scatter(x,y,z, c = results[:,5])
#     print x
#     print y
#     print z
    plt.show()