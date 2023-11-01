"""
This module provides a Django REST Framework view
    for managing and retrieving track features.

Raises:
    Http404: Raised if a track feature resource cannot be found.
  
Returns:
    JsonResponse: 
        Returns a JSON representation of track features or an error message.
"""

from ..serializers import TrackFeaturesSerializer
from ..models import TrackFeatures


from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView


class TrackFeatureListCreate(ListCreateAPIView):
    queryset = TrackFeatures.objects.all()  # Adjust the queryset to your needs
    serializer_class = TrackFeaturesSerializer


class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = TrackFeatures.objects.all()  # Adjust the queryset to your needs
    serializer_class = TrackFeaturesSerializer
    lookup_field = 'track_uri'  # The field in the URL to look up by
