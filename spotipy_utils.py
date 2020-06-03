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

        song_attrs = self.sp.audio_features([self.track_id])[0]       
        self.acousticness = song_attrs['acousticness']
        self.danceability = song_attrs['danceability']
        self.energy = song_attrs['energy']
        self.instrumentalness = song_attrs['instrumentalness']
        self.liveness = song_attrs['liveness']
        self.loudness = song_attrs['loudness']
        self.speechiness = song_attrs['speechiness']
        self.tempo = song_attrs['tempo']
        self.valence = song_attrs['valence']

        print()

    def full_print(self):
        print("Title: ", self.title)
        print("Album: ", self.album)
        print("Artists: ")
        for artist in self.artists:
            print(" * ", artist)
        print("-------------------------------------")
        print("Acousticness: ", self.acousticness)
        print("Danceability: ", self.danceability)
        print("Energy: ", self.energy)
        print("Instrumentalness: ", self.instrumentalness)
        print("Liveness: ", self.liveness)
        print("Loudness: ", self.loudness)
        print("Speechiness: ", self.speechiness)
        print("Tempo: ", self.tempo)
        print("Valence: ", self.valence)
        
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
    return curr['item']['id']

def currently_playing(sp):
    state = sp.current_playback()

    if state == None:
        return False
    else:
        return state['is_playing']
