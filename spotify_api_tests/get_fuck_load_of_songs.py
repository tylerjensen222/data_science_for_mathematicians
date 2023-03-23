import pandas as pd
import spotipy
import json
import csv
from spotipy import SpotifyOAuth
import random


#instantiate spotify api shit
client_id = '1cfc31cdb4604b8c99ebe48fd02ef49a'
client_secret = 'ae9e308a527145d3beb89e57bd4756ef'
tys_user_id = '3uokmyw850vdrusv9r6fwf3o9'
redirect_uri = 'http://example.com'

scope = ["user-library-read", "user-read-currently-playing", "user-read-playback-state", "user-modify-playback-state"]

def get_three(tys_tracks):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri))

    track_ids = [sublist[0] for sublist in tys_tracks]

    q = random.sample(track_ids, 5)

    rec_response = sp.recommendations(seed_tracks = q, limit = '3')['tracks']
    recs = []
    for rec in rec_response:
        recs = recs + [rec.get('id', '')]
    return recs

#read in tys tracks, some reccomendations
with open('Tys_track_data.csv', newline = '') as f:
    tys_tracks = list(csv.reader(f))
recs_output = []
for i in range(10000):
    print(i)
    try:
        recs_output = recs_output + get_three(tys_tracks[:3000])
    except:
        print('fuck')

pd.DataFrame(recs_output, columns = ['track_id']).to_csv('fuck_load_of_songs.csv', index = False)

