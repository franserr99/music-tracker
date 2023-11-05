import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, APIException
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import logging
from ..services.spotify.spotify_token_handler import SpotifyTokenHandler
from ..services.user_service import UserService
from ..models import User
# ,# SpotifyAuthException

# Configure logginglogger = logging.getLogger(__name__)
app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


@method_decorator(csrf_exempt, name='dispatch')
class SpotifyAuthCodeView(APIView):
    def post(self, request, *args, **kwargs):
        authorization_code = request.data.get('code')
        user_id = request.data.get('user_id')

        if not authorization_code:
            raise ValidationError(
                {'authorization_code': 'This field is required.'})

        try:
            print(authorization_code)
         
            user_service = UserService(user_model=User, logger=logger)
            token_handler = SpotifyTokenHandler(
                authorization_code=authorization_code,
                user_service=user_service, user_id=user_id)
            print(token_handler)
        # except SpotifyAuthException as e:
        #     logger.error(f"SpotifyAuthException occurred: {str(e)}")
        #     return Response({'error': 'Authentication failed.'}, 
        #           status=status.HTTP_400_BAD_REQUEST)
        except APIException as e:
            print(traceback.format_exc())
            # logger.exception(f"An unexpected error occurred: {str(e)}")
            return Response({'error': e.detail},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Do something with spotify_service like storing the access token,
        #  or performing other tasks

        return Response({'message': 'Successfully authenticated'},
                        status=status.HTTP_200_OK)
