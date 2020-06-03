import spotipy
import spotipy.util as util

CLIENT_ID = input("CLIENT_KEY: ")
CLIENT_SECRET = input("CLIENT_SECRET: ")
REDIRECT_URI = 'http://localhost:8080'

scope = ''

username = input("Enter your Spotify username: ")

token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

if token:
    print("User authenticated")
else:
    print("User not authenticated")
