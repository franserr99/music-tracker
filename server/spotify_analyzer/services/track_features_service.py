"""_summary_

    Returns:
        _type_: _description_
"""
import logging

from injector import inject

from ..models import TrackFeatures
from .service_dtos import TrackFeaturesData
from .track_service import TrackService
from ..util import log_error


class TrackFeaturesService:
    """_summary_

    Returns:
        _type_: _description_
    """
    @inject
    def __init__(self, track_features_model: TrackFeatures,
                 track_service: TrackService, logger: logging.Logger):
        self.track_features_model = track_features_model
        self.track_service = track_service
        self.logger = logger

    def create_track_features(self, track_features_data: TrackFeaturesData):
        """_summary_

        Args:
            track_features_data (TrackFeaturesData): _description_
        """
        track_uri = track_features_data['track_uri']
        track_instance = self.track_service.get_track(track_uri=track_uri)

        if track_instance:
            data_copy = track_features_data.copy()
            data_copy['track_uri'] = track_instance
            self.track_features_model.objects.create(**data_copy)
        else:
            log_error(logger=self.logger, entity="Track", identifier=track_uri)
    # identifiable by uri so only use it

    def get_track_features(self, track_uri: str):
        """_summary_

        Args:
            track_uri (str): _description_

        Returns:
            _type_: _description_
        """
        try:
            track_instance = self.track_service.get_track(track_uri=track_uri)
            # print(self.track_features_model.objects.get(track_uri=track_uri))
            if track_instance:
                return self.track_features_model.objects.get(track=track_instance)
            log_error(logger=self.logger, entity="Track", identifier=track_uri)
            return None

        except self.track_features_model.DoesNotExist:
            self.logger.exception(
                "An exception occured in get_track_features:")
        except self.track_features_model.MultipleObjectsReturned:
            self.logger.exception("More than two objects returned")

    def update_track_features(self, track_uri: str, track_features_data: TrackFeaturesData):
        """_summary_

        Args:
            track_uri (str): _description_
            track_features_data (TrackFeaturesData): _description_
        """
        track_feature = self.get_track_features(track_uri=track_uri)
        if track_feature:
            for key, value in track_features_data.items():
                setattr(track_feature, key, value)
            track_feature.save()
        else:
            log_error(logger=self.logger, entity="TrackFeatures",
                      identifier=track_uri)

    def delete_track_features(self, track_uri: str):
        """_summary_

        Args:
            track_uri (str): _description_
        """
        track_feature = self.get_track_features(track_uri=track_uri)
        if track_feature:
            track_feature.delete()
        else:
            log_error(logger=self.logger, entity="TrackFeatures",
                      identifier=track_uri)

    def get_all_tracks_features(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.track_features_model.objects.all()
