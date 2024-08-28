import numpy as np
import math as mt
from scipy.special import factorial
from sao.functions.telescope import *
dClass = type('dynamicClass', (), {})

def fstir(n):
    if n <= 10:
        return  np.array( mt.factorial(n) )
    elif n > 10 :# used to not blow up with integer recursion 
        # stirtling here
        return  np.round( np.sqrt(2*np.pi*n)*(n/np.e)**n).astype(np.int64)

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
        self.zModes = np.zeros((len(self.jModes),self.tel.nPx**2))
        self.norm_noll = np.zeros((len(self.jModes)))
        self.norm = norm
        # normalized coordinates inside pupil
        self.cor_z = dClass() 
        x,y,_,_ = get_coordinates(self.tel.nPx, self.tel.dxy, offset=self.tel.offset)
        self.cor_z.x,self.cor_z.y = x/np.max(x[self.tel.pupil]), y/np.max(y[self.tel.pupil])# normalize inside pupil
        self.cor_z.r,self.cor_z.theta = cart2pol(self.cor_z.x,self.cor_z.y)
        # NORMALIZATION 
        for i,mode in enumerate(self.jModes):
            n,m = self.j2nm(mode)# i -> n,m
            self.zModes[i,:] = self.get_zernikes(n,m).flatten()
            tmp = self.get_zernikes(n,m)[self.tel.pupil]# considering distribution inside the pupil
            if self.norm == 'pv':# problem when piston is included
                if ( np.max(tmp)-np.min(tmp) )!=0:  self.zModes[i,:] /= ( np.max(tmp)-np.min(tmp) )# handle division by zero
            elif self.norm == 'rms':
                self.zModes[i,:] /= np.sqrt( np.sum(tmp**2)/np.sum(self.tel.pupil) )
            elif self.norm == 'pm1':# problem when piston is included
                if ( np.max(tmp)-np.min(tmp) )!=0:  self.zModes[i,:] = 2*( (self.zModes[i,:]-np.min(tmp))/(np.max(tmp)-np.min(tmp))-0.5 )# handle division by zero
            #
        self.print_properties()
    #    
    def j2nm(self, j):
        """Find the [n,m] radial and azimuthal order, respectively. 

        Input:
            j (list): Noll index
            
        Output:
            n (): radial order\n
            m (): azimuthal order  
        """
        n = int( ( -1.+np.sqrt( 8*(j-1)+1 ) )/2. )
        p = ( j-( n*(n+1) )/2. )
        k = n%2
        m = int((p+k)/2.)*2 - k
        if m!=0:
            if j%2==0:
                s = 1
            else:
                s=-1
            m *= s
        return np.array([n,m])
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


    def get_zernikes(self, n,m):
        """Zernike generator function

        Input:
            n (int): radial order\n
            m (int): azimuthal order

        Output:
            z (np.nadarray): $Z_m^n$ 2D phasemap based on pupil
        """
        r,theta = self.cor_z.r,self.cor_z.theta
        Z = np.zeros((self.tel.nPx,self.tel.nPx))
        if m == 0:
            Z = np.sqrt( (n+1) )*self.zrf(n,0,r)
        else:
            if m > 0:# j is even
                Z = np.sqrt(2*(n+1))*self.zrf(n,m,r) * np.cos( m*theta )
            else:# j is odd
                m = np.abs(m)
                Z = np.sqrt(2*(n+1))*self.zrf(n,m,r) * np.sin( m*theta )
        return self.tel.pupil*Z# forcing distribution inside pupil
    def zrf(self, n,m,r):
        R = np.zeros_like(r).astype(np.float64)
        for k in range(0, int((n-m)/2)+1):
            num = (-1)**k * fstir( int(n)-k)
            den = fstir(k) * fstir( int((n+m)/2)-k ) * fstir( int((n-m)/2)-k )
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