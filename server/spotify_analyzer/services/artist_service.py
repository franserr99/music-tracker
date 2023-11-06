import logging
from typing import Optional
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError, OperationalError
from .service_dtos import ArtistData
from ..models import Artist

app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


class ArtistService:
    # @inject
    def __init__(self, artist_model: Artist, logger: logging.Logger):
        self.artist_model = artist_model
        self.logger = logger

    def create_artist(self, artist_data: ArtistData):

        try:
            return self.artist_model.objects.create(**artist_data)
        except (IntegrityError, ValidationError,
                DatabaseError, TypeError, ValueError) as e:
            self.logger.exception(
                f"An error occurred while creating an artist: {e}")
            return None

    def get_artist(self, uri: str) -> Optional[Artist]:

        try:
            # print(self.artist_model.objects.get(uri=uri))
            return self.artist_model.objects.get(uri=uri)
        except self.artist_model.DoesNotExist:
            self.logger.exception("An exception occured in get_artist:")
            return None

    def update_artist(self, uri: str, artist_data: ArtistData):

        artist = self.get_artist(uri=uri)
        if artist:
            for key, value in artist_data.items():
                setattr(artist, key, value)

            try:
                artist.save()
            except (IntegrityError, ValidationError,
                    OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while updating a artist: {e}")
                return None

    def delete_artist(self, uri: str):
        artist = self.get_artist(uri=uri)
        if artist:
            try:
                artist.delete()
            except (IntegrityError, OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while deleting a artist: {e}")
                return None

    def get_all_artists(self):
        try:
            return self.artist_model.objects.all()
        except (OperationalError, DatabaseError) as e:
            self.logger.exception(
                f"An error occurred while fetching all artists: {e}")
            return None
