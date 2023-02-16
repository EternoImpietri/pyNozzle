from pyNozzle.nozzle import Nozzle, ConicalNozzle
from pyNozzle.flow import Flow
from pyNozzle.substance import Substance
import matplotlib.pyplot as plt
import numpy as np

def test_nozzle_plot():
    nozzle = ConicalNozzle(5, 3, 7, 10, 30, "mm")
    nozzle.display()
    return 

test_nozzle_plot()

