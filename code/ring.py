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
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from utils import mkdir


def distance((x, y), (_x, _y)):
    """
    Compute the distance between 2 nodes.
    """
    return math.sqrt((x - _x) ** 2.0 + (y - _y) ** 2.0)


def draw_nodes(_nodes, labels, _range, output_file):
    """
    Plot the topology of the network.
    """

    # extract the coordinates
    xs = map(lambda node: node[0], _nodes)
    ys = map(lambda node: node[1], _nodes)

    # compute some colors
    # noinspection PyUnresolvedReferences
    colors = cm.rainbow(np.linspace(0, 1, len(xs)))

    # create the graph
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, aspect='equal')

    # compute the axes
    a = 0
    min_x = round(min(xs) - a - 1)
    max_x = round(max(xs) + a + 1)
    min_y = round(min(ys) - a - 1)
    max_y = round(max(ys) + a + 1)

    # set the axes
    ax.set_xlim((min_x, max_x))
    ax.set_ylim((min_y, max_y))

    # set labels
    ax.set_title('Network Topology', fontsize=16, y=1.02)
    ax.set_xlabel('X coordinate (m)', fontsize=12, labelpad=10)
    ax.set_ylabel('Y coordinate (m)', fontsize=12, labelpad=10)
    ax.tick_params(axis='both', which='major', labelsize=12)

    # add each point to the graph
    for i, (x, y, c, p) in enumerate(zip(xs, ys, colors, labels)):

        # nodes
        ax.scatter(x, y, s=350, marker='o', edgecolor='black', linewidth=1,
                   facecolor=c, zorder=2)

        # labels
        ax.annotate(i + 1, xy=(x, y), xytext=p, zorder=3, size='large',
                    textcoords='offset points', ha='center', va='center')

        # lines
        for _x, _y in zip(xs, ys):
            if distance((x, y), (_x, _y)) < _range and x < _x:
                ax.plot([x, _x], [y, _y], 'k--', dashes=(5, 3), zorder=1)

    # save the graph
    fig.savefig(output_file, bbox_inches='tight')


def main():
    """
    Generate a modified version of the configuration file given a base one.
    """

    # number of nodes
    n = 10

    # ring radius in meters
    r = 3.0

    nodes = []
    labels = []
    for i in range(n):
        angle = math.radians(360.0 / n * i)
        x = math.sin(angle) * r
        y = math.cos(angle) * r
        nodes.append([x, y])
        labels.append((math.sin(angle) * (r + 20), math.cos(angle) * (r + 20)))

    mkdir('plots')
    draw_nodes(nodes, labels, 10, 'plots/topology.pdf')


# entry point
if __name__ == '__main__':
    main()
