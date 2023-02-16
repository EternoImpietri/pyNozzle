from pyNozzle.substance import Substance

import matplotlib.pyplot as plt

water = Substance("Water")
fig, ax = plt.subplots()

T, P = water.get_vaporization_curve()
ax.plot(T, P)

T, P = water.get_melting_curve()
ax.plot(T,P)

T, P = water.get_sublimation_curve()
ax.plot(T,P)

ax.set_yscale("log")

ethanol = Substance("Ethanol")
# fig, ax = plt.subplots()

T, P = ethanol.get_vaporization_curve()
ax.plot(T, P)

T, P = ethanol.get_melting_curve()
ax.plot(T,P)

ax.set_yscale("log")