import numpy as np
from spotipy_utils import *

# Designed to return metrics for reccomendations from percentage of face emotions
def get_valence(Anger,Disgust,Fear,Happy,Sad,Surprise,Neutral): # float between 0 and 1
	
	if ((Sad + Disgust + Fear + Neutral)/4) > (Anger + Happy + Neutral)/3 :
		if (Sad + Disgust + Fear + Neutral)/4 * 1.6666 > 1: #just in case clause
			return 0.001
		return 1 - ((Sad + Disgust + Fear + Neutral)/4) * 1.6666
	else:
		if ((Anger + Happy + Neutral)/3)*1.666 > 1: #just in case clause
			return 0.999
		return ((Anger + Happy + Neutral)/3)*1.6666

def get_tempo(Anger,Disgust,Fear,Happy,Sad,Surprise,Neutral): #any number ranging from 0-185
	base_tempo = 75
	if((Sad + Disgust + Fear + Neutral)/4) > (Anger + Happy + Neutral)/3:
		return base_tempo - ((Sad + Disgust + Fear + Neutral)/4)/0.03
	else:
		return (base_tempo + ((Anger + Happy + Neutral)/0.00521))

def get_energy(Anger,Disgust,Fear,Happy,Sad,Surprise,Neutral): # float between 0 and 1

	if (Sad + Disgust + Neutral)/3 > (Anger + Happy + Neutral)/3:
		if ((Sad + Disgust + Fear + Neutral)/4) * 1.6666 > 1: #just in case clause
			return 0.001
		return 1 - ((Sad + Disgust + Fear + Neutral)/4) * 1.6666
	else:
		if ((Anger + Happy + Fear)/3) * 1.6666 > 1: #just in case clause
			return 0.999
		return ((Anger + Happy + Fear)/3) * 1.6666  

def get_dancebility(Anger,Disgust,Fear,Happy,Sad,Surprise,Neutral): #float betwwen 0 and 1
	if ((Sad + Disgust + Fear + Neutral)/4) > (Anger + Happy)/2:
		if ((Sad + Disgust + Fear + Neutral)/4) * 1.6666 > 1: #just in case clause
			return 0.001
		return 1 - ((Sad + Disgust + Fear + Neutral)/4) * 1.6666
	else:
		if ((Anger + Happy)/2)*1.6666 > 1: #just in case clause
		   return 0.999
		return ((Anger + Happy)/2)*1.6666

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
        sf.valence = get_valence(**emotions)
        #print("Valence: ", sf.valence)
        sf.tempo = get_tempo(**emotions)
        #print("Tempo: ", sf.tempo)
        sf.energy = get_energy(**emotions)
        #print("Energy: ", sf.energy)
        sf.danceability = get_dancebility(**emotions)
        #print("Danceability: ", sf.danceability)

        return sf
    
	
