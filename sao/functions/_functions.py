import numpy as np


def cart2pol(x, y): return np.sqrt(x**2 + y**2), np.arctan2(y, x)  
def pol2cart(r,o):  return r*np.cos(o),r*np.sin(o)

def get_coordinates(nPx, dxy, offset=[0,0], norm=False): 
    """Coordinate function for the creation of grids

    Input:
        nPx (list)      : Number of pixels accross each dimension\n
        dxy (list)      : Pixels size along each coordinate\n
        offset (list)   : Offset in pixels along both directions

    Output:
        X,Y,R,O         : Grids of these coordinates with _> assumption
        
    Example:
        X,Y,R,O = get_coordinates([128,128],[3/128,3/128],[0,0])
    """
    if isinstance(nPx, (int, float)):
        nPx = np.array([nPx, nPx])
    if isinstance(dxy, (int, float)):
        dxy = np.array([dxy, dxy])
    if isinstance(offset, (int,float)):
        offset = np.array([offset,offset])
    #
    x = np.linspace( -(nPx[0]-1)//2, (nPx[0]-1)//2, nPx[0] )
    y = np.linspace( -(nPx[1]-1)//2, (nPx[1]-1)//2, nPx[1] ) 
    # adjusted performed to achieve a right-hand positive assumption
    x,y = (x-offset[0])*dxy[0], (y-offset[1])*dxy[1]
    Y,X = np.meshgrid(y,x, indexing='ij')
    # ^> positive assumption 
    R,O = cart2pol(X,Y)
    return X,Y,R,O



def pupil(nPx:int,D:float,dxy:float,shape:str,offset=[0,0]):
    """Create a 2D numpy array:
    
    Input:
        D (float)       : diameter of the geometry\n
        npx (int)       : number of pixels of a square\n
        dx (float)      : pixel size\n
        shape (str)     : geometry, which can be {"circ","rect"}

    Output:
        ndarray (float) : the 2D numpy geometry

    Example:
        pupil = pupil(3,128,3/128,"circ")
    """
    X,Y,R,O = get_coordinates(nPx, dxy, offset)
    if shape == 'circ':
        ap = (R<=D/2)
    elif shape == 'rect':
        ap = np.abs(X)<=D/2 & np.abs(Y)<=D/2
    #
    return ap