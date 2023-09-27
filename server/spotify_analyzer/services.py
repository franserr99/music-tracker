#get models
from .models import TrackFeatures,Track,History,User,LikedTrack,Playlist,PlaylistTrack
#get dict data representation
from .models import TrackFeaturesData,TrackData, HistoryData,UserData,LikedTrackData,PlaylistTrackData,PlaylistData
from django_injector import inject
from typing import TypedDict

class TrackFeaturesService:
    @inject
    def __init__(self, track_features_model: TrackFeatures):
        self.track_features_model = track_features_model

    def create_track_features(self, track_features_data:TrackFeaturesData):
        self.track_features_model.objects.create(**track_features_data)
        pass
    def get_track_trackes(self):
        pass
    def update_track_features(self):
        pass
    def delete_track_features(self):
        pass
    def get_all_tracks_features(self):
        pass
    pass

class TrackService:
    @inject
    def __init__(self, track_model: Track):
        self.track_model = track_model

    def create_track(self, track_data:TrackData):
        self.track_model.objects.create(**track_data)
        pass
    def get_track(self):
        pass
    def update_track(self):
        pass
    def delete_track(self):
        pass
    def get_all_tracks(self):
        pass
    pass

class HistoryService:
    @inject
    def __init__(self, history_model: History):
        self.history_model = history_model

    def create_listening_history(self, history_data:HistoryData):
        self.history_model.objects.create(**history_data)
        pass
    def get_history(self):
        pass
    def update_history(self):
        pass
    def delete_history(self):
        pass
    def get_all_users_histories(self):
        pass
    pass

class UserService:
    @inject
    def __init__(self, user_model: User):
        self.user_model = user_model

    def create_user(self, user_data:UserData):
        self.user_model.objects.create(**user_data)
        pass
    def get_user(self):
        pass
    def update_user(self):
        pass
    def delete_user(self):
        pass
    def get_all_users(self):
        pass
    pass

class LikedTrackService:
    @inject
    def __init__(self, liked_track_model: LikedTrack):
        self.liked_track_model = liked_track_model

    def create_liked_track(self, liked_track_data:LikedTrackData):
        self.liked_track_model.objects.create(**liked_track_data)
        pass
    def get_liked_track(self):
        pass
    def update_liked_track(self):
        pass
    def delete_liked_track(self):
        pass
    def get_all_liked_tracks(self):
        pass
    
    pass

class PlaylistService:
    @inject
    def __init__(self, playlist_model: Playlist):
        self.playlist_model = playlist_model
    
    def create_user(self, ):
        self.playlist_model.objects.create(**liked_track_data)
        pass
    def get_user(self):
        pass
    def update_user(self):
        pass
    def delete_user(self):
        pass
    def get_all_users(self):
        pass
    
    pass

class PlaylistTrackService:
    @inject
    def __init__(self, playlist_track_model: PlaylistTrack):
        self.playlist_track_model = playlist_track_model
    
    def create_playlist_track(self,playlist_track_data:PlaylistTrackData ):
        self.playlist_track_model.objects.create(**playlist_track_data)
        pass
    def get_playlist_track(self):
        pass
    def update_playlist_track(self):
        pass
    def delete_playlist_track(self):
        pass
    def get_all_playlist_tracks(self):
        pass
    
    pass
################## defined dictionaries for
# why: I want to pass in an object and instantiate that way instead of through function paramters
#       but responsibility gets shifted of validation/correctness when I create said dictionary
#       either i create a batch of validation functions or use a typed dictionary


