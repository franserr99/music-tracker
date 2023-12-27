import traceback

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ...stats.analysis.playlist_stats import playlist_genres, \
    topNGenresInCommon, topNGenres


@method_decorator(csrf_exempt, name='dispatch')
class PlaylistsStats(APIView):
    def post(self, request):
        type = request.data.get('type')
        try:
            if (type == 'similar-group-bar-chart'):
                playlist_ids = list(request.data.get('ids'))
                return Response(topNGenresInCommon(playlist_ids))
            elif (type == 'different-group-bar-chart'):
                playlist_ids = list(request.data.get('ids'))
                p_genres = []
                for playlist in playlist_ids:
                    p_genres.append(playlist_genres(playlist))
                p_filtered_genres = []
                for genres in p_genres:
                    p_filtered_genres.append(topNGenres(genres))
                for index, genre_info in enumerate(p_filtered_genres):
                    genre_info['playlist_id'] = playlist_ids[index]
                return Response(p_filtered_genres)
            else:
                return Response("More options not implemented yet")

        except APIException as e:
            print(traceback.format_exc())
            return Response({'error': e.detail},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
