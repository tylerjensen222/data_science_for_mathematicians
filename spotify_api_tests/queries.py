import pandas as pd
import csv

def print_max(column):
    max_row = df.loc[df[column].astype(float).idxmax()]

    # print the result
    print(f"The row with the maximum value in {column} is:")
    print(max_row)
    return

with open("Tys_track_data.csv", newline = '') as f:
    data = list(csv.reader(f))

df = pd.DataFrame(data[1:], columns = data[0])

attributes = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', "instrumentalness", 'liveness', 'valence', 'tempo', "time_signature"]

for attribute in attributes:
    print_max(attribute)


