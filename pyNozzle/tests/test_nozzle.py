from pyNozzle.nozzle import Nozzle, ConicalNozzle




def test_nozzle_plot():
    nozzle = ConicalNozzle(5, 3, 7, 10, 30, "mm")
    nozzle.display()
    return nozzle

nozne = test_nozzle_plot()

