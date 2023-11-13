import logging
from typing import Optional
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DatabaseError, OperationalError
from ...dtos.retrieval_dtos import GenreData
from ...models import Genre


class GenreService:
    # @inject
    def __init__(self, genre_model: Genre, logger: logging.Logger):
        self.genre_model = genre_model
        self.logger = logger

    def create_genre(self, genre_data: GenreData):

        try:
            genre, created = self.genre_model.objects.get_or_create(
                **genre_data)
            return genre
        except (IntegrityError, ValidationError,
                DatabaseError, TypeError, ValueError) as e:
            self.logger.exception(
                f"An error occurred while creating an genre: {e}")
            return None

    def get_genre(self, name: str) -> Optional[Genre]:

        try:
            # print(self.genre_model.objects.get(name=name))
            return self.genre_model.objects.get(name=name)
        except self.genre_model.DoesNotExist:
            self.logger.exception("An exception occured in get_genre:")
            return None

    def update_genre(self, name: str, genre_data: GenreData):

        genre = self.get_genre(name=name)
        if genre:
            for key, value in genre_data.items():
                setattr(genre, key, value)

            try:
                genre.save()
            except (IntegrityError, ValidationError,
                    OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while updating a genre: {e}")
                return None

    def delete_genre(self, name: str):
        genre = self.get_genre(name=name)
        if genre:
            try:
                genre.delete()
            except (IntegrityError, OperationalError, DatabaseError) as e:
                self.logger.exception(
                    f"An error occurred while deleting a genre: {e}")
                return None

    def get_all_genres(self):
        try:
            return self.genre_model.objects.all()
        except (OperationalError, DatabaseError) as e:
            self.logger.exception(
                f"An error occurred while fetching all genres: {e}")
            return None
