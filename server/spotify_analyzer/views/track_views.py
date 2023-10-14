from typing import Type
from django.http import Http404, JsonResponse, HttpResponse
from django.views import View
from injector import inject
from rest_framework.views import APIView
from rest_framework import status

from ..services.track_service import TrackService
from ..serializers import TrackSerializer



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
        track_data = self.track_service.get_track(track_uri=track_uri)
        #check it exists
        if track_data:
            serializer = TrackSerializer(track_data)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            raise Http404("Track does not exist")

    def post(self, request):
        serializer=TrackSerializer(request.data)
        if serializer.is_valid():
            track=self.track_service.create_track(track_data=serializer.validated_data)
            return JsonResponse(TrackSerializer(track).data,status=status.HTTP_201_CREATED)

    def put(self, request,track_uri):
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
        track = self.track_service.delete_track(track_uri=track_uri)

        if not track:
            raise Http404("Track does not exist")
        else:
            return JsonResponse({"message": "Track deleted successfully"}, status=status.HTTP_200_OK)
