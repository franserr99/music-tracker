import traceback
import logging

from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response

from ...services.core.user_service import UserService
from ...services.spotify.token_handler import SpotifyTokenHandler
from ...models import User


app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


@method_decorator(csrf_exempt, name='dispatch')
class UserTokenView(APIView):
    def get(self, request, user_id):
        try:
            # create the token handler so it can refresh it
            # then use the user service to get the token
            user_service = UserService(User, logger)
            token_handler = SpotifyTokenHandler(
                user_service=user_service, user_id=user_id)
            return Response(token_handler.accessToken)

        except APIException as e:
            print(traceback.format_exc())
            return Response({'error': e.detail},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
