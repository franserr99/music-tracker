import logging
from typing import Optional
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError, OperationalError
from ..dtos.retrieval_dtos import AlbumData
from .track_service import TrackService
from .artist_service import ArtistService
from ...models import Album


class AlbumService:
    """Provides services for managing tracks in the database.

    This class is responsible for creating, retrieving,
    updating, and deleting tracks.
    It interacts with the Track model to perform CRUD operations.
    """
    # @inject

    def __init__(self, album_model: Album, logger: logging.Logger,
                 track_service: TrackService, artist_service: ArtistService):
        """Initializes the AlbumService with a track model and logger.

        Args:
            album_model (Track): The Track model class to operate on.
            logger (logging.Logger): Logger instance to 
                log information and errors.
        """
        self.album_model = album_model
        self.logger = logger
        self.track_service = track_service
        self.artist_service = artist_service

    def create_album(self, album_data: AlbumData):

        try:
            album, created = self.album_model.objects.get_or_create(
                **album_data)
            return album
        except (IntegrityError, ValidationError,
                DatabaseError, TypeError, ValueError):
            self.logger.info(
                "An error occurred while creating an album:")
            return None

    def get_album(self, uri: str) -> Optional[Album]:

        try:
            # print(self.album_model.objects.get(uri=uri))
            return self.album_model.objects.get(uri=uri)
        except self.album_model.DoesNotExist:
            self.logger.info("An exception occured in get_album:")
            return None

    def update_album(self, uri: str, album_data: AlbumData):

        album = self.get_album(uri=uri)
        if album:
            for key, value in album_data.items():
                setattr(album, key, value)

            try:
                album.save()
            except (IntegrityError, ValidationError,
                    OperationalError, DatabaseError):
                self.logger.info(
                    "An error occurred while updating a album:")
                return None

    def delete_album(self, uri: str):

        album = self.get_album(uri=uri)
        if album:
            try:
                album.delete()
            except (IntegrityError, OperationalError, DatabaseError):
                self.logger.info(
                    "An error occurred while deleting an album:")
                return None

    def get_all_albums(self):

        try:
            return self.album_model.objects.all()
        except (OperationalError, DatabaseError):
            self.logger.info(
                "An error occurred while fetching all tracks:")
            return None

    def get_all_identifiers(self):
        try:
            return self.album_model.objects.values_list('uri', flat=True)
        except (OperationalError, DatabaseError):
            self.logger.info(
                "An error occurred while fetching all tracks:")
            return None

    def add_track_to_album(self, album_uri, track_uri) -> bool:
        album = self.get_album(uri=album_uri)

        if album:
            track = self.track_service.get_track(track_uri=track_uri)
            if (track):
                album.tracks.add(track)
                album.save()
            else:
                self.logger.info("tried getting track when adding to album \
                                 but DNE in db yet. Check for race conditions.\
                                 Caller needs to check if track exsits, \
                                 then add it, not this function's job")
                return False
        else:
            self.logger.info("tried getting album when adding to album \
                                 but DNE in db yet. Check for race conditions.\
                                 Caller needs to check if album exsits, \
                                 then add it, not this function's job")
            return False

    def add_artist_to_album(self, album_uri, artist_uri):
        artist = self.artist_service.get_artist(artist_uri)
        album = self.get_album(album_uri)
        if artist and album:
            album.artists.add(artist)
