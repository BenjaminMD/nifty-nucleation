
"""
plot of time vs saturation, showing the actual Nucleation Growth model
"""
import numpy as np


def time_vs_saturation(df, ax):

    Au0_gr_col = df.columns[df.columns.str.startswith('grown')]
    df['grown'] = df[Au0_gr_col].sum(axis=1)
    Au0_nuc_max = df['nucleated'].max()
    expnt = np.floor(np.log10(abs(Au0_nuc_max)))
    df['nucleated'] *= 10**-(expnt+1)

    config = {
    'S':
         {'label': r'$S$', 'linestyle': '--'},
    }
    for species, species_style in config.items():
        ax.plot(df.t, df[species], **species_style)
    ax.set_xlim(df.t.iloc[0], df.t.iloc[-1])
    ax.set_ylim(0, df['S'].max())
    ax.legend(loc='center right')

    return ax