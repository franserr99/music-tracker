from injector import inject
from models import LikedTrack,LikedTrackData
from services import liked_track_service as TrackService
import logging

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