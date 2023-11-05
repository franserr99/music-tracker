import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import logging
import json
from ...services.spotify.spotify_token_handler import SpotifyTokenHandler
from ...services.user_service import UserService
from ...models import User
from ...services.spotify.spotify_track_service import SpotifyTrackService

app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


@method_decorator(csrf_exempt, name='dispatch')
class SpotifyFavorites(APIView):
    def post(self, request, id):
        user_id = id
        type = request.data.get('type')
        try:
            # print(authorization_code)
         
            user_service = UserService(user_model=User, logger=logger)
            token_handler = SpotifyTokenHandler(
                user_service=user_service, user_id=user_id)
            print(token_handler)
            sp_track_service = SpotifyTrackService(client=token_handler.client,
                                                   token_handler=token_handler)
            if type == 'tracks':
                top_tracks = sp_track_service.get_monthly_tracks()
                records = top_tracks.to_dict(orient='records')
                json_data = json.dumps(records)
                return Response(json_data)
            elif type == 'artists':
                top_artists = sp_track_service.get_monthly_artists()
                records = top_artists.to_dict(orient='records')
                json_data = json.dumps(records)
                return Response(json_data)
            else:
                return Response({'error': 'Bad input'},
                                status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            print(traceback.format_exc())
            # logger.exception(f"An unexpected error occurred: {str(e)}")
            return Response({'error': e.detail},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)