import server.spotify_analyzer.services.spotify.utility as utility
import spotipy
from ..token_handler import SpotifyTokenHandler
import requests


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
        playlist_owners = {}
        self._process_page(playlists=playlists,
                           user_flag=user_flag,
                           playlist_idx=playlists_idx,
                           playlist_owners=playlist_owners)
        if playlists['next']:
            token = self.token_handler.accessToken

            while playlists['next']:
                headers = {'Authorization': "Bearer"+" "+token}
                url = playlists['next'],
                playlists = requests.get(url=url, headers=headers,
                                         timeout=10).json()
                self._process_page(playlists=playlists,
                           user_flag=user_flag,
                           playlist_idx=playlists_idx,
                           playlist_owners=playlist_owners)
        df_with_audio = utility.get_tracks_df(
            self.client, self.oauth, ("p", playlists_idx), True)
        return df_with_audio

    def _process_page(self, playlists, user_flag, playlist_idx, playlist_owners):
        for playlist in playlists['items']:
            me = self.client.me()['id']
            owner = playlist['owner']['id']
            playlist_owners[playlist['id']] = owner
            if user_flag:
                if (me == owner):
                    playlist_idx.append(playlist['id'])
            else:
                if (owner != me):
                    playlist_idx.append(playlist['id'])
