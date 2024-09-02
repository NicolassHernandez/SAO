import numpy as np
import torch
import math


def factorial(n): return torch.tensor(math.factorial(n), dtype=torch.float64)
#
def cart2pol(x, y): return torch.sqrt(x**2 + y**2), torch.atan2(y, x)  
def pol2cart(r,o):  return r*torch.cos(o),r*torch.sin(o)
#
def get_coordinates(nPx, dxy, offset=[0,0]): 
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
        nPx = torch.tensor([nPx, nPx])
    else:
        nPx = torch.tensor(nPx)

    if isinstance(dxy, (int, float)):
        dxy = torch.tensor([dxy, dxy])
    else:
        dxy = torch.tensor(dxy)

    if isinstance(offset, (int, float)):
        offset = torch.tensor([offset, offset])
    else:
        offset = torch.tensor(offset)
    #
    x = torch.arange(-(nPx[0]-1)/2,(nPx[0]-1)/2+1,1) #np.linspace( -(nPx[0]-1)/2, (nPx[0]-1)/2, nPx[0] )
    y = torch.arange(-(nPx[1]-1)/2,(nPx[1]-1)/2+1,1) #np.linspace( -(nPx[1]-1)/2, (nPx[1]-1)/2, nPx[1] ) 
    # adjusted performed to achieve a right-hand positive assumption
    x,y = (x-offset[0])*dxy[0], (y-offset[1])*dxy[1]
    Y,X = torch.meshgrid(y,x, indexing='ij')
    # ^> positive assumption 
    R,O = cart2pol(X,Y)
    return X,Y,R,O
#
def pupil(nPx:int,D:float,dxy:float=1,shape:str='circ',offset=[0,0]):
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
        ap = torch.abs(X)<=D/2 & torch.abs(Y)<=D/2
    #
    return ap





def set_binning(input, bin_factor, mode="mean"):
    """Binning operation function

    Input:
        input (array):          Input array to be binned\n
        bin_factor (int):       Integer factor\n
        mode (str, optional):   Mode of binning

    Output:
        binned (array):         Binned array
    """
    if input.shape[0] % bin_factor != 0 or input.shape[1] % bin_factor != 0:
        raise ValueError("input dimensions must be divisible by the binning factor.")
    reshaped_array = input.reshape(input.shape[0] // bin_factor,bin_factor,
                    input.shape[1] // bin_factor, bin_factor)
    # Apply the selected mode
    if mode == 'mean':
        binned = reshaped_array.mean(axis=(1, 3))
    elif mode == 'sum':
        binned = reshaped_array.sum(axis=(1, 3))
    elif mode == 'max':
        binned = reshaped_array.max(axis=(1, 3))
    elif mode == 'min':
        binned = reshaped_array.min(axis=(1, 3))
    elif mode == 'median':
        binned = np.median(reshaped_array, axis=(1, 3))
    else:
        raise ValueError(f"Unsupported mode: {mode}. Choose from 'mean', 'sum', 'max', 'min', 'median'.")
    return binned


## PROPAGATORS

def ones_fresnel_integral(u1, wvl, d1, z):
    """_summary_

    Args:
        u1 (_type_): _description_
        wvl (_type_): _description_
        d1 (_type_): _description_
        z1 (_type_): _description_
    """
    if len(input.shape) != 4: raise ValueError('Dimension must be (b,c,N,M)')
    N = u1.shape[-1]
    k = 2*torch.pi/wvl
    x1,y1,_,_ = get_coordinates(N, d1, offset=[0,0])# source plane
    df1 = 1/(N*d1)
    d2 = wvl*z*df1
    x2,y2,_,_ = get_coordinates(N, d2, offset=[0,0])
    # eval integral
    outer = (torch.exp(torch.tensor(1j)*k*z)/(1j*wvl*z))*torch.exp((1j*k/(2*z))*(x2**2+y2**2))
    inner = u1*torch.exp((1j*k/(2*z))*(x1**2+y1**2))
    u2 = outer*ft2(inner, d=d1, dim=(-2,-1))
    return u2,(d2,x2,y2)


def ft2(input, d, dim=(-2,-1)):
    if len(input.shape) != 4: raise ValueError('Dimension must be (b,c,N,M)')
    """Discrete Direct Fourier Transform

    Input:
        input (input):  2D input field of dim=(b,c,N,M)\n
        dxy (float):    Grid spacing\n
        dim (optional): Dimension along FT2 is computed

    Output:
        (input):        Output field
    """
    return torch.fft.fftshift(torch.fft.fft2(torch.fft.fftshift(input), dim=dim)) * d**2
#
def ift2(input, df, dim=(-2,-1)):
    if len(input.shape) != 4: raise ValueError('Dimension must be (b,c,N,M)')
    """Discrete Inverse Fourier Transform

    Input:
        input (input):      2D input field of dim=(b,c,N,M)\n
        dfxy (float):       Frequency grid spacing\n
        dim (optional):     Dimension along FT2 is computed

    Output:
        (input):            Output field
    """
    return torch.fft.ifftshift(torch.fft.ifft2(torch.fft.ifftshift(input), dim=dim))* (input.shape[-1]*df)**2
#
def ones_fresnel_integral(u1, wvl, d1, z):
    """_summary_

    Args:
        u1 (_type_): _description_
        wvl (_type_): _description_
        d1 (_type_): _description_
        z1 (_type_): _description_
    """
    if len(input.shape) != 4: raise ValueError('Dimension must be (b,c,N,M)')
    N = u1.shape[-1]
    k = 2*torch.pi/wvl
    x1,y1,_,_ = get_coordinates(N, d1, offset=[0,0])# source plane
    df1 = 1/(N*d1)
    d2 = wvl*z*df1
    x2,y2,_,_ = get_coordinates(N, d2, offset=[0,0])
    # eval integral
    outer = (torch.exp(torch.tensor(1j)*k*z)/(1j*wvl*z))*torch.exp((1j*k/(2*z))*(x2**2+y2**2))
    inner = u1*torch.exp((1j*k/(2*z))*(x1**2+y1**2))
    u2 = outer*ft2(inner, d=d1, dim=(-2,-1))
    return u2,(d2,x2,y2)
#
def twos_fresnel_integral(u1, wvl, d1,d2, z1):
    """Two step Fresnel-integral propagation\n
    There are four possible geometries which consider the sign of m:\n
    1. Forward-Forward, Backward-Backward for m>0
    2. Forward-Backward, Backward-Forward for m<0
    (z2a/z1a)=+-m, and m=dx2/dx1\n
    The sign of m consider both cases with negative-positive distances.
    In theory, all m can be simulated with +m
    Input:
        u1 (b,c,N,M):       Input complex wave
        wvl (float):        Wavelength
        d1 (float):         Grid spacing in source plane
        d2 (float):         Desired grid spacing in observation plane
        z1 (float):         Distance between source-observation planes
    Output:
        u2 (b,c,N,M):       Observation complex wave
        cor2 (dx2,x2,y2):   Grid spacing, and coordinates at observation plane
    """
    if len(u1.shape) != 4: raise ValueError('Dimension must be (b,c,N,M)')
    m = d2/d1# magnification
    # z1a, -m for FB and BF, +m for FF and BB
    z1a = z1/(1+m)
    u1a,cor1a = ones_fresnel_integral(u1, wvl, d1, z1a)
    u2,cor2 = ones_fresnel_integral(u1a, wvl, cor1a[0], z1-z1a)# aqui los x2,y2 deben ser meshgrid(N*d2) directamente
    return u2,cor2