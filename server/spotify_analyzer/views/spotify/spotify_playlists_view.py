import traceback
import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ...util.services_util import init_all_services
from ...util.persistence_util import persist_retrived_data
from ...util.redis_util import get_data_from_redis, get_redis_instance

app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


@method_decorator(csrf_exempt, name='dispatch')
class SpotifyPlaylists(APIView):
    def post(self, request: Request, id):
        user_id = id
        type = request.data.get('type')
        # created, liked, all
        try:
            redis_data = get_data_from_redis(get_redis_instance())
            services = init_all_services(user_id, logger, redis_data)
            sp_playlist_service = services['sp_playlist_service']
            if type == 'created':
                parsedInfo = \
                    sp_playlist_service.get_user_created_playlists()
                persist_retrived_data(services, parsedInfo, user_id=user_id)
                # connect this to my old method, it will do the heavy
                # lifting for getting the audio features
                return Response(parsedInfo)
            elif type == 'liked':
                parsedInfo = sp_playlist_service.get_user_liked_playlists()
                persist_retrived_data(services, parsedInfo)
                return Response(parsedInfo)
            elif type == 'all':
                parsedInfo = sp_playlist_service. \
                    get_user_added_created_playlists()

                pass
            else:
                return Response({'error': 'Bad input'},
                                status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            print(traceback.format_exc())
            # logger.exception(f"An unexpected error occurred: {str(e)}")
            return Response({'error': e.detail},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
