from typing import TypedDict
from ..core.user_service import UserService
from ..core.track_service import TrackService
from ..core.album_service import AlbumService
from ..core.artist_service import ArtistService
from ..core.playlist_service import PlaylistService
from ..core.image_service import ImageService
from ..core.genre_service import GenreService
from ..core.track_features_service import TrackFeaturesService
from ..spotify.token_handler import SpotifyTokenHandler
from ..spotify.persistence_service import SpotifyDataPersistence
from ..spotify.retrieval.spotify_favorite_service \
    import SpotifyFavoritesService
from ..spotify.retrieval.spotify_playlist_service \
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
