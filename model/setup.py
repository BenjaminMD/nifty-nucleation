import numpy as np


class Setup():
    def __init__(self, config, K):
        self.steps = config['const']['steps']
        self._zeros = np.zeros(self.steps*5)
        self.J = 0
        self.K = K

        self.species = ('Au+', 'B', 'Au0', 'Au0_nuc', 'Au0_gr')
        self.c = {key: 0 for key in self.species}
        self.c['Au0_gr'] = self.zeros()
        self.ddt = {key: 0 for key in self.species}
        self.ddt['Au0_gr'] = self.zeros()
         
        self.var = {key: 0 for key in ('S', 'R_crit', 'V_crit', 'k_nuc')} \
            | {key: self.zeros() for key in ('P', 'V', 'R', 'k_gr', 'r_ratio')}
        self.var['t_nuc'] = np.zeros(self.steps)
        self.var['P_nuc'] = np.zeros(self.steps)

        self.prev = {key: self.zeros() for key in ('R', 'P', 'Au0_gr')}

        self.columns = (
                't', 'S', 
                *self.species[:-1],
                *[f'Au0_gr{i}' for i in range(self.steps*5)],
                *[f'P{i}' for i in range(self.steps*5)],
                *[f'R{i}' for i in range(self.steps*5)],
                )

    def zeros(self):
        return self._zeros.copy()
