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
import math

NUM_SAMPLES = 10 # number of samples for avg emotion
SAMPLE_PERIOD = 1 # in seconds

mood = md.Mood(NUM_SAMPLES)
prev_sample_time = 0
last_track = None
added_song_rec = False
username = ""

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

def add_song_rec_to_queue(mood):
    global added_song_rec
    
    sf = mood.get_song_features_alt()
    print("Valence: ", sf.valence, " Danceability: ", sf.danceability, " Energy: ", sf.energy)
    song_rec = get_song_rec(sp,['pop','rock','alternative'],sf)

    add_song_to_queue(sp,song_rec)
    added_song_rec = True

    print("I recommended: ")
    print(song_rec)
    print()

    return song_rec

def next_song():
    global mood
    global added_song_rec

    if not added_song_rec:
        add_song_rec_to_queue(mood)
    
    sp.next_track()

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

def handle_track_change():
    global last_track
    global added_song_rec
    
    curr_track = get_current_song(sp)

    # Check if track has changed
    if last_track == None and curr_track != None:
        last_track = curr_track
        added_song_rec = False # reset
        return True
    if last_track != None and curr_track != None:
        if last_track.track_id != curr_track.track_id:
            print("RESET")
            last_track = curr_track
            added_song_rec = False # reset
            return True
    return False

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("MoodyMusic")
        self.pack(fill=BOTH,expand=1)
        
        skipButton = Button(self, text="Skip", command=next_song)
        skipButton.pack(side=BOTTOM)
        skipButton.config(font=("Ariel",24))

    def showImg(self):
        load = Image.open('emotions.png')
        render = ImageTk.PhotoImage(load)

        img = Label(self,image=render)
        img.image = render
        img.place(relx=0.5,rely=0.4,anchor=CENTER)


class EntryWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("MoodyMusic")
        self.pack(fill=BOTH,expand=1)
        
        submitButton= Button(self,text="Submit",command=self.submit)
        submitButton.place(relx=0.5,rely=0.5,anchor=CENTER)
        submitButton.config(font=("Ariel",20))

        label = Label(self,text="Please enter your Spotify username:",font=("Ariel",18))
        label.place(relx=0.5,rely=0.15,anchor=CENTER)

        label2 = Label(self,text="Instructions:\n Make sure your Spotify queue is cleared before using!",font=("Ariel",16))
        label2.place(relx=0.5,rely=0.7,anchor=CENTER)
        
        self.editText = Entry(self)
        self.editText.place(relx=0.5,rely=0.25,anchor=CENTER)
        self.editText.config(font=("Ariel",18))

    def submit(self):
        global username
        username = str(self.editText.get())
        self.master.destroy()

class GenreSelectionWindow(Frame):
    def __init__(self,master=None,sp=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window(sp)

    def init_window(self,sp):
        self.master.title("MoodyMusic")
        #self.pack(fill=BOTH,expand=1)

        items = get_genre_options(sp)
        self.ch_genres = dict(zip(items,np.zeros(len(items)).tolist()))

        COLS = 7
        ROWS = math.ceil(1.0 * len(items) / COLS)
        for i,item in enumerate(items):
            r = int(i / COLS) # row number
            c = i % COLS # col number
            
            self.ch_genres[item] = Variable()
            l = Checkbutton(root, text=item, variable=self.ch_genres[item],state=NORMAL)
            self.ch_genres[item].set('0')
            l.grid(row=r+1,column=c+1)

        submitButton = Button(self,text="Submit",command=self.submit)
        submitButton.grid(row=ROWS+1,column=int(COLS/2))

    def submit(self):
        checked = list()
        for key in self.ch_genres:
            if self.ch_genres[key].get() == '1':
                checked.append(key)
        print(checked)

    
            

root = Tk()
root.geometry("800x800")

genreSelect = GenreSelectionWindow(root,sp=spotipy.Spotify(auth=authenticate_user('dts182')))
genreSelect.mainloop()


entry = EntryWindow(root)
entry.mainloop()

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
token = authenticate_user(username)
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

    # Check song progress, add to queue if necessary
    progress = get_song_progress(sp)
    if progress != None and added_song_rec == False and progress >= 0.8:
        add_song_rec_to_queue(mood)

    app.showImg()

    handle_track_change()
    root.update_idletasks()
    root.update()
