'''
Created on Feb 15, 2016

@author: Rick
'''
import numpy

def centroid(axis, objects):
    '''
    axis: string, either x, y or z
    objects: list of (area, (x[, y[, z]]))
    '''
    naxis = 0 if axis=="x" else 1 if axis=="y" else 2
    if not all(len(o[1])>naxis for o in objects):
        raise ValueError, "Position argument of object must be at least %d for axis %s" % (naxis+1, axis)
    sumAd = 0.
    sumA = 0.
    for o in objects:
        sumAd+=o[0]*o[1][naxis]
        sumA+=o[0]
    return sumAd/sumA

def neutralLine(axis, objects):
    return centroid(axis, objects)

