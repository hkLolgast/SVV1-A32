"""
Created on Mon Feb 22 2016

@author: Laurence V

Purpose of program: import von Mises data from reference file and create an array of (14761,4)
with in the different colums the [x-location, y-location, z-location, mean Von Mises], which can be used later in the Validation
"""
import numpy as np

f1 = open('Fuselage_Boeing_737_Combined_Loads.rpt','r')
data = f1.readlines()
f1.close()

data1 = data[15:14775]          #selecting the desired data, layer at Z1
data2 = data[14785:29545]       #selecting the desired data, layer at Z2

result1 = np.genfromtxt(data1, usecols = (2,3,4,5))         #selecting the desired columns for the array
meanVonMises = np.genfromtxt(data1, usecols = (2,3,4,5))
result2 = np.genfromtxt(data2, usecols = (2,3,4,5))

for i in range(len(result1)):
    if(result1[i,0]==result2[i,0] and result1[i,1]==result2[i,1] and result1[i,2]==result2[i,2]):
        new_value = (result1[i,3]+result2[i,3])/2
        meanVonMises[i,3]= new_value

quantities = ["x-location","y-location","z-location","mean Von Mises"]

meanVonMises = np.vstack((quantities,meanVonMises))


### if you want to save to numpy array to make computations go faster###
'''
np.save('meanVonMises',meanVonMises)
'''
