import scipy.optimize as opt
import math
import matplotlib.pyplot as plt
import numpy as np
from alive_progress import alive_bar


from pyNozzle.nozzle import Nozzle, ConicalNozzle
from pyNozzle.substance import Substance

class Flow :
    
    def __init__(
        self, 
        T_c : float, 
        p_c : float, 
        nozzle : Nozzle,
        substance : Substance
    ):
        
        self.T_c = T_c
        self.p_c = p_c
        self.nozzle = nozzle
        self.substance = substance
        
class IsentropicFlow(Flow) :

    def __init__(
        self, 
        T_c : float, 
        p_c : float, 
        nozzle : Nozzle,
        substance : Substance
    ):
        
        super().__init__(T_c, p_c, nozzle, substance)
    
    def simple_calculation(self, 
        p_a : float = 0,
    ):

        p_c = self.p_c
        T_c = self.T_c
        A_t = self.nozzle.A_t
        A_e = self.nozzle.A_e
        
        k = self.substance.get_heat_capacity_ratio(T_c)
        R = self.substance.R

        # ----------------------------- Throat conditions ---------------------------- #
       
        p_t = p_c*(2/(k+1))**(k/(k-1))
        T_t = 2*T_c/(k+1)
        a_t = math.sqrt(k*R*T_t)
        m_dot = A_t*p_c*k*math.sqrt(((2/(k+1))**((k+1)/(k-1)))/(k*R*T_c))
        c_star = p_c*A_t/m_dot

        # ---------------------------- Objective Function ---------------------------- #

        def objective_function(x):
            return abs((((k+1)/2)**(1/(k-1))*x**(1/k)*math.sqrt(((k+1)/(k-1))*(1-x**((k-1)/k))))-1/self.nozzle.epsilon)

        pressure_ratio = opt.minimize_scalar(objective_function, 
                                         method = "bounded",
                                         bounds = (0,1))
        
        # ------------------------------ Exit conditions ----------------------------- #

        p_e = p_c*pressure_ratio.x
        M_e = math.sqrt(2*((p_c/p_e)**((k-1)/k)-1)/(k-1))
        T_e = T_c/(1+0.5*(k-1)*M_e**2)
        a_e = math.sqrt(k*R*T_e)
        v_e = a_e*M_e

        # -------------------------------- Performance ------------------------------- #

        F_1 = m_dot*v_e*self.nozzle.correction
        F_2 = (p_e-p_a)*A_e
        F_total = (F_1 + F_2)
        C_F = F_total/(A_t*p_c)

        Isp = F_total/(m_dot*9.80665)

        return F_total, Isp, m_dot, T_e, p_e

    def iterative_simple_calculation(self,
        p_a : float = 0,
        points : int = 20,
    ):
        if type(self.nozzle) is Nozzle:
            raise AssertionError("Must specify which kind of nozzle")
        
        k = self.substance.get_heat_capacity_ratio(self.T_c)
        # p = [self.p_c]
        # T = [self.T_c]

        p = [self.p_c]
        T = [self.T_c]
        M = [0]
        
        # -------------------------------- Convergent -------------------------------- #

        print("Iterative Convergent")

        x_1, y = self.nozzle.get_envelope_convergent(points)
        x_1 = np.insert(x_1, 0, 0)
        with alive_bar(points) as bar :
            for i in range(points):
                A = math.pi*y[i]**2
                def objective_function(x):
                    return abs((1/x)*(((k+1)/2)**(-(k+1)/(2*(k-1))))*((1+0.5*(k-1)*x*x)**(0.5*(k+1)/(k-1)))-A/self.nozzle.A_t)
                
                mach = opt.minimize_scalar(objective_function, 
                                         method = "bounded",
                                         bounds = (0, 1))
                
                p_e = self.p_c*(1+0.5*(k-1)*mach.x**2)**(-k/(k-1))
                T_e = self.T_c*(1+0.5*(k-1)*mach.x**2)**(-1)
                
                T.append(T_e)
                p.append(p_e)
                M.append(mach.x)
                bar()

        # --------------------------------- Divergent -------------------------------- #


        print("Iterative Divergent")

        x_2, y = self.nozzle.get_envelope_divergent(points)
        with alive_bar(points) as bar :
            for i in range(points):
                A = math.pi*y[i]**2
                def objective_function(x):
                    return abs((1/x)*(((k+1)/2)**(-(k+1)/(2*(k-1))))*((1+0.5*(k-1)*x*x)**(0.5*(k+1)/(k-1)))-A/self.nozzle.A_t)
                
                mach = opt.minimize_scalar(objective_function, 
                                         method = "bounded",
                                         bounds = (1, 1e9))
                
                p_e = self.p_c*(1+0.5*(k-1)*mach.x**2)**(-k/(k-1))
                T_e = self.T_c*(1+0.5*(k-1)*mach.x**2)**(-1)
                
                T.append(T_e)
                p.append(p_e)
                M.append(mach.x)
                bar()

        
        return np.concatenate((x_1,x_2)), np.array(T), np.array(p), np.array(M)


class CFDFlow(Flow):
    # https://nbviewer.org/github/barbagroup/CFDPython/blob/master/lessons/14_Step_11.ipynb
    def __init__(
        self, 
        T_c : float, 
        p_c : float, 
        nozzle : Nozzle,
        substance : Substance
    ):
        
        super().__init__(T_c, p_c, nozzle, substance)