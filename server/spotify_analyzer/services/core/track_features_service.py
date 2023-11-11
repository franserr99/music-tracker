"""_summary_

    Returns:
        _type_: _description_
"""
import logging

from injector import inject
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError, OperationalError

from ...models import TrackFeatures
from ..dtos.retrieval_dtos import TrackFeaturesData
from .track_service import TrackService


class TrackFeaturesService:
    """Service class for managing track features.

    Attributes:
        features_model (TrackFeatures): 
            The Django model representing track features.
        track_service (TrackService): 
            Service class for managing tracks.
        logger (logging.Logger): 
            The logger instance.
    """
    @inject
    def __init__(self, features_model: TrackFeatures,
                 track_service: TrackService, logger: logging.Logger):
        self.features_model = features_model
        self.track_service = track_service
        self.logger = logger

    def create_track_features(self, track_features_data: TrackFeaturesData):
        """Create a new track feature entry.

        Args:
            track_features_data (TrackFeaturesData): 
                The data for the track features.
        """
        track_uri = track_features_data['track_uri']
        track_instance = self.track_service.get_track(uri=track_uri)

        if track_instance:
            data_copy = track_features_data.copy()
            data_copy['track_uri'] = track_instance
            try:

                features, created = self.features_model.objects.get_or_create(
                                        **data_copy)
                return features
            except (IntegrityError, ValidationError,
                    DatabaseError, TypeError, ValueError) as e:
                self.logger.exception(
                    f"error occurred while creating a track's features: {e}")
                return None
    # identifiable by uri so only use it

    def get_track_features(self, track_uri: str):
        """Retrieve the features of a track by URI.

        Args:
            track_uri (str): The URI of the track.

        Returns:
            TrackFeatures: The features of the track or None if not found.
        """
        track_instance = self.track_service.get_track(track_uri=track_uri)
        # print(self.features_model.objects.get(track_uri=track_uri))
        if track_instance:
            try:
                return self.features_model.objects.get(
                    track=track_instance)
            except self.features_model.DoesNotExist:
                self.logger.exception(
                    "An exception occured in get_track_features:")
                return None

    def update_track_features(self, track_uri: str,
                              track_features_data: TrackFeaturesData):
        """Update the features of a track.

        Args:
            track_uri (str): 
                The URI of the track.
            track_features_data (TrackFeaturesData): 
                The new data for the track features.
        """
        track_feature = self.get_track_features(track_uri=track_uri)
        if track_feature:
            for key, value in track_features_data.items():
                setattr(track_feature, key, value)
            try:
                track_feature.save()
            except (IntegrityError, ValidationError,
                    OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while updating a track's feature: {e}")
                return None

    def delete_track_features(self, track_uri: str):
        """Delete the features of a track.

        Args:
            track_uri (str): The URI of the track.
        """
        track_feature = self.get_track_features(track_uri=track_uri)
        if track_feature:
            try:
                track_feature.delete()
            except (IntegrityError, OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"error occurred while deleting a track's features: {e}")
                return None

    def get_all_tracks_features(self):
        """Retrieve all track features.

        Returns:
            QuerySet: 
                contains all track features or None if an error occurs.
        """
        try:
            return self.features_model.objects.all()
        except (OperationalError, DatabaseError) as e:
            self.logger.exception(
                f"An error occurred while fetching all track's features: {e}")
            return None
