from pyNozzle.nozzle import Nozzle, ConicalNozzle
from pyNozzle.substance import Substance
from pyNozzle.flow import Flow, IsentropicFlow

import math
import matplotlib.pyplot as plt
import numpy as np

import CoolProp as CP

def test_flow():
    water = Substance('Water')
    nozzle = ConicalNozzle(1.5, 0.4, 2*math.tan(math.radians(30))*4.15 + 0.4, 30, 30, 'mm')
    flow = IsentropicFlow(300.15,water.get_saturated_pressure(300.15),nozzle,water)
    return flow


flow = test_flow()


x, T, p, M, v, Q = flow.iterative_simple_calculation(points=500)


# ------------------------------- Plot profile ------------------------------- #
fig, ax = plt.subplots()
a, b = flow.nozzle.get_envelope_convergent()
ax.plot(a, b, "k")
ax.plot(a, -b, "k")
a, b = flow.nozzle.get_envelope_divergent()
ax.plot(a, b, "k")
ax.plot(a, -b, "k")

ax2 = ax.twinx()
ax2.plot(x, T, "r")

ax3 = ax.twinx()
# ax3.set_yscale("log")
ax3.plot(x, p/flow.p_c, "b")

ax4 = ax.twinx()
ax4.plot(x, M, "g")

ax5 = ax.twinx()
ax5.plot(x, v, "purple")

fig, ax = plt.subplots()
a, b = flow.nozzle.get_envelope_convergent()
ax.plot(a, b, "k")
ax.plot(a, -b, "k")
a, b = flow.nozzle.get_envelope_divergent()
ax.plot(a, b, "k")
ax.plot(a, -b, "k")
ax2 = ax.twinx()
ax2.plot(x, Q, "r")

# ------------------------------ Plot TP diagram ----------------------------- #

# fig, ax = plt.subplots()
# ax.plot(T,p,'r')
# T, P = flow.substance.get_vaporization_curve()
# ax.plot(T,P,'k')
# T, P = flow.substance.get_melting_curve()
# ax.plot(T,P,'k')
# T, P = flow.substance.get_sublimation_curve()
# ax.plot(T,P,'k')
# ax.set_yscale("log")

plt.show()