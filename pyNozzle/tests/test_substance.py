from pyNozzle.substance import Substance


water = Substance("Water")
water.display_phase_diagram(T_max=350, T_min = 250, p_max = 20000, p_min = 10, scale = "linear")
