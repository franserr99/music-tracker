from datetime import datetime
from typing import TypedDict
# typed dictionaries for use in the service layer
# will provide compile time type checking
# here are my data transfer objects
# im keeping the dtos seperate from the serializers used in the views layer
# i want to keep business logic seperate

class TrackFeaturesData(TypedDict):
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
    
class LikedTrackData(TypedDict):
    user_id:str
    track_uri :str
class PlaylistData(TypedDict):
    playlist_id:str
    user_id:str
    
class PlaylistTrackData(TypedDict):
    playlist_id:str
    track_uri:str