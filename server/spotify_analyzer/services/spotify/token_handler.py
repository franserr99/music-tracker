# from django.conf import settings
import spotipy
from ..core.user_service import UserService
import requests
# from base64 import b64encode
from ...dtos.retrieval_dtos import UserData
from rest_framework.exceptions import APIException

import time


class SpotifyTokenHandler:
    """_summary_
    The SpotifyOAuth object manages the OAuth 2.0 Authorization Code Flow.
    It can handle generating the authorization URL, 
    exchanging the authorization code for an access token,
      and refreshing the access token when it expires. 

    It is designed to encapsulate all the necessary OAuth
        logic for your application.

    SpotifyOAuth provides the necessary OAuth 2.0 capabilities that spotipy.
    Spotify uses to authenticate the api requests
    The client can take an auth_manager as an argument, 
    which is where you would pass in the SpotifyOAuth object. 
    Doing so means that the client will delegate all the token 
        management to that SpotifyOAuth object.

    """

    def __init__(self, user_service: UserService, user_id: str,
                 authorization_code=None):
        # i need to set some of these things as enviormental variables
        # before i try to run these
        # i need my client id etc to be there
        # self.oauth = SpotifyOAuth(scope=sp_utility.scope)
        self.user_service = user_service
        self.user_id = user_id
        if authorization_code:
            accessToken = self.getAccessToken(user_id=user_id,
                                              auth_code=authorization_code)
            if accessToken is None:
                raise Exception  # let fe know something went wrong, try again
            self.accessToken = accessToken
            self.client = spotipy.Spotify(auth=self.accessToken)
        else:
            # check if we have access token
            accessToken = self.getAccessToken(user_id=user_id)
            self.accessToken = accessToken
            self.client = spotipy.Spotify(auth=self.accessToken)
            if accessToken is None:
                raise Exception  # let fe know something went wrong, try again

    def getAccessAndRefreshToken(self, authorization_code, user_id: str):
        # retrieval logic
        client_id = '4cbf19a57d8a45248430ffe0a199b9fd'
        client_secret = 'e88c052b9ae04c48b804aa7e6893c988'
        body = {
            'grant_type': 'authorization_code',
            'code': str(authorization_code),
            'redirect_uri': 'http://localhost:3000/auth/callback',
            'client_secret': client_secret,
            'client_id': client_id
        }
        # test to see if you can use this content-type instead:
        #  application/json
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            # 'Authorization': f'Basic {encoded_credentials}'

        }
        url = 'https://accounts.spotify.com/api/token'
        response = requests.post(url=url, data=body, headers=headers)
        token_info = response.json()
        print("when getting both refresh and access: \n")
        print(token_info)

        if (response.ok):
            accessToken = token_info['access_token']
            refreshToken = token_info['refresh_token']
            now = int(time.time())
            expires_at = int(token_info['expires_in']) + now
            self.saveTokenInfo(user_id, accessToken, expires_at, refreshToken)
            return accessToken, refreshToken
        else:
            print("bad response!!!!")
            if token_info['error'] == 'invalid_grant':
                # let the front end know to put them through the process again
                raise APIException("Bad response when getting access token")

    # returns none or later will raise exception,
    # need to handle it when you call it
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
        else:  # neither access nor refresh token exist, fetch both
            assert (auth_code is not None)
            accessToken, refreshToken = self.getAccessAndRefreshToken(
                user_id=user_id, authorization_code=auth_code)
            print(refreshToken)
            return accessToken

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
