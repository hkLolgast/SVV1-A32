'''
Created on Feb 9, 2016

@author: Rick
'''
import unittest
from CalcISA import *

class TestCalcISA(unittest.TestCase):
    def testcalcHeight(self):
        self.assertAlmostEqual(calcHeight(83749.8),1578,0)

    def testvaluesAtHeight(self):
        T, P, rho = valuesAtHeight(1578)
        self.assertAlmostEqual(T, 277.893, 2)
        self.assertAlmostEqual(P, 83749.8, -1)
        self.assertAlmostEqual(rho, 1.04989,4)

    def testmeter(self):
        self.assertAlmostEqual(0.3048, meter(1))
        self.assertAlmostEqual(15*0.3048,meter(15))
        
    def testft(self):
        self.assertAlmostEqual(1/0.3048, ft(1))
        self.assertAlmostEqual(15/0.3048, ft(15))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
