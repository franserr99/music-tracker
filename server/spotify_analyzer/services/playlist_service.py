from injector import inject,singleton
from models import Playlist
from service_dtos import PlaylistData
import logging
from services import track_service as TrackService

@singleton
class PlaylistService:
    @inject
    def __init__(self, playlist_model: Playlist, track_service: TrackService,user_service:UserService,logger: logging.Logger):
        self.playlist_model = playlist_model
        self.track_service=track_service
        self.user_service=user_service
        self.logger=logger
    def create_playlist(self, playlist_data:PlaylistData):
        payload=playlist_data.copy()
        user_id=playlist_data['user_id']
        user=self.user_service.get_user(user_id=user_id)
        if(user):
            payload['user_id']=user
            self.playlist_model.objects.create(**payload)
        else:
            self.logger.warning("User record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("User: id: %s",user_id," was attempted to be pulled from the db but does not exist")
    def get_playlist(self,playlist_data:PlaylistData):
        payload=playlist_data.copy()
        user_id=playlist_data['user_id']
        user=self.user_service.get_user(user_id=user_id)
        try:
            if(user):
                payload['user_id']=user
                self.playlist_model.objects.get(**payload)
            else:
                self.logger.warning("User record does not exist. Check for race conditions or validate your input sources.")
                self.logger.warning("User: id: %s",user_id," was attempted to be pulled from the db but does not exist")
        except Exception:
            self.logger.exception("An exception occured in get_playlist:")
    def update_playlist(self, old_data:PlaylistData, new_data:PlaylistData):
        playlist=self.get_playlist(self,playlist_data=old_data)
        if(playlist):
            for key,value in new_data.items():
                setattr(playlist,key,value)
            playlist.save()
        else:
            self.logger.warning("Playlist record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Playlist with playlist_id: %s",old_data['playlist_id']," was attempted to be pulled from the db but does not exist")
    def delete_playlist(self,playlist_data:PlaylistData):
        playlist=self.get_playlist(self,playlist_data=playlist_data)
        if(playlist):
            playlist.delete()
        else:
            self.logger.warning("Playlist record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Playlist with playlist_id: %s",playlist['playlist_id']," was attempted to be pulled from the db but does not exist")
    def get_all_users_playlists(self, user_id:str):
        user=self.user_service.get_user(user_id=user_id)
        if(user):
            return self.playlist_model.objects.get(user=user)
        else:
            self.logger.warning("User record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("User: id: %s",user_id," was attempted to be pulled from the db but does not exist")