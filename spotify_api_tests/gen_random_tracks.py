import random
import spotipy
import track_data
import random
from spotipy.oauth2 import SpotifyClientCredentials

def get_rand_tracks(N):
    client_id = '1cfc31cdb4604b8c99ebe48fd02ef49a'
    client_secret = 'ae9e308a527145d3beb89e57bd4756ef'
    tys_user_id = '3uokmyw850vdrusv9r6fwf3o9'
    redirect_uri = 'http://example.com'

    # set up Spotipy client credentials
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                        client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # get the total number of tracks available on Spotify
    random_year = str(random.randint(1950, 2022))
    print("Year: " + random_year)
    total_tracks = sp.search(q='year:'+random_year, type='track')['tracks']['total']

    # set the number of tracks to retrieve
    num_tracks = N

    # initialize an empty list to store the track IDs
    track_ids = []

    # loop until we have the desired number of track IDs
    while len(track_ids) < num_tracks:
        # generate a random offset value
        offset = random.randint(0, total_tracks - 1)

        # retrieve a batch of tracks from the random offset
        batch = sp.search(q='year:'+random_year, type='track', limit=50, offset=offset)

        # extract the track IDs from the batch and add them to the list
        track_ids.extend([t['id'] for t in batch['tracks']['items']])

    track_ids = track_ids[:num_tracks]

    random_tracks = []
    for id in track_ids:
        random_tracks.append([id] + track_data.get_track_features(id))

    return random_tracks