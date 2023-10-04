#my models
from .models import TrackFeatures,Track,History,User,LikedTrack,Playlist,PlaylistTrack
#my dict data representation
from .models import TrackFeaturesData,TrackData, HistoryData,UserData,LikedTrackData,PlaylistTrackData,PlaylistData
#from django_injector import inject
import traceback
from injector import singleton, inject
from typing import Optional
import logging 

@singleton
class TrackService:
    @inject
    def __init__(self, track_model: Track,logger: logging.Logger ):
        self.track_model = track_model
        self.logger=logger
    def create_track(self, track_data:TrackData):
        self.track_model.objects.create(**track_data)
    #identifiable by uri so only use it
    def get_track(self, track_uri:str):
        try:
            print(self.track_model.objects.get(track_uri=track_uri))
            track=self.track_model.objects.get(track_uri=track_uri)
            if(track):
                return track
            else:
                self.logger.error("")
        except Exception as e:
            self.logger.exception("An exception occured in get_track:")
    def update_track(self, track_uri:str, track_data:TrackData):
        track=self.get_track(self,track_uri=track_uri)
        if(track):
            for key, value in track_data.items():
                setattr(track, key, value)
            track.save()
        else:
            self.logger.warning("Track does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Track with uri: %s",track_uri," was attempted to be pulled from the db but does not exist")
            
    def delete_track(self,track_uri:str):
        track=self.get_track(self,track_uri=track_uri)
        if(track):
            track.delete()
        else:
            self.logger.warning("Track does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Track with uri: %s",track_uri," was attempted to be pulled from the db but does not exist")
    def get_all_tracks(self):
        return self.track_model.objects.all()
    
