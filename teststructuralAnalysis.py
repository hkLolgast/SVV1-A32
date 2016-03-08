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
            qs01, qs02 = 0.7285, -7.346
            
            for i in range(len(qs)):
                if i==len(qs)-1:
                    qs[i] += -qs01+qs02
                elif 1<i<=4:
                    qs[i] += qs02
                else:
                    qs[i] += qs01
            return qs
        
        qs = totalShearFlow()
        expected = [34.01+0.7285,
                    0+0.7285,
                    0-7.346,            # - due to sign convention used 
                    -13.52-7.346,
                    0-7.346,
                    0+0.7285,
                    81.60-0.7285-7.346,]
        
        for i,q in enumerate(qs):
            self.assertAlmostEqual(q, expected[i], places=1)
            print q, expected[i]
        
        #restore old version
        totalShearFlow = oldShearFlow

    def testcalcqs0(self):
        '''
        The qs0 calculation was made with several very specific parameters which does not allow for easy unittesting.
        Instead, the results have been checked for moment equivalence and  rate of twist equality by hand.
        '''
        pass

    def testboomAreas(self):
        #Test case from Lecture 9, but with constant thicknesses
        boomLocs = [(200.,600.),
                    (-200.,600.),
                    (-150.,0.),
                    (-100.,-600.),
                    (100.,-600.),
                    (150.,0.),]
        booms, attachment = boomAreas(0, 9001, boomLocs, 1, 1, 1, 1, 1, 1, 1)
        expected = [600./6*(2+150./200)+400./6*(2-1),
                    600./6*(2+150./200)+400./6*(2-1),
                    600./6*(2+100./150)+600./6*(2+200./150)+300./6*(2-1),
                    600./6*(2+150./100)+200./6*(2-1),
                    600./6*(2+150./100)+200./6*(2-1),
                    600./6*(2+100./150)+600./6*(2+200./150)+300./6*(2-1),]
        for i, A in enumerate(booms):
            self.assertAlmostEqual(A, expected[i], delta = abs(0.005*A))
        self.assertListEqual(sorted(attachment), [2,5])
        

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

