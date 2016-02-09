'''
Created on Feb 9, 2016

@author: Rick
'''
import unittest
from unittest.loader import TestLoader
import time
import os

class TestMain(unittest.TestCase):
    def testMain(self):
        self.failUnless(False)
        
def main():
    suite = TestLoader().discover(".")
    unittest.TextTestRunner().run(suite)
    
def checkTests():
    testFiles = set()
    checkedFunctions = {}
    functionsToCheck = {}
    for name in os.listdir("."):
        if name.endswith(".py"):
            if name=="testManager.py":
                continue
            if name.startswith("test"):
                with open(name,"r") as f:
                    n = name[4:name.index(".py")]
                    checkedFunctions[n] = set()
                    for line in f:
                        if line.lstrip().startswith("#"):
                            continue
                        if "def test" in line:
                            func = line[line.index("def test")+8:line.index("(")]
                            checkedFunctions[n].add(func)
            else:
                with open(name,"r") as f:
                    n = name[:name.index(".py")]
                    functionsToCheck[n] = set()
                    for line in f:
                        if line.lstrip().startswith("#"):
                            continue
                        if "def " in line:
                            func = line[line.index("def ")+4:line.index("(")]
                            functionsToCheck[n].add(func)
                    if functionsToCheck[n] == set():
                        del functionsToCheck[n]
    
    uncheckedFunctions = {}
    for name in functionsToCheck:
        if name in checkedFunctions:
            uncheckedFunctions[name] = functionsToCheck[name]-checkedFunctions[name]
        else:
            uncheckedFunctions[name] = functionsToCheck[name]
            
#     print checkedFunctions
#     print uncheckedFunctions
    if uncheckedFunctions!={}:
        print "Unchecked functions:"
        for name in uncheckedFunctions:
            print "In %s:" % (name+".py")
            for f in uncheckedFunctions[name]:
                print "\t%s" % f
    return uncheckedFunctions
    
def generateTests():
    uncheckedFunctions = checkTests()
    if uncheckedFunctions!={}:
        print "\nGenerating tests..."
        for name in uncheckedFunctions:
            print "test"+name
            if os.path.exists("./test"+name):
                print "yay"
            else:
                print "no"
        
    
if __name__=="__main__":
    stop = False
    while not stop:
        inp = raw_input("action: ")
        if inp=="test":
            main()
            time.sleep(0.1)                     #To correct output placement
        elif inp=="generate":
            generateTests()
        elif inp=="check":
            print "-"*20
            checkTests()
            print "-"*20
        elif inp=="stop":
            stop = True
