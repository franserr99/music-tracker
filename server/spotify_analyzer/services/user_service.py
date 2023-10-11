from typing import Optional
import logging

from injector import inject,singleton

from ..models import User
from .service_dtos import UserData
from ..util import log_error

@singleton
class UserService:
    """_summary_

    Returns:
        _type_: _description_
    """
    @inject
    def __init__(self, user_model: User,logger: logging.Logger):
        self.user_model = user_model
        self.logger=logger
    def create_user(self, user_data:dict):
        """_summary_

        Args:
            user_data (UserData): _description_
        """
        self.user_model.objects.create(**user_data)
    def get_user(self, user_id)->Optional[User]:
        """_summary_

        Args:
            user_id (_type_): _description_

        Returns:
            Optional[User]: _description_
        """
        try:
            return self.user_model.objects.get(user_id=user_id)
        except self.user_model.DoesNotExist:
            self.logger.exception("An exception occured in get_user:")
        except self.user_model.MultipleObjectsReturned:
            self.logger.exception("More than two objects get_user")
    def update_user(self,user_id, user_data:UserData):
        """_summary_

        Args:
            user_id (_type_): _description_
            user_data (UserData): _description_
        """
        user=self.get_user(user_id=user_id)
        if(user):
            for key, value in user_data.items():
                setattr(user,key,value)
            user.save()
        else:
            log_error(logger=self.logger,entity="User",identifier=user_id)
    def delete_user(self, user_id):
        """_summary_

        Args:
            user_id (_type_): _description_
        """
        user=self.get_user(user_id=user_id)
        if user:
            user.delete()
        log_error(logger=self.logger,entity="User",identifier=user_id)
    def get_all_users(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.user_model.objects.all()
    

    