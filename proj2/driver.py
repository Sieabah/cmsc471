"""
driver.py - Optimization Driver
CMSC 471 - Spring 2016
Author: Christopher Sidell (csidell1@umbc.edu)
ID: JZ28610

driver.py runs optimization hill climb, and simulated annealing
PYTHON VERSION: 3.5.1

Usage: driver.py

Dependencies:
    Optimization - Optimization algorithms
    math - For defining the 2d function
    mathplotlib & mpl_toolkits - Visual graphs
    time - calculating time
    typing - Python 3.5.x+ typing
"""

from Optimization import Optimization
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from time import time
from typing import Tuple, List
import Additional


def color(tup: Tuple[int, int, int]) -> str:
    """
    Convert rgb tuple to hex
    :param tup: (r,g,b)
    :return:
    """
    return '#%02x%02x%02x' % (tup[0], tup[1], tup[2])


def create_graph(plot: List[dict], title: str) -> None:
    """
    Create a 3D graph of plot data given
    :param plot: expects dictionary {'color' :optional, 'points' :required}
    :param title: Graph title
    :return:
    """
    # Build 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', title=title)
    # For each plot iteration
    for idx, trial in enumerate(plot):
        # Pull out points to variable
        points = trial['points']
        # Add lines
        ax.plot(points['x'], points['y'], points['z'], color=color(trial['color']))

    plt.show()


def build_result(func):
    """
    Build the result set
    :param func: function to get results from
    :return: {'start', 'end', 'result', 'plot'}
    """
    results = dict()
    results['start'] = time()

    result = func()

    results['end'] = time()
    results['result'], results['plot'] = result

    return results


def main():
    """
    Main driver
    :return:
    """
    # Function to optimize
    def z(_x: float, _y: float) -> float:
        """
        Function
        :param _x: x parameter
        :param _y: y parameter
        :return:
        """
        # Example function given
        _r = math.sqrt(_x ** 2 + _y ** 2)
        return math.sin(_x ** 2 + (3 * _y ** 2)) / (0.1 + _r ** 2) + \
            (_x ** 2 + 5 * _y ** 2) * (math.exp(1 - _r ** 2) / 2)

    Additional.genGraph(z)

    # Variables to define
    # How far should each step be
    step_size = 0.1
    # How many restarts should be calculated
    restarts = 20
    # Max temperature
    max_temperature = 50

    # Result holder
    results = dict(hill_climb={}, hill_climb_random={}, simulated_annealing={})

    # Run tests
    print('Running hill climb...', end='')
    results['hill_climb'] = build_result(lambda: Optimization.hill_climb(z, step_size))
    print(' DONE')

    print('Running hill climb with restart...', end='')
    results['hill_climb_random'] = build_result(lambda: Optimization.hill_climb_random_restart(z, step_size, restarts))
    print(' DONE')

    print('Running simulated annealing...', end='')
    results['simulated_annealing'] = build_result(lambda: Optimization.simulated_annealing(z, step_size, max_temperature))
    print(' DONE')

    # Create the graphs
    create_graph([{'color': (0, 0, 0), 'points': results['hill_climb']['plot']}], 'Hill Climb')
    create_graph(results['hill_climb_random']['plot'], 'Hill climb with restarts')
    create_graph(results['simulated_annealing']['plot'], 'Simulated Annealing')

    # Make variables smaller
    hc = results['hill_climb']
    hc_res = results['hill_climb_random']
    sa = results['simulated_annealing']

    # Print results
    print('hill climbing', hc['result'], 'time: ', hc['end']-hc['start'])
    print('hill climbing with restarts', hc_res['result'], 'time: ', hc_res['end']-hc_res['start'])
    print('simulated annealing', sa['result'], 'time: ', sa['end']-sa['start'])


main()
