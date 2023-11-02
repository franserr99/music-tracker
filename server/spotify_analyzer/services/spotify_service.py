# from django.conf import settings
from spotipy.oauth2 import SpotifyOAuth
from .. import sp_utility
import spotipy


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

    def __init__(self, authorization_code=None):

        self.oauth = SpotifyOAuth(scope=sp_utility.scope)
        if authorization_code:
            token_info = self.oauth.get_access_token(code=authorization_code)
            self.access_token = token_info['access_token']
        self.client = spotipy.Spotify(
            auth=self.access_token if authorization_code else None)

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
