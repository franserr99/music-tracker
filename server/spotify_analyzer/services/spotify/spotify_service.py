# from django.conf import settings
from spotipy.oauth2 import SpotifyOAuth
from . import sp_utility
import spotipy
from ..user_service import UserService
import requests
from base64 import b64encode
from ..service_dtos import UserTokenInfo,UserData

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

    def __init__(self, user_service: UserService, authorization_code=None):
        # i need to set some of these things as enviormental variables
        # before i try to run these
        # i need my client id etc to be there
        # self.oauth = SpotifyOAuth(scope=sp_utility.scope)
        self.user_service=user_service
        if authorization_code:
            # token_info = self.oauth.get_access_token(code=authorization_code)
            # self.access_token = token_info['access_token']
            self.accessToken = getAccessToken()
            self.client = spotipy.Spotify(auth=self.access_token)

            pass
        else:
            raise Exception
        
    def getAccessAndRefreshToken(self,authorization_code):
        # retrieval logic
        client_id = '4cbf19a57d8a45248430ffe0a199b9fd',
        client_secret = 'e88c052b9ae04c48b804aa7e6893c988',
        body = {
            'grant_type': 'authorization_code',
            'code': str(authorization_code),
            'redirect_uri': 'http://localhost:3000/auth/callback'
        }
        encoded_credentials = b64encode(f'{client_id}:{client_secret}'
                                        .encode('utf-8')).decode('utf-8')
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {encoded_credentials}'

        }
        token_info = requests.get(url='https://accounts.spotify.com/api/token',
                                  data=body, headers=headers).json()
        accessToken = token_info['access_token']
        refreshToken = token_info['refresh_token']
        token_dict = UserTokenInfo(refresh_token=refreshToken,
                                   access_token=accessToken)
        user_data=UserData()
        self.user_service.create_user()
        self.user_service.add_user_tokens()
        SpotifyService.saveAccessToken(accessToken)
        SpotifyService.saveRefreshToken(refreshToken)
    
        return accessToken, refreshToken

    def getAccessToken(self):
        # check if current access token is expired 
        # return it if valid


        # else fetch the refresh token 
        # if refresh token does not exist, call getAccessAndRefreshToken

        # get the access token using the refresh token and return it
        pass

    def saveAccessToken(self):
        pass

    def saveRefreshToken(self):

        pass

    def isAccessTokenExpired(token: str, auth: spotipy.SpotifyOAuth):
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
