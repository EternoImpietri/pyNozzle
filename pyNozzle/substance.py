import math 
import numpy as np
import matplotlib.pyplot as plt

import CoolProp as CP


class Substance :

    def __init__(
        self, 
        name : str
    ):

        self.name = name

    @property
    def R(self):
        """ Gas constant in J.kg¯¹.K¯¹ """
        return CP.CoolProp.PropsSI('GAS_CONSTANT', self.name)/CP.CoolProp.PropsSI('M', self.name)

    @property
    def T_crit(self):
        return CP.CoolProp.PropsSI('TCRIT', self.name)

    @property
    def p_crit(self):
        return CP.CoolProp.PropsSI('PCRIT', self.name)

    @property
    def T_triple(self):
        return CP.CoolProp.PropsSI('T_TRIPLE', self.name)
    
    @property
    def p_triple(self):
        return CP.CoolProp.PropsSI('P_TRIPLE', self.name)

    def get_vaporization_curve(self):
        T = np.arange(self.T_triple,self.T_crit,1)
        P = np.array([CP.CoolProp.PropsSI('P', 'T', t, 'Q', 1 ,self.name) for t in T])
        return T, P
    
    def get_melting_curve(self):
        s = CP.AbstractState("HEOS", self.name)
        P = np.logspace(math.log10(self.p_triple + 0.01), math.log10(s.keyed_output(CP.iP_max)),1000)
        T = np.array([s.melting_line(CP.iT, CP.iP, p) for p in P])
        return T, P

    def get_sublimation_curve(self):
        if self.name == "Water" :
            # https://doi.org/10.1063/1.555947
            # https://doi.org/10.1063/1.1461829

            T = np.arange(190, self.T_triple, 1)
            p_n = 611.657
            T_n = 273.16
            Theta = T/T_n
            a_1 = -13.928169
            a_2 = 34.7078238
            P = np.array([p_n*math.exp(a_1*(1-t**(-1.5)) + a_2*(1-t**(-1.25))) for t in Theta])
            
            return T, P
        else :
            raise ValueError("No sublimation curve for this substance")
        
    def display_phase_diagram(
        self,
        T_min = None,
        T_max = None,
        scale = 'log' 
    ):

        fig, ax = plt.subplots()

        # Vaporization
        T, P = self.get_vaporization_curve()
        ax.plot(T, P, 'k')

        # Melting
        T, P = self.get_melting_curve()
        ax.plot(T, P, 'k')

        # Sublimation
        try :
            T, P = self.get_sublimation_curve()
            ax.plot(T, P,'k')
        except :
            print("No sublimation curve for this substance")

        # Settings
        ax.set_xlabel("Temperature / K")
        ax.set_ylabel("Pressure / Pa")

        ax.set_yscale(scale)

        if scale == "log":
            ax.yaxis.get_major_locator().set_params(numticks=99)
            ax.yaxis.get_minor_locator().set_params(numticks=99, subs=[.2, .4, .6, .8])


        plt.tight_layout()
        plt.show()
        return fig, ax