from django.http import JsonResponse, HttpResponse
from django.views import View
from injector import inject
from rest_framework.views import APIView
from server.spotify_analyzer.services.track_features_service import TrackFeaturesService

#i want CBV but also want DI
#best of both worlds is wrapping the creation of a CBV with a 
#function that gets the service bean injected
@inject
def create_track_features_view(track_features_service: TrackFeaturesService):
    return TrackFeaturesView.as_view(track_features_service=track_features_service)

class TrackFeaturesView(APIView):
    def __init__(self, track_features_service, *args, **kwargs):
        self.track_features_service = track_features_service
        super().__init__(*args, **kwargs)
    
    def get(self, request):
        # Handle GET request
        return JsonResponse({"message": "This is a GET request"})

    def post(self, request):
        # Handle POST request
        return JsonResponse({"message": "This is a POST request"})

    def put(self, request):
        # Handle PUT request
        return JsonResponse({"message": "This is a PUT request"})

    def delete(self, request):
        # Handle DELETE request
        return JsonResponse({"message": "This is a DELETE request"})
