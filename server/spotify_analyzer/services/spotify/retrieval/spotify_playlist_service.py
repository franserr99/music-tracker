from typing import List
from ....util.parse_results_util import get_tracks
import spotipy
from ..token_handler import SpotifyTokenHandler
import requests
from ...dtos.retrieval_dtos import PlaylistsInfo
from ....util.parse_results_util import get_missing_artist_info, get_owner_dtos


class SpotifyPlaylistService:
    def __init__(self, client: spotipy.Spotify,
                 token_handler: SpotifyTokenHandler):
        # getting reference from token handler when we init it
        # but good for easy access
        self.client = client
        self.token_handler = token_handler

    def get_user_created_playlists(self) -> PlaylistsInfo:
        info = self._begin_build(user_flag=True, with_audio=True)
        # get_missing_artist_info(missing, self.token_handler, info)

        return info

    def get_user_liked_playlists(self) -> PlaylistsInfo:
        info = self._begin_build(
            user_flag=False, with_audio=True)
        # get_missing_artist_info(missing, self.token_handler, info)
        return info

    def get_user_added_created_playlists(self) -> (PlaylistsInfo,
                                                   dict, List[str]):
        pass
        # rework this one i think i can process it all in one go
        # user_created_tracks, missing1 = self._begin_build(
        #     user_flag=True, with_audio=True)
        # liked_playlist_tracks, missing2 = self._begin_build(
        #     user_flag=False, with_audio=True)
        # return user_created_tracks, \
        #     liked_playlist_tracks, owners1.extend(
        #         owners2), missing1.extend(missing2)

    def _begin_build(self, user_flag: bool,
                     with_audio=True) -> (PlaylistsInfo, List[str]):
        playlists_idx = []
        playlists = self.client.current_user_playlists()
        # print(playlists)
        playlist_owners = {}
        self._process_page(playlists=playlists,
                           user_flag=user_flag,
                           playlist_idx=playlists_idx,
                           playlist_owners=playlist_owners)
        if playlists['next']:
            token = self.token_handler.accessToken

            while playlists['next']:
                headers = {'Authorization': "Bearer"+" "+token}
                url = playlists['next']
                playlists = requests.get(url=url, headers=headers,
                                         timeout=10).json()
                self._process_page(
                    playlists=playlists,
                    user_flag=user_flag,
                    playlist_idx=playlists_idx,
                    playlist_owners=playlist_owners)
        info = get_tracks(
            self.client, self.token_handler,
            ("p", playlists_idx), True, playlist_owners
        )
        # add users
        owner_dtos = get_owner_dtos(owners=playlist_owners)
        for owner in owner_dtos:
            id = owner['id']
            info['users'][id] = owner
        return info

    def _process_page(self, playlists, user_flag,
                      playlist_idx: List[str], playlist_owners):
        for playlist in playlists['items']:
            me = self.client.me()['id']
            owner = playlist['owner']['id']
            id = playlist['id']
            playlist_owners[id] = owner
            if user_flag and me == owner:
                # current user is already in system
                playlist_idx.append(id)
            elif not user_flag and owner != me:
                # other users, need it for my models
                playlist_idx.append(id)
