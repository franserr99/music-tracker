from django.http import JsonResponse, HttpResponse
from django.views import View
from injector import inject

from server.spotify_analyzer.services.track_service import TrackService


#i want CBV but also want DI
#best of both worlds is wrapping the creation of a CBV with a 
#function that gets the service bean injected
@inject
def create_track_view(track_service: TrackService):
    return TrackView.as_view(track_service=track_service)
class TrackView(View):
    def __init__(self, track_service, *args, **kwargs):
        self.track_service = track_service
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
