import numpy as np


class Setup():
    def __init__(self, config, K):
        self.max_cohorts = config['const']['max_cohorts']
        self._zeros = np.zeros(self.max_cohorts*5)
        self.J = 0
        self.K = K

        self.species = ('initial', 'active', 'amorphus', 'nucleated', 'grown')
        self.c = {key: 0 for key in self.species}
        self.c['grown'] = self.zeros()
        self.ddt = {key: 0 for key in self.species}
        self.ddt['grown'] = self.zeros()
         
        self.var = {key: 0 for key in ('S', 'R_crit', 'V_crit', 'k_nuc')} \
            | {key: self.zeros() for key in ('P', 'V', 'R', 'k_gr', 'r_ratio')}
        self.var['t_nuc'] = np.zeros(self.max_cohorts)
        self.var['P_nuc'] = np.zeros(self.max_cohorts)

        self.prev = {key: self.zeros() for key in ('R', 'P', 'grown')}

        self.columns = (
                't', 'S', 
                *self.species[:-1],
                *[f'grown{i}' for i in range(self.max_cohorts*5)],
                *[f'P{i}' for i in range(self.max_cohorts*5)],
                *[f'R{i}' for i in range(self.max_cohorts*5)],
                )

    def zeros(self):
        return self._zeros.copy()
