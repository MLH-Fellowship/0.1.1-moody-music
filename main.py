import spotipy.util as util
from spotipy_utils import *
import numpy as np
import random
import time
import mood as md

class Mood:
    def __init__(self, num_samples):
        self.anger = np.zeros(num_samples)
        self.anger[:] = np.NaN
        self.disgust = np.zeros(num_samples)
        self.disgust[:] = np.NaN
        self.fear = np.zeros(num_samples)
        self.fear[:] = np.NaN
        self.happy = np.zeros(num_samples)
        self.happy[:] = np.NaN
        self.sad = np.zeros(num_samples)
        self.sad[:] = np.NaN
        self.surprise = np.zeros(num_samples)
        self.surprise[:] = np.NaN
        self.neutral = np.zeros(num_samples)
        self.neutral[:] = np.NaN

        self.num_samples = num_samples
        self.counter = 0

    def get_emotion_dict(self):
        emotions = dict()

        emotions['Anger'] = np.nanmean(self.anger)
        emotions['Disgust'] = np.nanmean(self.disgust)
        emotions['Fear'] = np.nanmean(self.fear)
        emotions['Happy'] = np.nanmean(self.happy)
        emotions['Sad'] = np.nanmean(self.sad)
        emotions['Surprise'] = np.nanmean(self.surprise)
        emotions['Neutral'] = np.nanmean(self.neutral)

        return emotions

    def add_data_point(self, emotions):
        index = self.counter % self.num_samples
        self.anger[index] = emotions['Anger']
        self.disgust[index] = emotions['Disgust']
        self.fear[index] = emotions['Fear']
        self.happy[index] = emotions['Happy']
        self.sad[index] = emotions['Sad']
        self.surprise[index] = emotions['Surprise']
        self.neutral[index] = emotions['Neutral']
        
        self.counter += 1

    def get_song_features(self):
        emotions = self.get_emotion_dict()
        
        sf = SongFeatures()
        sf.valence = md.get_valence(**emotions)
        print("Valence: ", sf.valence)
        sf.tempo = md.get_tempo(**emotions)
        print("Tempo: ", sf.tempo)
        sf.energy = md.get_energy(**emotions)
        print("Energy: ", sf.energy)
        sf.danceability = md.get_dancebility(**emotions)
        print("Danceability: ", sf.danceability)

        return sf
    
        
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

mood = Mood(NUM_SAMPLES)
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
