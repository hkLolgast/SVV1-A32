'''
Created on Feb 15, 2016

@author: Rick
'''
import unittest
from main import *

class Testmain(unittest.TestCase):
    def testneutralLine(self):
        objects = [
                   (5,(1,2,3)),
                   (3,(4,2,0)),
                   (2,(-5,1,-2))
                   ]
        
        self.assertEquals(neutralLine("x", objects),0.7)
        self.assertEquals(neutralLine("y", objects),1.8)
        self.assertEquals(neutralLine("z", objects),1.1)

if __name__ == "__main__":
    unittest.main()

