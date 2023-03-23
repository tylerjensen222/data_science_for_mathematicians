from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import csv
import pandas as pd


# Define the numeric and categorical column names
cols = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'track_name', 'artist', 'duration_ms', 'album', 'realease_date']
numeric_cols = ['danceability', 'energy', 'key', 'loudness', 'speechiness', 
                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                'duration_ms']
string_cols = ['track_name', 'artist', 'album']
date_cols = ['realease_date']

# 

# Define the function to extract year from the date column
def extract_year(X):
    # Extract the first 4 digits in the date string and cast to int
    X['realease_date'] = X['realease_date'].str.slice(stop=4).astype(int)
    return X['realease_date'].values.reshape(-1, 1)

with open('data/synthetic_data.csv', newline = '') as f:
    data = list(csv.reader(f))

data = pd.DataFrame(data[1:], columns = cols + ['rating']).drop(string_cols, axis = 1)

# Define the column transformer to preprocess different data types
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_cols),  # standardize numeric columns
        ('year', FunctionTransformer(extract_year), date_cols)  # extract year from date column
    ])

# Define the pipeline with the column transformer and the estimator
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor())
])


y_train = data['rating']
X_train = data.drop(['rating'], axis = 1)
# Fit the pipeline to your training data
pipeline.fit(X_train, y_train)

with open('data/random_track_data.csv', newline = '') as f:
    new_tracks = list(csv.reader(f))

# Predict the ratings of new songs
X_new = pd.DataFrame(new_tracks[1:], columns = cols).drop(string_cols, axis = 1) # your new tracks here
y_pred = pipeline.predict(X_new)

max_indices = np.argpartition(list(y_pred), -10)[-10:]

best_songs = []
for i in max_indices:
    best_songs.append([new_tracks[i + 1][12], new_tracks[i + 1][13]])

print(best_songs)