from pyNozzle.nozzle import Nozzle, ConicalNozzle
from pyNozzle.substance import Substance
from pyNozzle.flow import Flow, IsentropicFlow

import math
import matplotlib.pyplot as plt
import numpy as np

def test_flow():
    water = Substance('Water')
    nozzle = ConicalNozzle(1e-3*1.5, 1e-3*0.4, 1e-3*2*math.tan(math.radians(30))*4.15+1e-3*0.4, 30, 30, 'm')
    flow = IsentropicFlow(303.15,water.get_saturated_pressure(303.15),nozzle,water)
    return flow


flow = test_flow()

x, p, T, M = flow.iterative_simple_calculation(points=100)


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

plt.show()
