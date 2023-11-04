"""
    _summary_

    Returns:
        _type_: _description_
"""
from typing import Optional
import logging

from injector import inject, singleton

from ..models import Playlist
from .user_service import UserService
from .service_dtos import PlaylistData
from .track_service import TrackService
from ..serializers import PlaylistSerializer
from ..util import log_error


@singleton
class PlaylistService:
    """_summary_

    Returns:
        _type_: _description_
    """
    @inject
    def __init__(self, playlist_model: Playlist, track_service: TrackService, user_service: UserService, logger: logging.Logger):
        self.playlist_model = playlist_model
        self.track_service = track_service
        self.user_service = user_service
        self.logger = logger

    def create_playlist(self, serializer: PlaylistSerializer):
        """_summary_

        Args:
            serializer (PlaylistSerializer): _description_
        """
        # data validation occurs at the view layer
        payload = serializer.validated_data.copy()
        user_id = payload['created_by']
        user = self.user_service.get_user(user_id=user_id)
        if user:
            payload['created_by'] = user
            self.playlist_model.objects.create(**payload)
        else:
            log_error(logger=self.logger, entity="User", identifier=user_id)

    def get_playlist(self, playlist_data: PlaylistData) -> Optional[Playlist]:
        """_summary_

        Args:
            playlist_data (PlaylistData): _description_

        Returns:
            Optional[Playlist]: _description_
        """
        payload = playlist_data.copy()
        user_id = playlist_data['user_id']
        user = self.user_service.get_user(user_id=user_id)
        try:
            if user:
                payload['user_id'] = user
                return self.playlist_model.objects.get(**payload)
            log_error(logger=self.logger, entity="User", identifier=user_id)
        except self.playlist_model.DoesNotExist:
            self.logger.exception("An exception occured in get_playlist:")
        except self.playlist_model.MultipleObjectsReturned:
            self.logger.exception("More than two objects get_playlist")

    def update_playlist(self, old_data: PlaylistData, new_data: PlaylistData):
        """_summary_

        Args:
            old_data (PlaylistData): _description_
            new_data (PlaylistData): _description_
        """
        playlist = self.get_playlist(playlist_data=old_data)
        playlist_id = old_data['playlist_id']
        if (playlist):
            for key, value in new_data.items():
                setattr(playlist, key, value)
            playlist.save()
        else:
            log_error(logger=self.logger, entity="Playlist",
                      identifier=playlist_id)

    def delete_playlist(self, playlist_data: PlaylistData):
        """_summary_

        Args:
            playlist_data (PlaylistData): _description_
        """
        playlist = self.get_playlist(playlist_data=playlist_data)
        playlist_id = playlist['playlist_id']
        if (playlist):
            playlist.delete()
        else:
            log_error(logger=self.logger, entity="Playlist",
                      identifier=playlist_id)

    def get_user_playlists(self, user_id: str):
        """_summary_

        Args:
            user_id (str): _description_

        Returns:
            _type_: _description_
        """
        user = self.user_service.get_user(user_id=user_id)
        if (user):
            return self.playlist_model.objects.get(user=user)
        else:
            log_error(logger=self.logger, entity="User", identifier=user_id)
