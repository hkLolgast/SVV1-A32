import numpy as np
import matplotlib.pyplot as plt

def angle_theta(x,y):
    if x>0:
        theta = np.arctan2(x,y)*180/np.pi
    if x<0:
        theta = 360 + np.arctan2(x,y)*180/np.pi
    return theta


def vonMises_cross_section(z_location,rounded_vonMises):
    plotdata = np.array([11,22,33,44,55])              #create table to enable vstack'ing

    ##using the rounded data####
    for i in range(len(rounded_vonMises)):
        if (rounded_vonMises[i,2]==z_location):
            values = rounded_vonMises[i,:]
            plotdata = np.vstack((plotdata,values))
    plotdata = plotdata[1:]                         #remove first row, which was there only for enables vstack'ing

    ####plotting data is ready, now just plot it########
    theta_values = plotdata[:,3]
    Vonmises_values = plotdata[:,4]   

    #option for plotting with line (not so nice) or just the points (looks better)
    #plt.plot(z_values,Vonmises_values, linestyle='solid',color='black',  marker='o', markersize=3.0, markerfacecolor='orange',label='$experimental$ $2D$')
    plt.scatter(theta_values,Vonmises_values, color= 'black')
    plt.title('Von Mises stresses in cross section at z is ' + str(z_location) + 'mm')
    plt.xlabel('angle theta [degrees]', fontsize=15)
    plt.ylabel('mean Von Mises stress [MPA]',fontsize=15)
    return(theta_values,Vonmises_values)


def vonMises_fuselage(x_location,y_location,rounded_vonMises):
    plotdata = np.array([11,22,33,44,55])              #create table to enable vstack'ing

    ##using the rounded data####
    for i in range(len(rounded_vonMises)):
        if (rounded_vonMises[i,0]==x_location and rounded_vonMises[i,1]==y_location):
            values = rounded_vonMises[i,:]
            plotdata = np.vstack((plotdata,values))
    plotdata = plotdata[1:]                         #remove first row, which was there only for enables vstack'ing


    ####plotting data is ready, now just plot it########
    z_values = plotdata[:,2]
    Vonmises_values = plotdata[:,4]   

    #option for plotting with line (not so nice) or just the points (looks better)
    #plt.plot(z_values,Vonmises_values, linestyle='solid',color='black',  marker='o', markersize=3.0, markerfacecolor='orange',label='$experimental$ $2D$')
    plt.scatter(z_values,Vonmises_values, color= 'black')


    #x_location 'and' y_location
    plt.title('Von Mises stress for fixed x = ' + str(x_location) + ' mm and y = ' + str(y_location) + ' mm')            
    plt.xlabel('z-coordinate [mm]', fontsize=15)
    plt.ylabel('mean Von Mises stress [MPA]',fontsize=15)
    return(z_values,Vonmises_values)
