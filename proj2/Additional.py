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
    matplotlib & mpl_toolkits - Visual graphs
    matplotlib cm - Color mapping
    time - calculating time
    typing - Python 3.5.x+ typing
    numpy - Range generation with decimals
"""
from typing import Callable, Tuple, List
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from time import time
import numpy as np


def color(tup: Tuple[int, int, int]) -> str:
    """
    Convert rgb tuple to hex
    :param tup: (r,g,b)
    :return:
    """

    return '#%02x%02x%02x' % (tup[0], tup[1], tup[2])


def create_graph(plot: List[dict], title: str, func: Callable[[float, float], float]) -> None:
    """
    Create a 3D graph of plot data given
    :param plot: expects dictionary {'color' :optional, 'points' :required}
    :param title: Graph title
    :return:
    """

    # Build 3D graphgenGraph
    fig, ax = build(func, title, showgraph=True)

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


def build(func: Callable[[float, float], float]=None, title: str='', showgraph: bool=False, graphsize: int=10) -> Tuple:
    """
    Build the graph with horribly optimized generation
    :param func: function to determine z value
    :param title: title of graph
    :param showgraph: Show the graph of the function
    :param graphsize: The range of the graph (-size, -size) to (size, size)
    :return:
    """
    # Build 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', title=title)

    if showgraph:
        plot = {
            'x': [],
            'y': [],
            'z': []
        }

        #Generate 3d-graph plot
        for x in np.arange(-graphsize, graphsize, 0.1):
            plot['x'].append([])
            plot['y'].append([])
            plot['z'].append([])
            for y in np.arange(-graphsize, graphsize, 0.1):
                plot['x'][-1].append(x)
                plot['y'][-1].append(y)
                plot['z'][-1].append(func(x, y))

        ax.plot_surface(plot['x'], plot['y'], plot['z'], cmap=cm.RdGy, alpha=0.3)

    return fig, ax
