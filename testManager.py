'''
Created on Feb 9, 2016

@author: Rick
'''
import unittest

class TestMain(unittest.TestCase):
    def testMain(self):
        self.failUnless(False)
        
def main():
    print "testing..."
    
    unittest.main()
    
def checkTests():
    pass

def generateTests():
    pass
    
if __name__=="__main__":
    stop = False
    while not stop:
        inp = raw_input("action: ")
        if inp=="test":
            main()
        elif inp=="generate":
            generateTests()
        elif inp=="check":
            checkTests()