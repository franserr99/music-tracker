from typing import Optional
from injector import inject,singleton
from models import User
from service_dtos import UserData
import logging

@singleton
class UserService:
    @inject
    def __init__(self, user_model: User,logger: logging.Logger):
        self.user_model = user_model
        self.logger=logger
    def create_user(self, user_data:UserData):
        self.user_model.objects.create(**user_data)
    def get_user(self, user_id)->Optional[User]:
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
    

    