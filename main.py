from tkinter import *
import spotipy.util as util
from spotipy_utils import *
import numpy as np
import random
import time
import mood as md

NUM_SAMPLES = 10 # number of samples for avg emotion
SAMPLE_PERIOD = 1 # in seconds

mood = md.Mood(NUM_SAMPLES)
prev_sample_time = 0

# Inspired by: https://pythonprogramming.net/
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

def next_song():
    global mood
    
    sf = mood.get_song_features()
    song_rec = get_song_rec(sp,['pop','rock','alternative'],sf)
    add_song_to_queue(sp,song_rec)
    sp.next_track()

    print("I recommended: ")
    print(song_rec)
    print()

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("MoodyMusic")
        self.pack(fill=BOTH,expand=1)
        skipButton = Button(self, text="Skip", command=next_song)
        skipButton.place(x=0,y=0)

root = Tk()
root.geometry("400x300")
app = Window(root)


# Main Code
token, username = authenticate_user()
if not token:
    print("Could not authenticate, aborting...")
    exit()
    
sp = spotipy.Spotify(auth=token)
while True:
    # Wait for sample period
    while time.time() - prev_sample_time < SAMPLE_PERIOD:
        pass

    # Record emotions and update mood
    prev_sample_time = time.time()
    emotions = get_emotions()
    mood.add_data_point(emotions)
    
    root.update_idletasks()
    root.update()
