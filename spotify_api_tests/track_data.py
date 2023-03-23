import pandas as pd
import json
import csv
import spotipy
from spotipy import SpotifyOAuth

client_id = '1cfc31cdb4604b8c99ebe48fd02ef49a'
client_secret = 'ae9e308a527145d3beb89e57bd4756ef'
tys_user_id = '3uokmyw850vdrusv9r6fwf3o9'
redirect_uri = 'http://example.com'

def get_track_features(track_id):

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri))

    ftrs = sp.audio_features(track_id)[0]

    with open("analysis_test.json", 'w') as f:
        f.write(json.dumps(ftrs, indent = 4))

    return [ftrs.get("danceability", 0), ftrs.get("energy", 0), ftrs.get("key", 0), ftrs.get("loudness", 0), ftrs.get("mode", 0), ftrs.get("speechiness", 0), ftrs.get("acousticness", 0), ftrs.get("instrumentalness", 0), ftrs.get("liveness", 0), ftrs.get("valence", 0), ftrs.get("tempo", 0), ftrs.get("time_signature", 0)]

def get_track_attributes(track_id):

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri))

    track = sp.track(track_id)

    with open("attribute_test.json", 'w') as f:
        f.write(json.dumps(track, indent = 4))

    return [track.get('name', ''), track['artists'][0]['name']]

def get_tys_tracks():

    with open('Tys_Spotify_Library.csv', newline = '') as f:
        tracks = list(csv.reader(f))

    track_library = []

    for track in tracks[1:]:
        print(track[1])
        track_library.append(track + get_track_features(track[0]))

    df = pd.DataFrame(track_library, columns = ['track_id', 'track_name', 'artist', 'artist_id', 'album_id', 'album_name', 'track_duration', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', "instrumentalness", 'liveness', 'valence', 'tempo', "time_signature"])
    df.to_csv('Tys_track_data.csv', index = False)
    return df
