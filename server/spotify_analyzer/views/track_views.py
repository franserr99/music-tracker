"""
Module to handle the TrackView API endpoints.

This module provides the API endpoints for the `Track` model, 
supporting the usual CRUD operations (Create, Read, Update, Delete).
It makes use of dependency injection to separate out the business logic.

Classes:
    - TrackView: Provides the API endpoints for the `Track` model.

Functions:
    - create_track_view: Factory function to inject dependencies into TrackView.
"""
from typing import Type
from django.http import Http404, JsonResponse# HttpResponse
from injector import inject
from rest_framework.views import APIView
from rest_framework import status

from ..services.track_service import TrackService
from ..services.track_features_service import TrackFeaturesService
from ..serializers import TrackSerializer,TrackFeaturesSerializer


@inject
def create_track_view(track_service: TrackService,feature_service:TrackFeaturesService
                      )-> Type[APIView]:
    """
    Factory function to inject dependencies into TrackView.

    Args:
        track_service (TrackService): Service for track-related operations.
        feature_service (TrackFeaturesService): Service for track features operations.

    Returns:
        Type[APIView]: A TrackView class with the necessary services injected.
    """
    return TrackView.as_view(track_service=track_service,)
class TrackView(APIView):
    """
    API endpoints for the Track model.

    Provides the CRUD operations for `Track` objects including 
    creation, reading, updating, and deleting tracks.

    Attributes:
        track_service (TrackService): Service for track-related operations.
        feature_service (TrackFeaturesService): Service for track features operations.
    """
    #use type hints to keep function hinting 
    def __init__(self, track_service: TrackService,feature_service:TrackFeaturesService, *args, **kwargs):
        """
        Initialize the TrackView with injected dependencies.

        Args:
            track_service (TrackService): Service for track-related operations.
            feature_service (TrackFeaturesService): Service for track features operations.
        """
        self.track_service = track_service
        self.feature_service = feature_service
        super().__init__(*args, **kwargs)

    def get(self, request, **kwargs):
        """
        Retrieve a track based on URI.

        Args:
            request: The HTTP request object.
            **kwargs: Additional keyword arguments (includes 'track_uri').

        Raises:
            Http404: If the track does not exist.

        Returns:
            JsonResponse: Serialized track data.
        """
        #track_uri is a URL parameter
        track_uri = kwargs.get('track_uri')
        #dispatch service obj to get track from db
        track_data = self.track_service.get_track(track_uri=track_uri)
        #check it exists
        if track_data:
            serializer = TrackSerializer(track_data)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            raise Http404("Track does not exist")

    def post(self, request):
        """
        Create a new track.

        Args:
            request: The HTTP request object containing the track data.

        Returns:
            JsonResponse: Serialized data of the newly created track.
            status: HTTP status code indicating the success or failure of the operation.

        Raises:
            Http404: If the track could not be created.
        """
        serializer=TrackSerializer(request.data)
        if serializer.is_valid():
            track=self.track_service.create_track(track_data=serializer.validated_data)
            return JsonResponse(TrackSerializer(track).data,status=status.HTTP_201_CREATED)

    def put(self, request,track_uri):
        """
        Update an existing track.

        Args:
            request: The HTTP request object containing the updated track data.
            track_uri: URI of the track to be updated.

        Returns:
            JsonResponse: Serialized data of the updated track.
            status: HTTP status code indicating the success or failure of the operation.

        Raises:
            Http404: If the track does not exist.
        """
        serializer = TrackSerializer(request.data)
        if serializer.is_valid():
            track=self.track_service.update_track(track_uri=track_uri,track_data=serializer.validated_data)
            if track:
                return JsonResponse(TrackSerializer(track).data,status=status.HTTP_200_OK)
            else:
                raise Http404("Track does not exist")
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,track_uri):
        """
        Delete an existing track.

        Args:
            request: The HTTP request object.
            track_uri: URI of the track to be deleted.

        Returns:
            JsonResponse: Message indicating successful deletion.
            status: HTTP status code indicating the success or failure of the operation.

        Raises:
            Http404: If the track does not exist.
        """
        track = self.track_service.delete_track(track_uri=track_uri)

        if not track:
            raise Http404("Track does not exist")
        else:
            return JsonResponse({"message": "Track deleted successfully"}, status=status.HTTP_200_OK)
    def get_track_features(self,request,track_uri):
        """
        Retrieve features of a specific track based on URI.

        Args:
            request: The HTTP request object.
            track_uri: URI of the track whose features are to be retrieved.

        Returns:
            JsonResponse: Serialized track feature data.
            status: HTTP status code indicating the success or failure of the operation.

        Raises:
            Http404: If the track's features do not exist.
        """
        track_features=self.feature_service.get_track_features(track_uri=track_uri)
        if track_features:
            serializer = TrackFeaturesSerializer(track_features)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            raise Http404("Track's Features do not exist")
