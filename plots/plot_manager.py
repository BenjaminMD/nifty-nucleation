import datetime
import os

from dataclasses import dataclass
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

from .ezplot import plot_defaults, ctwinx, create_basic_plot, create_dual_plot, gather_legend

from .line.time_vs_concentration import time_vs_concentration
from .line.time_vs_saturation import time_vs_saturation
from .line.time_vs_variance import time_vs_variance
from .line.time_vs_size import time_vs_size
from .hist.number_vs_size import number_vs_size
from .scatter.number_vs_size_scatter import number_vs_size_scatter


class Plot:
    def __init__(self, df: pd.DataFrame):
        self.df = df

        self.axlabels = {
            'time': r'$t\,/\,$s',
            'radius': r'$r\,/\,$m',
            'conc': r'$c\,/\,$mol/m$^3$',
            'sat': r'$S\,/\,$-',
        }

    def particle_size_dist_plot(self):
        fig, ax = create_basic_plot(
            self.axlabels['radius'],
            self.axlabels['conc'])
        ax = number_vs_size(self.df, ax)
        ax = number_vs_size_scatter(self.df, ax)
        handles, labels = gather_legend([ax])
        ax.legend(handles, labels, loc='upper left')
        return fig, ax

    def time_conc_sat_plot(self):
        fig, ax_main, ax_right = create_dual_plot(
            self.axlabels['time'],
            self.axlabels['conc'],
            self.axlabels['sat'],
            'red')
        ax_main = time_vs_concentration(self.df, ax_main)
        ax_right = time_vs_saturation(self.df, ax_right, 'red')
        handles, labels = gather_legend([ax_main, ax_right])
        ax_main.legend(handles, labels, loc='upper right')
        self.axs = [ax_main, ax_right]
        return fig, [ax_main, ax_right]

    def time_size_dist_variance_plot(self):
        fig, ax_main, ax_right = create_dual_plot(
            self.axlabels['conc'],
            self.axlabels['radius'],
            self.axlabels['radius'],
            'red')
        ax_main = time_vs_variance(self.df, ax_main)
        ax_right = time_vs_size(self.df, ax_right, 'red')
        handles, labels = gather_legend([ax_main, ax_right])
        ax_main.legend(handles, labels, loc='upper left')
        return fig, ax_main
