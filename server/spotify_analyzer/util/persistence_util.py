from typing import Union
from ..dtos.service_dtos import Services
from ..dtos.retrieval_dtos import FavoriteArtistsInfo, \
    FavoriteTracksInfo, PlaylistsInfo


scope = "user-library-read user-read-playback-position user-top-read \
user-read-recently-played playlist-read-private"


def persist_retrived_data(services: Services,
                          info: Union[FavoriteArtistsInfo,
                                      FavoriteTracksInfo,
                                      PlaylistsInfo], user_id=None):
    persistence = services['persistence_service']
    # if we grow how much we collect, then we need to add a field in the dicts
    # to identify which is which is which, i cannot class check on typed dicts
    # since it does not create a new class for each typed dict i have
    if 'tracks' in info:
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
        if 'playlists' in info:
            playlists = list(info['playlists'].values())
            users = list(info['users'].values())
            # save users
            persistence.user.add_users_to_lib(users)
            # add playlists to library
            # it takes care of fk relationship to user/owner
            persistence.playlist.add_playlists_to_library(playlists)
            # add tracks to playlists
            persistence.playlist.add_tracks_to_playlist(playlists)
            # add likes to playlists
            # might need to refactor or do this like elsewhere
            if (user_id):
                persistence.playlist.add_likes_playlists(playlists, user_id)
        # handle foreign key relationships
        persistence.image.link_images_to_albums(albums)
        persistence.image.link_images_to_artists(artists)
        persistence.album.add_tracks_to_albums(tracks)
        persistence.artist.add_genres_to_artists(artists)
        persistence.album.add_artists_to_albums(albums)
        persistence.track.add_artists_to_tracks(tracks)

    elif len(info.keys()) == 3:
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
