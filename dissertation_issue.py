import matplotlib.pyplot as plt
# plt.rcParams.update({'font.size': 16})
import pandas as pd
import matplotlib.mlab as mlab
import numpy as np

sigma_z_c = []
sigma_z_d = []
sigma_z_e = []
sigma_z_f = []
for x in range(201):
    sigma_z_c.append(.08*x*(1+.0002*x)**(-.5))
    sigma_z_d.append(.06 * x * (1 + .0015 * x) ** (-.5))
    sigma_z_e.append(.03 * x * (1 + .0003 * x) ** (-1))
    sigma_z_f.append(.016 * x * (1 + .0003 * x) ** (-1))

plt.plot(sigma_z_c)
plt.plot(sigma_z_d)
plt.plot(sigma_z_e)
plt.plot(sigma_z_f)
plt.show()
plt.legend(['sigma_z_c', 'sigma_z_d','sigma_z_e','sigma_z_f',])