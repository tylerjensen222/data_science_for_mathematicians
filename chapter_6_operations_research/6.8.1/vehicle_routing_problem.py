import numpy as np
import random
import pandas as pd 


def generate_graph(n):
    #get clients (o = 0 and d = n + 1)
    V = np.arange(n+2)
    #generate weights
    q_i = []
    for v in V:
        if v == 0 or v == n + 1:
            q_i.append([v, 0])
        else:
            q_i.append([v, random.randint(1,5)])
    
    A = []
    for i in range(0, n+2):
        for j in range(0, n+2):
            if i == j:
                A.append([i, j, 0])
            else:
                A.append([i, j, random.uniform(0, 1)])

    return np.around(np.array(q_i), 2), V, np.around(np.array(A), 2)

def delta_plus(A, S):
    d = []
    for ij in A:
        if ij[0] not in S and ij[1] in S:
            d.append(ij)
    return d

def delta_minus(A, S):
    d = []
    for ij in A:
        if ij[0] in S and ij[1] not in S:
            d.append(ij)
    return d

#instantiate variables
K = 0 #num vehicles
Q = 0 #capacity
n = 5 #clients

print(generate_graph(n))