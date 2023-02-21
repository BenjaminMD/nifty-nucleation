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
    
    agg_sol = solve_agg(**config['rate_const'], **config['sim_params']).sol
    for _ in range(10):
        results = solve_nuc_gr_agg(model, config, agg_sol)
        model.__init__(config)
    
    save_results(results, model, config)


if __name__ == "__main__":
    main()
