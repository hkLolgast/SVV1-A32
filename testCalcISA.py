'''
Created on Feb 9, 2016

@author: Rick
'''
import unittest
from CalcISA import *

class TestCalcISA(unittest.TestCase):
    def testmeter(self):
        self.fail("Not implemented")

    def testcalcHeight(self):
        self.fail("Not implemented")

    def testvaluesAtHeight(self):
        self.fail("Not implemented")

    def testft(self):
        self.assertEquals(1/0.3047, ft(1))
        self.assertEqual(15/0.3047, ft(15))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
