"""
Optimization.py - Optimization functions
CMSC 471 - Spring 2016
Author: Christopher Sidell (csidell1@umbc.edu)
ID: JZ28610

Holds all the different optimization functions
"""
from typing import Callable, Dict, Tuple, List
from random import uniform, randint
import math


class Optimization:
    @staticmethod
    def rand_coords(step_size) -> Dict[str, float]:
        """
        Returns random x,y coordinates between 1/step_size
        :param step_size
        :return:
        """
        return {'x': uniform(-1/step_size, 1/step_size), 'y': uniform(-1/step_size, 1/step_size)}

    @staticmethod
    def calculate_func_at_degree(func: Callable[[float, float], float], step_size:
                float, x: float, y: float, deg: int) -> Tuple[float, float, float]:
        """
        Calculate the next value given center, radius, and degree
        :param func: function that has a value
        :param step_size: radius
        :param x:
        :param y:
        :param deg: degree location
        :return:
        """
        rad = math.radians(deg)
        local_x = x+math.cos(rad)*step_size
        local_y = y+math.sin(rad)*step_size
        return local_x, local_y, func(local_x, local_y)

    @staticmethod
    def get_highest(func: Callable[[float, float], float], step_size: float, x: float,
                    y: float, divisions: int = 1) -> Tuple[float, float, float]:
        """
        Get highest value looking around the center step_size away (360 degrees default)
        :param func: Function to determine value
        :param step_size: distance away
        :param x: center-x
        :param y: center-y
        :param divisions: How many divisions of the circle
        :return: max_x, max_y, highest
        """
        highest = func(x, y)
        max_x = x
        max_y = y

        # For entire range 0 - 360
        for deg in range(math.ceil(360/divisions)):
            local_x, local_y, curr = Optimization.calculate_func_at_degree(func, step_size, x, y, deg)
            if curr >= highest:
                highest = curr
                max_x = local_x
                max_y = local_y

        # If max_x or max_y didn't change we didn't move
        if max_x == x and max_y == y:
            return None

        # Return new x, y, and resulting value
        return max_x, max_y, highest

    @staticmethod
    def color(r: int = None, g: int = None, b: int = None) -> Tuple[int, int, int]:
        """
        Randomly generate a rgb color of values not present
        :param r: red
        :param g: green
        :param b: blue
        :return: tuple of three colors
        """
        r = r if r else randint(0, 255)
        g = g if g else randint(0, 255)
        b = b if b else randint(0, 255)

        #return '#%02x%02x%02x' % (r, g, b)

        return r, g, b

    @staticmethod
    def hill_climb(func: Callable[[float, float], float], step_size: float,
                   start_x: float = None, start_y: float = None) -> Tuple[float, dict]:
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
    def hill_climb_random_restart(func: Callable[[float, float], float], step_size: float,
                                  num_restarts: int) -> Tuple[float, List[dict]]:
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
    def simulated_annealing(func: Callable[[float, float], float], step_size: float,
                            max_temp: float) -> Tuple[float, List[dict]]:
        """
        Simulated annealing
        :param func: function to call
        :param step_size: step size
        :param max_temp: max temperature
        :return:
        """

        total_max = func(0, 0)
        cooling_rate = 0.003
        plotgraph = []

        # for max_temp times
        for i in range(max_temp):
            temp = max_temp
            coords = Optimization.rand_coords(step_size)

            x = coords.get('x', 0)
            y = coords.get('y', 0)

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
                current = func(x, y)
                plotgraph[len(plotgraph)-1]['points']['x'].append(x)
                plotgraph[len(plotgraph)-1]['points']['y'].append(y)
                plotgraph[len(plotgraph)-1]['points']['z'].append(current)

                if current > total_max:
                    total_max = current

                # Go in a random direction
                local_x, local_y, high = Optimization.calculate_func_at_degree(func, step_size, x*uniform(0,1), y*uniform(0,1), randint(0,360))

                # get probability of both sides
                probability = Optimization.annealing_probability(current, high, temp)

                threshold = uniform(0, 1)

                # Determine which side is better
                if probability > threshold:
                    x = local_x
                    y = local_y

                # Decrement temperature
                temp *= cooling_rate

        return total_max, plotgraph
