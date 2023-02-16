from pyNozzle.nozzle import Nozzle, ConicalNozzle
from pyNozzle.flow import Flow

def test_flow():
    nozzle = ConicalNozzle(5, 3, 7, 10, 30, "mm")
    flow = Flow(300,1000,nozzle,"water")
    return flow

flow = test_flow()