"""
Pupil Maps
----------

Functions for the creation of pupil maps and masks.

"""

import numpy as np


def cart2pol(x, y): return np.sqrt(x**2 + y**2), np.arctan2(y, x)  
def pol2cart(r,o):  return r*np.cos(o),r*np.sin(o)

def pupil(D:float,npx:int,dx:float,shape:str):
    """
    Create a 2D numpy array:
    
    Inputs:
        D (float)       : diameter of the geometry\n
        npx (int)       : number of pixels of a square\n
        dx (float)      : pixel size\n
        shape (str)     : geometry, which can be {"circ","rect"}\n

    Outputs:
        ndarray (float) : the 2D numpy geometry

    Examples: ::
        pupil = pupil(3,128,3/128,"circ")
    """
    x = np.arange( -(npx-1)/2,(npx-1)/2,1 )* dx
    x,y = np.meshgrid(x,x, indexing='ij')
    r,o = cart2pol(x,y)
    if shape == 'circ':
        ap = (r<=D)
    elif shape == 'rect':
        ap = np.abs(x)<=1 & np.abs(y)<=1
    #
    return ap