# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:52:45 2016

@author: Marc CB
"""
import numpy as np
import matplotlib.pyplot as plt

# input data:
R = 2.0
ts = 0.003
Fx1 = 220779.0
Fx2 = 390779.0
Fy1 = 226856.0
Fy2 = 1686094.0
A = np.pi*R*R
n = 100

# moments of inertia
Ixx = np.pi*R*R*R*ts
Iyy = Ixx
Ixy = 0.

# solving the equations
interval = np.linspace(0.,2*np.pi,n)
part11 = - Fx1/Ixx*ts*(R*R*np.sin(interval))
part21 = - Fy1/Iyy*ts*(R*R*np.cos(interval))
part12 = - Fx2/Ixx*ts*(R*R*np.sin(interval))
part22 = - Fy2/Iyy*ts*(R*R*np.cos(interval))

qb1 =  part11 + part21
q01 = Fx1*R/(2*A)
qtot1 = qb1 - q01

qb2 = part12 + part22
q02 = Fx2*R/(2*A)
qtot2 = qb2 - q02

plt.plot(interval, qtot1, label='frame 1')
plt.plot(interval, qtot2, label='frame 2')
plt.legend()
plt.show()

ax = plt.subplot(111, projection='polar')
ax.plot(interval, qtot1, label='frame 1')
ax.plot(interval, qtot2, label='frame 2')
ax.grid(True)
plt.legend()
plt.show()
