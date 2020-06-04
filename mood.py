class MoodEquations
#designed to return metrics for reccomendations from percentage of face emotions

def get_valence(Angry,Disguist,Fear,Happiness,Sad,Suprise,Neutral): #float betwwen 0 and 1
	
	if( ((Sad + Disguist + Fear + Neutral)/4) > (Angry + Happiness + Neutral)/3)) :
		return (1 - (((Sad + Disguist + Fear + Neutral)/4) * 1.6666))
	else
		return ((Angry + Happiness + Neutral)/3)*1.6666) 

def get_tempo(Anger,Disguist,Fear,Happy,Sad,Suprise,Neutral): #any number ranging from 0-185
	base_tempo = 75
	if( ((Sad + Disguist + Fear + Neutral)/4) > (Angry + Happiness + Neutral)/3)) :
		return (base_tempo - ((Sad + Disguist + Fear + Neutral)/4)/0.03)
	else
		return (base_tempo + (Angry + Happiness + Neutral)/0.00521)

def get_energy(Anger,Disguist,Fear,Happy,Sad,Suprise,Neutral): # float between 0 and 1

	if( ((Sad + Disguist + Neutral/ 3) > (Angry + Happiness + Neutral)/3)) :
		return (1 - ((Sad + Disguist + Fear + Neutral)/4) * 1.6666))
	else
		return ((Angry + Happiness + Fear)/3) *1.6666 ) 

def get_dancebility(Anger,Disguist,Fear,Happy,Sad,Suprise,Neutral): #float betwwen 0 and 1
	if( ((Sad + Disguist + Fear + Neutral)/4) > (Angry + Happiness)/2)) :
		return (1 - (((Sad + Disguist + Fear + Neutral)/4) * 1.6666))
	else
		return ((Angry + Happiness)/2)*1.6666) 
	