import datetime
import os

from dataclasses import dataclass
from .ezplot import plot_defaults
from .line.time_vs_concentration import time_vs_concentration
from typing import List
import matplotlib.pyplot as plt


@dataclass
class Plot:
    """A class for managing a plot with its properties."""
    name: str
    xlabel: str
    ylabel: str
    plot_func: callable = None

    labels = {
            'time': '$t\,/\,$s',
            'radius': '$r\,/\,$m',
            'conc': '$c\,/\,$mol/m$^3$',
        }


class PlotManager:
    def __init__(self, folder, plots: List[Plot]):
        self.folder = folder
        self.plots = plots

    def single_plot(self, df, plot: Plot):
        """Plot the data using the plot function."""
        if plot.plot_func is not None:
            fig, grid_spec = plot_defaults(1, 1)
            ax = fig.add_subplot(grid_spec[0, 0])
            ax = plot.plot_func(df, ax)
            ax.set_xlabel(plot.labels[plot.xlabel])
            ax.set_ylabel(plot.labels[plot.ylabel])
            return fig
        else:
            print(f"No plot function defined for {plot.name}.")

    def save_plots(self, df):
        for plot in self.plots:
            fig = self.single_plot(df, plot)
            if not fig:
                continue
            fig.savefig(f'./results/{self.folder}/{plot.name}.pdf')
            fig.savefig(f'./results/{self.folder}/{plot.name}.png')

    def __repr__(self):
        repr_str = f"PlotManager with {len(self.plots)} plots:\n\n"
        for plot in self.plots:
            if plot.plot_func is not None:
                repr_str += f"{plot.name}:\n"
                repr_str += f"{' ' * 4}xlabel = {plot.xlabel}\n"
                repr_str += f"{' ' * 4}ylabel = {plot.ylabel}\n"
                repr_str += f"{' ' * 4}plot_func = {plot.plot_func.__name__}\n"
                repr_str += "\n"
        repr_str += f"Saving plots to folder: {self.folder}\n"
        return repr_str

