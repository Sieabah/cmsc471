from typing import Callable, Dict
from enum import Enum
from random import uniform
import math


class Direction(Enum):
    left = -1
    equal = 0
    right = 1


class Optimization:

    @staticmethod
    def get_direction(left: float, current: float, right: float) -> Direction:
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
        if start_x is None:
            start_x = 0
        if start_y is None:
            start_y = 0

        x = start_x
        y = start_y

        left = lambda: func(x-step_size, y-step_size)
        current = lambda: func(x, y)
        right = lambda: func(x+step_size, y+step_size)

        direction = Optimization.get_direction(left(), current(), right())

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
            if evaluated_side() < curr:
                return curr

            x += step_size
            y += step_size

        return None


    @staticmethod
    def hill_climb_random_restart(func: Callable[[float, float], float], step_size: float, num_restarts: int):
        def rand_coords() -> Dict[str, float]:
            return {'x': uniform(0, 1/step_size), 'y': uniform(0, 1/step_size)}

        def attempt():
            coords = rand_coords()
            return Optimization.hill_climb(func, step_size, coords.get('x', 0), coords.get('y', 0))

        total_max = None

        # +1 to always run once
        for n in range(num_restarts+1):
            tmp = attempt()

            if total_max is None or tmp > total_max:
                total_max = tmp

        return total_max

    @staticmethod
    def annealing_probability(current: float, other: float, temp: float) -> float:
        if other >= current:
            return 1.0

        if temp == 0:
            return 0

        return math.exp((other - current)/temp)

    @staticmethod
    def simulated_annealing(func: Callable[[float, float], float], step_size: float, max_temp: float) -> float:
        def rand_coords() -> Dict[str, float]:
            return {'x': uniform(0, 1/step_size), 'y': uniform(0, 1/step_size)}

        left = lambda: func(x-step_size, y-step_size)
        current = lambda: func(x, y)
        right = lambda: func(x+step_size, y+step_size)

        total_max = func(0, 0)

        for i in range(max_temp):
            temp = max_temp
            coords = rand_coords()

            x = coords.get('x', 0)
            y = coords.get('y', 0)

            left = lambda: func(x-step_size, y-step_size)
            current = lambda: func(x, y)
            right = lambda: func(x+step_size, y+step_size)

            while temp > 0:
                curr = current()

                if curr > total_max:
                    total_max = curr

                p_left = Optimization.annealing_probability(curr, left(), temp)
                p_right = Optimization.annealing_probability(curr, right(), temp)

                if p_left > p_right:
                    x -= step_size
                    y -= step_size
                else:
                    x += step_size
                    y += step_size

                temp -= 1

        return total_max
