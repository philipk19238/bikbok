import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyAccessObject:

    def __init__(self):
        self._auth_manager = SpotifyClientCredentials()
        self._sp = spotipy.Spotify(auth_manager=self._auth_manager)

    @property
    def client(self):
        return self._sp


class SpotifyTrack:

    def __init__(self, track_id: str, spotify_access_object: SpotifyAccessObject):
        self._sao = spotify_access_object.client
        self._id = track_id
        self._get_features()

    def _get_features(self):
        features = self._sao.audio_features(self._id)
        print(features)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    id = "37i9dQZF1E39fbb8esZc2T" # Champion - Kanye West

    sao = SpotifyAccessObject()
    st = SpotifyTrack(id, sao)
