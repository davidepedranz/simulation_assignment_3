# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2017 Davide Pedranz <davide.pedranz@gmail.com>

import math
import itertools
import matplotlib as mpl
from pandas import Categorical
from utils import mkdir

mpl.use('Agg')
import matplotlib.pyplot as plt


def _plot(traces, _dir, name, title, loc, label_x, label_y, x_lim=(0, 50),
          y_lim=(0, 4), dim=(8, 6)):
    """
    Generate a plot of the given traces to include in the report.
    """

    # generate 2 formats, 1 for LaTeX, 1 for visualization
    for ext in ['png', 'pdf']:

        # make sure the destination exits
        mkdir(_dir)

        # create the figure
        figure = plt.figure(figsize=dim, dpi=80)
        ax = figure.add_subplot(111)

        # plots
        marker = itertools.cycle((',', '>', 's', 'x', 'o', 'd', '<'))
        for (load, tr, legend) in traces:
            ax.plot(load, tr, label=legend, marker=marker.next())

        # labels
        ax.legend(shadow=True, loc=loc, borderpad=0.8, fontsize='large')
        ax.set_title(title, fontsize=20, y=1.02)
        ax.set_xlabel(label_x, fontsize=12, labelpad=10)
        ax.set_ylabel(label_y, fontsize=12, labelpad=10)
        ax.tick_params(axis='both', which='major', labelsize=12)

        # axes
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        ax.grid(True)

        # save plot
        figure.savefig(_dir + '/' + name + '.' + ext, bbox_inches='tight')
        plt.close(figure)


def throughput(traces, _dir, name, x_lim=(0, 50), y_lim=(0, 3.5), dim=(8, 6)):
    """
    Generate a plot for the throughput.
    """
    _plot(traces, _dir, name, 'Throughput', 'upper right',
          'Total offered load on the channel (Mbps)',
          'Average throughput at receiver (Mbps)', x_lim, y_lim, dim)


def collisions(traces, _dir, name, x_lim=(0, 50), dim=(8, 6)):
    """
    Generate a plot for the collision rate.
    """
    _plot(traces, _dir, name, 'Collision rate', 'lower right',
          'Total offered load on the channel (Mbps)',
          'Packets collision rate', x_lim, (0, 1), dim)
