"""
Classical nucleation and growth with aggregation using RK45. Kinetic model
and config file generate solution. Aggregation averaging keeps species low.

Author: Benjamin Fahl
"""
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
from ezplot import plot_defaults

from model import NucleationGrowthModel, solve_agg, solve_nuc_gr_agg
from rsc.utils import read_config, read_results, save_results


def number_vs_size(df, ax):
    R_col = df.columns[df.columns.str.startswith("R")]
    P_col = df.columns[df.columns.str.startswith("P")]

    df = df.iloc[-1]
    P = df[P_col].to_numpy()
    P = P / P.sum()
    R = df[R_col].to_numpy() * 1e9

    ax.hist(R, bins=20, weights=P, alpha=0.5, label="Size distribution")

    return ax


def compute_average_size(R, P):
    total = 0
    sum_of_products = 0
    for i in range(len(R)):
        total += P[i]
        sum_of_products += R[i] * P[i]
    average_size = sum_of_products / total
    return average_size


def e_gr(e_grs):
    mean_diameter = []
    for e in e_grs:
        config = read_config()
        config["activation"]["E_gr"] = e
        model = NucleationGrowthModel(config)
        agg_sol = solve_agg(agg=model.K.k_agg, **config["sim_params"]).sol
        results = solve_nuc_gr_agg(model, config)
        save_results(results, model, config)
        file_paths = glob("./results/*/*.h5")
        file_paths.sort()
        df = read_results(file_paths[-1])
        R_col = df.columns[df.columns.str.startswith("R")]
        P_col = df.columns[df.columns.str.startswith("P")]

        df = df.iloc[-1]
        P = df[P_col].to_numpy()
        P = P / P.sum()
        R = df[R_col].to_numpy() * 1e9
        mean_diameter.append(compute_average_size(R, P))
    return mean_diameter


def run_model():
    config = read_config()
    model = NucleationGrowthModel(config)
    
    agg_sol = solve_agg(agg=model.K.k_agg, **config["sim_params"]).sol
    results = solve_nuc_gr_agg(model, config, agg_sol)
    save_results(results, model, config)
    file_paths = glob("./results/*/*.h5")
    file_paths.sort()
    df = read_results(file_paths[-1])

    fig, gs = plot_defaults(1, 1)
    ax = fig.add_subplot(gs[0])
    number_vs_size(df, ax)
    plt.show()


def main():
    config = read_config('config.toml') ##either give here a path to the toml config file or leave empty if it is in the same directory
    model = NucleationGrowthModel(config) ##initialize the model with the starting parameters
    print(model.K.k_agg)
    agg_sol = solve_agg(agg=0, **config['sim_params']).sol
    results = solve_nuc_gr_agg(model, config, agg_sol)
    save_results(results, model, config)

if __name__ == "__main__":
    main()
