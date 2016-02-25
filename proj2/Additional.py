
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def genGraph(func):
    plot = {
        'x': [],
        'y': [],
        'z': []
    }

    for x in np.arange(-10,10, 0.1):
        for y in np.arange(-10,10,0.1):
            plot['x'].append(x)
            plot['y'].append(y)
            plot['z'].append(func(x,y))

    # Build 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', title="Graph")

    ax.plot_surface(plot['x'], plot['y'], plot['z'])

    plt.show()