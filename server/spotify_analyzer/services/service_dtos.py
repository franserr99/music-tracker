from datetime import datetime
from typing import TypedDict
# typed dictionaries for use in the service layer
# here are my data transfer objects

class TrackFeaturesData(TypedDict):
    track_uri:str
    danceability:float
    energy : float
    key : float
    loudness : float
    mode : float
    speechiness : float
    acousticness : float
    instrumentalness : float
    liveness : float
    valence : float
    tempo : float
class TrackData(TypedDict):
    uri :str
    track_name : str
    track_artists :str
class HistoryData(TypedDict):
    user_id :str
    date_recorded:datetime
    relative_term :str
    track_uri :str
class UserData(TypedDict):
    user_id:str
class PlaylistData(TypedDict):
    playlist_id:str
    created_by:str