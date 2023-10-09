from typing import Type
from django.http import JsonResponse, HttpResponse
from django.views import View
from injector import inject
from rest_framework.views import APIView
from server.spotify_analyzer.services.track_service import TrackService
from server.spotify_analyzer.serializers import TrackDataSerializer
from rest_framework import status


#CBV+DI: wrap the creation of a CBV with a 
#function that gets the service bean injected
@inject
def create_track_view(track_service: TrackService)-> Type[APIView]:
    return TrackView.as_view(track_service=track_service)
class TrackView(APIView):
    #use type hints to keep function hinting 
    def __init__(self, track_service: TrackService, *args, **kwargs):
        self.track_service = track_service
        super().__init__(*args, **kwargs)

    def get(self, request, **kwargs):
        #track_uri is a URL parameter
        track_uri = kwargs.get('track_uri')  
        #dispatch service obj to get track from db
        track_data = self.track_service.get_track(track_uri)  
        #check it exists
        if track_data:
            serializer = TrackDataSerializer(track_data)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({"error": "Track not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = TrackDataSerializer(data=request.data)

        if serializer.is_valid():
            
            
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
        return JsonResponse({"message": "This is a POST request"})

    def put(self, request):
        # Handle PUT request
        return JsonResponse({"message": "This is a PUT request"})

    def delete(self, request):
        # Handle DELETE request
        return JsonResponse({"message": "This is a DELETE request"})
