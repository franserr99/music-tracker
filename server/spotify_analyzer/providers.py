from .models import User,Track,TrackFeatures,History,LikedTrack,PlaylistTrack,Playlist
from django_injector import provider, singleton

@provider
@singleton
def provide_user_model() -> User:
    return User
@provider
@singleton
def provide_history_model() -> History:
    return History
@provider
@singleton
def provide_track_features_model() -> TrackFeatures:
    return TrackFeatures
@provider
@singleton
def provide_track_model() -> Track:
    return Track


@provider
@singleton
def provide_liked_track_model() -> LikedTrack:
    return LikedTrack
@provider
@singleton
def provide_playlist_track_model() -> PlaylistTrack:
    return PlaylistTrack
@provider
@singleton
def provide_playlist_model() -> Playlist:
    return Playlist