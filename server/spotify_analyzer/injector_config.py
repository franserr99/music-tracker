"""_summary_

Returns:
    _type_: _description_
"""
import logging

from injector import Module, provider, singleton
from django.apps import apps
from .services.core.track_service import TrackService
from .services.core.user_service import UserService
from .models import Track, User, History, Playlist, TrackFeatures


class Config(Module):
    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        logger = logging.getLogger('spotify_analyzer')
        logger.setLevel(logging.INFO)
        return logger

    @provider
    def provide_track_model(self) -> 'Track':
        Track = apps.get_model('spotify_analyzer', 'Track')
        return Track()

    @provider
    def provide_track_features_model(self) -> 'TrackFeatures':
        TrackFeatures = apps.get_model('spotify_analyzer', 'TrackFeatures')
        return TrackFeatures()

    @provider
    def provide_user_model(self) -> 'User':
        User = apps.get_model('spotify_analyzer', 'User')
        return User()

    @provider
    def provide_playlist_model(self) -> 'Playlist':
        Playlist = apps.get_model('spotify_analyzer', 'Playlist')
        return Playlist()

    @provider
    def provide_history_model(self) -> 'History':
        History = apps.get_model('spotify_analyzer', 'History')
        return History()

    @provider
    def provide_track_service(self, logger: logging.Logger) -> 'TrackService':
        Track = self.provide_track_model()
        return TrackService(track_model=Track, logger=logger)

    @provider
    def provide_user_service(self, logger: logging.Logger) -> 'UserService':
        User = self.provide_user_model()
        return UserService(user_model=User, logger=logger)
