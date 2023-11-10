from typing import Union
from ..services.service_dtos import Services, FavoriteArtistsInfo, \
    FavoriteTracksInfo, PlaylistsInfo


scope = "user-library-read user-read-playback-position user-top-read \
user-read-recently-played playlist-read-private"


def persist_retrived_data(services: Services,
                          info: Union[FavoriteArtistsInfo,
                                      FavoriteTracksInfo,
                                      PlaylistsInfo]):
    persistence = services['persistence_service']
    if isinstance(info, (PlaylistsInfo, FavoriteTracksInfo)):
        tracks = list(info['tracks'].values())
        artists = list(info['artists'].values())
        albums = list(info['albums'].values())
        images = list(info['images'].values())
        genres = list(info['genres'].values())
        # handle adding base records without fk relationships
        persistence.genre.add_genres_to_library(genres)
        persistence.track.add_tracks_to_library(tracks)
        persistence.image.add_images_to_library(images)
        persistence.artist.add_artists_to_library(artists)
        persistence.album.add_albums_to_library(albums)
        # handle foreign key relationships
        persistence.image.link_images_to_albums(albums)
        persistence.image.link_images_to_artists(artists)
        persistence.album.add_tracks_to_albums(tracks)
        persistence.artist.add_genres_to_artists(artists)
        persistence.album.add_artists_to_albums(albums)
        persistence.track.add_artists_to_tracks(tracks)
    elif isinstance(info, FavoriteArtistsInfo):
        images = list(info['images'].values())
        genres = list(info['genres'].values())
        artists = list(info['artists'].values())
        # handle adding base records without fk relationships
        persistence.genre.add_genres_to_library(genres)
        persistence.image.add_images_to_library(images)
        persistence.artist.add_artists_to_library(artists)
        # handle foreign key relationships
        persistence.image.link_images_to_artists(artists)
        persistence.artist.add_genres_to_artists(artists)
