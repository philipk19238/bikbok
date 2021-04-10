import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyAccessObject:

    def __init__(self):
        self._auth_manager = SpotifyClientCredentials() # uses environment variables
        self._sp = spotipy.Spotify(auth_manager=self._auth_manager)

    @property
    def client(self):
        return self._sp


class SpotifyTrack:

    def __init__(self, track_id: str, spotify_access_object: SpotifyAccessObject):
        self._sao = spotify_access_object.client
        self._id = track_id
        self._features = {}

        self._get_features()

    def _get_features(self):
        features = self._sao.audio_features(self._id)
        self._features.update(features[0])

    @property
    def danceability(self):
        return self._features.get("danceability")
    
    @property
    def hype(self):
        return self._features.get("energy")

    @property
    def tone(self):
        return self._features.get("key")

    @property
    def volume(self):
        return self._features.get("loudness")

    @property
    def lyricism(self):
        return self._features.get("speechiness")

    @property
    def acousticness(self):
        return self._features.get("acousticness")

    @property
    def instrumentalness(self):
        return self._features.get("instrumentalness")

    @property
    def concert_probability(self):
        return self._features.get("liveness")

    @property
    def positivity(self):
        return self._features.get("valence")

    @property
    def bpm(self):
        return self._features.get("tempo")

    @property
    def duration(self):
        return self._features.get("duration_ms")/1000
    
    @property
    def time_signature(self):
        return self._features.get("time_signature")




if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    id = "spotify:track:2aHlRZIGUFThu3eQePm6yI" # Champion - Kanye West

    sao = SpotifyAccessObject()
    st = SpotifyTrack(id, sao)
