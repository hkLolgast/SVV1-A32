import numpy as np
import matplotlib.pyplot as plt
from plotfunctions import *

#importing function made for the program
from datafunctions import *
from plotfunctions import *

filename = 'Fuselage_Boeing_737_Combined_Loads.rpt'

#### Compute plotting data for with and withour floor case
with_Floor_data = VonMises_with_Floor(filename)
without_Floor_data = VonMises_without_Floor(filename)

#### specifying locations to make the graphs
x_location = -1995
y_location = 58
z_location = 13375


#For cross section, possibilitie to change betweeen data with and without floor
z_values,VonMises_z_values = vonMises_cross_section(z_location,without_Floor_data)

#For fuselage, possibilitie to change betweeen data with and without floor
theta_values,VonMises_theta_values = vonMises_fuselage(x_location,y_location,without_Floor_data)

print z_values[0:200]






