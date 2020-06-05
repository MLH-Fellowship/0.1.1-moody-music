from tkinter import *
import spotipy.util as util
from spotipy_utils import *
import numpy as np
import random
import time
import mood as md
import os
import cv2
import time
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation

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

def capture_face():
    global model
    
    ret,test_img=cap.read()# captures frame and returns boolean value and captured image
    if not ret:
        return
    gray_img= cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    plt.imshow(gray_img)

    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

    if len(faces_detected) == 0:
        return None
    
    (x,y,w,h) = faces_detected[0]
    roi_gray=gray_img[y:y+w,x:x+h]#cropping region of interest i.e. face area from  image
    roi_gray=cv2.resize(roi_gray,(48,48))
    img_pixels = image.img_to_array(roi_gray)
    img_pixels = np.expand_dims(img_pixels, axis = 0)
    img_pixels /= 255

    predictions = model.predict(img_pixels)
    max_index = np.argmax(predictions[0])
    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    emotion = emotions[max_index]

    return predictions
    

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

#load model
model = model_from_json(open("fer.json", "r").read())
#load weights
model.load_weights('fer.h5')
face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)

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

    # Record emotions
    prev_sample_time = time.time()
    capture_face()


    # Update mood
    emotions = get_emotions()
    mood.add_data_point(emotions)
    
    root.update_idletasks()
    root.update()
