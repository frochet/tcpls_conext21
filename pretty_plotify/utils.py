"""
Utils functions and wrappers for processing and plotting statistics

__author__  = "Benoit Donnet (ULiege -- Institut Montefiore)"
__version__ = "1.0"
__date__    = "14/01/2021"
"""

from pylab import *
from matplotlib.font_manager import *
import numpy as np

rc('text', usetex=True)
rc('font',family='Times New Roman')
rc('xtick', labelsize='40')
rc('ytick', labelsize='40')
rc('lines', markersize=10)
rc('legend', numpoints=1)

"""
Font dictionary.

Used by (nearly) every plotting functions
"""
font = {
    'fontname'   : 'DejaVu Sans',
    'color'      : 'k',
    'fontsize'   : 30
       }
"""
Defines various linestyles for plotting

How to:
plot(..., ls=linestyles['dotted'])

Taken from https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html
"""
linestyle_tuple = [
     ('solid', (0, ())),
     ('loosely dotted',        (0, (1, 10))),
     ('dotted',                (0, (1, 1))),
     ('densely dotted',        (0, (1, 1))),

     ('loosely dashed',        (0, (5, 10))),
     ('dashed',                (0, (5, 5))),
     ('densely dashed',        (0, (5, 1))),

     ('loosely dashdotted',    (0, (3, 10, 1, 10))),
     ('dashdotted',            (0, (3, 5, 1, 5))),
     ('densely dashdotted',    (0, (3, 1, 1, 1))),

     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))]

linestyles = dict(linestyle_tuple)

def latex_label(s):
    """
    Format String for LaTeX style (axis label)
    """
    return r'\textrm{\textbf{' + s + '}}'

def legend_label(s):
    """
    Format String for LaTeX style (ticks/legend label)
    """
    return r'\textrm{' + s + '}'

def axis_aesthetic(ax, spine_position=10, axis_width=0.25, label_size=20, tick_length=4, tick_width=2):
    """
    General aesthetic of the plot.
    Args:
        ax: plot axis
        spine_position: space between the axis and the graph itself (10 by default)
        label_size: ticks label size (20 by default)
        tick_length: tick length (4 by default)
        tick_width: tick width (2 by default)
    """
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['left'].set_position(('outward', spine_position))
    ax.spines['bottom'].set_position(('outward', spine_position))

    ax.spines['left'].set_linewidth(axis_width)
    ax.spines['bottom'].set_linewidth(axis_width)

    ax.tick_params(axis='both', which='major', labelsize=label_size)

    ax.tick_params(direction='inout', length=tick_length, width=tick_width)
