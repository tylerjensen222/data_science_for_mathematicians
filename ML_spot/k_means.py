import pandas as pd
import numpy as np
import csv
import random

def compute_mean_vectors(data):
    # create a dictionary to group the vectors by their corresponding numbers
    groups = {}
    for vector, number in data:
        if number in groups:
            groups[number].append(vector)
        else:
            groups[number] = [vector]

    # compute the mean vector for each group
    means = {}
    for number, vectors in groups.items():
        mean_vector = [sum(x) / len(vectors) for x in zip(*vectors)]
        means[number] = mean_vector

    # replace the number with the mean vector
    result = []
    for vector, number in data:
        result.append([means[number], number])

    return result

with open('data/synthetic_data.csv', newline = '') as f:
    data = list(csv.reader(f))

data_arr = np.array(data[1:])[:, :12].astype(float)
df = pd.DataFrame(data[1:], columns = data[1])

# 1: set a value for k and define a metric
k = 4
def dist(x, y, p=2):
    return np.power(np.sum(np.power(np.abs(x - y), p)), 1/p) #return the minkowski p-distance (defaults to 2)

# 2: set the k cluster by randomly sampling some indices from the data array
cluster_centroids = random.sample(range(len(data_arr)), k)

# 3: assign each data point to a cluster
clusters = []
for x in data_arr:
    d_min = 100000000000
    cluster = 1
    for centroid in cluster_centroids:
        d = dist(x, data_arr[centroid])
        if d < d_min:
            d = d_min 
            cluster = centroid
    clusters.append([x, cluster])

# 4: replace the centroid value with the mean vector of each cluster
clusters = compute_mean_vectors(clusters)

print(clusters)

