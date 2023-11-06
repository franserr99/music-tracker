# is going to act like the intermediary between the spotify services
# and the services i built around the models
# now that the data is flowing through the system, i need to make it work more
#  this is the class that uses all the services i built,
#  im going to use it in the action views
#  is serving more like an orchestrator

import logging
from typing import List

from ..core.user_service import UserService
from ..core.track_service import TrackService
from ..core.album_service import AlbumService
from ..core.artist_service import ArtistService
from ..core.playlist_service import PlaylistService
from ..core.track_features_service import TrackFeaturesService
from ..service_dtos import TrackData, ArtistData, PlaylistData, AlbumData, \
    TrackFeaturesData

app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


class SpotifyDataPersistence:

    def __init__(self, track_service: TrackService, user_service: UserService,
                 album_service: AlbumService, artist_service: ArtistService,
                 playlist_service: PlaylistService,
                 feature_service: TrackFeaturesService):
        # save all references, pass what is needed to the others
        # for now we will keep them here, if i dont have a need for then
        # then we will only keep ref in the objects that need it
        # self.track_service = track_service
        # self.user_service = user_service
        # self.album_service = album_service
        # self.artist_service = artist_service
        # self.playlist_service = playlist_service
        # self.track_feature_service = feature_service
        # the others
        self.track = SpotifyTrackPersistence(track_service,
                                             feature_service)
        self.playlist = SpotifyPlaylistPersistence(
            playlist_service)
        self.album = SpotifyAlbumPersistence(album_service)
        self.artist = SpotifyArtistPersistence(artist_service)


class SpotifyTrackPersistence:

    def __init__(self, track_service: TrackService,
                 track_feature_service: TrackFeaturesService):
        self.track_service = track_service
        self.track_feature_service = track_feature_service

    def add_track_to_library(self, track: TrackData):
        self.track_service.create_track(track_data=track)

    def add_tracks_to_library(self, tracks: List[TrackData]):
        for track in tracks:
            self.add_track_to_library(track=track)

    def add_features_to_track(self, features: TrackFeaturesData):
        self.track_feature_service.create_track_features(
            track_features_data=features
        )

    def add_features_to_tracks(self, tracks_features: List[TrackFeaturesData]):
        for features in tracks_features:
            self.add_features_to_track(features)


class SpotifyPlaylistPersistence:

    def __init__(self, playlist_service: PlaylistService):
        self.playlist_service = playlist_service

    def add_playlist_to_library(self, playlist: PlaylistData):
        # make sure ALL your services use the dtos instead of the serializers,
        # i think some of them might be using serializers
        self.playlist_service.create_playlist(playlist=playlist)

    def add_playlists_to_library(self, playlists: List[PlaylistData]):
        for playlist in playlists:
            self.add_playlist_to_library(playlist=playlist)

    def add_track_to_playlist(self, playlist_id, track_uri):
        self.playlist_service.add_track_to_playlist(playlist_id, track_uri)

    def add_tracks_to_playlist(self, track_uris: List[str], playlist_id: str):
        for uri in track_uris:
            self.add_track_to_playlist(playlist_id, uri)


class SpotifyAlbumPersistence:
    def __init__(self, album_service: AlbumService):
        self.album_service = album_service

    def add_album_to_library(self, album: AlbumData):
        self.album_service.create_album(album_data=album)
    # non bulk create

    def add_albums_to_library(self, albums: List[AlbumData]):
        for album in albums:
            self.add_album_to_library(album=album)

    def add_track_to_album(self, album_uri, track_uri):
        self.album_service.add_track_to_album(album_uri, track_uri)

    def add_tracks_to_album(self, album_uri: str, tracks_uri: List[str]):
        for uri in tracks_uri:
            self.add_track_to_album(album_uri, uri)

    def add_tracks_to_albums(self, album_track_data: dict):
        for album_uri, track_uris in album_track_data.items():
            self.add_tracks_to_album(album_uri, track_uris)


class SpotifyArtistPersistence:
    def __init__(self, artist_service: ArtistService):
        self.artist_service = artist_service

    def add_artist_to_library(self, artist: ArtistData):
        self.artist_service.create_artist(artist_data=artist)

    def add_artists_to_library(self, artists: List[ArtistData]):
        for artist in artists:
            self.add_artist_to_library(artist=artist)
