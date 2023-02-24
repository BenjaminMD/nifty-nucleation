def time_vs_number(df, ax):
    P_col = df.columns[df.columns.str.startswith("P")]
    P = df[P_col].sum(axis=1)
    t = df.t
    ax.plot(t, P)
