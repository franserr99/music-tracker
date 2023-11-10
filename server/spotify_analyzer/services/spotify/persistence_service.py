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
from ..core.image_service import ImageService
from ..core.artist_service import ArtistService
from ..core.genre_service import GenreService
from ..core.playlist_service import PlaylistService
from ..core.track_features_service import TrackFeaturesService
from ..service_dtos import TrackData, ArtistData, PlaylistData, AlbumData, \
    TrackFeaturesData, ImageData, GenreData, FullTrackData, FullArtistData, \
    FullAlbumData, UserData

app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


class SpotifyDataPersistence:

    def __init__(self, track_service: TrackService, user_service: UserService,
                 album_service: AlbumService, artist_service: ArtistService,
                 playlist_service: PlaylistService,
                 feature_service: TrackFeaturesService,
                 image_service: ImageService, genre_service: GenreService):
        self.track = SpotifyTrackPersistence(track_service,
                                             feature_service)
        self.playlist = SpotifyPlaylistPersistence(
            playlist_service)
        self.album = SpotifyAlbumPersistence(album_service)
        self.artist = SpotifyArtistPersistence(artist_service)
        self.image = ImagePersistence(image_service)
        self.genre = GenrePersistence(genre_service)
        self.user = UserPersistence(user_service)


class GenrePersistence:
    def __init__(self, genre_service: GenreService):
        self.genre_service = genre_service

    def add_genre_to_library(self, genre: GenreData):
        self.genre_service.create_genre(genre)

    def add_genres_to_library(self, genres: List[GenreData]):
        for genre in genres:
            self.add_genre_to_library(genre)


class UserPersistence:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def add_user_to_lib(self, user: UserData):
        self.user_service.create_user(user_data=user)


class ImagePersistence:
    def __init__(self, image_service: ImageService):
        self.image_serivce = image_service

    def add_image_to_library(self, image: ImageData):
        self.image_serivce.create_image(image_data=image)

    def add_images_to_library(self, images: List[ImageData]):
        for image in images:
            self.add_image_to_library(image)

    def link_image_to_album(self, image_url: str, album_uri: str):
        self.image_serivce.link_image_to_album(album_uri, image_url)

    def link_image_to_artist(self, image_url: str, artist_uri: str):
        self.image_serivce.link_image_to_artist(artist_uri, image_url)
        pass

    def link_images_to_albums(self, albums: List[FullAlbumData]):
        for album in albums:
            images = album['image_urls']
            album_uri = album['album_uri']
            for image in images:
                self.link_image_to_album(image, album_uri)

    def link_images_to_artists(self, artists: List[FullArtistData]):
        for artist in artists:
            images = artist['image_urls']
            artist_uri = artist['artist_uri']
            for image in images:
                self.link_image_to_artist(image, artist_uri)


class SpotifyTrackPersistence:

    def __init__(self, track_service: TrackService,
                 track_feature_service: TrackFeaturesService):
        self.track_service = track_service
        self.track_feature_service = track_feature_service

    def add_track_to_library(self, track: TrackData):
        # create the base track then add the relationships, for now just create
        self.track_service.create_track(track_data=track)

    def add_tracks_to_library(self, tracks: List[FullTrackData]):
        base_track_dtos = [TrackData(
            uri=track['track_uri'],
            track_name=track['track_name']
        ) for track in tracks]
        for track_dto in base_track_dtos:
            self.add_track_to_library(track=track_dto)

    def add_features_to_track(self, features: TrackFeaturesData):
        self.track_feature_service.create_track_features(
            track_features_data=features
        )

    def add_features_to_tracks(self, tracks_features: List[TrackFeaturesData]):
        for features in tracks_features:
            self.add_features_to_track(features)

    def add_artist_to_track(self, artist_uri: str, track_uri: str):
        self.track_service.add_artist_to_track(track_uri, artist_uri)

    def add_artists_to_tracks(self, tracks: List[FullTrackData]):
        for track in tracks:
            track_uri = track['track_uri']
            artist_uris = track['artist_uri']
            for artist in artist_uris:
                self.add_artist_to_track(artist, track_uri)


class SpotifyPlaylistPersistence:

    def __init__(self, playlist_service: PlaylistService):
        self.playlist_service = playlist_service

    def add_playlist_to_library(self, playlist: PlaylistData):
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

    def add_albums_to_library(self, albums: List[FullAlbumData]):
        base_album_dtos = [
            AlbumData(uri=album['album_uri'], album_type=album['album_type'],
                      total_tracks=int(album['total_tracks']),
                      url=album['url'],
                      name=album['album_name']) for album in albums
        ]
        for album_dto in base_album_dtos:
            self.add_album_to_library(album=album_dto)

    def add_track_to_album(self, album_uri, track_uri):
        self.album_service.add_track_to_album(album_uri, track_uri)

    def add_tracks_to_albums(self, tracks_data: List[FullTrackData]):
        for track in tracks_data:
            track_uri = track['track_uri']
            album_uri = track['album_uri']
            self.add_track_to_album(album_uri, track_uri)

    def add_artist_to_album(self, album_uri, artist_uri):
        self.album_service.add_artist_to_album(album_uri, artist_uri)

    def add_artists_to_albums(self, albums: List[FullAlbumData]):
        for album in albums:
            artists = album['artists_uri']
            album_uri = album['album_uri']
            for artist in artists:
                self.add_artist_to_album(album_uri, artist)


class SpotifyArtistPersistence:
    def __init__(self, artist_service: ArtistService):
        self.artist_service = artist_service

    def add_artist_to_library(self, artist: ArtistData):
        self.artist_service.create_artist(artist_data=artist)

    def add_artists_to_library(self, artists: List[FullArtistData]):
        base_artist_dto = [ArtistData(uri=artist['artist_uri'],
                                      name=artist['name'])
                           for artist in artists]
        for artist_dto in base_artist_dto:
            self.add_artist_to_library(artist=artist_dto)

    def add_genre_to_artist(self, genre: str, artist_uri: str):
        self.artist_service.add_genre_to_artist(artist_uri, genre)

    def add_genres_to_artists(self, artists: List[FullArtistData]):
        for artist in artists:
            artist_uri = artist['artist_uri']
            genres = artist['genres']
            for genre in genres:
                self.add_genre_to_artist(genre, artist_uri)
