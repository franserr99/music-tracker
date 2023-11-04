from rest_framework.generics import ListAPIView
from ..models import Track
from ..serializers import TrackSerializer


class TrackListView(ListAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
