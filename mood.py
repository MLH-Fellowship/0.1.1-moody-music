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
	
