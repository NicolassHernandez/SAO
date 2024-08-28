from sao.functions._functions import *

class Telescope():
    def __init__(self, 
                nPx,
                D,
                dxy=1,
                fov=0,
                offset=0,
                shape='circ',
                ):
        super(Telescope,self).__init__()
        self.nPx = nPx
        self.D = D
        self.dxy = dxy
        self.offset = offset
        _,_,R,O = get_coordinates(self.nPx, self.dxy, self.offset)
        self.pupil = pupil(self.nPx,self.D,self.dxy,"circ",self.offset)
        self.r = R
        self.theta = O 