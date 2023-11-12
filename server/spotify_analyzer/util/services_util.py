
from ..services.core.user_service import UserService
from ..services.core.track_service import TrackService
from ..services.core.album_service import AlbumService
from ..services.core.artist_service import ArtistService
from ..services.core.playlist_service import PlaylistService
from ..services.core.image_service import ImageService
from ..services.core.genre_service import GenreService
from ..models import User, Track, Album, Artist, Playlist, TrackFeatures, \
    Image, Genre
from ..services.spotify.retrieval.spotify_favorite_service\
    import SpotifyFavoritesService
from ..services.spotify.persistence_service\
    import SpotifyDataPersistence
from ..services.dtos.service_dtos import Services, SpotifyPlaylistService, \
    CoreServices
from ..services.spotify.token_handler import SpotifyTokenHandler
from ..services.core.track_features_service import TrackFeaturesService

scope = "user-library-read user-read-playback-position user-top-read \
user-read-recently-played playlist-read-private"


def init_all_services(user_id, logger) -> Services:
    user_service = UserService(user_model=User, logger=logger)
    token_handler = SpotifyTokenHandler(
        user_service=user_service, user_id=user_id)
    sp_favorites_service = SpotifyFavoritesService(client=token_handler.client,
                                                   token_handler=token_handler)
    sp_playlist_service = SpotifyPlaylistService(client=token_handler.client,
                                                 token_handler=token_handler)

    genre_service = GenreService(genre_model=Genre, logger=logger)
    artist_service = ArtistService(
        artist_model=Artist, logger=logger, genre_service=genre_service)
    track_service = TrackService(
        track_model=Track, logger=logger, artist_service=artist_service)
    album_service = AlbumService(album_model=Album, logger=logger,
                                 track_service=track_service,
                                 artist_service=artist_service)

    playlist_service = PlaylistService(playlist_model=Playlist,
                                       logger=logger,
                                       track_service=track_service,
                                       user_service=user_service)
    feature_service = TrackFeaturesService(
        features_model=TrackFeatures,
        track_service=track_service, logger=logger)
    images_service = ImageService(image_model=Image, logger=logger,
                                  album_service=album_service,
                                  artist_service=artist_service)

    persistence_service = SpotifyDataPersistence(
        track_service=track_service, user_service=user_service,
        album_service=album_service, artist_service=artist_service,
        playlist_service=playlist_service,
        feature_service=feature_service,
        image_service=images_service, genre_service=genre_service
    )
    return Services(
        user_service=user_service, token_handler=token_handler,
        sp_favorites_service=sp_favorites_service,
        track_service=track_service, album_service=album_service,
        artist_service=artist_service,
        playlist_service=playlist_service,
        feature_service=feature_service, images_service=images_service,
        genre_service=genre_service,
        persistence_service=persistence_service,
        sp_playlist_service=sp_playlist_service
    )


def init_core_services(logger) -> CoreServices:
    user_service = UserService(user_model=User, logger=logger)
    genre_service = GenreService(genre_model=Genre, logger=logger)
    artist_service = ArtistService(
        artist_model=Artist, logger=logger, genre_service=genre_service)
    track_service = TrackService(
        track_model=Track, logger=logger, artist_service=artist_service)
    album_service = AlbumService(album_model=Album, logger=logger,
                                 track_service=track_service,
                                 artist_service=artist_service)

    playlist_service = PlaylistService(playlist_model=Playlist,
                                       logger=logger,
                                       track_service=track_service,
                                       user_service=user_service)
    return CoreServices(
        track_service=track_service,
        album_service=album_service,
        playlist_service=playlist_service,
        artist_service=artist_service)
