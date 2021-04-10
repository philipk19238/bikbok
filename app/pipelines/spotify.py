import os
import spotipy
import requests
import numpy as np

from bs4 import BeautifulSoup, SoupStrainer
from spotipy.oauth2 import SpotifyClientCredentials
from functools import cached_property


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


def get_top_songs():
    r = requests.get("https://spotifycharts.com")

    res = []

    # scrape through valid track links
    for link in BeautifulSoup(r.text, features="html.parser").find_all(href=True):
        if link["href"][25:30] == "track":
            res.append(link["href"][31:])

    return res


def generate_vector(track_id): # this can definitely be combined with generate_genre_vectors
    sao = SpotifyAccessObject()
    uri = SpotifyTrack.build_track_uri(id)

    # create feature vector
    song = SpotifyTrack(uri, sao)
    vector = [
        float(song.volume),
        float(song.danceability),
        float(song.bpm),
        float(song.instrumentalness)
    ]

    # turn into np readable object
    return np.array(vector)

def normalize_vector(vector, vmin, vmax, dmin, dmax, bmin, bmax, imin, imax):
    vector[0] = (vector[0] - vmin)/(vmax - vmin)
    vector[1] = (vector[1] - dmin)/(dmax - dmin)
    vector[2] = (vector[2] - bmin)/(bmax - bmin)
    vector[3] = (vector[3] - imin)/(imax - imin)


def generate_genre_vectors(track_ids):
    sao = SpotifyAccessObject()

    vectors = []
    for _id in track_ids:
        # create object to interact with spotify track
        uri = SpotifyTrack.build_track_uri(_id)
        song = SpotifyTrack(uri, sao)

        # create feature vector
        vectors.append(np.array([
            float(song.volume),
            float(song.danceability),
            float(song.bpm),
            float(song.instrumentalness)
        ]))

    # turn into np readable object
    vectors = np.array(vectors)
    return vectors


def cosine_similarity(a, b):
    """ Computes cosine similarity between two vectors a and b"""
    if a.ndim != 1 or b.ndim != 1:
        raise InvalidShapeException(a,b)

    if len(a) != len(b):
        raise InvalidLengthException(a,b)
    
    mag_a = np.linalg.norm(a)
    mag_b = np.linalg.norm(b)

    return np.dot(a,b)/(mag_a*mag_b)

def genre_average(genre_vectors):
    """Computes the vector average of genre vectors"""
    array = [vector for vector in genre_vectors]
    return np.average(array, axis=0)

def genre_similarity(song, genre_vectors):
    avg = genre_average(genre_vectors)
    similarity = cosine_similarity(song, avg)
    return similarity*100


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    id = "2aHlRZIGUFThu3eQePm6yI" # Champion - Kanye West

    # get top songs and calculate feature vectors
    top_song_ids = get_top_songs()
    genre_vectors = generate_genre_vectors(top_song_ids)

    # determine normalization constants
    volume_min, dance_min, bpm_min, instrumentalness_min = np.min(genre_vectors, axis=0)
    volue_max, dance_max, bpm_max, instrumentalness_max = np.max(genre_vectors, axis=0)
    
    # normalize
    for vector in genre_vectors:
        normalize_vector(
            vector,
            volume_min,
            volue_max,
            dance_min, 
            dance_max,
            bpm_min,
            bpm_max,
            instrumentalness_min,
            instrumentalness_max
        )
    
    # calculate feature vector for given song from 'id'
    song = generate_vector(id)
    normalize_vector(
            song,
            volume_min,
            volue_max,
            dance_min, 
            dance_max,
            bpm_min,
            bpm_max,
            instrumentalness_min,
            instrumentalness_max
        )

    # calculate similarity
    similarity = genre_similarity(song, genre_vectors)
    print(similarity)