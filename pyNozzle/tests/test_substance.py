from pyNozzle.substance import Substance


water = Substance("Water")
water.display_phase_diagram(T_max=350, T_min = 250, p_max = 20000, p_min = 10, scale = "linear") 
water.display_phase_diagram()

ethanol = Substance("Ethanol")
ethanol.display_phase_diagram(T_min=150, T_max = 200, p_min = 0.00001, p_max = 1) 
ethanol.display_phase_diagram()

from CoolProp.Plots import PropertyPlot
import CoolProp

name = "Ethanol"
plot = PropertyPlot(name, 'Ph')
plot.calc_isolines(CoolProp.iQ, num=11)
# plot.calc_isolines(CoolProp.iSmass, num=25)
# plot.calc_isolines(CoolProp.iT, num=25)


T0 = 300.15; h0 = CoolProp.CoolProp.PropsSI('Hmass', "T", T0, "Q", 1, name); s0 = CoolProp.CoolProp.PropsSI('Smass', "T", T0, "Q", 1, name)
plot.calc_isolines(CoolProp.iSmass, iso_range=[s0/1000], num=1)

plot.set_axis_limits([0,3000,1,1e4])
plot.show()