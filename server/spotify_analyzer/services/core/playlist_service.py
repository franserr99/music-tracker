"""
    _summary_

    Returns:
        _type_: _description_
"""

from typing import Optional
import logging

from django.db import DatabaseError, OperationalError

# from injector import inject

from ...models import Playlist
from .user_service import UserService
from ...dtos.retrieval_dtos import PlaylistData
from .track_service import TrackService


class PlaylistService:
    """_summary_

    Returns:
        _type_: _description_
    """
    # @inject

    def __init__(self, playlist_model: Playlist, track_service: TrackService,
                 user_service: UserService, logger: logging.Logger):
        self.playlist_model = playlist_model
        self.track_service = track_service
        self.user_service = user_service
        self.logger = logger

    def create_playlist(self, playlist_data: PlaylistData):
        payload = playlist_data.copy()
        user_id = playlist_data['created_by']
        user = self.user_service.get_user(user_id=user_id)
        try:
            if user:
                payload['created_by'] = user
                playlist, created = self.playlist_model.objects.get_or_create(
                    **payload)
                return playlist
        except Exception:
            self.logger.info("Error when trying to create the playlist")
    # def bulk_create_playlists(self, playlist_dtos: List[PlaylistData]):
    #     playlist_data = []

    #     for dto in playlist_dtos:
    #         payload = dto.copy()
    #         user_id = dto['user_id']
    #         user = self.user_service.get_user(user_id=user_id)
    #         if (user):
    #             payload['user_id']:
    #     playlist_instances = [Playlist(**)]

    def get_playlist(self, playlist_id) -> Optional[Playlist]:
        try:
            return self.playlist_model.objects.get(id=playlist_id)
        except self.playlist_model.DoesNotExist:
            self.logger.info("An exception occured in get_playlist:")
            return

    def get_all_playlists(self):
        try:
            return self.playlist_model.objects.all()
        except (OperationalError, DatabaseError):
            self.logger.info("trouble getting all playlists")

    def get_all_identifiers(self):
        try:
            return list(self.playlist_model.objects.values_list('id',
                                                                flat=True))
        except (OperationalError, DatabaseError):
            self.logger.info("error when getting all idszF")

    def update_playlist(self, id: str, new_data: PlaylistData):
        playlist = self.get_playlist(playlist_id=id)
        # playlist_id = old_data['playlist_id']
        if (playlist):
            for key, value in new_data.items():
                setattr(playlist, key, value)
            playlist.save()

    def delete_playlist(self, id: str):
        playlist = self.get_playlist(playlist_id=id)
        # playlist_id = playlist['playlist_id']
        if (playlist):
            playlist.delete()
    # need to double check this, i think i need to filter?
    # not sure if it is build in

    def get_user_playlists(self, user_id: str):
        user = self.user_service.get_user(user_id=user_id)
        if (user):
            return self.playlist_model.objects.filter(created_by=user)

    def add_track_to_playlist(self, playlist_id, track_uri) -> bool:
        playlist = self.get_playlist(playlist_id=playlist_id)
        if playlist:
            track = self.track_service.get_track(track_uri=track_uri)
            if (track):
                playlist.tracks.add(track)
                playlist.save()
            else:
                self.logger.info("tried getting track when adding to playlist \
                                 but DNE in db yet. Check for race conditions.\
                                 Caller needs to check if track exsits, \
                                 then add it, not this function's job")
                return False
        else:
            self.logger.info("tried getting playlist when adding track to it \
                                 but DNE in db yet. Check for race conditions.\
                                 Caller needs to check if playlist exsits, \
                                 then add it, not this function's job")
            return False

    def like_playlist(self, playlist_id, user_id):
        user = self.user_service.get_user(user_id)
        if user:
            playlist = self.get_playlist(playlist_id)
            if playlist:
                playlist.liked_by.add(user)
