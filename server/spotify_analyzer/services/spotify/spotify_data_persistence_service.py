# is going to act like the intermediary between the spotify services
# and the services i built around the models

# now that the data is flowing through the system, i need to make it work more
import logging
from typing import List

from ..user_service import UserService
from ..track_service import TrackService
from ..album_service import AlbumService
from ..artist_service import ArtistService
from ..playlist_service import PlaylistService
from ...models import User, Track, Album, Artist, Playlist
from ..service_dtos import TrackData, ArtistData, PlaylistData, AlbumData

app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)

#  this is the class that uses all the services i built,
#  im going to use it in the action views
#  is serving more like an orchestrator


class SpotifyDataPersistence:

    def __init__(self):

        self.track_service = TrackService(track_model=Track, logger=logger)
        self.user_service = UserService(user_model=User, logger=logger)
        self.album_service = AlbumService(album_model=Album, logger=logger)
        self.artist_service = ArtistService(artist_model=Artist, logger=logger)
        self.playlist_service = PlaylistService(playlist_model=Playlist,
                                                logger=logger)

    def add_track_to_library(self, track: TrackData):
        self.track_service.create_track(track_data=track)

    def add_tracks_to_library(self, tracks: List[TrackData]):
        for track in tracks:
            self.add_track_to_library(track=track)
    
    def add_playlist_to_library(self, playlist: PlaylistData):
        # make sure ALL your services use the dtos instead of the serializers,
        #  i think some of them might be using serializers
        self.playlist_service.create_playlist(playlist=playlist)

    def add_playlists_to_library(self, playlists: List[TrackData]):
        for playlist in playlists:
            self.add_playlist_to_library(playlist=playlist)

    def add_artist_to_library(self, artist: ArtistData):
        self.artist_service.create_artist(artist_data=artist)

    def add_artists_to_library(self, artists: List[ArtistData]):
        for artist in artists:
            self.add_artist_to_library(artist=artist)

    def add_album_to_library(self, album: AlbumData):
        self.artist_service.create_artist(artist_data=album)

    def add_albums_to_library(self, albums: List[AlbumData]):
        for album in albums:
            self.add_album_to_library(album=album)
    def add_track_to_album

    def add_tracks_to_album():

        pass

    def add_tracks_to_playlist():
        pass
    
