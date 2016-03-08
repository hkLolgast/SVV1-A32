"""
Created on Mon Feb 22 2016

@author: Laurence V

Purpose of program: import von Mises data from reference file and create an array of (14761,4)
with in the different colums the [x-location, y-location, z-location, mean Von Mises], which can be used later in the Validation
"""
import numpy as np
import matplotlib.pyplot as plt
from plotfunctions import *


def VonMises_without_Floor(filename):
    f1 = open(filename,'r')
    data = f1.readlines()
    f1.close()

    data1 = data[15:14775]          #selecting the desired data, layer at Z1
    data2 = data[14785:29545]       #selecting the desired data, layer at Z2

    result1 = np.genfromtxt(data1, usecols = (2,3,4,5), dtype = float)         #selecting the desired columns for the array
    meanVonMises = np.genfromtxt(data1, usecols = (2,3,4,5), dtype = float)
    result2 = np.genfromtxt(data2, usecols = (2,3,4,5), dtype = float)

    for i in range(len(result1)):
        if(result1[i,0]==result2[i,0] and result1[i,1]==result2[i,1] and result1[i,2]==result2[i,2]):
            new_value = (result1[i,3]+result2[i,3])/2
            meanVonMises[i,0]= meanVonMises[i,0]*(-1)               #invert the x-axis, to match set axis system
            meanVonMises[i,2]= meanVonMises[i,2]*(-1)               #invert the z-axis, to match set axis system
            meanVonMises[i,3]= new_value

    ### don't stack the quantities on top, it changes the data type to strings, YOU DONT WANT THAT
    #quantities = ["x-location","y-location","z-location","mean Von Mises"]
    #meanVonMises = np.vstack((quantities,meanVonMises))

    without_floor_VonMises = np.array([11,22,33,44])              #create table to enable vstack'ing
    for i in range(len(meanVonMises)):
        if (meanVonMises[i,1]!= -200):
            values = meanVonMises[i,:]
            without_floor_VonMises = np.vstack((without_floor_VonMises,values))
    without_floor_VonMises = without_floor_VonMises[1:]
    

    #onlyVonMises = meanVonMises[:,3]
    onlyVonMises = without_floor_VonMises[:,3]
    highest_VonMises = np.amax(onlyVonMises)
    lowest_VonMises = np.amin(onlyVonMises)

    place_highest_VonMises = np.where(meanVonMises == highest_VonMises)
    place_lowest_VonMises = np.where(meanVonMises == lowest_VonMises)

    highest_stress =  meanVonMises[place_highest_VonMises[0][0],:]
    lowest_stress =  meanVonMises[place_lowest_VonMises[0][0],:]

    '''
    print "Highest Von Mises stress without Floor is found at location:"
    print  highest_stress
    print "And the lowest Von Mises stress without Floor is found at location:"
    print  lowest_stress
    '''
    ####first define the desired x,y-locations to be evaluated, the corresponding z-value and mean Von Mises will be found by program######

    ###using without floor, but don't want to rewrite everything####
    meanVonMises = without_floor_VonMises               
    
    x_location = meanVonMises[:,0]
    y_location = meanVonMises[:,1]
    z_location = meanVonMises[:,2]
    VonMisesValues = meanVonMises[:,3]

    #creating an array with values for theta
    theta_array = np.ones(len(x_location))
    for i in range(len(x_location)):
        theta_array[i] = angle_theta(x_location[i],y_location[i])  



    #rounding the values and putting it in a matrix
    x_location = np.matrix(np.round(x_location, decimals = 0))
    y_location = np.matrix(np.round(y_location, decimals = 0))
    z_location = np.matrix(np.round(z_location, decimals = 0))
    theta_array = np.matrix(np.round(theta_array, decimals =0))
    VonMisesValues = np.matrix(np.round(VonMisesValues, decimals = 2))


    #tranposing the matrices for hstacking later
    x_location = x_location.transpose()
    y_location = y_location.transpose()
    z_location = z_location.transpose()
    theta_array = theta_array.transpose()
    VonMisesValues = VonMisesValues.transpose()

    # h.stack to make the same matrix again
    rounded_vonMises = np.hstack((x_location,y_location,z_location,theta_array,VonMisesValues))
    rounded_vonMises = np.array(rounded_vonMises)

    return(rounded_vonMises)



def VonMises_with_Floor(filename):
    f1 = open(filename,'r')
    data = f1.readlines()
    f1.close()

    data1 = data[15:14775]          #selecting the desired data, layer at Z1
    data2 = data[14785:29545]       #selecting the desired data, layer at Z2

    result1 = np.genfromtxt(data1, usecols = (2,3,4,5), dtype = float)         #selecting the desired columns for the array
    meanVonMises = np.genfromtxt(data1, usecols = (2,3,4,5), dtype = float)
    result2 = np.genfromtxt(data2, usecols = (2,3,4,5), dtype = float)

    for i in range(len(result1)):
        if(result1[i,0]==result2[i,0] and result1[i,1]==result2[i,1] and result1[i,2]==result2[i,2]):
            new_value = (result1[i,3]+result2[i,3])/2
            meanVonMises[i,0]= meanVonMises[i,0]*(-1)               #invert the x-axis, to match set axis system
            meanVonMises[i,2]= meanVonMises[i,2]*(-1)               #invert the z-axis, to match set axis system
            meanVonMises[i,3]= new_value

    ### don't stack the quantities on top, it changes the data type to strings, YOU DONT WANT THAT
    #quantities = ["x-location","y-location","z-location","mean Von Mises"]
    #meanVonMises = np.vstack((quantities,meanVonMises))

    
    

    onlyVonMises = meanVonMises[:,3]
    highest_VonMises = np.amax(onlyVonMises)
    lowest_VonMises = np.amin(onlyVonMises)

    place_highest_VonMises = np.where(meanVonMises == highest_VonMises)
    place_lowest_VonMises = np.where(meanVonMises == lowest_VonMises)

    highest_stress =  meanVonMises[place_highest_VonMises[0][0],:]
    lowest_stress =  meanVonMises[place_lowest_VonMises[0][0],:]

    '''
    print "Highest Von Mises stress with Floor is found at location:"
    print  highest_stress
    print "And the lowest Von Mises stress with Floor is found at location:"
    print  lowest_stress
    '''
    
    ####first define the desired x,y-locations to be evaluated, the corresponding z-value and mean Von Mises will be found by program######
             
    x_location = meanVonMises[:,0]
    y_location = meanVonMises[:,1]
    z_location = meanVonMises[:,2]
    VonMisesValues = meanVonMises[:,3]

    #creating an array with values for theta
    theta_array = np.ones(len(x_location))
    for i in range(len(x_location)):
        theta_array[i] = angle_theta(x_location[i],y_location[i])  


    #rounding the values and putting it in a matrix
    x_location = np.matrix(np.round(x_location, decimals = 0))
    y_location = np.matrix(np.round(y_location, decimals = 0))
    z_location = np.matrix(np.round(z_location, decimals = 0))
    theta_array = np.matrix(np.round(theta_array, decimals =0))
    VonMisesValues = np.matrix(np.round(VonMisesValues, decimals = 2))


    #tranposing the matrices for hstacking later
    x_location = x_location.transpose()
    y_location = y_location.transpose()
    z_location = z_location.transpose()
    theta_array = theta_array.transpose()
    VonMisesValues = VonMisesValues.transpose()

    # h.stack to make the same matrix again
    rounded_vonMises = np.hstack((x_location,y_location,z_location,theta_array,VonMisesValues))
    rounded_vonMises = np.array(rounded_vonMises)

    return(rounded_vonMises)








