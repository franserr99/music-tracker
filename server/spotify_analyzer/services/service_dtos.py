from datetime import datetime
from typing import List, TypedDict, Dict
# typed dictionaries for use in the service layer
# here are my data transfer objects
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
    import SpotifyTrackService


class TrackFeaturesData(TypedDict):
    track_uri: str
    danceability: float
    energy: float
    key: float
    loudness: float
    mode: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
# can use for both, we get another dict and place the refernece in there


class HistoryData(TypedDict):
    user_id: str
    date_recorded: datetime
    relative_term: str
    track_uri: str


class UserData(TypedDict):
    id: str


class UserTokenInfo (TypedDict):
    refresh_token: str
    access_token: str


class LikedTrackData(TypedDict):
    user_id: str
    track_uri: str


class ImageData(TypedDict):
    url: str
    height: int
    width: int


class AlbumData(TypedDict):
    uri: str
    album_type: str
    total_tracks: int
    url: str
    name: str


class GenreData(TypedDict):
    name: str


class TrackData(TypedDict):
    uri: str
    track_name: str


class ArtistData(TypedDict):
    uri: str
    name: str


class FullArtistData(TypedDict):
    artist_uri: str
    image_urls: List[str]
    genres: List[GenreData]
    name: str


class FullAlbumData(TypedDict):
    album_uri: str
    album_name: str
    image_urls: List[str]
    album_type: str
    total_tracks: int
    url: str
    artists_uri: List[str]

# make the high level entity one as hollow as possible
# only keep the uris, we will insert them in the right order so there
# wont be any issue there


class FullTrackData(TypedDict):
    track_uri: str
    track_name: str
    artist_uri: List[str]
    album_uri: str


class PlaylistData(TypedDict):
    playlist_id: str
    owner: str
    tracks: List[str]


class FavoriteTracksInfo(TypedDict):
    tracks: Dict[str, FullTrackData]
    albums: Dict[str, FullAlbumData]
    artists: Dict[str, FullArtistData]
    images: Dict[str, ImageData]
    genres: Dict[str, GenreData]


class PlaylistsInfo(TypedDict):
    tracks: Dict[str, FullTrackData]
    albums: Dict[str, FullAlbumData]
    artists: Dict[str, FullArtistData]
    images: Dict[str, ImageData]
    playlists: Dict[str, PlaylistData]
    users: Dict[str, UserData]


class FavoriteArtistsInfo(TypedDict):
    artists: Dict[str, FullArtistData]
    images: Dict[str, ImageData]
    genres: Dict[str, GenreData]


class Services(TypedDict):
    user_service: UserService
    token_handler: SpotifyTokenHandler
    sp_track_service: SpotifyTrackService
    track_service: TrackService
    album_service: AlbumService
    artist_service: ArtistService
    playlist_service: PlaylistService
    feature_service: TrackFeaturesService
    images_service: ImageService
    genre_service: GenreService

    persistence_service: SpotifyDataPersistence
