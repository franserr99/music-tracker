"""_summary_

Returns:
    _type_: _description_
"""

from injector import inject
from rest_framework.generics import RetrieveAPIView,ListCreateAPIView

from ..models import Playlist
from..serializers import PlaylistWithTracksSerializer,PlaylistSerializer
from ..services.playlist_service import PlaylistService

# @inject
# def create_playlist_view(playlist_service: PlaylistService):
#     return PlaylistView.as_view(playlist_service=playlist_service)
# class PlaylistView(APIView):
#     # Endpoint: /api/playlists/
#     # HTTP Method: GET
#     # Query Parameters: user_id=<user_id>

#     def __init__(self, playlist_service, *args, **kwargs):
#         self.playlist_service = playlist_service
#         super().__init__(*args, **kwargs)
#     def get(self, request):
#         # Handle GET request
#         return JsonResponse({"message": "This is a GET request"})

#     def post(self, request):
#         # Handle POST request
#         return JsonResponse({"message": "This is a POST request"})

#     def put(self, request):
#         # Handle PUT request
#         return JsonResponse({"message": "This is a PUT request"})

#     def delete(self, request):
#         # Handle DELETE request
#         return JsonResponse({"message": "This is a DELETE request"})

#responsible for listing all playlists or creating one
class PlaylistListView(ListCreateAPIView):
    # Specify the serializer for Playlist
    serializer_class = PlaylistSerializer

    #query set is the list of elements available for the operation
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            return Playlist.objects.filter(user_id=user_id)# pylint: disable=no-member
        return Playlist.objects.all()# pylint: disable=no-member

    def perform_create(self, serializer):
        user_id = self.request.query_params.get('user_id', None)
        serializer.save(user_id=user_id)

class PlaylistTracksRetrieveView(RetrieveAPIView):

    queryset = Playlist.objects.all() # pylint: disable=no-member
    serializer_class = PlaylistWithTracksSerializer
    lookup_url_kwarg = 'playlist_id'

    