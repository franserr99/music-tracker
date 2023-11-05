from typing import List, Optional
import logging

from injector import inject  # , singleton
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError, OperationalError

from ..models import User
from .service_dtos import UserData


# @singleton
class UserService:
    """Service class to manage CRUD operations for User entities.

    Attributes:
        user_model: A model class representing a user.
        logger: A logging.Logger instance for logging information.
    """
    @inject
    def __init__(self, user_model: User, logger: logging.Logger):
        """Initializes UserService with the given user model and logger."""
        self.user_model = user_model
        self.logger = logger

    def create_user(self, user_data: dict) -> User:
        """Creates a new user.

        Args:
            user_data (dict): Dictionary containing data to create a new user
        Returns:
            Optional[User]: 
                The User object if created successfully None otherwise
        """
        
        user = self.get_user(user_id=user_data['id'])
        if user is None:
            try:
                return self.user_model.objects.create(**user_data)
            except (IntegrityError, ValidationError,
                    DatabaseError, TypeError, ValueError) as e:
                # logger will display more info about the error
                # calling code will know something went wrong,
                #  but not the context
                self.logger.exception(
                    f"An error occurred while creating a user: {e}")
                return None
        else:
            return user

    def get_user(self, user_id) -> Optional[User]:
        """Fetches a user by their ID.

        Args:
            user_id: The ID of the user to fetch.

        Returns:
            Optional[User]: The User object if found, None otherwise.
        """
        try:
            return self.user_model.objects.get(id=user_id)
        except self.user_model.DoesNotExist:
            self.logger.info("User does not exist")
            # log_error(logger=self.logger, entity="User", identifier=user_id)
            return None

    def update_user(self, user_id, user_data: UserData):
        """Updates an existing user.

        Args:
            user_id: The ID of the user to update.
            user_data (dict): Dictionary containing new data for the user.
        """
        user = self.get_user(user_id=user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            try:
                user.save()
            except (IntegrityError, ValidationError,
                    OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while updating a user: {e}")
                return None
        
    def add_token(self, user_id, token, access=True):
        print(token)
        user = self.get_user(user_id=user_id)
        if user is not None:
            if access:
                user.access_token = token
            else:
                user.refresh_token = token
            try:
                print("saving the token now")
                user.save()
            except (IntegrityError, ValidationError,
                    OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while adding token info to a user: {e}"
                    )
                
    def add_token_metadata(self, user_id, expires_at):
        user = self.get_user(user_id=user_id)
        if user is not None:
            user.expires_at = int(expires_at)
            try:
                print("saving the token metadata now")
                user.save()
            except (IntegrityError, ValidationError,
                    OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while adding token metadata: {e}"
                    )

    def delete_user(self, user_id):
        """Deletes a user.

        Args:
            user_id: The ID of the user to delete.
        """
        user = self.get_user(user_id=user_id)
        if user:
            try:
                return user.delete()
            except (IntegrityError, OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while deleting a user: {e}")
                return None

    def get_all_users(self) -> Optional[List[User]]:
        """Fetches all users.   
        Returns:
        Returns:
            QuerySet:
            A QuerySet containing all track features or None if error occurs.
        """
        try:
            return self.user_model.objects.all()
        except (OperationalError, DatabaseError) as e:
            self.logger.exception(
                f"An error occurred while fetching all users: {e}")
            return None
