creating_a_database.py calls the gutendex api to get (and clean) a term-by-document dataframe
indexed by words from books written by philosophy authors (the columns).

the raw dataframe is then normalized in different ways (by col, row, and bool). Each of these is outputted as 
a .csv to the data folder, along with the raw json responses for the book authors and the list of words by author