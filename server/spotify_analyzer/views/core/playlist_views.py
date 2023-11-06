"""_summary_

Returns:
    _type_: _description_
"""
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView

from ...models import Playlist
from ..serializers import PlaylistWithTracksSerializer, PlaylistSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class PlaylistListView(ListCreateAPIView):
    # Specify the serializer for Playlist
    serializer_class = PlaylistSerializer

    # query set is the list of elements available for the operation
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            return Playlist.objects.filter(user_id=user_id)
        return Playlist.objects.all()

    def perform_create(self, serializer):
        user_id = self.request.query_params.get('user_id', None)
        serializer.save(user_id=user_id)


@method_decorator(csrf_exempt, name='dispatch')
class PlaylistTracksRetrieveView(RetrieveAPIView):

    queryset = Playlist.objects.all()
    serializer_class = PlaylistWithTracksSerializer
    lookup_url_kwarg = 'playlist_id'
