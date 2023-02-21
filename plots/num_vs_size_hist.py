def num_vs_size_hist(df, ax):
    R_col = df.columns[df.columns.str.startswith('R')]
    P_col = df.columns[df.columns.str.startswith('P')]

    return P_col, R_col
