import spotipy.util as util
from spotipy_utils import *
import numpy as np
import random
import time
import mood as md
        
def get_emotions():
    emotions = dict()

    emotions['Anger'] = random.random()
    emotions['Disgust'] = random.random()
    emotions['Fear'] = random.random()
    emotions['Happy'] = random.random()
    emotions['Sad'] = random.random()
    emotions['Surprise'] = random.random()
    emotions['Neutral'] = random.random()

    return emotions



NUM_SAMPLES = 10 # number of samples for avg emotion
SAMPLE_PERIOD = 1 # in seconds

prev_sample_time = 0


# Main Code
token = authenticate_user()
if not token:
    print("Could not authenticate, aborting...")
    exit()

sp = spotipy.Spotify(auth=token)

mood = md.Mood(NUM_SAMPLES)
while True:
    while time.time() - prev_sample_time < SAMPLE_PERIOD:
        pass

    prev_sample_time = time.time()
    emotions = get_emotions()
    mood.add_data_point(emotions)

    print(mood.get_song_features())

sf = emotions_to_song_features(get_emotions())

song = get_song_rec(sp, ['pop','rock','alternative'], sf)
print(song)
