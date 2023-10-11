"""_summary_

    Returns:
        _type_: _description_
"""
from typing import Optional
import logging

from injector import inject

from ..models import History
from .service_dtos import HistoryData
from .user_service import  UserService
from .track_service import TrackService

class HistoryService:
    """_summary_

    Returns:
        _type_: _description_
    """
    @inject
    def __init__(self, history_model: History,user_service:UserService,track_service: TrackService,logger: logging.Logger):
        self.history_model = history_model
        self.logger=logger
        self.user_service=user_service
        self.track_service=track_service
    def create_listening_history(self, history_data:HistoryData):
        self.history_model.objects.create(**history_data)
    #pass the data object, need alot more fields from it 
    def get_history(self,history_data:HistoryData )->Optional[History]:
        try:
            #history=self.history_model.objects.get(**history_data)
            track=self.track_service.get_track(history_data['track_uri'])
            user=self.user_service.get_user(history_data['user_id'])
            payload=history_data.copy()
            payload['track_uri']=track
            payload['user_id']=user
            #tuple is returned, first elem is the record and second one is the flag denoting if it was present to begin with
            return self.history_model.objects.get_or_create()[0]
        except Exception :
            self.logger.exception("An exception occured in get_track:")
    def update_history(self , updated_history_data:HistoryData, prev_history_data:HistoryData):
        history=self.get_history(history_data=prev_history_data)
        if(history):
            for key, value in updated_history_data.items():
                setattr(history, key, value)
            history.save()
        else:
            self.logger.warning("History record does not exist. Check for race conditions or validate your input sources.")
    def delete_history(self, history_data:HistoryData):
        history=self.get_history(self,history_data=history_data)
        if(history is not None):
            history.delete()
        else:
            self.logger.warning("History record does not exist. Check for race conditions or validate your input sources.")
    def get_all_users_histories(self, user_id):
        return self.history_model.objects.filter(user_id=user_id)