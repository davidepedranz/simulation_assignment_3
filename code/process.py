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
import functools
import plot
import numpy
import simulations


def lambda_from_load(load, n_nodes=10.0, packet_size=(1460 + 32) / 2):
    """
    Compute the lambda for a single station for a given total load (Mbps).
    """
    return float(load) / (n_nodes * packet_size * 8.0 / 1024 / 1024)


def tr_theoretical(load, tx_rate=8.0):
    """
    Compute the theoretical throughput for Aloha.
    tx_rate is the transmission rate in Mbps.
    """
    normalized_load = load / tx_rate
    return normalized_load * math.e ** (-2 * normalized_load) * tx_rate


def tr_mc_simple(_lambda, n=10, tx_rate=8.0, s=746.0):
    """
    Compute the throughput for Aloha using the first CTMC model.
    n is the number of nodes, tx_rate is the transmission rate in Mbps.
    """
    mu = tx_rate * 1000000.0 / (s * 8)
    return n * _lambda * (mu ** (n - 1)) * tx_rate / ((_lambda + mu) ** n) * (
        n - 1) / n


def tr_mc_1g1b(_lambda, n=10, tx_rate=8.0, s=746.0):
    """
    Compute the throughput for Aloha using the second CTMC model.
    n is the number of nodes, tx_rate is the transmission rate in Mbps.
    """
    mu = tx_rate * 1000000.0 / (s * 8)
    return tx_rate * n * _lambda * (mu ** n) / (
        ((_lambda + mu) ** n) * ((n - 1) * _lambda + mu)) * (n - 1) / n


def cr_mc_simple(_lambda, n=10, tx_rate=8.0, s=746.0):
    """
    Compute the collision rate for Aloha using the first CTMC model.
    n is the number of nodes, tx_rate is the transmission rate in Mbps.
    """
    mu = tx_rate * 1000000.0 / (s * 8)

    def pi(j):
        return math.factorial(n) / math.factorial(n - j) / math.factorial(j) * (
            _lambda ** j) * (mu ** (n - j)) / ((_lambda + mu) ** n)

    c = functools.reduce(lambda ac, i: pi(i) + ac, range(2, n + 1), 0)
    tot = functools.reduce(lambda ac, i: pi(i) + ac, range(1, n + 1), 0)
    return c / tot


def cr_mc_1g1b(_lambda, n=10, tx_rate=8.0, s=746.0):
    """
    Compute the collision rate for Aloha using the second CTMC model.
    n is the number of nodes, tx_rate is the transmission rate in Mbps.
    """
    mu = tx_rate * 1000000.0 / (s * 8)

    def pi(j):
        return math.factorial(n) / math.factorial(n - j) / math.factorial(j) * (
            _lambda ** j) * (mu ** (n - j)) / ((_lambda + mu) ** n)

    def pi_1b():
        return n * (n - 1) * (_lambda ** 2) * (mu ** (n - 1)) / (
            ((_lambda + mu) ** n) * (mu + (n - 1) * _lambda))

    c = functools.reduce(lambda ac, i: pi(i) + ac, range(2, n + 1), pi_1b())
    tot = functools.reduce(lambda ac, i: pi(i) + ac, range(1, n + 1), 0)
    return c / tot


def compute_model(n, model, name='unknown'):
    """
    Computes the given model for n stations.
    Returns a triple <load, throughput, name>
    """
    loads = [0.2] + range(1, 10, 1) + range(11, 50, 2)  # TODO!
    lambdas = map(lambda load: lambda_from_load(load, n), loads)
    tr = map(lambda l: model(l, n), lambdas)
    return loads, tr, name


def compute_model_theoretic():
    """
    Compute the theoretical model for Aloha.
    """
    loads = list(numpy.arange(0.5, 10, 0.5)) + range(11, 50, 1)
    return loads, map(tr_theoretical, loads), 'Theoretic'


def main():
    """
    Generate a plot to compare the different models.
    """

    # theoretic model
    theoretic = compute_model_theoretic()

    # tr first model
    tr_simple_5 = compute_model(5, tr_mc_simple, 'Model 1 (n=5)')
    tr_simple_10 = compute_model(10, tr_mc_simple, 'Model 1 (n=10)')
    tr_simple_15 = compute_model(15, tr_mc_simple, 'Model 1 (n=15)')

    # tr second model
    tr_complex_5 = compute_model(5, tr_mc_1g1b, 'Model 2 (n=5)')
    tr_complex_10 = compute_model(10, tr_mc_1g1b, 'Model 2 (n=10)')
    tr_complex_15 = compute_model(15, tr_mc_1g1b, 'Model 2 (n=15)')

    # tr simulations
    tr_simulator_5 = simulations.throughput('runs/summary_aloha_5.h5',
                                            'Simulator (n=5)')
    tr_simulator_10 = simulations.throughput('runs/summary_aloha_10.h5',
                                             'Simulator (n=10)')
    tr_simulator_15 = simulations.throughput('runs/summary_aloha_15.h5',
                                             'Simulator (n=15)')
    # compare 10 nodes
    plot.throughput([tr_simulator_10, tr_simple_10, tr_complex_10, theoretic],
                    'plots', name='tr_10')

    # compare model 2
    plot.throughput([tr_complex_5, tr_complex_10, tr_complex_15, theoretic],
                    'plots', name='tr_1g1b', y_lim=(0, 2))

    # throughput all models
    plot.throughput([
        theoretic,
        tr_simulator_5,
        tr_simulator_10,
        tr_simulator_15,
        tr_simple_5,
        tr_simple_10,
        tr_simple_15,
        tr_complex_5,
        tr_complex_10,
        tr_complex_15
    ], 'plots', name='tr_all', x_lim=(0, 30), y_lim=(0, 3.5), dim=(20, 12))

    # cr simple model
    cr_simple_5 = compute_model(5, cr_mc_simple, 'Model 1 (5 stations)')
    cr_simple_10 = compute_model(10, cr_mc_simple, 'Model 1')
    cr_simple_15 = compute_model(15, cr_mc_simple, 'Model 1 (15 stations')

    # cr complex model
    cr_1b1g_5 = compute_model(5, cr_mc_1g1b, 'Model 2 (5 stations)')
    cr_1b1g_10 = compute_model(10, cr_mc_1g1b, 'Model 2')
    cr_1b1g_15 = compute_model(15, cr_mc_1g1b, 'Model 2 (15 stations')

    # cr simulations
    cr_simulator_5 = simulations.collisions('runs/summary_aloha_5.h5',
                                            'Simulator (5 stations)')
    cr_simulator_10 = simulations.collisions('runs/summary_aloha_10.h5',
                                             'Simulator')
    cr_simulator_15 = simulations.collisions('runs/summary_aloha_15.h5',
                                             'Simulator (15 stations)')

    # collisions - all models
    plot.collisions([
        cr_simple_5,
        cr_simple_10,
        cr_simple_15,
        cr_1b1g_5,
        cr_1b1g_10,
        cr_1b1g_15,
        cr_simulator_5,
        cr_simulator_10,
        cr_simulator_15
    ], 'plots', 'cr_all')

    # collisions - comparison for 10 stations
    plot.collisions([
        cr_simulator_10,
        cr_simple_10,
        cr_1b1g_10
    ], 'plots', 'cr_10')


# entry point
if __name__ == '__main__':
    main()
