from rest_framework.generics import ListAPIView
from server.spotify_analyzer.models import User
from server.spotify_analyzer.views.serializers import UserSerializer


class TrackListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
