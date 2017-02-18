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

import utils
import pandas


def throughput(path, name):
    """
    Load the result of a single simulation.
    :param path: H5 file to load (relative location).
    :param name: Name of the simulation.
    :return: Triple <load, throughput, name>.
    """

    # load statistics
    statistics = pandas.read_hdf(utils.locate(path), 'summary')
    assert len(statistics.id.unique()) == 1

    # extract the wanted data
    load = list(statistics.load)
    tr = list(statistics.tr)

    # return the triple
    return load, tr, name


def collisions(path, name):
    """
    Load the collision rate of a single simulation.
    :param path: H5 file to load (relative location).
    :param name: Name of the simulation.
    :return: Triple <load, collision rate, name>.
    """

    # load statistics
    statistics = pandas.read_hdf(utils.locate(path), 'summary')
    assert len(statistics.id.unique()) == 1

    # extract the wanted data
    load = list(statistics.load)
    cr = list(statistics.cr)

    # return the triple
    return load, cr, name
