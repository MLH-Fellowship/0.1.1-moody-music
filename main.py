import spotipy.util as util
from spotipy_utils import *
import numpy as np
import random
import time
import mood as md

NUM_SAMPLES = 10 # number of samples for avg emotion
SAMPLE_PERIOD = 1 # in seconds

prev_sample_time = 0
last_track = None

        
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

def track_has_changed():
    global last_track
    
    curr_track = get_current_song(sp)
    if last_track == None and curr_track != None:
        last_track = curr_track
        return True
    if last_track != None and curr_track != None:
        if last_track.track_id != curr_track.track_id:
            last_track = curr_track
            return True
    return False
    
def handle_track_change(sp, mood):
    global last_track
    
    sf = mood.get_song_features()
    song_rec = get_song_rec(sp, ['pop','rock','alt'], sf)
    add_song_to_queue(sp, song_rec)
    sp.next_track()

    # Wait until song is actually skipped (some delay here, don't want runaway skipping)
    while get_current_song(sp).track_id != song_rec.track_id:
        pass

    last_track = song_rec

    print("I recommended: ")
    print(song_rec)
    print()
    

# Main Code
token, username = authenticate_user()
if not token:
    print("Could not authenticate, aborting...")
    exit()

sp = spotipy.Spotify(auth=token)

mood = md.Mood(NUM_SAMPLES)
while True:
    # Wait for sample period
    while time.time() - prev_sample_time < SAMPLE_PERIOD:
        # Check if song has changed
        if track_has_changed():
            handle_track_change(sp, mood)
        pass

    # Record emotions and update mood
    prev_sample_time = time.time()
    emotions = get_emotions()
    mood.add_data_point(emotions)

    # Check if song has changed
    if track_has_changed():
        handle_track_change(sp, mood)

sf = emotions_to_song_features(get_emotions())

song = get_song_rec(sp, ['pop','rock','alternative'], sf)
print(song)
