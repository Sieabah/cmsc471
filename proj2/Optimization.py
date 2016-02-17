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
        graphPlot = {
            'x': [],
            'y': [],
            'z': []
        }
        # Define easy to use functions
        left = lambda: func(x-step_size, y-step_size)
        current = lambda: func(x, y)
        right = lambda: func(x+step_size, y+step_size)

        # Get the direction we're going to be going in
        direction = Optimization.get_direction(left(), current(), right())

        # Condense to one direction or exit
        if direction == Direction.right:
            evaluated_side = right
        elif direction == Direction.left:
            evaluated_side = left
            # Account for going left
            step_size = -step_size
        else:
            return current()

        while True:
            curr = current()

            # If we can't go up anymore, exit
            if evaluated_side() < curr:
                return curr

            x += step_size
            y += step_size

        return None


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

        # +1 to always run once
        for n in range(num_restarts+1):
            tmp = attempt()

            # Get total max
            if total_max is None or tmp > total_max:
                total_max = tmp

        return total_max

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

        color = lambda r,g,b: '#%02x%02x%02x' % (r, g, b)

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
                'color': color(randint(0,255),randint(0,255),randint(0,255)),
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

                # get probability of both sides
                p_left = Optimization.annealing_probability(curr, left(), temp)
                p_right = Optimization.annealing_probability(curr, right(), temp)

                threshold = uniform(0, 0.5)

                # Determine which side is better
                if p_left > p_right:
                    if p_left >= threshold:
                        x -= step_size
                        y -= step_size
                else:
                    if p_right >= threshold:
                        x += step_size
                        y += step_size

                # Decrement temperature
                temp -= 0.1





        return total_max, plotgraph
