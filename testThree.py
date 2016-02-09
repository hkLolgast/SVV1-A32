'''
Created on Feb 9, 2016

@author: Rick
'''
import unittest


class Test(unittest.TestCase):


    def testName(self):
        self.failUnless(False)
        
    def testTwo(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()