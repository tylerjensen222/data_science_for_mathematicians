import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from ripser import ripser
from persim import plot_diagrams

def generate_flat_torus(N):
    points = np.random.rand(N, 2)
    dist_matrix = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            dx = np.abs(points[i, 0] - points [j, 0])
            dy = np.abs(points[i, 1] - points [j, 1])
            dx = np.minimum(dx, 1-dx)      #take minimum to compensate for identification
            dy = np.minimum(dy, 1- dy)     #take minimum to compensate for identification
            dist = np.sqrt(dx*2 + dy**2)   #take euclidean distance between these vals
            dist_matrix[i, j] = dist
    return points, dist_matrix

num_points = 400
points, dist_matrix = generate_flat_torus(num_points)

dgms = ripser(dist_matrix)['dgms']

plot_diagrams(dgms, show = True)



