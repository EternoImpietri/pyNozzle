from pyNozzle.nozzle import Nozzle, ConicalNozzle
from pyNozzle.substance import Substance
from pyNozzle.flow import Flow, IsentropicFlow

import math
def test_flow():
    water = Substance('Water')
    nozzle = ConicalNozzle(1e-3*0.5, 1e-3*0.4, 1e-3*2*math.tan(math.radians(30))*4.15+1e-3*0.4, 30, 30, 'm')
    flow = IsentropicFlow(303.15,water.get_saturated_pressure(303.15),nozzle,water)
    return flow

flow = test_flow()
a, b, c = flow.simple_calculation()