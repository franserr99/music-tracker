from datetime import datetime
from typing import List, TypedDict
# typed dictionaries for use in the service layer
# here are my data transfer objects


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


class TrackData(TypedDict):
    uri: str
    track_name: str


class ArtistData(TypedDict):
    uri: str
    name: str


class GenreData(TypedDict):
    name: str

# can use for both, we get another dict and place the refernece in there


class AlbumData(TypedDict):
    uri: str


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


class PlaylistData(TypedDict):
    playlist_id: str


class LikedTrackData(TypedDict):
    user_id: str
    track_uri: str


class ImageData(TypedDict):
    url: str
    height: int
    width: int


class FavoriteItemsInfo(TypedDict):
    track_uris: List[str]
    track_name: List[str]
    track_artist: List[str]
    track_album_uri: List[str]
    track_album_type: List[str]
    album_num_of_tracks: List[int]
    album_images: List[ImageData]
