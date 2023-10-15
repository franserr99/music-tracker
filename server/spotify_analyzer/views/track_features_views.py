"""
This module provides a Django REST Framework view for managing and retrieving track features.

Raises:
    Http404: Raised if a track feature resource cannot be found.
  
Returns:
    JsonResponse: Returns a JSON representation of track features or an error message.
"""
from django.http import Http404
from injector import inject
from rest_framework.generics import RetrieveAPIView

from ..serializers import TrackFeaturesSerializer
from ..services.track_features_service import TrackFeaturesService

@inject
def create_track_features_view(track_features_service: TrackFeaturesService):
    """
    Function to create and configure an instance of TrackFeaturesView.
    
    Args:
        track_features_service (TrackFeaturesService): Service for handling track features.
        
    Returns:
        TrackFeaturesView: Configured instance of the view.
    """
    return TrackFeaturesView.as_view(track_features_service=track_features_service)


class TrackFeaturesView(RetrieveAPIView):
    """
    A class-based view for retrieving track features.
    """
    serializer_class = TrackFeaturesSerializer  # specify the serializer class here
    
    def __init__(self, track_features_service: TrackFeaturesService, *args, **kwargs):
        """
        Initialize the view with the injected track features service.
        
        Args:
            track_features_service (TrackFeaturesService): Service for handling track features.
        """
        self.track_features_service = track_features_service
        super().__init__(*args, **kwargs)

    def get_object(self):
        """
        Retrieve the track features object.
        
        Raises:
            Http404: If the track features do not exist.
            
        Returns:
            dict: Serialized track features.
        """
        track_uri = self.kwargs.get('track_uri')
        track_features = self.track_features_service.get_track_features(track_uri=track_uri)
        if not track_features:
            raise Http404("Track's Features do not exist")
        return track_features