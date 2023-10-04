from injector import inject
from models import PlaylistTrack,PlaylistTrackData,PlaylistData,TrackData
from services import playlist_service as PlaylistService,track_service as TrackService
import logging
from typing import Optional

class PlaylistTrackService:
    @inject
    def __init__(self, playlist_track_model: PlaylistTrack, playlist_service:PlaylistService, track_service: TrackService,logger: logging.Logger):
        self.playlist_track_model = playlist_track_model
        self.playlist_service=playlist_service
        self.track_service=track_service
        self.logger=logger
    
    def create_playlist_track(self, data:PlaylistTrackData, user_id:str, track_data:Optional[TrackData]=None):
        payload=PlaylistData(playlist_id=data['playlist_id'], user_id=user_id)
        playlist=self.playlist_service.get_playlist(playlist_data=payload)
        track=self.track_service.get_track(track_uri=data['track_uri'])
        if(playlist is None):
            self.playlist_service.create_playlist(**payload)
        if(track is None):
            #throw error if they did not pass in data properly
            self.logger.warning("")
            assert(track_data)
            self.track_service.create_track(track_data=track_data)
        self.playlist_track_model.objects.create(**data)

    def get_playlist_track(self,data:PlaylistTrackData, user_id:str ):
        payload=PlaylistData(playlist_id=data['playlist_id'], user_id=user_id)
        playlist=self.playlist_service.get_playlist(playlist_data=payload)
        track=self.track_service.get_track(track_uri=data['track_uri'])

        payload={'playlist_id':playlist,'track_uri':track}
        try:
            if(playlist and track):
                return self.playlist_track_model.objects.get(**payload)
            elif(playlist is not None and track is not None):
                self.logger.info("Trying to add a track to a playlist. Both the playlist record and the track record dont exist in the db.")
                self.logger.warning("Check for race conditions or validate your input sources.")
            elif(playlist is not None):
                self.logger.info("Trying to add a track to a playlist. Playlist record doesnt exist in the db.")
                self.logger.warning("Check for race conditions or validate your input sources.")
            else:#track is not None
                self.logger.info("Trying to add a track to a playlist. Track record does not exist in the db.")
                self.logger.warning("Check for race conditions or validate your input sources.")
        except Exception:
            self.logger.exception("An exception occured in get_playlist_track:")
    def update_playlist_track(self,old_data:PlaylistTrackData,new_data:PlaylistTrackData, user_id:str):
        playlist_track=self.get_playlist_track(data=old_data,user_id=user_id)
        if(playlist_track):
            for key,value in new_data.items():
                setattr(playlist_track,key,value)
            playlist_track.save()

    def delete_playlist_track(self,data:PlaylistTrackData,user_id:str):
        playlist_track=self.get_playlist_track(data=data,user_id=user_id)
        if(playlist_track):
            playlist_track.delete()
    def get_all_playlist_tracks(self, playlist:PlaylistData):
        playlist=self.playlist_service.get_playlist(playlist_data=playlist)
        user=self.playlist_service.user_service.get_user(playlist['user_id'])
        return self.playlist_track_model.objects.filter(playlist_id__user_id=playlist['user_id'])