import sp_utility
import spotipy
from ..spotify_token_handler import SpotifyTokenHandler


class SpotifyPlaylistService:
    def __init__(self, client: spotipy.Spotify,
                 token_handler: SpotifyTokenHandler):
        # getting reference from token handler when we init it
        # but good for easy access
        self.client = client
        self.token_handler = token_handler

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
