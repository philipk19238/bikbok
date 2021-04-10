import os
import spotipy
import requests

from bs4 import BeautifulSoup, SoupStrainer
from spotipy.oauth2 import SpotifyClientCredentials
from functools import cached_property

def get_top_songs():
    r = requests.get("https://spotifycharts.com")

    for link in BeautifulSoup(r.text, parse_only=SoupStrainer("a")):
        print(link)



class SpotifyAccessObject:

    def __init__(self):
        self._auth_manager = SpotifyClientCredentials() # uses environment variables
        self._sp = spotipy.Spotify(auth_manager=self._auth_manager)

    @property
    def client(self):
        return self._sp


class SpotifyTrack:

    def __init__(self, track_uri: str, spotify_access_object: SpotifyAccessObject):
        self._sao = spotify_access_object.client
        self._id = track_uri
        self._features = {}
        self._track_info = None

        self._get_features()

    @classmethod
    def build_track_uri(cls, track_id):
        return f"spotify:track:{track_id}"

    def _get_features(self):
        try:
            features = self._sao.audio_features(self._id)
            self._features.update(features[0])
        except:
            pass

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
        if not self._track_info:
            self._track_info = self._sao.track(self._id)

        uri = self._track_info["album"]["images"][1]["url"]
        return uri

    @cached_property
    def genres(self):
        if not self._track_info:
            self._track_info = self._sao.track(self._id)

        artist_uri = self._track_info["album"]["artists"][0]["uri"]
        artist = self._sao.artist(artist_uri)
        genres = artist["genres"]

        return genres

    @cached_property
    def name(self):
        if not self._track_info:
            self._track_info = self._sao.track(self._id)

        name = self._track_info["name"]
        return name

    @cached_property
    def artist(self):
        if not self._track_info:
            self._track_info = self._sao.track(self._id)

        artist_name = self._track_info["album"]["artists"][0]["name"]
        return artist_name


class SpotifyGenre:
    pass


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    id = "2aHlRZIGUFThu3eQePm6yI" # Champion - Kanye West
    uri = SpotifyTrack.build_track_uri(id)

    sao = SpotifyAccessObject()
    champion = SpotifyTrack(uri, sao)

    get_top_songs() 