import pandas as pd
import json
import spotipy
from spotipy import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

def get_curr_track():
    current_track = sp.current_user_playing_track()
    try:
        with open('current_track.json', 'w') as f:
            f.write(json.dumps(current_track, indent = 4))
    except: 
        print('no current track')
    return current_track

client_id = '1cfc31cdb4604b8c99ebe48fd02ef49a'
client_secret = 'ae9e308a527145d3beb89e57bd4756ef'
tys_user_id = '3uokmyw850vdrusv9r6fwf3o9'
redirect_uri = 'http://example.com'

scope = ["user-library-read", "user-read-currently-playing", "user-read-playback-state"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri))

info = sp.current_user()


data = []
for i in range(0,200):
    data = data + sp.current_user_saved_tracks(offset = 20*i)["items"]

with open('raw_library.json', 'w') as f:
        f.write(json.dumps(data, indent = 4))

tracks = []
for item in data:
    track = item.get("track", {})
    album = track.get("album", {})
    for artist in track.get("artists", []):
        current_track = [track.get("id", ""), track.get("name", ""), artist.get("name", ""), artist.get("id", ""), album.get("id", ""), album.get("name", ""), track.get("duration_ms", "")]
        tracks.append(current_track)


with open('library.json', 'w') as f:
        f.write(json.dumps({'data': tracks}, indent = 4))

pd.DataFrame(tracks, columns = ['track_id', 'track_name', 'artist', 'artist_id', 'album_id', 'album_name', 'track_duration']).to_csv('Tys_Spotify_Library.csv', index = False)