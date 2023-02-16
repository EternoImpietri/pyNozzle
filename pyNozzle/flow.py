import scipy.optimize as opt

from pyNozzle.nozzle import Nozzle

class Flow :
    
    def __init__(
        self, 
        T_0 : float, 
        p_0 : float, 
        nozzle : Nozzle,
        substance : str
    ):
        
        self.T_0 = T_0
        self.p_0 = p_0
        self.nozzle = nozzle
        self.substance = substance
        
class IsentropicFlow(Flow) :
    def __init__(
        self, 
        T_0 : float, 
        p_0 : float, 
        nozzle : Nozzle,
        substance : str
    ):
        
        super.__init__(T_0, p_0, nozzle, substance)
    
    def short_calculation(self):
        
        return 0



class CFDFlow(Flow):
    # https://nbviewer.org/github/barbagroup/CFDPython/blob/master/lessons/14_Step_11.ipynb
    def __init__(
        self, 
        T_0 : float, 
        p_0 : float, 
        nozzle : Nozzle,
        substance : str
    ):
        
        super.__init__(T_0, p_0, nozzle, substance)