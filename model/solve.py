from model import apply_agg_avg

from scipy import integrate
from tqdm import tqdm
import numpy as np


def solve_nuc_gr_agg(model, config, agg_sol=None):
    data = []
 
    values = list(model.c.values())
    y0 = np.concatenate([np.array(values[:-1]), values[-1]])
    ode = integrate.RK45(model.model, y0=y0, **config['sim_params'])

    progress_bar = tqdm(total=1e2, mininterval=0.5, unit_scale=True)
    while ode.status == 'running':

        ode.step()
        
        model.var['t_nuc'][model.J] = ode.t
        model.prev['R'] = model.var['R'].copy()
        model.prev['P'] = model.var['P'].copy()
        model.prev['Au0_gr'] = np.array(model.ddt['Au0_gr']).copy()


        paramavg = {
            't': ode.t, 't_old': ode.t_old, 'sol': agg_sol,
        } | {key: model.var[key] for key in ['P', 'P_nuc', 'R', 't_nuc']}
        
        # ---- Aggregation ----
        if agg_sol: model.var['P'], model.var['R'] = apply_agg_avg(**paramavg)
        # ---- Aggregation ----
        
        model.J += 1 if model.var['P'][model.J] > 1e-14 else 0
        if model.J == config['const']['steps']: break

        data.append([
            ode.t, model.var['S'], *ode.y, *model.var['R'], *model.var['P']
        ])

        progress = (ode.t - ode.t_old)
        progress /= config['sim_params']['t_bound']
        progress *= 0.9999e2
        
        progress_bar.update(progress)
    progress_bar.close()
    
    return data
