"""
Module to handle the TrackView API endpoints.

This module provides the API endpoints for the `Track` model, 
supporting the usual CRUD operations (Create, Read, Update, Delete).
It makes use of dependency injection to separate out the business logic.

Classes:
    - TrackView: Provides the API endpoints for the `Track` model.

Functions:
    - create_track_view: Factory function to 
        inject dependencies into TrackView.
"""

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from ..serializers import TrackSerializer
from ..models import Track


class TrackListCreate(ListCreateAPIView):
    queryset = Track.objects.all()  # Adjust the queryset to your needs
    serializer_class = TrackSerializer

    # # If you need additional business logic on POST, override this method
    # def perform_create(self, serializer):
    #     # Here you could potentially integrate your 'track_service'
    #     serializer.save()


class TrackRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Track.objects.all()  # Adjust the queryset to your needs
    serializer_class = TrackSerializer
    lookup_field = 'track_uri'  # The field in the URL to look up by

    # # If you have additional logic for the PUT or DELETE methods,
    #  you can override methods like:
    # def perform_update(self, serializer):
    #     # Here you could potentially integrate your 'track_service'
    #     serializer.save()

    # def perform_destroy(self, instance):
    #     # Here you could potentially integrate your 'track_service'
    #     instance.delete()
