'''
Created on Feb 22, 2016

@author: Rick
'''
import unittest
from structuralAnalysis import *

class TeststructuralAnalysis(unittest.TestCase):
    def setUp(self):
        #Test case from structural analysis, lecture 11
        self.boomPos = [(-647.,-177.),
                   (0.,-203.),
                   (775.,-101.),
                   (775.,101.),
                   (0.,203.),
                   (-647.,-177.)]
        
        #     Sx = 0
#     Sy = 44500.
        self.booms = [
                     (1290.,(-647.,-127.)),
                     (1936.,(0,-203.)),
                     (645.,(775.,-101.)),
                     (645.,(775.,101.)),
                     (1936.,(0,203.)),
                     (1290.,(-647.,127.)),]
        self.floorAttachment = (1,4)
    
    def testshearCenter(self):
        self.fail("Not implemented")

    def testboomAreas(self):
        self.fail("Not implemented")

    def teststandardShearFlows(self):
        flows = standardShearFlows(self.booms, 0, 44500, self.floorAttachment)
        expected = [34.01,      #Sign swapped because of convention
                    0,
                    0,
                    -13.52,
                    0,
                    0,
                    81.60,]
        for i, qs in enumerate(flows):
            self.assertAlmostEqual(qs, expected[i], places=1)
        
    def testconnections(self):
        con = connections(self.booms, self.floorAttachment)
        expected = [[1,5],[0,2,4],[1,3],[2,4],[1,3,5],[0,4]]
        for i,c in enumerate(con):
            self.assertListEqual(sorted(c), expected[i])

    def test_shearCenter(self):
        self.fail("Not implemented")

if __name__ == "__main__":
    unittest.main()

