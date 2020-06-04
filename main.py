import spotipy.util as util
from spotipy_utils import *
import time
import mood

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
    

# Main Code
token = authenticate_user()
if not token:
    print("Could not authenticate, aborting...")
    exit()

sp = spotipy.Spotify(auth=token)

sf = emotions_to_song_features(get_emotions())

song = get_song_rec(sp, ['pop','rock','alternative'], sf)
print(song)
