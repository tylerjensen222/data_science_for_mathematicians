import pandas as pd
import csv
import json
import numpy as np
import random
import spotipy
from spotipy import SpotifyOAuth

#instantiate spotify api shit
client_id = '1cfc31cdb4604b8c99ebe48fd02ef49a'
client_secret = 'ae9e308a527145d3beb89e57bd4756ef'
tys_user_id = '3uokmyw850vdrusv9r6fwf3o9'
redirect_uri = 'http://example.com'

cols = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'track_name', 'artist', 'duration_ms', 'album', 'realease_data']

scope = ["user-library-read", "user-read-currently-playing", "user-read-playback-state", "user-modify-playback-state"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri))

def get_all_data(track_id):

    def get_track_features(track_id):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri))
        ftrs = sp.audio_features(track_id)[0]
        return [ftrs.get("danceability", 0), ftrs.get("energy", 0), ftrs.get("key", 0), ftrs.get("loudness", 0), ftrs.get("mode", 0), ftrs.get("speechiness", 0), ftrs.get("acousticness", 0), ftrs.get("instrumentalness", 0), ftrs.get("liveness", 0), ftrs.get("valence", 0), ftrs.get("tempo", 0), ftrs.get("time_signature", 0)]

    def get_track_attributes(track_id):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri))
        track = sp.track(track_id)
        return [track.get('name', ''), track['artists'][0]['name'], track.get('popularity', 0), track.get('duration_ms', 0), track.get('album', {}).get('release_date', '')]

    return get_track_features(track_id) + get_track_attributes(track_id)

def get_synth_lib_ratings(data):
    tracks = [t[0] for t in data[1:]]
    rand_tracks = random.sample(tracks, 500)
    output = []
    for l in rand_tracks:
        output.append([l, random.randint(7,10)])
    return output

def get_synth_data():
    with open('data/Tys_track_ratings.csv', newline = '') as f:
        ratings = list(csv.reader(f))

    with open('data/Tys_Spotify_Library.csv', newline = '') as f:
        library = list(csv.reader(f))

    synthetic_ratings = ratings + get_synth_lib_ratings(library)

    synthetic_data = []
    for track in synthetic_ratings[1:]:
        #synthetic_data.append(get_all_data(track[0]) + [track[1]])
        try:
            synthetic_data.append(get_all_data(track[0]) + [track[1]])
        except:
            print('fuck you')

    pd.DataFrame(synthetic_data).to_csv('data/synthetic_data.csv', index = False)
    return




