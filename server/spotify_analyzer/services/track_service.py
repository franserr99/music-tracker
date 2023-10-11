"""_summary_

    Returns:
        _type_: _description_
"""
from typing import Optional
import logging

from injector import singleton, inject

from..util import log_error
from ..models import Track
from .service_dtos import TrackData



@singleton
class TrackService:
    """_summary_

    Returns:
        _type_: _description_
    """
    @inject
    def __init__(self, track_model: Track, logger: logging.Logger):
        self.track_model = track_model
        self.logger = logger

    def create_track(self, track_data: TrackData):
        """_summary_

        Args:
            track_data (TrackData): _description_
        """
        self.track_model.objects.create(**track_data)
    # identifiable by uri so only use it

    def get_track(self, track_uri: str) -> Optional[Track]:
        """_summary_

        Args:
            track_uri (str): _description_

        Returns:
            Optional[Track]: _description_
        """
        try:
            print(self.track_model.objects.get(track_uri=track_uri))
            track = self.track_model.objects.get(track_uri=track_uri)
            if track:
                return track
            self.logger.error("")
        except self.track_model.DoesNotExist:
            self.logger.exception("An exception occured in get_track:")
        except self.track_model.MultipleObjectsReturned:
            self.logger.exception("More than two objects returned")

    def update_track(self, track_uri: str, track_data: TrackData):
        """_summary_

        Args:
            track_uri (str): _description_
            track_data (TrackData): _description_
        """
        track = self.get_track(track_uri=track_uri)
        if track:
            for key, value in track_data.items():
                setattr(track, key, value)
            track.save()
        else:
            log_error(logger=self.logger, entity="Track", identifier=track_uri)

    def delete_track(self, track_uri: str):
        """_summary_

        Args:
            track_uri (str): _description_
        """
        track = self.get_track(track_uri=track_uri)
        if track:
            track.delete()
        else:
            log_error(logger=self.logger, entity="Track", identifier=track_uri)

    def get_all_tracks(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.track_model.objects.all()
