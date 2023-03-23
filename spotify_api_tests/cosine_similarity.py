import pandas as pd
import numpy as np
import csv
import gen_random_tracks
import track_data
from sklearn.metrics.pairwise import cosine_similarity


def get_best_fit(tys_track_array):
    #instantiate the random tracks as an array and a df
    random_tracks = gen_random_tracks.get_rand_tracks(150)
    random_tracks_df = pd.DataFrame(random_tracks, columns = ['id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', "instrumentalness", 'liveness', 'valence', 'tempo', "time_signature"])
    random_tracks_with_id = np.array(random_tracks)
    random_tracks_array = np.array(random_tracks)[:,1:]
    random_tracks_array = random_tracks_array.astype(np.float64)

    # Calculate cosine similarities between music_taste and random_tracks_array
    similarities = cosine_similarity(tys_track_array, random_tracks_array)

    # Find the index of the most similar song for each row in music_taste
    most_similar_song_indices = np.argmax(similarities, axis=1)

    # Get unique values in the same order
    unique_values, indices, inverse = np.unique(most_similar_song_indices, return_index=True, return_inverse=True)

    # Reorder indices to match original array order
    sorted_indices = np.argsort(indices)

    # Get unique values in the original order
    unique_values_ordered = unique_values[sorted_indices]

    for index in unique_values_ordered[:3]:
        best_fit = random_tracks_with_id[index, 0]
        print(track_data.get_track_attributes(best_fit))

    return


#instantiate all of Ty's tracks as a reference df and an array
with open('Tys_track_data.csv', newline = '') as f:
    raw_data = list(csv.reader(f))
tys_track_df = pd.DataFrame(raw_data)
tys_track_array = np.array(raw_data)[1:, -12:]
tys_track_array = tys_track_array.astype(np.float64)

for i in range(10):
    try:
        get_best_fit(tys_track_array)
    except:
        print("whoopsies")



