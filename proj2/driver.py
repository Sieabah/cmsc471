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
    Additional - Graph generating
    math - For defining the 2d function
"""
from Additional import create_graph, build_result
from Optimization import Optimization
import math


# THIS IS THE FUNCTION THAT IS USED
def z(_x: float, _y: float) -> float:
    """
    Z-function given a x and y coordinate
    :param _x: x parameter
    :param _y: y parameter
    :return:
    """

    # Example function given
    _r = math.sqrt(_x ** 2 + _y ** 2)
    return math.sin(_x ** 2 + (3 * _y ** 2)) / (0.1 + _r ** 2) + \
           (_x ** 2 + 5 * _y ** 2) * (math.exp(1 - _r ** 2) / 2)


def main():
    """
    Main driver
    :return:
    """

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
    create_graph([{'color': (255, 0, 0), 'points': results['hill_climb']['plot']}], 'Hill Climb', z)
    create_graph(results['hill_climb_random']['plot'], 'Hill climb with restarts', z)
    create_graph(results['simulated_annealing']['plot'], 'Simulated Annealing', z)

    # Make variables smaller
    hc = results['hill_climb']
    hc_res = results['hill_climb_random']
    sa = results['simulated_annealing']

    # Print results
    print('hill climbing', hc['result'], 'time: ', hc['end']-hc['start'])
    print('hill climbing with restarts', hc_res['result'], 'time: ', hc_res['end']-hc_res['start'])
    print('simulated annealing', sa['result'], 'time: ', sa['end']-sa['start'])


main()
