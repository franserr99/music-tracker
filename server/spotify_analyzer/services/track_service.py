from injector import singleton, inject
from models import Track
from service_dtos import TrackData
import logging
@singleton
class TrackService:
    @inject
    def __init__(self, track_model: Track,logger: logging.Logger ):
        self.track_model = track_model
        self.logger=logger
    def create_track(self, track_data:TrackData):
        self.track_model.objects.create(**track_data)
    #identifiable by uri so only use it
    def get_track(self, track_uri:str):
        try:
            print(self.track_model.objects.get(track_uri=track_uri))
            track=self.track_model.objects.get(track_uri=track_uri)
            if(track):
                return track
            else:
                self.logger.error("")
        except Exception as e:
            self.logger.exception("An exception occured in get_track:")
    def update_track(self, track_uri:str, track_data:TrackData):
        track=self.get_track(self,track_uri=track_uri)
        if(track):
            for key, value in track_data.items():
                setattr(track, key, value)
            track.save()
        else:
            self.logger.warning("Track does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Track with uri: %s",track_uri," was attempted to be pulled from the db but does not exist")
            
    def delete_track(self,track_uri:str):
        track=self.get_track(self,track_uri=track_uri)
        if(track):
            track.delete()
        else:
            self.logger.warning("Track does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Track with uri: %s",track_uri," was attempted to be pulled from the db but does not exist")
    def get_all_tracks(self):
        return self.track_model.objects.all()