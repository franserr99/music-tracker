"""
track_service.py
================

This module contains the TrackService class, which provides
high-level operations for managing tracks in the application.
The class includes methods for creating, retrieving, updating,
 and deleting tracks using the Track model as its data interface.

Classes:
    - TrackService: Manages CRUD operations for tracks.

Usage:
    from track_service import TrackService

    track_service = TrackService(TrackModel, Logger)
    track_service.create_track(track_data)
    track_service.get_track(track_uri)
    track_service.update_track(track_uri, new_data)
    track_service.delete_track(track_uri)
    track_service.get_all_tracks()
"""
from .service_dtos import TrackData
from ..models import Track
from typing import Optional
import logging

from injector import inject
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError, OperationalError


# @singleton


class TrackService:
    """Provides services for managing tracks in the database.

    This class is responsible for creating, retrieving,
    updating, and deleting tracks.
    It interacts with the Track model to perform CRUD operations.
    """
    @inject
    def __init__(self, track_model: Track, logger: logging.Logger):
        """Initializes the TrackService with a track model and logger.

        Args:
            track_model (Track): The Track model class to operate on.
            logger (logging.Logger): Logger instance to 
                log information and errors.
        """
        self.track_model = track_model
        self.logger = logger

    def create_track(self, track_data: TrackData):
        """Creates a new track in the database.

        Args:
            track_data (TrackData): Data required to create a new track.

        Returns:
            Optional[Track]: The newly created Track object if 
                successful, None otherwise.
        """

        try:
            return self.track_model.objects.create(**track_data)
        except (IntegrityError, ValidationError,
                DatabaseError, TypeError, ValueError) as e:
            # logger will display more info about the error
            # calling code will know something went wrong, but not the context
            self.logger.exception(
                f"An error occurred while creating a track: {e}")
            return None
    # identifiable by uri so only use it

    def get_track(self, track_uri: str) -> Optional[Track]:
        """Fetches a track by its URI.

        Args:
            track_uri (str): The URI of the track to fetch.

        Returns:
            Optional[Track]: The Track object if found, None otherwise.
        """
        try:
            # print(self.track_model.objects.get(track_uri=track_uri))
            return self.track_model.objects.get(track_uri=track_uri)
        except self.track_model.DoesNotExist:
            self.logger.exception("An exception occured in get_track:")
            return None

    def update_track(self, track_uri: str, track_data: TrackData):
        """Updates an existing track.

        Args:
            track_uri (str): The URI of the track to update.
            track_data (TrackData): New data to update the track.

        Returns:
            Optional[bool]: True if the update is successful, None otherwise.
        """
        track = self.get_track(track_uri=track_uri)
        if track:
            for key, value in track_data.items():
                setattr(track, key, value)

            try:
                track.save()
            except (IntegrityError, ValidationError,
                    OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while updating a track: {e}")
                return None
        
    def delete_track(self, track_uri: str):
        """Deletes a track by its URI.

        Args:
            track_uri (str): The URI of the track to delete.

        Returns:
            Optional[bool]: True if the deletion is successful, None otherwise.
        """
        track = self.get_track(track_uri=track_uri)
        if track:
            try:
                track.delete()
            except (IntegrityError, OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while deleting a track: {e}")
                return None
            
    def get_all_tracks(self):
        """Fetches all tracks in the database.

        Returns:
            QuerySet: A QuerySet containing all track
                features or None if an error occurs.
        """
        try:
            return self.track_model.objects.all()
        except (OperationalError, DatabaseError) as e:
            self.logger.exception(
                f"An error occurred while fetching all tracks: {e}")
            return None
