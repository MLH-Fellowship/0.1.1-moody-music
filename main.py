import spotipy.util as util
from spotipy_utils import *
import numpy as np
import time
import mood

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

        self.num_samples = 0
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

    def add_data_point(self, emotions):
        index = self.counter % self.num_samples
        self.anger[index] = emotions['Anger']
        self.disgust[index] = emotions['Disgust']
        self.fear[index] = emotions['Fear']
        self.happy[index] = emotions['Happy']
        self.sad[index] = emotions['Sad']
        self.surprise[index] = emotions['Surprise']
        self.neutral[index] = emotions['Neutral']
        
        self.num_samples += 1
        
def get_emotions():
    emotions = dict()

    emotions['Anger'] = 0.15
    emotions['Disgust'] = 0.01
    emotions['Fear'] = 0.01
    emotions['Happy'] = 0.01
    emotions['Sad'] = 0.8
    emotions['Surprise'] = 0.01
    emotions['Neutral'] = 0.01

    return emotions

def emotions_to_song_features(emotions):
    sf = SongFeatures()
    sf.valence = mood.get_valence(**emotions)
    print("Valence: ", sf.valence)
    sf.tempo = mood.get_tempo(**emotions)
    print("Tempo: ", sf.tempo)
    sf.energy = mood.get_energy(**emotions)
    print("Energy: ", sf.energy)
    sf.danceability = mood.get_dancebility(**emotions)
    print("Danceability: ", sf.danceability)

    return sf
    

NUM_SAMPLES = 10 # number of samples for avg emotion
SAMPLE_PERIOD = 1 # in seconds

prev_sample_time = 0


# Main Code
token = authenticate_user()
if not token:
    print("Could not authenticate, aborting...")
    exit()

sp = spotipy.Spotify(auth=token)

while True:
    while time.time() - prev_sample_time < SAMPLE_PERIOD:
        pass

    prev_sample_time = time.time()
    print("Ding!")

sf = emotions_to_song_features(get_emotions())

song = get_song_rec(sp, ['pop','rock','alternative'], sf)
print(song)
