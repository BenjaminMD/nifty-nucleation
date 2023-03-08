def number_vs_size_scatter(df, ax):
    R_col = df.columns[df.columns.str.startswith("R")]
    P_col = df.columns[df.columns.str.startswith("P")]

    df = df.iloc[-1]
    P = df[P_col].to_numpy()
    P = P / P.sum()
    R = df[R_col].to_numpy() * 1e9

    ax.scatter(R, P, label="Particle Size")

    return ax