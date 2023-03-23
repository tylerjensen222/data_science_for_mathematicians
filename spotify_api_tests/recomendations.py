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

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri))

info = sp.current_user()

#read in tys tracks, some reccomendations
with open('Tys_track_data.csv', newline = '') as f:
    tys_tracks = list(csv.reader(f))

df = pd.DataFrame(tys_tracks[1:], columns = tys_tracks[0])

tys_tracks = tys_tracks[:3000]

track_ids = [sublist[0] for sublist in tys_tracks]

q = random.sample(track_ids, 5)

rec_response = sp.recommendations(seed_tracks = q, limit = '3')['tracks']
recs = []
for rec in rec_response:
    recs = recs + [rec.get('id', '')]

#add them to tys queue
for rec in recs:
    sp.add_to_queue(rec)


l = []
for t in q:
    l = l + [sp.track(t)['name']]
print("Tracks queried: ", l)

l = []
for t in rec_response:
    l = l + [t['name']]
print("Tracks added: ", l)

with open('Tys_track_ratings.csv', newline = '') as f:
    track_ratings = list(csv.reader(f))

ratings = []
for i in range(len(recs)):
    ratings.append([recs[i], input("Song " + str(i + 1) + " (" + l[i] + ")" + " Rating: ")])


data = track_ratings + ratings
pd.DataFrame(data[1:], columns = data[0]).to_csv('Tys_track_ratings.csv', index = False)


