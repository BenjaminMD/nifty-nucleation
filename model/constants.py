from scipy.constants import k, N_A, pi, R
import numpy as np


class Constants():
    def __init__(self, config):
        self.k = k * 1e3
        constants = config['const']
        self.rho = constants['rho']
        self.M = constants['M']
        self.eta = constants['eta']
        self.T = constants['T']
        self.gamma = constants['gamma']

        self.v_m = self.M / (self.rho * N_A)
        self.R_0 = ((3 * self.v_m) / (4 * pi))**(1/3)
        self.Beta = 4 * self.k * self.T / (9 * self.eta * self.v_m)
        self.R_cap = 2 * self.gamma * self.v_m / (self.k * self.T)
        self.dG = (16 * pi * self.gamma**3 * self.v_m**2) / (self.k**3 * self.T**3)
        self.D = (self.k * self.T) / (6 * pi * self.eta * self.R_0)
        self.A_gr = 4 * pi * self.D * N_A

        act = config['activation']
        self.k1 = act['k_10'] * np.exp(- act['E_1'] / (R * 1e-3 * self.T))
        self.k_agg = act['k_agg0'] * np.exp(- act['E_agg'] / (R * 1e-3 * self.T))
        self.k_gr = act['k_gr0'] * np.exp(- act['E_gr'] / (R * 1e-3 * self.T))
        self.Au_sat = act['k_sol0'] \
            * np.exp(- act['E_sol'] / (R * 1e-3 * self.T))
        


