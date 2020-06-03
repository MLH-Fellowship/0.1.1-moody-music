import spotipy
import spotipy.util as util

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

def get_current_track(sp):
    curr = sp.current_playback()
    return curr
