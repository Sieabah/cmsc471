from Optimization import Optimization
import math


def main():
    # Function to optimize
    def z(_x: float, _y: float) -> float:
        # Step function
        _r = math.sqrt(_x ** 2 + _y ** 2)
        return math.sin(_x ** 2 + (3 * _y ** 2)) / (0.1 + _r ** 2) + \
            (_x ** 2 + 5 * _y ** 2) * (math.exp(1 - _r ** 2) / 2)

    #    print(Optimization.hill_climb(z, 0.1))
    print(Optimization.hill_climb(z, 0.1))

    print(Optimization.hill_climb_random_restart(z, 0.1, 200))


main()
