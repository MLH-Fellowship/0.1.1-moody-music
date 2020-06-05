# 0.1.1-moody-music

## Overview
Moody Music is an application that integrates with Spotify to play songs based on your current mood. By accessing your web camera, Moody Music can detect your current emotion and use that data to tell Spotify which song to play next.

## Set-Up
To use this program, clone or fork the repository. Aside from installing the necessary Python packages (when applicable -- see the bottom of this README), no other configurations are necessary.

## Using Moody Music
To use Moody Music, run the script _main.py_. Note that this project uses tensor flow, so it is important that you have a 64-bit version of Python installed. After running _main.py_, you should be greeted by the following window:

![Username Window](https://github.com/MLH-Fellowship/0.1.1-moody-music/blob/master/rsc/username_window.png?raw=true)

In this window, input your Spotify username and press "Submit". You may be asked by Spotify to grant Moody Music with some permissions. In order to use this program, all of these permission must be granted.

After clicking submit, you will be asked to choose which genres of music you would like to listen to. Select between 1 and 5 (inclusive) of these genres and click "Submit":

![Genre Window](https://github.com/MLH-Fellowship/0.1.1-moody-music/blob/master/rsc/genres_window.png?raw=true)

Finally, you should see that your web camera has turned on and you should see a bar graph displaying your time-averaged distribution of emotions:

![Mood Window](https://github.com/MLH-Fellowship/0.1.1-moody-music/blob/master/rsc/mood_window.png?raw=true)

This bar graph will change over time. To play a song based on your current mood, click "Skip." Note that you may have to have a song already playing before pressing "Skip" for this to work (so Spotify can identify which device you want to play the music on). Note that if you skip from within Spotify, the song that plays next will not be correlated with your emotion -- you must use the "Skip" button from the Moody Music application. Alternatively, if you let a song play out until its completion, Moody Music will automatically queue a song based on your current mood, so you do not have to do anything else.


## Technologies Used
* KerasML - is a machine learning API is which we derived the data set to base our emotion detection on
* OpenCV - to have access to the webcam to see the user’s facial expressions; used with KerasML to determine the ranges of emotions that the user’s face 
* Spotipy - Spotify API that held specific song metrics including valence, energy,danceability, etc. 
* Tkinter - Python GUI package used to make the GUI of Moody Music
* Other - numpy, blackbox

