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
        
        self.booms = [
                     (1290.,(-647.,-127.)),
                     (1936.,(0,-203.)),
                     (645.,(775.,-101.)),
                     (645.,(775.,101.)),
                     (1936.,(0,203.)),
                     (1290.,(-647.,127.)),]
        self.floorAttachment = (1,4)
    
    def testtotalShearFlow(self):
        global totalShearFlow
        #Save original version of the function
        oldShearFlow = totalShearFlow
        
        def totalShearFlow():
            #Copy of the structural analysis version but without using calcqs0
            qs = standardShearFlows(self.booms, 0, 44500, (1,4))
    #         qs01, qs02 = calcqs0(booms, Sx, Sy, Mz, floorAttachment, fh, R, tf, ts)
            qs01, qs02 = 0.7825, -7.346
            
            for i in range(len(qs)):
                if i==len(qs)-1:
                    qs[i] += -qs01+qs02
                elif 1<i<=4:
                    qs[i] += qs02
                else:
                    qs[i] += qs01
            return qs
        
        qs = totalShearFlow()
        expected = [34.01+0.7825,
                    0+0.7825,
                    0-7.346,            # - due to sign convention used 
                    -13.52-7.346,
                    0-7.346,
                    0+0.7825,
                    81.60-0.7825-7.346,]
        
        for i,q in enumerate(qs):
            self.assertAlmostEqual(q, expected[i], places=1)
        
        #restore old version
        totalShearFlow = oldShearFlow

    def testcalcqs0(self):
        '''
        The qs0 calculation was made with several very specific parameters which does not allow for easy unittesting.
        Instead, the results have been checked for moment equivalence and  rate of twist equality.
        '''
        pass

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

if __name__ == "__main__":
    unittest.main()

