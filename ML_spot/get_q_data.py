import pandas as pd
import csv
import synthesize_training_data


with open ('data/fuck_load_of_songs.csv', newline = '') as f:
    random_tracks = list(csv.reader(f))

count = 1
q_data = []
for track in random_tracks[1:]:
    print(count)
    count += 1
    try:
        q_data.append(synthesize_training_data.get_all_data(track[0]))
    except:
        print('fuck')

pd.DataFrame(q_data).to_csv('random_track_data.csv', index = False)