from typing import TypedDict
from ..services.core.user_service import UserService
from ..services.core.track_service import TrackService
from ..services.core.album_service import AlbumService
from ..services.core.artist_service import ArtistService
from ..services.core.playlist_service import PlaylistService
from ..services.core.image_service import ImageService
from ..services.core.genre_service import GenreService
from ..services.core.track_features_service import TrackFeaturesService
from ..services.spotify.token_handler import SpotifyTokenHandler
from ..services.spotify.persistence_service import SpotifyDataPersistence
from ..services.spotify.retrieval.spotify_favorite_service \
    import SpotifyFavoritesService
from ..services.spotify.retrieval.spotify_playlist_service \
    import SpotifyPlaylistService


class Services(TypedDict):
    user_service: UserService
    token_handler: SpotifyTokenHandler
    sp_favorites_service: SpotifyFavoritesService
    sp_playlist_service: SpotifyPlaylistService
    track_service: TrackService
    album_service: AlbumService
    artist_service: ArtistService
    playlist_service: PlaylistService
    feature_service: TrackFeaturesService
    images_service: ImageService
    genre_service: GenreService

    persistence_service: SpotifyDataPersistence


class CoreServices(TypedDict):
    track_service: TrackService
    album_service: AlbumService
    artist_service: ArtistService
    playlist_service: PlaylistService
