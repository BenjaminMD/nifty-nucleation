from typing import Tuple  # type: ignore

from matplotlib.gridspec import GridSpec  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore


def plot_defaults(cols, rows, width_in_cm=15) -> Tuple[plt.Figure, GridSpec]:
    """
    Sets up plot defaults for a grid of subplots.

    Args:
        cols (int): Number of columns in the grid.
        rows (int): Number of rows in the grid.
        width (int, optional): Width of the plot in centimeters. Default is 15.

    Returns:
        Tuple[plt.Figure, GridSpec]: A tuple containing figure and grid spec.
    """
    φ: float = (1 + 5**0.5)/2
    cm_to_in: float = 2.54

    width: float = width_in_cm / cm_to_in
    height: float = width / φ
    github: str = 'https://raw.githubusercontent.com/benjaminmd'
    path: str = f'{github}/mplstyle/main/style.rc'
    plt.style.use(path)

    fig: plt.figure = plt.figure(figsize=(width, height))
    grid_spec: GridSpec = GridSpec(
        cols, rows, figure=fig,
        left=0.15, right=0.85,
        bottom=0.15,  top=0.85,
        wspace=0.05 / φ, hspace=0.05
    )

    return fig, grid_spec


def create_basic_plot(xlabel: str, ylabel: str, title=None):
    fig, gs = plot_defaults(1, 1)
    ax = fig.add_subplot(gs[0, 0])

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)

    return fig, ax


def create_dual_plot(xlabel, y1label, y2label, y2color='red'):
    fig, ax_main = create_basic_plot(xlabel, y1label)
    ax_right = ctwinx(ax_main, y2color, y2label)
    return fig, ax_main, ax_right


def gather_legend(axs):
    handles, labels = zip(*[ax.get_legend_handles_labels() for ax in axs])
    handles = np.concatenate(handles)
    labels = np.concatenate(labels)
    return handles, labels


def ctwinx(ax_main, color, ylabel):
    """Create a twin axis with a colored label.

    Parameters:
    -----------
    ax_main : matplotlib axis object
        The main axis to which the twin axis will be twinned.
    color : str
        The color of the label and tick marks.
    label : str
        The label to be displayed on the twin axis.

    Returns:
    --------
    ax_r : matplotlib axis object
        The twin axis with the specified label and color.
    """
    ax_r = ax_main.twinx()
    ax_r.set_ylabel(ylabel, color=color)
    ax_r.tick_params(axis='y', colors=color)
    return ax_r
