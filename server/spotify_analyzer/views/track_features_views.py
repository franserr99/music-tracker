"""
This module provides a Django REST Framework view for managing and retrieving track features.

Raises:
    Http404: Raised if a track feature resource cannot be found.
  
Returns:
    JsonResponse: Returns a JSON representation of track features or an error message.
"""

from injector import inject
from rest_framework.generics import RetrieveAPIView

from ..serializers import TrackFeaturesSerializer
from ..models import TrackFeatures
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
    # Assume TrackFeatures is the name of your model
    queryset = TrackFeatures.objects.all()  # pylint: disable=no-member
    serializer_class = TrackFeaturesSerializer  # specify the serializer class here
    lookup_url_kwarg = 'track_uri'  # The keyword argument in the URL that determines the object to retrieve
