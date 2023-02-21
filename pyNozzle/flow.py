import scipy.optimize as opt
import math

from pyNozzle.nozzle import Nozzle, ConicalNozzle
from pyNozzle.substance import Substance

class Flow :
    
    def __init__(
        self, 
        T_0 : float, 
        p_0 : float, 
        nozzle : Nozzle,
        substance : Substance
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
        substance : Substance
    ):
        
        super().__init__(T_0, p_0, nozzle, substance)
    
    def simple_calculation(self, 
        p_a : float = 0,
    ):
        print("Simple calculation - Start")

        p_0 = self.p_0
        T_0 = self.T_0
        A_t = self.nozzle.A_t
        A_e = self.nozzle.A_e
        
        k = self.substance.get_heat_capacity_ratio(T_0)
        R = self.substance.R

        # ----------------------------- Throat conditions ---------------------------- #
       
        p_t = p_0*(2/(k+1))**(k/(k-1))
        T_t = 2*T_0/(k+1)
        a_t = math.sqrt(k*R*T_t)
        m_dot = A_t*p_0*k*math.sqrt(((2/(k+1))**((k+1)/(k-1)))/(k*R*T_0))
        c_star = p_0*A_t/m_dot

        # ---------------------------- Objective Function ---------------------------- #

        def objective_function(x):
            return abs((((k+1)/2)**(1/(k-1))*x**(1/k)*math.sqrt(((k+1)/(k-1))*(1-x**((k-1)/k))))-1/self.nozzle.epsilon)

        pressure_ratio = opt.minimize_scalar(objective_function, 
                                         method = "bounded",
                                         bounds = (0,1))
        
        # ------------------------------ Exit conditions ----------------------------- #

        p_e = p_0*pressure_ratio.x
        M_e = math.sqrt(2*((p_0/p_e)**((k-1)/k)-1)/(k-1))
        T_e = T_0/(1+0.5*(k-1)*M_e**2)
        a_e = math.sqrt(k*R*T_e)
        v_e = a_e*M_e

        # -------------------------------- Performance ------------------------------- #

        F_1 = m_dot*v_e*self.nozzle.correction
        F_2 = (p_e-p_a)*A_e
        F_total = (F_1 + F_2)
        C_F = F_total/(A_t*p_0)

        Isp = F_total/(m_dot*9.80665)

        print("Simple calculation - End")
        return F_total, Isp, m_dot, T_e, p_e

    def iterative_simple_calculation(self,
        p_a : float = 0,
        points : int = 20,
    ):
        if type(self.nozzle) is Nozzle:
            raise AssertionError("Must specify which kind of nozzle")
        
        p = [self.p_0]
        T = [self.T_0]
        x, y = self.nozzle.get_envelope_divergent(points)
        for i in range(points):
            self.nozzle.D_e = 2*y[i]
            _, _, _, T_e, p_e = self.simple_calculation(p_a = p_a)
            p.append(p_e)
            T.append(T_e)
        return p, T

        

class CFDFlow(Flow):
    # https://nbviewer.org/github/barbagroup/CFDPython/blob/master/lessons/14_Step_11.ipynb
    def __init__(
        self, 
        T_0 : float, 
        p_0 : float, 
        nozzle : Nozzle,
        substance : Substance
    ):
        
        super().__init__(T_0, p_0, nozzle, substance)