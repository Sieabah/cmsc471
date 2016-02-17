"""
Optimization.py - Optimization functions
CMSC 471 - Spring 2016
Author: Christopher Sidell (csidell1@umbc.edu)
ID: JZ28610

Holds all the different optimization functions
"""
from typing import Callable, Dict
from enum import Enum
from random import uniform, randint
import math


class Direction(Enum):
    left = -1
    equal = 0
    right = 1


class Optimization:
    @staticmethod
    def rand_coords(step_size) -> Dict[str, float]:
        """
        Returns random x,y coordinates between 1/step_size
        :param step_size
        :return:
        """
        return {'x': uniform(0, 1/step_size), 'y': uniform(0, 1/step_size)}

    @staticmethod
    def get_direction(left: float, current: float, right: float) -> Direction:
        """
        Get direction for basic hill climbing
        :param left: left value
        :param current: current value
        :param right: right value
        :return: Direction to go
        """
        # Right greater than current
        if right > current:
            # Is right greater than left
            if right > left:
                # Confirmed right is highest
                return Direction.right

        # Knowing right is less than current or right is less than left

        # Is left greater than current?
        if left > current:
            # Found the direction
            return Direction.right

        # Found max
        return None

    @staticmethod
    def calculate_func_at_degree(func: Callable[[float, float], float], step_size: float, x: float, y: float, deg: int) -> float:
        """

        :param func:
        :param step_size:
        :param x:
        :param y:
        :param deg:
        :return:
        """
        rad = math.radians(deg)
        local_x = x+math.cos(rad)*step_size
        local_y = y+math.sin(rad)*step_size
        return local_x, local_y, func(local_x, local_y)

    @staticmethod
    def get_highest(func: Callable[[float, float], float], step_size: float, x: float, y: float, divisions: int = 1):
        """

        :param func:
        :param step_size:
        :param x:
        :param y:
        :param divisions:
        :return:
        """
        highest = func(x, y)
        max_x = x
        max_y = y

        for deg in range(math.ceil(360/divisions)):
            local_x, local_y, curr = Optimization.calculate_func_at_degree(func, step_size, x, y, deg)
            if curr >= highest:
                highest = curr
                max_x = local_x
                max_y = local_y

        if max_x == x and max_y == y:
            return None

        return max_x, max_y, highest

    @staticmethod
    def color(r: int = None, g: int = None, b: int = None) -> str:
        """

        :param r:
        :param g:
        :param b:
        :return:
        """
        r = r if r else randint(0, 255)
        g = g if g else randint(0, 255)
        b = b if b else randint(0, 255)

        return '#%02x%02x%02x' % (r, g, b)

    @staticmethod
    def hill_climb(func: Callable[[float, float], float], step_size: float, start_x: float = None, start_y: float = None):
        """
        Generalize hill climb algorithm
        :param func: function to call
        :param step_size: how big is the step
        :param start_x: starting x
        :param start_y: starting y
        :return:
        """
        if start_x is None:
            start_x = 0
        if start_y is None:
            start_y = 0

        x = start_x
        y = start_y

        # Start with empty plot
        plotgraph = {
            'x': [],
            'y': [],
            'z': []
        }

        # Fill our first point
        plotgraph['x'].append(x)
        plotgraph['y'].append(y)
        plotgraph['z'].append(func(x, y))

        # CLIMB
        while True:
            # Get the highest
            result = Optimization.get_highest(func, step_size, x, y)

            # If result is none, we're at the peak
            if result is None:
                return func(x, y), plotgraph

            # Unwrap the variables
            x, y, z = result

            # Push to plot
            plotgraph['x'].append(x)
            plotgraph['y'].append(y)
            plotgraph['z'].append(z)

        # If we got to this point we're at the peak from the start
        return None, plotgraph


    @staticmethod
    def hill_climb_random_restart(func: Callable[[float, float], float], step_size: float, num_restarts: int):
        """
        Hill climbing with random restarts
        :param func: function to call
        :param step_size: step size
        :param num_restarts: how many times to restart
        :return:
        """

        def attempt():
            """
            Attempt a hill climb with random starting points
            :return:
            """
            coords = Optimization.rand_coords(step_size)
            return Optimization.hill_climb(func, step_size, coords.get('x', 0), coords.get('y', 0))

        total_max = None

        graphPlots = []

        # +1 to always run once
        for n in range(num_restarts+1):
            tmp, plot = attempt()

            graphPlots.append({'color': Optimization.color(), 'points': plot})

            # Get total max
            if total_max is None or tmp > total_max:
                total_max = tmp

        return total_max, graphPlots

    @staticmethod
    def annealing_probability(current: float, other: float, temp: float) -> float:
        """
        Probability function
        :param current: current value
        :param other: other value
        :param temp: temperature
        :return:
        """

        # If it's greater
        if other >= current:
            return 1.0

        if temp == 0:
            return 0

        return math.exp((other - current)/temp)

    # TODO: Make this work correctly
    @staticmethod
    def simulated_annealing(func: Callable[[float, float], float], step_size: float, max_temp: float) -> float:
        """
        Simulated annealing
        :param func: function to call
        :param step_size: step size
        :param max_temp: max temperature
        :return:
        """

        total_max = func(0, 0)

        plotgraph = []

        # for max_temp times
        for i in range(max_temp):
            temp = max_temp
            coords = Optimization.rand_coords(step_size)

            x = coords.get('x', 0)
            y = coords.get('y', 0)

            left = lambda: func(x-step_size, y-step_size)
            current = lambda: func(x, y)
            right = lambda: func(x+step_size, y+step_size)

            plotgraph.append({
                'color': Optimization.color(),
                'points': {
                    'x': [],
                    'y': [],
                    'z': []
                }
            })

            # while temp
            while temp > 0:
                curr = current()
                plotgraph[len(plotgraph)-1]['points']['x'].append(x)
                plotgraph[len(plotgraph)-1]['points']['y'].append(y)
                plotgraph[len(plotgraph)-1]['points']['z'].append(curr)

                if curr > total_max:
                    total_max = curr

                # Go in a random direction
                local_x, local_y, nxt = Optimization.calculate_func_at_degree(func, step_size, x, y, randint(0, 360))

                # get probability of both sides
                probability = Optimization.annealing_probability(curr, nxt, temp)

                threshold = uniform(0, 1)

                # Determine which side is better
                if probability > threshold:
                    x = local_x
                    y = local_y
                else:
                    continue

                # Decrement temperature
                temp -= 0.1





        return total_max, plotgraph
