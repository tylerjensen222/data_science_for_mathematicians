import csv
import pandas as pd
import numpy as np

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
with open('data/row_normalized_words_by_book.csv', newline = '') as csvfile:
    words_by_book = np.array((list(csv.reader(csvfile))))
df = pd.DataFrame(words_by_book[1:, 1:], columns = words_by_book[0, 1:], index = words_by_book[1:, 0])
W = np.array(words_by_book[1:, 1:], dtype = float)


with open('data/sentences.csv', newline='') as f:
    sentences = list(csv.reader(f))


for s in sentences[1:]:
    print('"', s[0], '"')
    #get the query vector from the sentence
    z = get_query_vector(s[0], df)

    #query and print!
    q_1 = W.T.dot(z).T
    print('query result without rank reduction: ', df.columns[np.argmax(q_1)])


    #get the QR decomposition of W
    Q, R = np.linalg.qr(W)

    #reduce the rank of R to reduce the rank of W
    R_QRD = reduce_rank(R, 10)
    W_QRD = Q.dot(R_QRD)

    #query and print!
    q_2 = W_QRD.T.dot(z).T
    print('query result with rank reduction: ', df.columns[np.argmax(q_1)], '\n')

pd.DataFrame(np.around(W, 2)).to_csv('W.csv', index = False)
pd.DataFrame(np.around(W_QRD, 2)).to_csv('W_QRD.csv', index = False)
