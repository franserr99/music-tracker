"""_summary_

    Returns:
        _type_: _description_
"""
from typing import Optional
import logging

from injector import inject
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError

from ...models import History
from ..service_dtos import HistoryData
from .user_service import UserService
from .track_service import TrackService


class HistoryService:
    """_summary_

    Returns:
        _type_: _description_
    """
    @inject
    def __init__(self, history_model: History, user_service: UserService,
                 track_service: TrackService, logger: logging.Logger):
        self.history_model = history_model
        self.logger = logger
        self.user_service = user_service
        self.track_service = track_service

    def create_listening_history(self, history_data: HistoryData):
        """_summary_

        Args:
            history_data (HistoryData): _description_
        """
        user_id = history_data.get('user_id')
        track_uri = history_data.get('track_uri')

        # get the instances
        user_instance = self.user_service.get_user(id=user_id)
        track_instance = self.track_service.get(track_uri=track_uri)

        if user_instance and track_instance:
            # repplace the id's w the instances
            history_data['user'] = user_instance
            history_data['track'] = track_instance
            try:
                history, created = self.history_model.objects.get_or_create(
                    **history_data)
                return history
            except (IntegrityError, ValidationError,
                    DatabaseError, TypeError, ValueError) as e:
                self.logger.exception(
                    f"error occurred while creating a history record: {e}")
                return None
        else:
            self.logger.error(f"Could not find instances for User ID {
                              user_id} or Track URI {track_uri}")
            return None

    # pass the data object, need alot more fields from it
    def get_history(self, history_data: HistoryData) -> Optional[History]:
        """_summary_

        Args:
            history_data (HistoryData): _description_

        Returns:
            Optional[History]: _description_
        """

        user_id = history_data.get('user_id')
        track_uri = history_data.get('track_uri')

        # get the instances
        user_instance = self.user_service.get_user(id=user_id)
        track_instance = self.track_service.get_track(track_uri=track_uri)

        payload = history_data.copy()
        if user_instance and track_instance:
            # repplace the id's w the instances
            payload['user'] = user_instance
            payload['track'] = track_instance
            # tuple is returned:
            # first elem is the record
            # second one is the flag denoting if it was present to begin with
            try:

                return self.history_model.objects.get_or_create()[0]
            except self.history_model.DoesNotExist:
                self.logger.exception("An exception occured in get_history:")

    def update_history(self, updated_history_data: HistoryData,
                       prev_history_data: HistoryData):
        """_summary_

        Args:
            updated_history_data (HistoryData): _description_
            prev_history_data (HistoryData): _description_
        """
        history = self.get_history(history_data=prev_history_data)
        if (history):
            for key, value in updated_history_data.items():
                setattr(history, key, value)
            history.save()
        else:
            self.logger.warning(
                "History record DNE. Check for race conditions or validate.")

    def delete_history(self, history_data: HistoryData):
        """_summary_

        Args:
            history_data (HistoryData): _description_
        """
        history = self.get_history(history_data=history_data)
        if (history is not None):
            history.delete()
        else:
            self.logger.warning(
                "History record DNE. Check for race conditions or validate.")

    def get_all_users_histories(self, user_id):
        """_summary_

        Args:
            user_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.history_model.objects.filter(user_id=user_id)
