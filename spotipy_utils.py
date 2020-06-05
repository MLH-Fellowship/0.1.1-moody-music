import spotipy
import spotipy.util as util

class SongFeatures:
    def __init__(self, track_id=None, sp=None):
        if track_id != None and sp != None:
            self.populate_features_by_track(track_id, sp)
            return
            
        self.acousticness = None
        self.danceability = None
        self.energy = None
        self.instrumentalness = None
        self.liveness = None
        self.loudness = None
        self.speechiness = None
        self.tempo = None
        self.valence = None

    def populate_features_by_track(self, track_id, sp):
        if track_id == None or sp == None:
            return

        song_attrs = sp.audio_features([track_id])[0]       
        self.acousticness = song_attrs['acousticness']
        self.danceability = song_attrs['danceability']
        self.energy = song_attrs['energy']
        self.instrumentalness = song_attrs['instrumentalness']
        self.liveness = song_attrs['liveness']
        self.loudness = song_attrs['loudness']
        self.speechiness = song_attrs['speechiness']
        self.tempo = song_attrs['tempo']
        self.valence = song_attrs['valence']

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

        self.duration_ms = track['duration_ms']
        self.sf = SongFeatures(track_id=self.track_id,sp=self.sp)

    def full_print(self):
        print("Title: ", self.title)
        print("Album: ", self.album)
        print("Artists: ")
        for artist in self.artists:
            print(" * ", artist)
        print("Duration: ", self.duration_ms, " ms")
        print("Track ID: ", self.track_id)
        print("-------------------------------------")
        print("Acousticness: ", self.sf.acousticness)
        print("Danceability: ", self.sf.danceability)
        print("Energy: ", self.sf.energy)
        print("Instrumentalness: ", self.sf.instrumentalness)
        print("Liveness: ", self.sf.liveness)
        print("Loudness: ", self.sf.loudness)
        print("Speechiness: ", self.sf.speechiness)
        print("Tempo: ", self.sf.tempo)
        print("Valence: ", self.sf.valence)
        print()
        
    def __str__(self):
        out = "Title: " + str(self.title) + '\n'
        out += ("Album: " + str(self.album) + '\n')
        out += "Aritsts:\n"
        for artist in self.artists:
            out += (" * " + artist + "\n")
        out += ("Duration: " + str(self.duration_ms) + " ms\n")
        out += ("Track ID: " + self.track_id)
        return out

# Returns authentication token if successful, None otherwise
def authenticate_user(username):
    try:
        with open("env/.env") as f:
            data = f.readlines()
            client_id = data[0].strip().split(' ')[-1]
            client_secret = data[1].strip().split(' ')[-1]
    except:
        return None # If file does not exist

    REDIRECT_URI = 'http://localhost:8080'
    scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state playlist-modify-public playlist-read-private playlist-modify-private'

    token = util.prompt_for_user_token(username, scope, client_id, client_secret, REDIRECT_URI)

    if token:
        print("User authenticated")
    else:
        print("User not authenticated")

    return token

# Returns None if no song is playing
def get_current_song(sp):
    curr = sp.current_playback()

    if curr == None:
        return None
    
    return Song(track_id=curr['item']['id'], sp=sp)

def currently_playing(sp):
    state = sp.current_playback()

    if state == None:
        return False
    else:
        return state['is_playing']

def get_song_rec(sp, genres, sf):
    args = dict()
    args['target_acousticness'] = sf.acousticness
    args['target_danceability'] = sf.danceability
    args['target_energy'] = sf.energy
    args['target_instrumentalness'] = sf.instrumentalness
    args['target_liveness'] = sf.liveness
    args['target_loudness'] = sf.loudness
    args['target_speechiness'] = sf.speechiness
    args['target_tempo'] = sf.tempo
    args['target_valence'] = sf.valence

    recs = sp.recommendations(seed_genres=genres,**args)

    if recs != None:
        return Song(track_id=recs['tracks'][0]['id'], sp=sp)

    return None

# Returns None if no song is playing (or if user is in a private session)
def get_song_progress(sp):
    curr_song = get_current_song(sp)
    state = sp.current_playback()
    
    if curr_song == None or state == None:
        return None
    
    progress = 1.0 * state['progress_ms'] / curr_song.duration_ms
    return progress

def add_song_to_queue(sp, song):
    if sp == None or song == None:
        return False

    sp.add_to_queue(song.track_id)
    return True

def get_playlist_id(sp, username, target_name):
    user_playlists = sp.user_playlists(username)['items']

    for playlist in user_playlists:
        playlist_name = playlist['name']
        if playlist_name == target_name:
            return playlist['id']
    return None

def create_playlist(sp, username, name):
    playlist = sp.user_playlist_create(username, name, public=False)
    return playlist['id']
