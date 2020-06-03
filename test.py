import spotipy
import spotipy.util as util
from spotipy_utils import *


token = authenticate_user()
sp = spotipy.Spotify(auth=token)

while True:
    curr_track = get_current_track(sp)
    print(curr_track)
