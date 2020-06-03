import spotipy
import spotipy.util as util

class Song:
    def __init__(self, track_id, sp):
        self.track_id = track_id
        self.sp = sp

        self.pull_song_data()

    def pull_song_data(self):
        track = self.sp.track(self.track_id)

        self.title = track['name']
        self.album = track['album']['name']

        self.artists = list()
        for artist in track['artists']:
            self.artists.append(artist['name'])

    def __str__(self):
        out = "Title: " + str(self.title) + '\n'
        out += ("Album: " + str(self.album) + '\n')
        out += "Aritsts:\n"
        for artist in self.artists:
            out += (" * " + artist + "\n")
        return out

def authenticate_user():
    CLIENT_ID = input("CLIENT_KEY: ")
    CLIENT_SECRET = input("CLIENT_SECRET: ")
    REDIRECT_URI = 'http://localhost:8080'

    scope = 'user-read-currently-playing user-read-playback-state'

    username = input("Enter your Spotify username: ")

    token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    if token:
        print("User authenticated")
    else:
        print("User not authenticated")

    return token

def get_current_track_id(sp):
    curr = sp.current_playback()
    return curr
