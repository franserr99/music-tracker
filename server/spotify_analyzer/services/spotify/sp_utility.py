import spotipy
import os
import sys
import requests
import pandas as pd
from dotenv import load_dotenv
from .spotify_token_handler import SpotifyTokenHandler
from ...services.service_dtos import ImageData, FavoriteItemsInfo
scope = "user-library-read user-read-playback-position user-top-read \
user-read-recently-played playlist-read-private"

# TODO
# def welcome_user(engine: sqlalchemy.engine.Engine, client:spotipy.Spotify):
#    spotipy_id=client.me()['id']
#    db_sp_id=db_util.user_util.user_id_list(engine=engine)
#    if spotipy_id not in db_sp_id:
#        db_util.user_util.create_user(spotipy_id, engine)


def setup():
    if (os.getenv("SPOTIPY_CLIENT_SECRET") and
        os.getenv("SPOTIPY_CLIENT_ID") and
            os.getenv("SPOTIPY_REDIRECT_URI")):
        return
    load_dotenv("sp.env")
    try:
        # load_dotenv should load env var,
        # now just check they exist in the enviorment
        os.environ["SPOTIPY_CLIENT_SECRET"]
        os.environ['SPOTIPY_CLIENT_ID']
        os.environ["SPOTIPY_REDIRECT_URI"]
    except Exception:
        print("one of these were not set as an enviormental variable")
        # use this instead of exit() bc it speaks to interpreter
        sys.exit(1)


def get_tracks(client: spotipy.Spotify, token_handler: SpotifyTokenHandler,
               source=None, with_audio=True):
    assert token_handler.accessToken is not None

    info = process_source(
        client, token_handler, source)

    # changing to a df in here
    user_df = pd.DataFrame(
        {'uri': info[''], 'track name': user_tracks_names,
         'artist': user_track_artists})
    user_df.drop_duplicates(inplace=True)
    user_df.dropna()
    user_df.reset_index(drop=True, inplace=True)
    if (with_audio):
        user_df_with_features = get_audio_feature_df(client, user_df)
        return user_df_with_features
    else:
        return user_df


def paginate_results(tracks: dict, info: FavoriteItemsInfo,
                     token_handler: SpotifyTokenHandler, choice):

    access_token = token_handler.accessToken
    assert access_token is not None

    while (tracks['next']):
        tracks = requests.get(tracks['next'], headers={
                              'Authorization': "Bearer"+" "+access_token}
                              ).json()
        if (choice == "t"):
            get_tracks_info(tracks, "t", info)
        elif (choice == "p"):
            get_tracks_info(tracks, "p", info)


def process_source(client: spotipy.Spotify,
                   token_handler: SpotifyTokenHandler, source):
    # init dict with all our arrays
    info = FavoriteItemsInfo(track_uris=[], track_name=[],
                             track_artist=[], track_album_uri=[],
                             track_album_type=[], album_num_of_tracks=[],
                             album_images=[])

    if (source[0] == "p"):
        for id in source[1]:
            # keep track of counts to make sure it lines up later
            before_counts = get_counts(info)
            # get first page of tracks
            tracks = client.playlist_tracks(id)
            get_tracks_info(tracks, "p", info)
            # page if needed
            paginate_results(tracks, info,
                             token_handler=token_handler, choice="p")
            # count check
            after_counts = get_counts(info)
            assert_count_after_pagination(before_counts, after_counts, 
                                          tracks['total'])
    elif (source[0] == "t"):
        tracks = get_tracks_info(source[1], "t", info)
        if (source[1]['next']):
            paginate_results(source[1], info,
                             token_handler=token_handler, choice="t")
    return info


def assert_count_after_pagination(before_counts, after_counts, expected_total):
    for prior_count, after_count in zip(before_counts.values(), after_counts.values()):
        assert expected_total == after_count-prior_count
def assert_count_uniformity(count:dict):
    for 


def get_counts(info):
    counts = []
    for arr in info.values():
        counts.append(len(arr))
    return counts


def get_tracks_info(tracks: dict, choice, info: FavoriteItemsInfo):
    for item in tracks['items']:
        if (choice == "p"):
            info['track_uris'].append(item['track']['uri'])
            info['track_name'].append(item['track']['name'])
            # get first artist associated with the song in the json obj
            info['track_artist'].append(item['track']['artists'][0]['name'])
        elif (choice == "t"):
            # different json structure
            # this is for top monthly tracks
            info['track_uris'].append(item['uri'])
            info['track_name'].append(item['name'])
            info['track_artist'].append(item['artists'][0]['name'])
    assert (len(tracks_URI) == len(tracks_name) == len(artists_name))
    return tracks_URI, tracks_name, artists_name


def get_audio_feature_df(client: spotipy.Spotify, parent_df: pd.DataFrame):
    print(parent_df)
    parent_df.reset_index(inplace=True, drop=True)
    partitioned_list = []
    trackIDX = parent_df['id'][:]
    # prep data: break into 100 item chunks
    for i in range(0, len(trackIDX), 100):
        partitioned_list.append(trackIDX[i:i+100])
    all_features = dict(client.audio_features(partitioned_list[0])[0])
    # print(all_features.keys())
    # get numerical data
    feature_column_names = list(all_features.keys())[:-7]
    # keep a copy to make sure data lines up later
    # feature_column_names.append('id')
    songs_audio_features = []
    # account for songs that dont have audio features
    all_bad_indices = []
    # iterate in chunks
    for k, chunk in enumerate(partitioned_list):
        features = list(client.audio_features(chunk))
        assert (len(features) == len(chunk))
        # clean up data
        if None in features:
            bad_indices = []
            # get indicies of null values
            for i, v in enumerate(features):
                if (v is None):
                    # account for the partioning
                    all_bad_indices.append(int(i+((k)*100)))
                    bad_indices.append(i)
            # get rid of items in feature list that are null
            for j in range(len(bad_indices)):
                features.pop(bad_indices[j])
        # removed all nulls by now, dealing with only a list of dictionaries
        for song_features in features:
            feats = []
            for column_name in feature_column_names:
                feats.append(song_features[column_name])
            songs_audio_features.append(feats)
    eligible_parents = parent_df.drop(index=all_bad_indices)
    eligible_parents.dropna(inplace=True)
    eligible_parents.reset_index(inplace=True, drop=True)
    assert (len(eligible_parents['id'][:]) == len(
        songs_audio_features)), "tracks were not dropped correctly somewhere"
    features_df = pd.DataFrame(
        songs_audio_features, columns=feature_column_names)
    features_df.dropna(inplace=True)
    features_df.reset_index(drop=True, inplace=True)
    complete_df = pd.concat([eligible_parents, features_df], axis=1)
    complete_df.reset_index(inplace=True, drop=True)
    return complete_df
