import logging
from typing import Optional
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError, OperationalError
from ..service_dtos import ImageData
from ...models import Image
from ..core.album_service import AlbumService
from ..core.artist_service import ArtistService


class ImageService:
    # @inject
    def __init__(self, image_model: Image, logger: logging.Logger,
                 album_service: AlbumService, artist_service: ArtistService):
        self.image_model = image_model
        self.logger = logger
        self.artist_service = artist_service
        self.album_service = album_service

    def create_image(self, image_data: ImageData):

        try:
            return self.image_model.objects.create(**image_data)
        except (IntegrityError, ValidationError,
                DatabaseError, TypeError, ValueError) as e:
            self.logger.exception(
                f"An error occurred while creating an image: {e}")
            return None

    def get_image(self, url: str) -> Optional[Image]:

        try:
            # print(self.image_model.objects.get(url=url))
            return self.image_model.objects.get(url=url)
        except self.image_model.DoesNotExist:
            self.logger.exception("An exception occured in get_image:")
            return None

    def update_image(self, url: str, image_data: ImageData):

        artist = self.get_image(url=url)
        if artist:
            for key, value in image_data.items():
                setattr(artist, key, value)

            try:
                artist.save()
            except (IntegrityError, ValidationError,
                    OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while updating a artist: {e}")
                return None

    def delete_image(self, url: str):
        artist = self.get_image(url=url)
        if artist:
            try:
                artist.delete()
            except (IntegrityError, OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while deleting a artist: {e}")
                return None

    def get_all_images(self):
        try:
            return self.image_model.objects.all()
        except (OperationalError, DatabaseError) as e:
            self.logger.exception(
                f"An error occurred while fetching all artists: {e}")
            return None

    def link_image_to_artist(self, artist_uri: str, url: str):
        image = self.get_image(url)
        if (image):
            artist = self.artist_service.get_artist()
            image.artist
