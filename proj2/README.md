# Project 2 - CMSC 471 - Spring 2016
## Author: Christopher Sidell (csidell1@umbc.edu)

## NOTES:
Python version: 3.5.1 (I use types extensively so ~3.5.x is needed)

Required Packages:
    - Matplotlib
        - PyPlot
    - Numpy 

For hill climbing for accuracy the algorithm doesn't randomly choose a direction to go in and see's if it's higher, it will look 360 degrees around the point and take the highest (if there is one). This brings up a problem if there is a higher point in between one of the degrees. 

## Instructions

python driver.py

The output will run all three algorithms and will one after another open a graph of the function and the path that algorithm took (This part can take a while). It may also be hard to see the line (See Config).

## Config:
To change the function uses modify what the function z(float, float) found in driver.py

### Graph settings
xmin, ymin, xmax, ymax - Values that represent the plane the algorithm will search over

GraphSettings.graph_resolution - This is the output resolution of the plotted function (not algorithm path). The smaller the number the higher the resolution.

GraphSettings.graph_alpha - How visible is the underlying graph (0,1)

GraphSettings.show_graph - Whether or not it shows the underlying graphed function (bool)

### Algorithm Settings
step_size - How far to move each step

restarts - How many restarts to take for the random restarts

max_temperature - For simulated annealing what temperature to start at

### Additional Settings
Within Optimization.py in the simulated_annealing function there is a setting *iterations* to run the function for multiple iterations (similar to hill climb with random restarts).