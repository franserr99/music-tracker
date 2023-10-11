""""
Module for:
"""

import logging

from injector import inject

from .service_dtos import LikedTrackData
from .track_service import TrackService
from .user_service import UserService
from ..util import log_error


class LikedTrackService:
    """_summary_

    Returns:
        _type_: _description_
    """
    @inject
    def __init__(self,track_service:TrackService,user_service:UserService,logger:logging.Logger):
        self.track_service=track_service
        self.user_service=user_service
        self.logger=logger
    def like_track(self, liked_track_data:LikedTrackData):
        """_summary_

        Args:
            liked_track_data (LikedTrackData): _description_
        """
        user_id=liked_track_data['user_id']
        user=self.user_service.get_user(user_id)
        if not user:
            log_error(logger=self.logger,entity="User",identifier=user_id)
        track_uri=track_uri=liked_track_data['track_uri']
        track=self.track_service.get_track(track_uri)
        if(track is None):
            log_error(logger=self.logger,entity="Track",identifier=track_uri)
        user.liked_tracks.add(track)

    def get_user_liked_tracks(self, user_id:str):
        """_summary_

        Args:
            user_id (str): _description_

        Returns:
            _type_: _description_
        """
        user=self.user_service.get_user('user_id')
        if(user):
            return user.liked_tracks.all()
        else:
            log_error(logger=self.logger,entity="User",identifier=user_id)

    def unlike_track(self, liked_track_data:LikedTrackData):
        """_summary_

        Args:
            liked_track_data (LikedTrackData): _description_
        """
        track_uri=liked_track_data['track_uri']
        track=self.track_service.get_track(track_uri)
        user=self.user_service.get_user(liked_track_data['user_id'])
        if user.liked_tracks.filter(id=track_uri).exists():
            user.liked_tracks.remove(track)
        else:
            track_uri=liked_track_data['track_uri']
            user_id=liked_track_data['user_id']
            log_error(logger=self.logger,entity="TrackLiked",identifier=track_uri)
    