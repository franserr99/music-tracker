from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import logging
from ..services.spotify_service import SpotifyService  
# ,# SpotifyAuthException

# Configure logginglogger = logging.getLogger(__name__)
app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


@method_decorator(csrf_exempt, name='dispatch')
class SpotifyAuthCodeView(APIView):
    def post(self, request, *args, **kwargs):
        authorization_code = request.data.get('code')

        if not authorization_code:
            raise ValidationError(
                {'authorization_code': 'This field is required.'})

        try:
            print(authorization_code)
            spotify_service = SpotifyService(
                authorization_code=authorization_code)
            print(spotify_service)
        # except SpotifyAuthException as e:
        #     logger.error(f"SpotifyAuthException occurred: {str(e)}")
        #     return Response({'error': 'Authentication failed.'}, 
        #           status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            # logger.exception(f"An unexpected error occurred: {str(e)}")
            return Response({'error': 'An unexpected error occurred.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Do something with spotify_service like storing the access token,
        #  or performing other tasks

        return Response({'message': 'Successfully authenticated'},
                        status=status.HTTP_200_OK)
