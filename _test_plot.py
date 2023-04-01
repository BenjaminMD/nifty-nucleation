from plots import create_basic_plot, time_vs_concentration
from rsc.utils import read_config
from glob import glob

import matplotlib.pyplot as plt
import numpy as np

from scipy.constants import k, N_A, pi, R
import numpy as np


class Constants():
    def __init__(self, config):
        self.k = k * 1e3
        self.N_A = N_A * 1
        constants = config['const']
        self.rho = constants['rho']
        self.M = constants['M']
        self.eta = constants['eta']
        self.T = constants['T']
        self.gamma = constants['gamma']

        self.v_m = self.M / (self.rho * N_A)
        self.R_0 = ((3 * self.v_m) / (4 * pi)) ** (1 / 3)
        self.Beta = 4 * self.k * self.T / (9 * self.eta * self.v_m)
        self.R_cap = 2 * self.gamma * self.v_m / (self.k * self.T)
        self.dG = (16 * pi * self.gamma ** 3 * self.v_m ** 2) / (self.k ** 3 * self.T ** 3)
        self.D = (self.k * self.T) / (6 * pi * self.eta * self.R_0)
        self.A_gr = 4 * pi * self.D * N_A

        act = config['activation']
        self.k1 = act['k_10'] * np.exp(- act['E_1'] / (R * 1e-3 * self.T))

        self.k_gr = act['k_gr0'] * np.exp(- act['E_gr'] / (R * 1e-3 * self.T))
        self.Au_sat = act['k_sol0'] \
                      * np.exp(- act['E_sol'] / (R * 1e-3 * self.T))


config = read_config()


def calc_growth_rate(K, var):
    var["r_ratio"] = K.R_cap / var["R"]
    # var["r_ratio"][var["r_ratio"] > 7] = 7

    var["k_gr"] = 1 - 1 / var["S"] * np.exp(var["r_ratio"])
    var["k_gr"] /= 1 + K.D / (var["R"] * 5.3 * 1e-5)
    var["k_gr"] *= K.A_gr * var["R"]

    return var


var = {"P": [1], "S": [2], "V": [1], "R": [1], "r_ratio": 1, "k_gr": 1, "P_nuc": 1, "R_nuc": 1, "V_nuc": 1}
# convert arrays to numpy arrays
for key in var:
    var[key] = np.array(var[key])

#
# plot growth vs oversaturation
#
r = np.linspace(0.5e-9, 5e-9, 1000)
K = Constants(config)
var["R"] = r
# print all values in dir(K) in a well formatted way
for key in dir(K):
    if not key.startswith('_'):
        print("{:10} = {}".format(key, getattr(K, key)))

for S in [1.1, 1.5, 2, 5, 10]:
    var['S'] = S
    kgr = calc_growth_rate(K, var)
    plt.plot(r, kgr["k_gr"])

plt.show()
