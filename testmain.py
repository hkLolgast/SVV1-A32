'''
Created on Feb 15, 2016

@author: Rick
'''
try:
    import unittest
except ImportError:
    import os
    os.system("pip install unittest")
    import unittest
from main import *

class Testmain(unittest.TestCase):
    def testpolygonArea(self):
        A = polygonArea(4., 1.)
        self.assertEqual(A,2.)      #Note that R is actually the distance from the center to a corner
        A = polygonArea(9001.,42.)
        self.assertAlmostEqual(A, np.pi*42*42, places=1)          #For n->inf the result will approximate a circle
        self.assertRaises(ZeroDivisionError, polygonArea, 0,1)
        for n in (1,2):
            self.assertAlmostEqual(polygonArea(n, 1),0)
        self.assertEqual(polygonArea(4, 0),0)

    def testrealMomentOfInertia(self):
        fh = 1.8
        R = 2.
        ts = 0.003
        tf = 0.02
        hst = 0.015
        wst = 0.02
        tst = 0.012
        Ixx = realMomentOfInertia("x", R, ts, fh, tf, hst, wst, tst)
        Iyy = realMomentOfInertia("y", R, ts, fh, tf, hst, wst, tst)
        expIxx = 0.1069
        expIyy = 0.2123
        self.assertAlmostEqual(Ixx, expIxx,delta=abs(0.05*expIxx))
        self.assertAlmostEqual(Iyy, expIyy,delta=abs(0.05*expIyy))

    def testboomLocations(self):
        boomLocs = boomLocations(36, 2., True, 1.8)
        n = 0
        for (x,y) in boomLocs:
            expX, expY = 2*np.sin(n*2*np.pi/36), 2*np.cos(n*2*np.pi/36)
            if abs(expX-x)>0.001 or abs(expY-y)>0.001:
                self.assertAlmostEqual(y, -0.2, \
                                       msg="Location was ({x}, {y}), expected ({expX}, {expY}) or y=-0.2".format(x=x,y=y,expX=expX,expY=expY))         #Floor attachment
            else:
                n+=1

    def testrealCentroid(self):
        fh = 1.8
        R = 2.
        ts = 0.003
        tf = 0.02
        hst = 0.015
        wst = 0.02
        tst = 0.012
        Cx, Cy = realCentroid(R, ts, fh, tf, hst, wst, tst)
        expX, expY = (0,1.8772-R)
        self.assertAlmostEqual(Cx, expX, 3)
        self.assertAlmostEqual(Cy, expY, delta=abs(0.05*Cy))
            
    def testidealMomentOfInertia(self):
        booms = [(5,(3,2))]
        self.assertEqual(idealMomentOfInertia("x", booms), 0.)
        self.assertEqual(idealMomentOfInertia("y", booms), 0.)
        self.assertEqual(idealMomentOfInertia("xy", booms),0.)
        booms.append((5,(-3,-2)))
        self.assertEqual(idealMomentOfInertia("x", booms),40)
        self.assertEqual(idealMomentOfInertia("y", booms),90)
        self.assertEqual(idealMomentOfInertia("xy",booms),60)
        booms.append((5,(3,-2)))
        booms.append((5,(-3,2)))
        self.assertEqual(idealMomentOfInertia("xy", booms),0)
        

    def testcentroid(self):
        objects = [
                   (5,(1,2)),
                   (3,(4,2)),
                   (2,(-5,1))
                   ]
        cx, cy = centroid(objects)
        self.assertEquals(cx, 0.7)
        self.assertEquals(cy, 1.8)

    def testneutralLine(self):
        objects = [
                   (5,(1,2,3)),
                   (3,(4,2,0)),
                   (2,(-5,1,-2))
                   ]
        
        self.assertEquals(neutralLine("x", objects),1.8)
        self.assertEquals(neutralLine("y", objects),0.7)

    def testreactionForces(self):
        Lf1 = 4.0
        Lf2 = 12.5
        Lf3 = 5.2
        L   = 30.0
        R   = 2.0
        W   = 65000.0
        Sx  = 1.7e5
        dtailz  = 2.8
        dtaily  = 4.0
        dlgy    = 1.8
        
        FfrontxVER = -221680.
        FfrontyVER = 229554.
        FrearxVER = 391680.
        FrearyVER = 1683396.
        
        (FfrontxACT, FfrontyACT), \
        (Frear1xACT, Frear1yACT), \
        (Frear2xACT, Frear2yACT) = reactionForces(Lf1, Lf2, Lf3, L, R, W, Sx, dtailz, dtaily, dlgy)
        
        self.assertAlmostEqual(FfrontyACT+Frear1yACT+Frear2yACT, W*3*9.81, places=1, msg = "No force equilibrium in y")
        self.assertAlmostEqual(FfrontxACT+Frear1xACT+Frear2xACT, Sx, places=1, msg = "No force equilibrium in x")
        self.assertAlmostEqual(FfrontxACT, FfrontxVER, delta=abs(0.01*FfrontxVER))
        self.assertAlmostEqual(FfrontyACT, FfrontyVER, delta=abs(0.01*FfrontyVER))
        self.assertAlmostEqual(Frear1xACT+Frear2xACT, FrearxVER, delta=abs(0.01*FrearxVER))
        self.assertAlmostEqual(Frear1yACT+Frear2yACT, FrearyVER, delta=abs(0.01*FrearyVER))
        

if __name__ == "__main__":
    unittest.main()

