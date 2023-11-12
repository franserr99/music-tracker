import traceback
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ...util.services_util import init_all_services
from ...util.persistence_util import persist_retrived_data

app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


@method_decorator(csrf_exempt, name='dispatch')
class SpotifyFavorites(APIView):
    def post(self, request, id):
        user_id = id
        type = request.data.get('type')
        try:
            services = init_all_services(user_id, logger)
            sp_favorites_service = services['sp_favorites_service']
            if type == 'tracks':
                parsedInfo = sp_favorites_service.get_monthly_tracks()
                persist_retrived_data(services, parsedInfo, user_id)
                # connect this to my old method, it will do the heavy
                # lifting for getting the audio features
                return Response(parsedInfo)
            elif type == 'artists':
                parsedInfo = sp_favorites_service.get_monthly_artists()
                persist_retrived_data(services, parsedInfo)
                return Response(parsedInfo)
            else:
                return Response({'error': 'Bad input'},
                                status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            print(traceback.format_exc())
            # logger.exception(f"An unexpected error occurred: {str(e)}")
            return Response({'error': e.detail},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
