'''
Created on Feb 22, 2016

@author: Rick
'''
import unittest
from Torque import *

class TestTorque(unittest.TestCase):
    def testshearstressT(self):
        '''
        This is tested by simply checking if the torque is 0 at the nose (since there is no reaction moment there)
        '''
        shearT, T = shearstressT()
        self.assertTupleEqual(shearT[-1], (0.0,0.0,0.0))
        self.assertEqual(T[-1], 0.)


if __name__ == "__main__":
    unittest.main()

