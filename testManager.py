'''
Created on Feb 9, 2016

@author: Rick
'''
import unittest
from unittest.loader import TestLoader
import time
import os
from datetime import datetime
from getpass import getuser 

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

    if uncheckedFunctions!={} and not all(uncheckedFunctions[name]==set() for name in uncheckedFunctions):
        print "Unchecked functions:"
        for name in uncheckedFunctions:
            if uncheckedFunctions[name]!=set():
                print "In %s:" % (name+".py")
                for f in uncheckedFunctions[name]:
                    print "\t%s" % f
    else:
        print "All functions checked"
        return {}
    return uncheckedFunctions
    
def generateTests():
    fileTemplate = \
"""'''
Created on {date}

@author: {userName}
'''
import unittest
from {fileName} import *

class Test{fileName}(unittest.TestCase):

if __name__ == "__main__":
    unittest.main()
"""
    
    functionTemplate = \
"""    def test{functionName}(self):
        self.fail("Not implemented")
"""
#Note: the indentation is important

    uncheckedFunctions = checkTests()
    if uncheckedFunctions!={}:
        print "\nGenerating tests..."
        for name in uncheckedFunctions:
            d = {"fileName":name,
                 "date":datetime.now().strftime("%b %d, %Y"),
                 "userName":getuser()}
            
            #Load old contents, or generate from template if the file does not exist yet
            if not os.path.isfile("test"+name+".py"):
                contents = fileTemplate.format(**d).split("\n")
            else:
                with open("test"+name+".py","r") as f:
                    contents = f.readlines()
            
            #Determine where in the file the new lines should be inserted
            for i,line in enumerate(contents):
                if line.rstrip()=="class Test{fileName}(unittest.TestCase):".format(**d):
                    insertion = i+1
                    break
            else:
                print "Corrupted test file for {fileName}.py: no Test class found. Please remove the file manually.".format(**d)
                continue
            
            #Insert the new lines
            for func in uncheckedFunctions[name]:
                for i,line in enumerate(functionTemplate.format(functionName = func).split("\n")):
                    contents.insert(insertion+i, line)
                    
            #Write the new contents
            with open("test"+name+".py","w") as f:
                for line in contents:
                    f.write(line.rstrip("\n")+"\n")
    print "Tests generated."
    print
    
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
