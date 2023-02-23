import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#convert a sentence to a vector z that queries W
def get_query_vector(s, df):
    word_list = s.split(' ')
    z = np.zeros(len(df.index))
    for word in word_list:
        if word in df.index:
            z[df.index.get_loc(word)] = 1
    return z

#reduce the rank of a matrix to n
def reduce_rank(A, rank):
    A_reduced = A
    A_reduced[rank:, :] = 0
    A_reduced[:, rank:] = 0
    return A_reduced

#get the data, make it a dataframe to help query, and load the values into W
with open('data/boolean_words_by_book.csv', newline = '') as csvfile:
    words_by_book = np.array((list(csv.reader(csvfile))))
df = pd.DataFrame(words_by_book[1:, 1:], columns = words_by_book[0, 1:], index = words_by_book[1:, 0])
W = np.array(words_by_book[1:, 1:], dtype = float).T

#get the SVD of W
U, singular_values, V_T = np.linalg.svd(W)

S = np.zeros(W.shape)
S[:len(singular_values), :len(singular_values)] = np.diag(singular_values)

#reduce the rank of S to 2, reduce W
S_r = reduce_rank(S, 2)
W_r = U.dot(S_r).dot(V_T)

#project to 2 dimesnions
projection = U.T.dot(W_r)

pd.DataFrame(projection[:, :2]).to_csv('data/projection.csv', index = False)

# Plot the first two columns of the data array
plt.scatter(projection[:,0], projection[:,1])

# Add text labels for each point

for i in range(len(projection)):
    plt.text(projection[i,0], projection[i,1], df.columns[i])


# Show the plot
plt.show()






