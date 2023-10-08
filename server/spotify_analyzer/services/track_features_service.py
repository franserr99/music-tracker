from injector import singleton, inject
from models import TrackFeatures
from service_dtos import TrackFeaturesData
from services import track_service as TrackService
import logging

class TrackFeaturesService:
    @inject
    def __init__(self, track_features_model: TrackFeatures,track_service: TrackService,logger: logging.Logger ):
        self.track_features_model = track_features_model
        self.track_service = track_service
        self.logger=logger
    def create_track_features(self, track_features_data:TrackFeaturesData):
        track_instance = self.track_service.get_track(track_features_data['track_uri'])
        if track_instance:
            data_copy=track_features_data.copy()
            data_copy['track_uri']=track_instance
            self.track_features_model.objects.create(**data_copy)
        else:
            self.logger.warning("Track does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("Track with uri: %s",track_features_data['track_uri']," was attempted to be pulled from the db but does not exist")
    #identifiable by uri so only use it
    def get_track_features(self, track_uri:str):
        try:
            track_instance = self.track_service.get_track(track_uri=track_uri)
            #print(self.track_features_model.objects.get(track_uri=track_uri))
            if(track_instance):
                return self.track_features_model.objects.get(track=track_instance)
            else:
                self.logger.warning("Track does not exist. Check for race conditions or validate your input sources.")
                self.logger.warning("Track with uri: %s",track_uri," was attempted to be pulled from the db but does not exist")
        except Exception:
            self.logger.exception("An exception occured in get_track_features:")
    def update_track_features(self, track_uri:str, track_features_data:TrackFeaturesData):
        
        track_feature=self.get_track_features(track_uri=track_uri)
        if(track_feature):
            for key, value in track_features_data.items():
                setattr(track_feature, key, value)
            track_feature.save()
        else:
            self.logger.warning("TrackFeatures record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("TrackFeatures for track with uri: %s",track_uri," was attempted to be pulled from the db but does not exist")
    def delete_track_features(self, track_uri:str):
        track_feature=self.get_track_features(track_uri=track_uri)
        if(track_feature):    
            track_feature.delete()
        else:
            self.logger.warning("TrackFeatures record does not exist. Check for race conditions or validate your input sources.")
            self.logger.warning("TrackFeatures for track with uri: %s",track_uri," was attempted to be pulled from the db but does not exist")
    def get_all_tracks_features(self):
        return self.track_features_model.objects.all()