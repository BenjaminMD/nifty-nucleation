from scipy.constants import k, N_A, pi
#from rsc.utils import FloatAttributes


class Constants():
    def __init__(self, config):
        self.k = k * 1e3
        constants = config['const']
        self.rho = constants['rho']
        self.M = constants['M']
        self.eta = constants['eta']
        self.T = constants['T']
        self.gamma = constants['gamma']
        self.Au_sat = constants['Au_sat']
        
        rate_constants = config['rate_const']
        self.k1 = rate_constants['k1']
        self.k_gr = rate_constants['gr']
        self.k_agg = rate_constants['agg']

        self.v_m = self.M / (self.rho * N_A)
        self.R_0 = ((3 * self.v_m) / (4 * pi))**(1/3)
        self.Beta = 4 * self.k * self.T / (9 * self.eta * self.v_m)
        self.R_cap = 2 * self.gamma * self.v_m / (self.k * self.T)
        self.dG = (16 * pi * self.gamma**3 * self.v_m**2) / (self.k**3 * self.T**3)
        self.D = (self.k * self.T) / (6 * pi * self.eta * self.R_0)
        self.A_gr = 4 * pi * self.D * N_A