@singleton
class UserService:
    @inject
    def __init__(self, user_model: User,logger: logging.Logger):
        self.user_model = user_model
        self.logger=logger
    def create_user(self, user_data:UserData):
        self.user_model.objects.create(**user_data)
    def get_user(self, user_id):
        try:
            self.user_model.objects.get(user_id=user_id)
        except Exception:
            self.logger.exception("An exception occured in get_user:")
    def update_user(self,user_id, user_data:UserData):
        user=self.get_user(self,user_id=user_id)
        if(user):
            for key, value in user_data.items():
                setattr(user,key,value)
            user.save()
        else:
            self.logger.warning("User does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("User with id: %s",user_id," was attempted to be pulled from the db but does not exist")
    def delete_user(self, user_id):
        user=self.get_user(self,user_id=user_id)
        if(user):
            user.delete()
        else:
            self.logger.warning("User does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("User with id: %s",user_id," was attempted to be pulled from the db but does not exist")
    def get_all_users(self):
        return self.user_model.objects.all()

class TrackFeaturesService:
    @inject
    def __init__(self, track_features_model: TrackFeatures,track_service: TrackService,logger: logging.Logger ):
        self.track_features_model = track_features_model
        self.track_service = track_service
        self.logger=logger
    def create_track_features(self, track_features_data:TrackFeaturesData):
        track_instance = self.track_service.get_track(track_features_data['track_uri'])
        if track_instance:
            data_copy=track_features_data.copy()
            data_copy['track_uri']=track_instance
            self.track_features_model.objects.create(**data_copy)
        else:
            self.logger.warning("Track does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Track with uri: %s",track_features_data['track_uri']," was attempted to be pulled from the db but does not exist")
    #identifiable by uri so only use it
    def get_track_features(self, track_uri:str):
        try:
            track_instance = self.track_service.get_track(track_uri=track_uri)
            #print(self.track_features_model.objects.get(track_uri=track_uri))
            if(track_instance):
                return self.track_features_model.objects.get(track=track_instance)
            else:
                self.logger.warning("Track does not exist. Check for race conditions or validate your input sources.")
                self.logger.warning("Track with uri: %s",track_uri," was attempted to be pulled from the db but does not exist")
        except Exception:
            self.logger.exception("An exception occured in get_track_features:")
    def update_track_features(self, track_uri:str, track_features_data:TrackFeaturesData):
        
        track_feature=self.get_track_features(track_uri=track_uri)
        if(track_feature):
            for key, value in track_features_data.items():
                setattr(track_feature, key, value)
            track_feature.save()
        else:
            self.logger.warning("TrackFeatures record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("TrackFeatures for track with uri: %s",track_uri," was attempted to be pulled from the db but does not exist")
    def delete_track_features(self, track_uri:str):
        track_feature=self.get_track_features(track_uri=track_uri)
        if(track_feature):    
            track_feature.delete()
        else:
            self.logger.warning("TrackFeatures record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("TrackFeatures for track with uri: %s",track_uri," was attempted to be pulled from the db but does not exist")
    def get_all_tracks_features(self):
        return self.track_features_model.objects.all()
    
class LikedTrackService:
    @inject
    def __init__(self, liked_track_model: LikedTrack,track_service: TrackService,user_service:UserService,logger: logging.Logger  ):
        self.liked_track_model = liked_track_model
        self.track_service=track_service
        self.user_service=user_service
        self.logger=logger
    def create_liked_track(self, liked_track_data:LikedTrackData):
        user=self.user_service.get_user(liked_track_data['user_id'])
        track=self.track_service.get_track(track_uri=liked_track_data['track_uri'])
        payload={ 
            'user_id':user,'track_uri':track
        }
        self.liked_track_model.objects.create(**payload)
    def get_liked_track(self,liked_track_data:LikedTrackData ):
        track_uri=liked_track_data['track_uri']
        user_id=liked_track_data['user_id']
        user=self.user_service.get_user(user_id=user_id)
        track=self.track_service.get_track(track_uri=track_uri)
        payload={ 
            'user_id':user,'track_uri':track
        }
        try:
            liked_track=self.liked_track_model.objects.get(**payload)
            if liked_track:
                return liked_track
            else:
                self.logger.warning("LikedTrack record does not exist. Check for race conditions or validate your input sources.")
                self.logger.warning("LikedTrack: track_uri: %s",track_uri," for user %s was attempted to be pulled from the db but does not exist",user_id)
        except Exception:
            self.logger.exception("An exception occured in get_track:")
    def update_liked_track(self,old_data:LikedTrackData, new_data:LikedTrackData ):
        liked_track=self.get_liked_track(self,liked_track_data=old_data)
        if(liked_track):
            for key,value in new_data.items():
                setattr(liked_track,key,value)
            liked_track.save()
        else:
            track_uri=old_data['track_uri']
            user_id=old_data['user_id']
            self.logger.warning("LikedTrack record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("LikedTrack: track_uri: %s",track_uri," for user %s was attempted to be pulled from the db but does not exist",user_id)
    def delete_liked_track(self, liked_track_data:LikedTrackData):
        liked_track=self.get_liked_track(self,liked_track_data=liked_track_data)
        if(liked_track):
            liked_track.delete()
        else:
            track_uri=liked_track_data['track_uri']
            user_id=liked_track_data['user_id']
            self.logger.warning("LikedTrack record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("LikedTrack: track_uri: %s",track_uri," for user %s was attempted to be pulled from the db but does not exist",user_id)
    def get_all_liked_tracks(self, user_id:str):
        user=self.user_service.get_user('user_id')
        if(user):
            return self.liked_track_model.objects.filter(user=user)
        else:
            self.logger.warning("User record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("User: id: %s",user_id," was attempted to be pulled from the db but does not exist")
@singleton
class PlaylistService:
    @inject
    def __init__(self, playlist_model: Playlist, track_service: TrackService,user_service:UserService,logger: logging.Logger):
        self.playlist_model = playlist_model
        self.track_service=track_service
        self.user_service=user_service
        self.logger=logger
    def create_playlist(self, playlist_data:PlaylistData):
        payload=playlist_data.copy()
        user_id=playlist_data['user_id']
        user=self.user_service.get_user(user_id=user_id)
        if(user):
            payload['user_id']=user
            self.playlist_model.objects.create(**payload)
        else:
            self.logger.warning("User record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("User: id: %s",user_id," was attempted to be pulled from the db but does not exist")
    def get_playlist(self,playlist_data:PlaylistData):
        payload=playlist_data.copy()
        user_id=playlist_data['user_id']
        user=self.user_service.get_user(user_id=user_id)
        try:
            if(user):
                payload['user_id']=user
                self.playlist_model.objects.get(**payload)
            else:
                self.logger.warning("User record does not exist. Check for race conditions or validate your input sources.")
                self.logger.warning("User: id: %s",user_id," was attempted to be pulled from the db but does not exist")
        except Exception:
            self.logger.exception("An exception occured in get_playlist:")
    def update_playlist(self, old_data:PlaylistData, new_data:PlaylistData):
        playlist=self.get_playlist(self,playlist_data=old_data)
        if(playlist):
            for key,value in new_data.items():
                setattr(playlist,key,value)
            playlist.save()
        else:
            self.logger.warning("Playlist record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Playlist with playlist_id: %s",old_data['playlist_id']," was attempted to be pulled from the db but does not exist")
    def delete_playlist(self,playlist_data:PlaylistData):
        playlist=self.get_playlist(self,playlist_data=playlist_data)
        if(playlist):
            playlist.delete()
        else:
            self.logger.warning("Playlist record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Playlist with playlist_id: %s",playlist['playlist_id']," was attempted to be pulled from the db but does not exist")
    def get_all_users_playlists(self, user_id:str):
        user=self.user_service.get_user(user_id=user_id)
        if(user):
            return self.playlist_model.objects.get(user=user)
        else:
            self.logger.warning("User record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("User: id: %s",user_id," was attempted to be pulled from the db but does not exist")

class PlaylistTrackService:
    @inject
    def __init__(self, playlist_track_model: PlaylistTrack, playlist_service:PlaylistService, track_service: TrackService,logger: logging.Logger):
        self.playlist_track_model = playlist_track_model
        self.playlist_service=playlist_service
        self.track_service=track_service
        self.logger=logger
    
    def create_playlist_track(self, data:PlaylistTrackData, user_id:str, track_data:Optional[TrackData]=None):
        payload=PlaylistData(playlist_id=data['playlist_id'], user_id=user_id)
        playlist=self.playlist_service.get_playlist(playlist_data=payload)
        track=self.track_service.get_track(track_uri=data['track_uri'])
        if(playlist is None):
            self.playlist_service.create_playlist(**payload)
        if(track is None):
            #throw error if they did not pass in data properly
            self.logger.warning("")
            assert(track_data)
            self.track_service.create_track(track_data=track_data)
        self.playlist_track_model.objects.create(**data)

    def get_playlist_track(self,data:PlaylistTrackData, user_id:str ):
        payload=PlaylistData(playlist_id=data['playlist_id'], user_id=user_id)
        playlist=self.playlist_service.get_playlist(playlist_data=payload)
        track=self.track_service.get_track(track_uri=data['track_uri'])

        payload={'playlist_id':playlist,'track_uri':track}

        try:
            if(playlist and track):
                return self.playlist_track_model.objects.get(**payload)
            elif(playlist is not None and track is not None):
                self.logger.info("Trying to add a track to a playlist. Both the playlist record and the track record dont exist in the db.")
                self.logger.warning("Check for race conditions or validate your input sources.")
            elif(playlist is not None):
                self.logger.info("Trying to add a track to a playlist. Playlist record doesnt exist in the db.")
                self.logger.warning("Check for race conditions or validate your input sources.")
            else:#track is not None
                self.logger.info("Trying to add a track to a playlist. Track record does not exist in the db.")
                self.logger.warning("Check for race conditions or validate your input sources.")
        except Exception:
            self.logger.exception("An exception occured in get_playlist_track:")
    def update_playlist_track(self,old_data:PlaylistTrackData,new_data:PlaylistTrackData, user_id:str):
        playlist_track=self.get_playlist_track(data=old_data,user_id=user_id)
        for key,value in new_data.items():
            setattr(playlist_track,key,value)
    def delete_playlist_track(self):
        pass
    def get_all_playlist_tracks(self):
        pass
    
    pass

class HistoryService:
    @inject
    def __init__(self, history_model: History,user_service:UserService,track_service: TrackService,logger: logging.Logger):
        self.history_model = history_model
        self.logger=logger
        self.user_service=user_service
        self.track_service=track_service
    def create_listening_history(self, history_data:HistoryData):
        self.history_model.objects.create(**history_data)
    #pass the data object, need alot more fields from it 
    def get_history(self,history_data:HistoryData ):
        try:
            print(self.history_model.objects.get(**history_data))
            return self.history_model.objects.get(**history_data)
        except Exception :
            self.logger.exception("An exception occured in get_track:")
    def update_history(self , updated_history_data:HistoryData, prev_history_data:HistoryData):
        track=self.get_history(self,history_data=prev_history_data)
        for key, value in updated_history_data.items():
            setattr(track, key, value)
        track.save()

    def delete_history(self, history_data:HistoryData):
        history=self.get_history(self,history_data=history_data)
        if(history is not None):
            history.delete()
 
    def get_all_users_histories(self, user_id):
        return self.history_model.objects.filter(user_id=user_id)

def handleError(self):
    self.logger.error("Here is the trace back:")
    self.logger.error(traceback.format_exc())