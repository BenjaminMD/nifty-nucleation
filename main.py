"""
Classical nucleation and growth with aggregation using RK45. Kinetic model
and config file generate solution. Aggregation averaging keeps species low.

Author: Benjamin Fahl
"""
from model import NucleationGrowthModel, solve_agg, solve_nuc_gr_agg 
from rsc.utils import read_config, save_results

import numpy as np

def main():
    config = read_config()
    model = NucleationGrowthModel(config)
    model.K.k_agg
    agg_sol = solve_agg(agg=model.K.k_agg, **config['sim_params']).sol
    results = solve_nuc_gr_agg(model, config, agg_sol)
    model.__init__(config)
    
    save_results(results, model, config)


if __name__ == "__main__":
    main()
