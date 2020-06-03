import spotipy
import spotipy.util as util
from spotipy_utils import *


token = authenticate_user()
sp = spotipy.Spotify(auth=token)

last_track_id = None

print()

while True:
    if not currently_playing(sp):
        last_track_id = None
    else:
        curr_track_id = get_current_track_id(sp)

        if curr_track_id != last_track_id: 
            curr_song = Song(curr_track_id, sp)
            print(curr_song)
            last_track_id = curr_track_id
