import os
import spotipy
from fycharts.SpotifyCharts import SpotifyCharts
from spotipy.oauth2 import SpotifyClientCredentials
from functools import cached_property

charts_api = SpotifyCharts()

class SpotifyAccessObject:

    def __init__(self):
        self._auth_manager = SpotifyClientCredentials() # uses environment variables
        self._sp = spotipy.Spotify(auth_manager=self._auth_manager)

    @property
    def client(self):
        return self._sp

    @classmethod
    def top_songs(cls, term):
        print(charts_api.top200Daily())
        


class SpotifyTrack:

    def __init__(self, track_id: str, spotify_access_object: SpotifyAccessObject):
        self._sao = spotify_access_object.client
        self._id = track_id
        self._features = {}

        self._get_features()

    @classmethod
    def build_track_uri(cls, track_id):
        return f"spotify:track:{track_id}"

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

    @cached_property
    def image_uri(self):
        t = self._sao.track(self._id)
        uri = t["album"]["images"][1]["url"]
        return uri

    @cached_property
    def genres(self):
        t = self._sao.track(self._id)
        artist_uri = t["album"]["artists"][0]["uri"]
        
        artist = self._sao.artist(artist_uri)
        genres = artist["genres"]

        return genres



class SpotifyGenre:
    pass


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    id = "spotify:track:2aHlRZIGUFThu3eQePm6yI" # Champion - Kanye West

    sao = SpotifyAccessObject()
    champion = SpotifyTrack(id, sao)
    
    SpotifyAccessObject.top_songs()