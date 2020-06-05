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
from PIL import Image, ImageTk

NUM_SAMPLES = 10 # number of samples for avg emotion
SAMPLE_PERIOD = 1 # in seconds

mood = md.Mood(NUM_SAMPLES)
prev_sample_time = 0

# Inspired by: https://pythonprogramming.net/
# ML models inspired by: https://sefiks.com/2018/01/01/facial-expression-recognition-with-keras/
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

def get_user_live_emotions():
    global model
    
    ret,test_img=cap.read()# captures frame and returns boolean value and captured image
    if not ret:
        return
    gray_img= cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)

    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

    if len(faces_detected) == 0:
        return None
    
    (x,y,w,h) = faces_detected[0]
    roi_gray=gray_img[y:y+w,x:x+h]#cropping region of interest i.e. face area from  image
    roi_gray=cv2.resize(roi_gray,(48,48))
    img_pixels = image.img_to_array(roi_gray)
    img_pixels = np.expand_dims(img_pixels, axis = 0)
    img_pixels /= 255

    predictions = model.predict(img_pixels).tolist()[0]
    print(predictions)
    max_index = np.argmax(predictions[0])
    emotions = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    emotion = emotions[max_index]

    return dict(zip(emotions,predictions))

def create_emotion_bar_graph(emotions):
    objects = list(emotions.keys())
    y_pos = np.arange(len(objects))

    plt.bar(y_pos,list(emotions.values()),align='center')
    plt.xticks(y_pos,objects)
    plt.ylabel('percentage')
    plt.title('emotion')

    plt.savefig("emotions.png")
    plt.clf()

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

    def showImg(self):
        load = Image.open('emotions.png')
        render = ImageTk.PhotoImage(load)

        img = Label(self,image=render)
        img.image = render
        img.place(x=40,y=40)

root = Tk()
root.geometry("800x800")
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
    emotions = get_user_live_emotions()
    
    # Update mood
    if emotions != None:
        mood.add_data_point(emotions)
        create_emotion_bar_graph(mood.get_emotion_dict())
    else:
        print("Scrap")

    app.showImg()
    
    root.update_idletasks()
    root.update()
