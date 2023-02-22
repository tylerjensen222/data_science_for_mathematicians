import requests
import json
import pandas as pd
import numpy as np

#print some pretty json
def printer(response, name):
    with open(name, 'w') as f:
        f.write(json.dumps(response, indent = 4))
    return

#call the getenburg api and get a list of books
def get_books():
    #url = 'http://gutendex.com/books?ids=1232,1497,5827,4363,574,2500,61'
    url = 'http://gutendex.com/books?topic=philosophy'
    response = json.loads(requests.get(url).text)
    printer(response, 'data/response.json')
    return response

#call the getenburg api and get a dictionary with keys book titles and values arrays of words with no-special-charachters and delimeted by ' '
def get_words(response, char_num):
    words = {}
    print('Book count: ', len(response['results']))
    for book in response['results']:
        try:
            book_text = requests.get(book.get('formats', {}).get('text/plain', '')).text.lower()
            book_text = "".join(c if c.isalpha() and c!= '***' else " " for c in book_text)
            words[book.get('title', 'yeet')] = book_text[book_text.find('***') + 170:char_num].split(' ')
        except:
            print('No cigar: ', book['title'])
    printer(words, 'data/words.json')
    return words

#stem words (eg, add rows together if the words share stem_num common leading chars)
def stem(df, n):
    for index1 in df.index:
        for index2 in df.index:
            if index1[:n] == index2[:n] and index1 != index2:
                if index1 in df.index and index2 in df.index:
                    df.loc[index1] += df.loc[index2]
                    # Drop the second row from the dataframe
                    df.drop(index2, inplace=True)
    return df

#get a dataframe with rows words, columns book titles, and indices how many times each word is used in each book
def get_raw_words_by_book(stem_num):
    books = get_books()
    book_data = get_words(books, 60000)
    word_set = list(set(word for words in book_data.values() for word in words))
    df = pd.DataFrame(index = word_set, columns = book_data.keys())
    #drop the row filled with spaces
    df = df.drop(df.index[1])
    for book, words in book_data.items():
        print('Book added: ', book)
        for word in word_set:
            df.loc[word, book] = words.count(word)
    df = df.fillna(0)
    df = stem(df, stem_num)
    df.to_csv('data/raw_words_by_book.csv')
    return df

#get boolean rep, ie all 1s and 0s
def get_boolean(df):
    df = df.applymap(lambda x: 1 if x!= 0 else 0)
    df.to_csv('data/boolean_words_by_book.csv')
    return df

#get df normed by rows
def get_row_normed(df):
    row_norms = np.sqrt((df**2).sum(axis = 1))
    df_normalized = df.div(row_norms, axis = 0)
    df_normalized.to_csv('data/row_normalized_words_by_book.csv')
    return df_normalized

#get df normed by columns
def get_col_normed(df):
    col_norms = np.sqrt((df**2).sum(axis = 0))
    df_normalized = df.div(col_norms, axis = 1)
    df_normalized.to_csv('data/col_normalied_words_by_book.csv')
    return df_normalized

raw_words_by_book = get_raw_words_by_book(stem_num = 6)

get_boolean(raw_words_by_book)
get_row_normed(raw_words_by_book)
get_col_normed(raw_words_by_book)



