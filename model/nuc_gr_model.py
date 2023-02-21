from model.constants import Constants
from model.setup import Setup
from model.functions import calc_nuc_rate, calc_growth_rate

import numpy as np


class NucleationGrowthModel(Setup):

    def __init__(self, config):
        self.J = 0
        self.K = Constants(config)
        super().__init__(config, self.K)
        self.c['initial'] = config['conc']['initial']

    def model(self, t, y):
        ddt, var, c, K = self.ddt, self.var, self.c, self.K
        c['initial'], c['active'], c['nucleated'], c['amorphus'] \
                = y[0], y[1], y[2], y[3]
        c['grown'] = y[4:-1]
       
        #var = temperature_dependance(t, var)
        var = calc_nuc_rate(K, var, c)
        var = calc_growth_rate(self.prev, K, self.J, c, var)

        # Model: calculation ---------------------------------------
        self.ddt['initial'] = - K.k1 * c['initial']  # precursor react
        self.ddt['nucleated'] = var['k_nuc'] * c['active']  # nucleation
        self.ddt['grown'] = var['k_gr'] * c['active']  # growth
        self.ddt['amorphus'] = + K.a * c['active'] - K.b * c['amorphus']
        self.ddt['active'] = + K.k1 * c['initial'] \
            - K.a * c['active'] \
            + K.b * c['amorphus'] \
            - var['k_nuc'] * c['active']  \
            - np.sum(var['k_gr'] * c['active'])  # active species
        # -----------------------------------------------------------

        values = list(ddt.values())
        return np.concatenate([np.array(values[:-1]), values[-1]])
