import math
import numpy as np
import matplotlib.pyplot as plt


class Nozzle():

    def __init__(
        self, 
        D_0 : float, 
        D_t : float, 
        D_e : float,
        unit : str):

        self.D_0 = D_0
        self.D_t = D_t
        self.D_e = D_e
        self.unit = unit

    def __str__(self):
        return f"Nozzle : D_0 = {self.D_0}, \
                D_t = {self.D_t}, \
                D_e = {self.D_e}, \
                in {self.unit}"

    @property
    def A_p(self):
        """ Plenum chamber area"""
        return math.pi*self.D_0**2/4
    
    @property
    def A_t(self):
        """ Nozzle area """
        return math.pi*self.D_t**2/4

    @property
    def A_e(self):
        """ Nozzle exit area"""
        return math.pi*self.D_e**2/4

    @property
    def epsilon(self):
        """ Expansion ratio """
        return self.A_e/self.A_t
    
    @property
    def correction(self):
        return 1
    

class ConicalNozzle(Nozzle):

    def __init__(
        self, 
        D_0 : float, 
        D_t : float, 
        D_e : float,
        alpha: float,
        beta : float,
        unit : str
    ):

        super().__init__(D_0, D_t, D_e, unit)
        self.alpha = alpha
        self.beta = beta
    
    def __str__(self):
        return f"ConicalNozzle : D_0 = {self.D_0}, D_t = {self.D_t}, D_e = {self.D_e}," +\
            f" \u03B1 = {self.alpha}°, \u03B2 = {self.beta}°, unit = {self.unit}"
        
    @property
    def l(self):
        """ Length of convergent section """
        return (self.D_0-self.D_t)/2/math.tan(math.radians(self.beta))
    
    @property
    def L(self):
        """ Length of divergent section """
        return (self.D_e-self.D_t)/2/math.tan(math.radians(self.alpha))

    @property
    def correction(self):
        """ Conical nozzle correction factor """
        return (1+math.cos(math.radians(self.alpha)))/2
    
    def get_envelope_convergent(self,
        points : int
    ):
        x = np.linspace(0,self.l,10)
        y = self.D_0/2 - x*math.tan(math.radians(self.beta))
        return x, y

    def get_envelope_divergent(self,
        points : int
    ):
        x = np.linspace(0,self.L,points)
        y = self.D_t/2 + x*math.tan(math.radians(self.alpha))
        return x + self.l, y

    def display(self):
        """ Display, trough matplotlib, a representation of the nozzle """
        fig, ax = plt.subplots()

        # Plenum 
        x = np.linspace(-self.D_0/2,0,10)
        y = np.full_like(x, self.D_0/2)
        ax.plot(x, y, 'k')
        ax.plot(x, -y, 'k')

        # Convergent
        x, y = self.get_envelope_convergent(10)
        ax.plot(x, y, 'k')
        ax.plot(x, -y, 'k')

        # Divergent 
        x, y = self.get_envelope_divergent(10)
        ax.plot(x, y, 'k')
        ax.plot(x, -y, 'k')

        # Settings
        ax.set_xlim(-self.D_0/2,self.l + self.L)
        ax.set_xlabel(f"x / {self.unit}")
        ax.set_ylabel(f"y / {self.unit}")

        ax.spines[['right', 'top']].set_visible(False)
        ax.set_aspect('equal')

        plt.tight_layout()
        plt.show()
        return fig,ax

