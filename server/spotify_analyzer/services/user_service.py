""" UserService Module

This module contains the UserService class that provides CRUD operations
for managing User entities. The class relies on dependency injection to 
receive a user model and a logging instance for operation and debugging.

Classes:
    UserService: Manages CRUD operations for User entities.

Exceptions:
    User.DoesNotExist: Raised when a requested user does not exist.
    User.MultipleObjectsReturned: Raised when more than one user exists for a given ID.

Attributes:
    None

Example:
    from UserService import UserService

    user_service = UserService(user_model, logger)
    user_service.create_user({"name": "John", "email": "john@example.com"})
    user = user_service.get_user(user_id=1)
    user_service.update_user(user_id=1, {"name": "John Smith"})
    user_service.delete_user(user_id=1)

    I am going to wire the service to the view CBV through injecting it via a wrapper function 
Note:
    Make sure to handle the exceptions raised by the service methods in the client code.

"""
from typing import List, Optional
import logging

from injector import inject,singleton
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError, OperationalError

from ..models import User
from .service_dtos import UserData
from ..util import log_error, log_error_dependency


@singleton
class UserService:
    """Service class to manage CRUD operations for User entities.
    
    Attributes:
        user_model: A model class representing a user.
        logger: A logging.Logger instance for logging information.
    """
    @inject
    def __init__(self, user_model: User,logger: logging.Logger):
        """Initializes UserService with the given user model and logger."""
        self.user_model = user_model
        self.logger=logger
    def create_user(self, user_data:dict)->User:
        """Creates a new user.

        Args:
            user_data (dict): Dictionary containing data to create a new user
        Returns:
            Optional[User]: The User object if created successfully, None otherwise.
        """
        try:
            return self.user_model.objects.create(**user_data)
        except (IntegrityError,ValidationError,
                DatabaseError,TypeError,ValueError) as e:
            #logger will display more info about the error
            #calling code will know something went wrong, but not the context
            self.logger.exception(f"An error occurred while creating a user: {e}")
            return None
    def get_user(self, user_id)->Optional[User]:
        """Fetches a user by their ID.

        Args:
            user_id: The ID of the user to fetch.

        Returns:
            Optional[User]: The User object if found, None otherwise.
        """
        try:
            return self.user_model.objects.get(user_id=user_id)
        except self.user_model.DoesNotExist:
            self.logger.exception("An exception occured in get_user:")
            log_error(logger=self.logger,entity="User",identifier=user_id)
            return None
    def update_user(self,user_id, user_data:UserData):
        """Updates an existing user.

        Args:
            user_id: The ID of the user to update.
            user_data (dict): Dictionary containing new data for the user.
        """
        user=self.get_user(user_id=user_id)
        if user:
            for key, value in user_data.items():
                setattr(user,key,value)
            try:
                user.save()
            except (IntegrityError,ValidationError,
                    OperationalError,DatabaseError) as e:
                self.logger.exception(f"An error occurred while updating a user: {e}")
                return None
        else:
            log_error_dependency(logger=self.logger,caller="update_user()",entity="User")
    def delete_user(self, user_id):
        """Deletes a user.

        Args:
            user_id: The ID of the user to delete.
        """
        user=self.get_user(user_id=user_id)
        if user:
            try:
                return user.delete()
            except (IntegrityError,OperationalError,DatabaseError) as e:
                self.logger.exception(f"An error occurred while deleting a user: {e}")
                return None
        log_error_dependency(logger=self.logger,caller="delete_user()",entity="User")
    def get_all_users(self)-> Optional[List[User]]:
        """Fetches all users.   
        Returns:
        Returns:
            QuerySet: A QuerySet containing all track features or None if an error occurs.
        """
        try:
            return self.user_model.objects.all()
        except (OperationalError, DatabaseError) as e:
            self.logger.exception(f"An error occurred while fetching all users: {e}")
            return None
        