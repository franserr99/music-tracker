import traceback

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ...stats.analysis.playlist_stats import playlist_genres


@method_decorator(csrf_exempt, name='dispatch')
class PlaylistStats(APIView):
    def post(self, request, id):
        playlist_id = id
        type = request.data.get('type')
        print("playlist gotten by backend",playlist_id)
        try:
            if type == 'wordmap' or type == 'bar-chart':
                genre_count = playlist_genres(playlist_id)
                return Response(genre_count)
            else:
                return Response("More options not implemented yet")

        except APIException as e:
            print(traceback.format_exc())
            # logger.exception(f"An unexpected error occurred: {str(e)}")
            return Response({'error': e.detail},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
