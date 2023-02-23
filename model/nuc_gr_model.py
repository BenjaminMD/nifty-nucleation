from model.constants import Constants
from model.setup import Setup
from model.functions import calc_nuc_rate, calc_growth_rate

import numpy as np


class NucleationGrowthModel(Setup):
    def __init__(self, config):
        self.J = 0
        self.K = Constants(config)
        super().__init__(config, self.K)
        self.c["Au+"] = config["conc"]["Au+"]
        self.c["B"] = config["conc"]["B"]

    def model(self, t, y):
        ddt, var, c, K = self.ddt, self.var, self.c, self.K
        c["Au+"], c["B"], c["Au0"], c["Au0_nuc"] = y[0], y[1], y[2], y[3]
        c["Au0_gr"] = y[5:-1]

        var = calc_nuc_rate(K, var, c)
        var = calc_growth_rate(self.prev, K, self.J, c, var)

        # Model: calculation ---------------------------------------
        self.ddt["Au+"] = -K.k1 * c["Au+"] * c["B"]  # precursor react
        self.ddt["B"] = -K.k1 * c["Au+"] * c["B"]  # precursor react
        self.ddt["Au0_nuc"] = var["k_nuc"] * c["Au0"]  # nucleation
        self.ddt["Au0_gr"] = var["k_gr"] * c["Au0"]  # growth
        self.ddt["Au0"] = (
            +K.k1 * c["Au+"] * c["B"]
            - var["k_nuc"] * c["Au0"]
            - np.sum(var["k_gr"] * c["Au0"])
        )  # active species
        # -----------------------------------------------------------

        values = list(ddt.values())
        return np.concatenate([np.array(values[:-1]), values[-1]])
