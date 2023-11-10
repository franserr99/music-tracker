from typing import List
from ....util.parse_results_util import get_tracks
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
        return self._begin_build(user_flag=True, with_audio=True)

    def get_user_liked_playlists(self):
        return self._begin_build(user_flag=False, with_audio=True)

    def get_user_added_created_playlists(self):
        user_created_tracks = self._begin_build(
            user_flag=True, with_audio=True)
        liked_playlist_tracks = self._begin_build(
            user_flag=False, with_audio=True)
        return user_created_tracks, liked_playlist_tracks

    def _begin_build(self, user_flag: bool, with_audio=True):
        playlists_idx = []
        playlists = self.client.current_user_playlists()
        playlist_owners = {}
        users = self._process_page(playlists=playlists,
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
                users.extend(self._process_page(playlists=playlists,
                                                user_flag=user_flag,
                                                playlist_idx=playlists_idx,
                                                playlist_owners=playlist_owners))
        info = get_tracks(
            self.client, self.oauth, ("p", playlists_idx), True)

        return info

    def _process_page(self, playlists, user_flag,
                      playlist_idx: List[str], playlist_owners):
        # TODO
        liked_playlists = {}

        for playlist in playlists['items']:
            me = self.client.me()['id']
            owner = playlist['owner']['id']
            playlist_owners[playlist['id']] = owner
            if user_flag:
                # current user is already in system
                if (me == owner):
                    playlist_idx.append(playlist['id'])
            else:
                # other users, need it for my models
                if (owner != me):
                    liked_playlists[id] = owner
                    playlist_idx.append(playlist['id'])
