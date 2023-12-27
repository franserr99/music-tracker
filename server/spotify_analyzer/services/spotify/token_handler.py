
import spotipy
from ..core.user_service import UserService
import requests

from ...dtos.retrieval_dtos import UserData
from ...dtos.service_dtos import TokenInfo
from rest_framework.exceptions import APIException

import time


class SpotifyTokenHandler:
    """_summary_
    The SpotifyOAuth object manages the OAuth 2.0 Authorization Code Flow.
    It can handle generating the authorization URL, 
    exchanging the authorization code for an access token,
      and refreshing the access token when it expires. 

    It is designed to encapsulate all the necessary OAuth logic

    SpotifyOAuth provides the necessary OAuth 2.0 capabilities that spotipy.
    Spotify uses to authenticate the api requests
    The client can take an auth_manager as an argument, 
    which is where you would pass in the SpotifyOAuth object. 
    Doing so means that the client will delegate all the token 
        management to that SpotifyOAuth object.

    """

    def __init__(self, user_service: UserService, token_info: TokenInfo):
        # TODO:i need to set some of these things as enviormental variables
        # before i try to run these
        # i need my client id etc to be there
        self.user_service = user_service
        # self.user_id = user_id
        self.token_info = token_info
    # main function clients will call
    # other functions are more tightly coupled,
    # but you can data prep and pass into them

    def init_user_and_token(self):
        user_id = self.token_info['user_id']
        refreshToken = self.token_info['refreshToken']
        accessToken = self.token_info['accessToken']
        expires_in = self.token_info['expires_in']

        if (refreshToken and accessToken):
            user = self.user_service.get_user(user_id=user_id)
            if user is None:
                user_data = UserData(id=user_id)
                user = self.user_service.create_user(user_data=user_data)
            self.accessToken = accessToken
            # self.client = spotipy.Spotify(auth=self.accessToken)
            now = int(time.time())
            expires_at = now + int(expires_in)
            self.saveTokenInfo(user_id, accessToken, expires_at, refreshToken)
        else:
            accessToken = self.getAccessToken(user_id=user_id)
            self.accessToken = accessToken
            # self.client = spotipy.Spotify(auth=self.accessToken)
            if accessToken is None:
                raise Exception  # let fe know something went wrong, try again

    def getAccessToken(self, user_id: str, auth_code=None):
        user = self.user_service.get_user(user_id=user_id)
        user_data = UserData(id=user_id)
        if user is None:
            user = self.user_service.create_user(user_data=user_data)

        client_id = '4cbf19a57d8a45248430ffe0a199b9fd'
        client_secret = 'e88c052b9ae04c48b804aa7e6893c988'
        redirect_uri = 'http://localhost:3000/auth/callback'
        auth = spotipy.SpotifyOAuth(client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri)

        token = user.access_token
        token_info = {'expires_at': user.expires_at}
        if (token):  # some exists
            # but it was expired
            if (user.expires_at is None or self.isAccessTokenExpired(
                    token=token_info, auth=auth)):
                accessToken = self.handleRefreshTokenChecking(user_id)
                return accessToken
            return token

    def handleRefreshTokenChecking(self, user_id):
        # get the refresh token, should be stored
        # if returns none then let FE know (their problem)
        refresh_token = self.getRefreshToken(user_id)
        if refresh_token is None:
            return None
        else:
            new_token = self.fetchAccessTokenWithRefreshToken(refresh_token,
                                                              user_id)
            return new_token

    def fetchAccessTokenWithRefreshToken(self, token, user_id):
        # retrieval logic
        client_id = '4cbf19a57d8a45248430ffe0a199b9fd'
        client_secret = 'e88c052b9ae04c48b804aa7e6893c988'
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': str(token),
            'client_secret': client_secret,
            'client_id': client_id
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
        }
        url = 'https://accounts.spotify.com/api/token'
        response = requests.post(url=url, data=body, headers=headers)
        token_info = response.json()
        print("printing the response after using refresh token:")
        print(token_info)
        if (response.ok):
            accessToken = token_info['access_token']
            if 'refresh_token' in token_info:
                refreshToken = token_info['refresh_token']
            else:
                refreshToken = None
            now = int(time.time())
            expires_at = now + int(token_info['expires_in'])
            # sometimes they send new refresh tokens, save them when they do
            self.saveTokenInfo(user_id, accessToken, expires_at, refreshToken)
            return accessToken
        else:
            print("bad response!!!!")
            if token_info['error'] == 'invalid_grant':
                # let the front end know to put them through the process again
                raise APIException("Bad response when getting access token")

    def saveTokenInfo(self, user_id, accessToken, expires_at, refreshToken):
        if (accessToken):
            self.saveAccessToken(user_id, accessToken)
        if (refreshToken):
            self.saveRefreshToken(user_id, refreshToken)
        if (expires_at):
            self.saveTokenMetaData(user_id, expires_at)

    def getRefreshToken(self, user_id):
        user = self.user_service.get_user(user_id=user_id)
        if (user):
            token = user.refresh_token
            return token
        else:
            return None

    def saveTokenMetaData(self, user_id, expires_at):
        self.user_service.add_token_metadata(user_id=user_id,
                                             expires_at=expires_at)

    def saveAccessToken(self, user_id: str, access_token: str):
        self.user_service.add_token(user_id=user_id,
                                    token=access_token, access=True)

    def saveRefreshToken(self, user_id: str, refresh_token: str):
        self.user_service.add_token(user_id=user_id,
                                    token=refresh_token, access=False)

    def isAccessTokenExpired(self, token: str, auth: spotipy.SpotifyOAuth):
        return auth.is_token_expired(token)
