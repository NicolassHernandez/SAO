import numpy as np
import math as mt
from scipy.special import factorial
from sao.functions.telescope import *
import torch
import math
dClass = type('dynamicClass', (), {})





class Zernike():
    def __init__(self, tel, jModes:list=[2,3], norm:str=''):
        """Zernike class for Zernike polynomial generator and others
            Input:
                tel (class)     : Telescope class, provide coordinate informaiton\n
                j (list)        : Noll index\n
                norm (str)      : Normalization format {"pv","pm1","rms",else}
                
            Example:
                zern = Zernike(tel, jModes=[2,3], norm='pv')
        """
        super(Zernike,self).__init__()
        # Telescope
        self.tel = dClass()
        self.tel.nPx = tel.nPx
        self.tel.dxy = tel.dxy
        self.tel.pupil = tel.pupil
        self.tel.offset = tel.offset
        # generate Zernike modes in form [modes,NM]
        self.jModes = jModes
        self.norm_noll = torch.zeros((len(self.jModes)))
        self.norm = norm
        # normalized coordinates inside pupil
        self.cor_z = dClass() 
        x,y,_,_ = get_coordinates(self.tel.nPx, self.tel.dxy, offset=[0,0])
        self.cor_z.x,self.cor_z.y = x/torch.max(x[self.tel.pupil]), y/torch.max(y[self.tel.pupil])# normalize inside pupil
        self.cor_z.r,self.cor_z.theta = cart2pol(self.cor_z.x,self.cor_z.y)
        # NORMALIZATION 
        self.zModes = torch.zeros((self.tel.nPx**2,len(self.jModes)), dtype=torch.float64)
        for i,mode in enumerate(self.jModes):
            n,m = self.j2nm(mode)# i -> n,m
            self.zModes[:,i] = self.get_zernikes(n,m).flatten()
            #
        # PRINT CLASS
        self.print_properties()
    #    
    def j2nm(self,j):
        """Find the [n,m] radial and azimuthal order, respectively. 

        Input:
            j (int): Noll index
            
        Output:
            n (int): radial order\n
            m (int): azimuthal order  
        """
        j = torch.tensor(j, dtype=torch.int64)
        n = int( ( -1.+torch.sqrt( 8*(j-1)+1 ) )/2. )
        p = ( j-( n*(n+1) )/2. )
        k = n%2
        m = int((p+k)/2.)*2 - k
        if m!=0:
            if j%2==0:
                s = 1
            else:
                s=-1
            m *= s
        return [n,m]
    #
    def nm2j(self, n,m):
        """Find the [n,m] radial and azimuthal order, respectively. 

        Input:
            j (list): Noll index
            
        Output:
            n (): radial order\n
            m (): azimuthal order  
        """
        pass


    def get_zernikes(self, n,m, **kwargs):
        """Zernike generator function

        Input:
            n (int): radial order\n
            m (int): azimuthal order

        Output:
            z (np.nadarray): $Z_m^n$ 2D phasemap based on pupil
        """
        norm = kwargs.get('norm',self.norm)
        r,theta = self.cor_z.r,self.cor_z.theta
        Z = torch.zeros((self.tel.nPx,self.tel.nPx), dtype=torch.float64)
        n,m = torch.tensor(n),torch.tensor(m)
        if m == 0:
            Z = torch.sqrt( (n+1) )*self.zrf(n,0,r)
        else:
            if m > 0:# j is even
                Z = torch.sqrt(2*(n+1))*self.zrf(n,m,r) * torch.cos( m*theta )
            else:# j is odd
                m = torch.abs(m)
                Z = torch.sqrt(2*(n+1))*self.zrf(n,m,r) * torch.sin( m*theta )
        tmp = Z[self.tel.pupil]# considering distribution inside the pupil
        if norm == 'pv':# problem when piston is included
            if ( torch.max(tmp)-torch.min(tmp) )!=0:  Z /= ( torch.max(tmp)-torch.min(tmp) )# handle division by zero
        elif norm == 'rms':
            Z /= torch.sqrt( torch.sum(tmp**2)/torch.sum(self.tel.pupil) )
        elif norm == 'pm1':# problem when piston is included
            if ( torch.max(tmp)-torch.min(tmp) )!=0:  Z = 2*( (Z-torch.min(tmp))/(torch.max(tmp)-torch.min(tmp))-0.5 )# handle division by zero
        return self.tel.pupil.to(torch.float64)*Z# forcing distribution inside pupil
    #
    def zrf(self, n,m,r):
        R = torch.zeros_like(r).to(torch.float64)
        for k in range(0, int((n-m)/2)+1):
            num = (-1)**k * factorial( int(n)-k)
            den = factorial(k) * factorial( int((n+m)/2)-k ) * factorial( int((n-m)/2)-k )
            R += (num/den) * r**(n-2*k)
        return R

# ONLY TO PRINT FUNCTIONS
    def print_properties(self):
        print('------------------------------------------------ ZERNIKE class ------------------------------------------------')
        print( f'nPx={self.tel.nPx} | jModes={self.jModes} | norm={self.norm}' )
        print('---------------------------------------------------------------------------------------------------------------')
    def __repr__(self):
        self.print_properties()
        return ''