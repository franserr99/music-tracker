# from django.conf import settings
from . import sp_utility
import spotipy
from ..user_service import UserService
import requests
# from base64 import b64encode
from ..service_dtos import UserData
from rest_framework.exceptions import APIException


class SpotifyService:
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
        if authorization_code:
            # token_info = self.oauth.get_access_token(code=authorization_code)
            # self.access_token = token_info['access_token']
            # self.accessToken = getAccessToken()
            accessToken, refreshToken = self.getAccessAndRefreshToken(
                authorization_code=authorization_code, user_id=user_id)
            self.accessToken = accessToken
            self.client = spotipy.Spotify(auth=self.accessToken)

        else:
            raise Exception
        
    def getAccessAndRefreshToken(self, authorization_code, user_id: str):
        # retrieval logic
        client_id = '4cbf19a57d8a45248430ffe0a199b9fd',
        client_secret = 'e88c052b9ae04c48b804aa7e6893c988',
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
        print(token_info)

        if (response.ok):
            accessToken = token_info['access_token']
            refreshToken = token_info['refresh_token']    
            user_data = UserData(id=user_id)
            self.user_service.create_user(user_data=user_data)
            self.saveAccessToken(user_id, accessToken)
            self.saveRefreshToken(user_id, refreshToken)
    
            return accessToken, refreshToken
            
        else:
            print("bad response!!!!")
            if token_info['error'] == 'invalid_grant':
                # let the front end know to put them through the process again
                raise APIException("Bad response when getting access token")
            
    # returns none or later will raise exception,
    # need to handle it when you call it 
    def getAccessToken(self, user_id: str):
        user = self.user_service.get_user(user_id=user_id)
        if user is None:
            print("no user exists with that id, ned to create it")
            #if it fits in the code flow then we can get all these things done at once
            return None
        client_id = '4cbf19a57d8a45248430ffe0a199b9fd',
        client_secret = 'e88c052b9ae04c48b804aa7e6893c988'
        redirect_uri = 'http://localhost:3000/auth/callback'
        auth = spotipy.SpotifyOAuth(client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri)
        token = user.access_token
        if (token):  # some exists
            # but it was expired
            if (self.isAccessTokenExpired(token=token, auth=auth)):
                
                accessToken = self.handleRefreshTokenChecking()
                return accessToken
            return token
        else:
            accessToken = self.handleRefreshTokenChecking()
            return accessToken

    def handleRefreshTokenChecking(self):
        # get the refresh token, should be stored 
        # if returns none then let FE know (their problem)
        refresh_token = self.getRefreshToken()
        if refresh_token is None:
            # let the front end know, returning none for now
            # later we will raise exception and handle it in higher layer
            pass
            return None
        else:
            new_token = self.fetchAccessTokenWithRefreshToken()
            return new_token

    def fetchAccessTokenWithRefreshToken(self):
        pass

    def getRefreshToken(self):
        user = self.user_service.get_user(user_id=user_id)
        if(user):


        token = user.access_token


        pass

    def saveAccessToken(self, user_id: str, access_token: str):
        self.user_service.add_token(user_id=user_id,
                                    token=access_token, access=True)
        
    def saveRefreshToken(self, user_id: str, refresh_token: str):
        self.user_service.add_token(user_id=user_id,
                                    token=refresh_token, access=False)

    def isAccessTokenExpired(self, token: str, auth: spotipy.SpotifyOAuth):
        return auth.is_token_expired(token)
    
    def get_user_created_playlists(self):
        """"""
        return self._begin_build(user_flag=True, with_audio=True)

    def get_user_liked_playlists(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._begin_build(user_flag=False, with_audio=True)

    def get_user_added_created_playlists(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        user_created_tracks = self._begin_build(
            user_flag=True, with_audio=True)
        liked_playlist_tracks = self._begin_build(
            user_flag=False, with_audio=True)
        return user_created_tracks, liked_playlist_tracks

    def _begin_build(self, user_flag: bool, with_audio=True):
        """_summary_

        Args:
            user_flag (bool): _description_
            with_audio (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        playlists_idx = []
        playlists = self.client.current_user_playlists()

        self._process_page(playlists=playlists,
                           user_flag=user_flag, playlist_idx=playlists_idx)
        # if playlists['next']:
        #     # token=get_user_token()
        #     # type=token['token_type']
        #     # access_token=token['access_token']
        #     while playlists['next']:
        #         # headers={ 'Authorization': type+" "+access_token }
        #         url = playlists['next'],
        #         # playlists= requests.get(url=url,headers=headers,
        # timeout=10).json()
        #         # _process_page(playlists=playlists,user_flag=user_flag,
        # client=self.client,playlist_idx=playlists_idx)
        #     # handle pagination
        df_with_audio = sp_utility.get_tracks(
            self.client, self.oauth, ("p", playlists_idx), True)
        return df_with_audio

    def _process_page(self, playlists, user_flag, playlist_idx):
        for playlist in playlists['items']:
            if user_flag:
                if (playlist['owner']['id'] == self.client.me()['id']):
                    playlist_idx.append(playlist['id'])
            else:
                if (playlist['owner']['id'] != self.client.me()['id']):
                    playlist_idx.append(playlist['id'])
