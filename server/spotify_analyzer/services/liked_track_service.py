from injector import inject

from service_dtos import LikedTrackData
from track_service import TrackService
from user_service import UserService
import logging

class LikedTrackService:
    @inject
    def __init__(self, track_service: TrackService,user_service:UserService,logger: logging.Logger  ):
        self.track_service=track_service
        self.user_service=user_service
        self.logger=logger
    def like_track(self, liked_track_data:LikedTrackData):
        user_id=liked_track_data['user_id']
        user=self.user_service.get_user(user_id)
        if(user is None):
            self.logger.warning("User record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("User: id: %s",user_id," was attempted to be pulled from the db but does not exist")
        track_uri=track_uri=liked_track_data['track_uri']
        track=self.track_service.get_track(track_uri)
        if(track is None):
            self.logger.warning("Track record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Track: uri: %s",track_uri," was attempted to be pulled from the db but does not exist")

        user.liked_tracks.add(track)

    def get_user_liked_tracks(self, user_id:str):
        user=self.user_service.get_user('user_id')
        if(user):
            return user.liked_tracks.all()
        else:
            self.logger.warning("User record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("User: id: %s",user_id," was attempted to be pulled from the db but does not exist")

    def unlike_track(self, liked_track_data:LikedTrackData):
        track_uri=liked_track_data['track_uri']
        track=self.track_service.get_track(track_uri)
        user=self.user_service.get_user(liked_track_data['user_id'])
        if user.liked_tracks.filter(id=track_uri).exists():
            user.liked_tracks.remove(track)
        else:
            track_uri=liked_track_data['track_uri']
            user_id=liked_track_data['user_id']
            self.logger.warning("Track was not liked to begin wtih. Check for race conditions or validate your input sources.")
            self.logger.warning("Track: track_uri: %s",track_uri," for user %s was attempted to be pulled from the db but does not exist",user_id)
    