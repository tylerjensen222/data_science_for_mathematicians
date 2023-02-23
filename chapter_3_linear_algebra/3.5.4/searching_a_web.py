import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def compute_stationary(K, v_1, k):
    v_i = v_1
    for i in range (1, k):
        numerator = K.dot(v_i)
        v_i = numerator/np.linalg.norm(numerator, ord = np.inf)
    return v_i

# Create a 100x100 zero matrix
matrix = np.zeros((100, 100))

# Fill column 42 randomly with 30 units
unit_idx_1 = np.random.choice(matrix.shape[0], 30, replace=False)
matrix[unit_idx_1, 42] = 1

# Fill column 22 randomly with 20 units
unit_idx_2 = np.random.choice(matrix.shape[0], 20, replace=False)
matrix[unit_idx_2, 22] = 1

# Fill the remaining columns with 5 to 15 units
for col_idx in range(matrix.shape[1]):
    if col_idx != 22 and col_idx != 42:  # Skip columns 22 and 42
        num_units = np.random.randint(5, 16)  # Randomly choose number of units
        unit_idx = np.random.choice(matrix.shape[0], num_units, replace=False)
        matrix[unit_idx, col_idx] = 1

# Normalize all columns
col_norms = np.linalg.norm(matrix, axis=0)  # Compute L2 norm of each column
P = matrix / col_norms  # Divide each column by its L2 norm

m = .15
K = (1-m)*P + m/100*P

v_1 = np.ones((100,)) * 1

stationary_vector = compute_stationary(K, v_1, 1000)

# Compute the dot product between the stationary vector and each column of the matrix
dot_products = np.dot(matrix.T, stationary_vector)

# Find the indices of the columns with the highest dot products
indices = np.argsort(dot_products)[::-1][:6]

# Print the indices of the best fit columns
print("Indices of the best fit columns:")
print(indices)

