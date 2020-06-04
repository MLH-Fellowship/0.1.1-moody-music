import spotipy
import spotipy.util as util
from spotipy_utils import *
import time


token = authenticate_user()
sp = spotipy.Spotify(auth=token)

last_song = None

print()

while True:
    if not currently_playing(sp):
        last_song = None
        time.sleep(1)
    else:
        curr_song = get_current_song(sp)

        if (last_song == None) or (curr_song != None and curr_song.track_id != last_song.track_id): 
            #print(curr_song)
            curr_song.full_print()
            last_song = curr_song
