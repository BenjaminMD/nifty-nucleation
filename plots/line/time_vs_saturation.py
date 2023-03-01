
"""
plot of time vs saturation, showing the actual Nucleation Growth model
"""
import numpy as np


def time_vs_saturation(df, ax):
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