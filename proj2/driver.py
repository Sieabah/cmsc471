"""
driver.py - Optimization Driver
CMSC 471 - Spring 2016
Author: Christopher Sidell (csidell1@umbc.edu)
ID: JZ28610

driver.py runs optimization hill climb, and simulated annealing
PYTHON VERSION: 3.5.1

Usage: driver.py
"""

from Optimization import Optimization
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def create_graph(plot):
    points = []
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for trial in plot:
        points = trial['points']
        ax.plot_wireframe(X=points['x'],Y=points['y'],Z=points['z'], color=trial['color'])

    plt.show()


def main():
    # Function to optimize
    def z(_x: float, _y: float) -> float:
        # Step function
        _r = math.sqrt(_x ** 2 + _y ** 2)
        return math.sin(_x ** 2 + (3 * _y ** 2)) / (0.1 + _r ** 2) + \
            (_x ** 2 + 5 * _y ** 2) * (math.exp(1 - _r ** 2) / 2)

    #    print(Optimization.hill_climb(z, 0.1))
    result, plot = Optimization.hill_climb(z, 0.1)
    print(result)

    create_graph([{'color': '#000000', 'points': plot}])

    result, plot = Optimization.hill_climb_random_restart(z, 0.1, 5)
    print(result)

    create_graph(plot)

    result, plot = Optimization.simulated_annealing(z, 0.1, 20)
    print(result)

    create_graph(plot)

main()
