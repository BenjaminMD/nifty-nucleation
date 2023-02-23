import numpy as np


def time_vs_variance(df, ax):
    # Select columns corresponding to particle size R and number of particles P
    R_col = df.columns[df.columns.str.startswith('R')]
    P_col = df.columns[df.columns.str.startswith('P')]

    # Convert particle size to nanometers and extract data as numpy arrays
    R = df[R_col].to_numpy() * 1e9
    P = df[P_col].to_numpy()

    # Only include rows where there are non-zero number of particles
    cnd = P.sum(axis=1) > 0
    R = R[cnd]
    P = P[cnd]

    # Extract time values for plotting
    t = df.t[cnd]

    # Calculate weighted variance of particle size distribution
    weighted_avg = np.average(R, axis=1, weights=P)
    deviation = R - weighted_avg.reshape(-1, 1)
    squared_deviation = deviation**2
    weighted_squared_deviation = P * squared_deviation
    sum_weighted_squared_deviation = np.sum(weighted_squared_deviation, axis=1)
    weighted_var = sum_weighted_squared_deviation / np.sum(P)

    # Plot weighted variance of particle size distribution
    ax.plot(t, weighted_var)
