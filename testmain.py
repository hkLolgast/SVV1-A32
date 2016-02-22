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
        self.fail("Not implemented")

    def testrealMomentOfInertia(self):
        self.fail("Not implemented")

    def testboomLocations(self):
        self.fail("Not implemented")

    def testrealCentroid(self):
        self.fail("Not implemented")

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
        
        FfrontxVER = -220779.
        FfrontyVER = 226856.
        Frear1xVER = 390779./2
        Frear1yVER = 0.
        Frear2xVER = 390779./2
        Frear2yVER = 0.
        
        (FfrontxACT, FfrontyACT), \
        (Frear1xACT, Frear1yACT), \
        (Frear2xACT, Frear2yACT) = reactionForces(Lf1, Lf2, Lf3, L, R, W, Sx, dtailz, dtaily, dlgy)
        
#         self.fail("Analytical solution not yet available")
        for loc in ("front", "rear1", "rear2"):
            for dir in ("x", "y"):
                self.assertAlmostEqual(eval("F"+loc+dir+"ACT"), eval("F"+loc+dir+"VER"), delta = 0.05*abs(eval("F"+loc+dir+"ACT")))

if __name__ == "__main__":
    unittest.main()

