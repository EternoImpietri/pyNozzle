from pyNozzle.substance import Substance


water = Substance("Water")
water.display_phase_diagram(T_max=350, T_min = 250, p_max = 20000, p_min = 10, scale = "linear") 
water.display_phase_diagram()

ethanol = Substance("Ethanol")
ethanol.display_phase_diagram(T_min=150, T_max = 200, p_min = 0.00001, p_max = 1) 
ethanol.display_phase_diagram()