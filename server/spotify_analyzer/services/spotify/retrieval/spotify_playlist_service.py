from typing import List
from ....util.parse_results_util import get_tracks
import spotipy
from ..token_handler import SpotifyTokenHandler
import requests
from ....dtos.retrieval_dtos import PlaylistsInfo
from ....dtos.redis_dtos import RedisData
from ....util.parse_results_util import get_owner_dtos


class SpotifyPlaylistService:
    def __init__(self, client: spotipy.Spotify,
                 token_handler: SpotifyTokenHandler,
                 redis_data: RedisData):
        # getting reference from token handler when we init it
        # but good for easy access
        self.client = client
        self.token_handler = token_handler
        self.redis_data = redis_data

    def get_user_created_playlists(self) -> PlaylistsInfo:
        info = self._begin_build(user_flag=True, with_audio=True)
        # get_missing_artist_info(missing, self.token_handler, info)
        if info is None:
            return {}
        return info

    def get_user_liked_playlists(self) -> PlaylistsInfo:
        info = self._begin_build(
            user_flag=False, with_audio=True)
        if info is None:
            return {}
        # get_missing_artist_info(missing, self.token_handler, info)
        return info

    def get_user_added_created_playlists(self) -> (PlaylistsInfo,
                                                   dict, List[str]):
        info = self._begin_build(
            user_flag=None, with_audio=True)
        if info is None:
            return {}
        # get_missing_artist_info(missing, self.token_handler, info)
        return info

        pass

    def _begin_build(self, user_flag: bool,
                     with_audio=True) -> (PlaylistsInfo, List[str]):
        playlists_idx = []
        playlists = self.client.current_user_playlists()
        # print(playlists)
        playlist_owners = {}
        playlist_names = {}
        playlist_descriptions = {}
        self._process_page(playlists=playlists,
                           user_flag=user_flag,
                           playlist_idx=playlists_idx,
                           playlist_owners=playlist_owners,
                           names=playlist_names,
                           descriptions=playlist_descriptions)
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
                    playlist_owners=playlist_owners,
                    names=playlist_names,
                    descriptions=playlist_descriptions)
        info = get_tracks(
            self.client, self.token_handler, self.redis_data,
            ("p", playlists_idx), True, playlist_owners,
            playlist_names, playlist_descriptions
        )
        if info is None:
            return None
        # add users
        owner_dtos = get_owner_dtos(owners=playlist_owners)
        for owner in owner_dtos:
            id = owner['id']
            info['users'][id] = owner
        return info

    def _process_page(self, playlists, user_flag,
                      playlist_idx: List[str],
                      playlist_owners, names, descriptions):
        for playlist in playlists['items']:
            me = self.client.me()['id']
            owner = playlist['owner']['id']
            id = playlist['id']
            playlist_name = playlist['name']
            if 'description' in playlist:
                description = playlist['description']
            else:
                description = None
            if id not in self.redis_data['playlists']:
                playlist_owners[id] = owner
                names[id] = playlist_name
                descriptions[id] = description
                if (user_flag is None):
                    playlist_idx.append(id)

                elif user_flag is True and me == owner:
                    # current user is already in system
                    playlist_idx.append(id)
                elif user_flag is False and owner != me:
                    # other users, need it for my models
                    playlist_idx.append(id)
