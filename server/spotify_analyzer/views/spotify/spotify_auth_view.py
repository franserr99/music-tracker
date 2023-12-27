import traceback
import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from ...services.spotify.token_handler import SpotifyTokenHandler
from ...services.core.user_service import UserService
from ...models import User
from ...dtos.service_dtos import TokenInfo


app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


@method_decorator(csrf_exempt, name='dispatch')
class SpotifyAuthCodeView(APIView):
    def post(self, request: Request, *args, **kwargs):
        refreshToken = request.data.get('refreshToken')
        accessToken = request.data.get('accessToken')
        user_id = request.data.get('user_id')
        expires_in = request.data.get('sp_expires_in')

        if not (accessToken and accessToken and user_id):
            return Response({'error': 'Need AccessToken, RefreshToken,\
                             and Time until Expiration'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user_service = UserService(user_model=User, logger=logger)
            token_info = TokenInfo({
                'accessToken': accessToken,
                'expires_in': expires_in,
                'refreshToken': refreshToken,
                'user_id': user_id
            })
            token_handler = SpotifyTokenHandler(
                user_service=user_service, token_info=token_info)
            token_handler.init_user_and_token()

        except APIException as e:
            print(traceback.format_exc())
            # logger.exception(f"An unexpected error occurred: {str(e)}")
            return Response({'error': e.detail},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response({'error': 'Authentication failed.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Successfully authenticated'},
                        status=status.HTTP_200_OK)
