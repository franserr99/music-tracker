from typing import Dict, List, Optional, Union, Any
import spotipy
import os
import sys
import requests
import pandas as pd
from dotenv import load_dotenv
from .token_handler import SpotifyTokenHandler
from ..service_dtos import PlaylistsInfo
from ..service_dtos import ImageData, FavoriteTracksInfo, \
    FullAlbumData, FullArtistData, FullTrackData, GenreData, \
    FavoriteArtistsInfo, PlaylistData

scope = "user-library-read user-read-playback-position user-top-read \
user-read-recently-played playlist-read-private"


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


def get_missing_artist_info(missing, token_handler: SpotifyTokenHandler,
                            info: Union[FavoriteTracksInfo, PlaylistsInfo]):
    # chunk size of 50
    chunk_size = 50
    # loop through the missing in increments of 50
    for i in range(0, len(missing), chunk_size):
        # Create a chunk of the list to process
        missing_chunk = missing[i:i + chunk_size]
        # Process each chunk
        get_chunk_of_missing_artists(missing_chunk, token_handler, info)


def get_chunk_of_missing_artists(missing_chunk: List[str],
                                 token_handler: SpotifyTokenHandler,
                                 info: Union[FavoriteTracksInfo, PlaylistsInfo]):
    ids = ','.join(missing_chunk)
    url = f'https://api.spotify.com/v1/artists?ids={ids}'
    res = requests.get(url=url, headers={
        'Authorization': "Bearer"+" "+token_handler.accessToken}
    ).json()
    for artist in res['artists']:
        uri = artist['uri']
        genres = process_genres(info, artist)
        images_urls = get_images_from_arr(
            images=artist['images'], info=info)
        info['artists'][uri]['genres'] = genres
        info['artists'][uri]['image_urls'] = images_urls


def get_artists_df(client: spotipy.Spotify, token_handler: SpotifyTokenHandler,
                   response: dict) -> (FavoriteArtistsInfo, List[str]):
    assert token_handler.accessToken is not None
    info = FavoriteArtistsInfo(artists={}, images={}, genres={})

    missing = []

    for artist in response['items']:
        process_single_artist(artist, info, missing)
    get_missing_artist_info(missing, token_handler, info)
    return info


def get_tracks_df(client: spotipy.Spotify, token_handler: SpotifyTokenHandler,
                  source=None, with_audio=True, playlist_owners=None) -> (Union[FavoriteTracksInfo,
                                                                                PlaylistsInfo],
                                                                          List[str]):
    assert token_handler.accessToken is not None

    info, missing = process_source(
        client, token_handler, source, playlist_owners)
    get_missing_artist_info(missing, token_handler, info)
    return info

    # changing to a df in here
    # user_df = pd.DataFrame(
    #     {'uri': , 'track name': info['track_name'],
    #      'artist': info['track_artist']})
    # user_df.drop_duplicates(inplace=True)
    # user_df.dropna()
    # user_df.reset_index(drop=True, inplace=True)
    # if (with_audio):
    #     user_df_with_features = get_audio_feature_df(client, user_df)
    #     return user_df_with_features
    # else:
    #     return user_df


def paginate_results(tracks: dict, info: Union[FavoriteTracksInfo,
                                               PlaylistsInfo],
                     token_handler: SpotifyTokenHandler, choice):

    access_token = token_handler.accessToken
    assert access_token is not None

    while (tracks['next']):
        tracks = requests.get(tracks['next'], headers={
                              'Authorization': "Bearer"+" "+access_token}
                              ).json()
        if (choice == "t"):
            return get_tracks_info(tracks, "t", info, token_handler)
        elif (choice == "p"):
            return get_tracks_info(tracks, "p", info, token_handler)


def process_source(client: spotipy.Spotify,
                   token_handler: SpotifyTokenHandler, source, playlist_owners) -> \
        Union[FavoriteTracksInfo, PlaylistsInfo]:
    if (source[0] == "p"):
        info = PlaylistsInfo(tracks={}, albums={},
                             artists={}, playlists={}, images={})
        for id in source[1]:
            tracks = client.playlist_tracks(id)
            # i need
            missing, track_uris = get_tracks_info(
                tracks, "p", info, token_handler)
            more_missing, more_track_uris = paginate_results(
                tracks, info,
                token_handler=token_handler,
                choice="p")
            missing.extend(more_missing)
            track_uris.extend(more_track_uris)
            if id not in info['playlists']:
                info['playlists'][id] = PlaylistData(
                    playlist_id=id, owner=playlist_owners[id],
                    tracks=track_uris)
            return info, missing
    elif (source[0] == "t"):
        info = FavoriteTracksInfo(tracks={}, albums={}, artists={},
                                  images={}, genres={})
        missing = get_tracks_info(source[1], "t", info, token_handler)
        if (source[1]['next']):
            missing.extend(paginate_results(source[1], info,
                                            token_handler=token_handler,
                                            choice="t"))
    return info, missing


def get_tracks_info(tracks: dict, choice, info: Union[FavoriteTracksInfo,
                                                      PlaylistsInfo],
                    token_handler: SpotifyTokenHandler):
    missing_artist_info = []
    # recall that structure is like this:
    # items is a list of track objects
    #       where each track has
    #           a list of artist objects
    #           a list of images
    #           an album object
    #               has a list of artist objects
    #               has a list of images
    if (choice == "p"):
        track_uris = []
    for item in tracks['items']:
        # jsons are nested almost exactly the same,
        # adjut for the change here
        if (choice == "p"):
            track = item['track']
            track_uris.append(track['uri'])
        elif (choice == "t"):
            track = item

        # get track info
        track_uri = track['uri']
        track_name = track['name']
        # handle all info in album obj
        album = track['album']
        album_uri = album['uri']
        album_type = album['album_type']
        album_total_tracks = album['total_tracks']
        album_name = album['name']
        album_url = album['external_urls']['spotify']
        # now go into the nested arrays
        track_artists_uri, missing1 = get_entity_artists_info(
            track, info, token_handler)
        missing_artist_info.extend(missing1)
        album_artists_uri, missing2 = get_entity_artists_info(
            album, info, token_handler)
        missing_artist_info.extend(missing2)
        album_image_urls = get_images_from_arr(album['images'], info)

        if track_uri not in info['tracks']:
            info['tracks'][track_uri] = FullTrackData(
                track_uri=track_uri,
                track_name=track_name,
                artist_uri=track_artists_uri,
                album_uri=album_uri)
        if album_uri not in info['albums']:
            info['albums'][album_uri] = FullAlbumData(
                album_uri=album_uri, album_type=album_type,
                total_tracks=album_total_tracks,
                album_name=album_name, url=album_url,
                artists_uri=album_artists_uri,
                image_urls=album_image_urls)
    if choice == "p":
        return missing_artist_info, track_uris
    else:
        return missing_artist_info


def process_genres(info: Union[FavoriteTracksInfo, PlaylistsInfo], artist):
    if 'genres' in artist:
        genres = artist['genres']
        for genre in genres:
            genre_dto = GenreData(name=genre)
            if genre not in info['genres']:
                info['genres'][genre] = genre_dto
        return genres
    else:
        return []


def get_entity_artists_info(entity,
                            info: Union[FavoriteTracksInfo, PlaylistsInfo,
                                        FavoriteArtistsInfo],
                            token_handler: SpotifyTokenHandler):
    entity_artists_uri = []
    missing = []
    for artist in entity['artists']:
        process_single_artist(artist, info, missing, entity_artists_uri)
    return entity_artists_uri, missing


def process_single_artist(artist, info: Union[FavoriteTracksInfo,
                                              PlaylistsInfo,
                                              FavoriteArtistsInfo],
                          missing: List[str],
                          entity_artists_uri: Optional[List[str]] = None):
    artist_uri = artist['uri']
    artist_name = artist['name']
    if (entity_artists_uri):
        entity_artists_uri.append(artist_uri)
    # some of this info is costly to get, only get it if we dont have it
    if artist_uri not in info['artists']:
        genres = process_genres(info, artist)

        if 'images' in artist:
            images_urls = get_images_from_arr(
                images=artist['images'], info=info)
        else:
            images_urls = []

        # fetch more data for the artist + get the images
        if ('images' not in artist or 'genres' not in artist):
            # the better way to do this is having some global list
            # that gets passed back up to a higher level so they can add this logic
            missing.append(artist['id'])
        info['artists'][artist_uri] = FullArtistData(
            artist_uri=artist_uri, genres=genres,
            image_urls=images_urls, name=artist_name)


def get_images_from_arr(images, info: Union[FavoriteTracksInfo,
                                            PlaylistsInfo, FavoriteArtistsInfo]):
    images_urls = []
    for image in images:
        url = image['url']
        height = image['height']
        width = image['width']
        # place at global object
        if url not in info['images']:
            info['images'][url] = (ImageData(url=url, height=height,
                                             width=width))
        # list of uris for the foreign key relationship
        images_urls.append(url)
    return images_urls


def partition_track_ids(track_ids: pd.Series,
                        chunk_size: int = 100) -> List[List[str]]:
    """Break track IDs into chunks of a specified size."""
    return [track_ids[i:i + chunk_size]
            for i in range(0, len(track_ids), chunk_size)]


def get_audio_features_for_tracks(client: spotipy.Spotify, track_id_chunks: List[List[str]]) -> List[Dict[str, Any]]:
    """Fetch audio features for each chunk of track IDs."""
    all_features = []
    for chunk in track_id_chunks:
        chunk_features = client.audio_features(chunk)
        if chunk_features:
            all_features.extend(chunk_features)
    return all_features


def clean_audio_features(features: List[Dict[str, Any]]
                         ) -> List[Dict[str, Any]]:
    """Remove None entries from the list of features."""
    return [feature for feature in features if feature is not None]


def extract_features(features: List[Dict[str, Any]],
                     feature_keys: List[str]) -> List[List[Any]]:
    """Extract specified audio features from the feature data."""
    return [[feature[key] for key in feature_keys] for feature in features]


def create_audio_feature_df(parent_df: pd.DataFrame,
                            features: List[List[Any]],
                            feature_keys: List[str]) -> pd.DataFrame:
    """Create a DataFrame from audio features
    and merge with the parent DataFrame."""
    features_df = pd.DataFrame(features, columns=feature_keys)
    features_df.dropna(inplace=True)
    features_df.reset_index(drop=True, inplace=True)
    # Merge with the parent dataframe
    complete_df = pd.concat([parent_df, features_df], axis=1)
    complete_df.reset_index(drop=True, inplace=True)
    return complete_df


def get_audio_feature_df(client: spotipy.Spotify,
                         parent_df: pd.DataFrame) -> pd.DataFrame:
    """Main function to get audio feature DataFrame."""
    print(parent_df)
    parent_df.reset_index(inplace=True, drop=True)
    track_ids = parent_df['id'][:]

    # Prepare data: break into 100 item chunks
    track_id_chunks = partition_track_ids(track_ids)

    # Fetch and clean audio features
    raw_features = get_audio_features_for_tracks(client, track_id_chunks)
    clean_features = clean_audio_features(raw_features)

    # Get numerical data and extract features
    if clean_features:
        feature_column_names = list(clean_features[0].keys())[:-7]
        songs_audio_features = extract_features(
            clean_features, feature_column_names)

        # Drop tracks that do not have audio features
        eligible_parents = parent_df[~parent_df['id'].isin(
            [f['id'] for f in raw_features if f is None])]
        eligible_parents.dropna(inplace=True)
        eligible_parents.reset_index(drop=True, inplace=True)

        # Check if the tracks and features align
        assert len(eligible_parents['id']) == len(
            songs_audio_features), "Tracks were not dropped correctly."

        # Create the complete DataFrame
        return create_audio_feature_df(eligible_parents,
                                       songs_audio_features,
                                       feature_column_names)
    else:
        # Return an empty DataFrame or raise an error as appropriate
        return pd.DataFrame()


# def get_audio_feature_df(client: spotipy.Spotify, parent_df: pd.DataFrame):
#     print(parent_df)
#     parent_df.reset_index(inplace=True, drop=True)
#     partitioned_list = []
#     trackIDX = parent_df['id'][:]
#     # prep data: break into 100 item chunks
#     for i in range(0, len(trackIDX), 100):
#         partitioned_list.append(trackIDX[i:i+100])
#     all_features = dict(client.audio_features(partitioned_list[0])[0])
#     # print(all_features.keys())
#     # get numerical data
#     feature_column_names = list(all_features.keys())[:-7]
#     # keep a copy to make sure data lines up later
#     # feature_column_names.append('id')
#     songs_audio_features = []
#     # account for songs that dont have audio features
#     all_bad_indices = []
#     # iterate in chunks
#     for k, chunk in enumerate(partitioned_list):
#         features = list(client.audio_features(chunk))
#         assert (len(features) == len(chunk))
#         # clean up data
#         if None in features:
#             bad_indices = []
#             # get indicies of null values
#             for i, v in enumerate(features):
#                 if (v is None):
#                     # account for the partioning
#                     all_bad_indices.append(int(i+((k)*100)))
#                     bad_indices.append(i)
#             # get rid of items in feature list that are null
#             for j in range(len(bad_indices)):
#                 features.pop(bad_indices[j])
#         # removed all nulls by now, dealing with only a list of dictionaries
#         for song_features in features:
#             feats = []
#             for column_name in feature_column_names:
#                 feats.append(song_features[column_name])
#             songs_audio_features.append(feats)
#     eligible_parents = parent_df.drop(index=all_bad_indices)
#     eligible_parents.dropna(inplace=True)
#     eligible_parents.reset_index(inplace=True, drop=True)
#     assert (len(eligible_parents['id'][:]) == len(
#         songs_audio_features)), "tracks were not dropped correctly somewhere"
#     features_df = pd.DataFrame(
#         songs_audio_features, columns=feature_column_names)
#     features_df.dropna(inplace=True)
#     features_df.reset_index(drop=True, inplace=True)
#     complete_df = pd.concat([eligible_parents, features_df], axis=1)
#     complete_df.reset_index(inplace=True, drop=True)
#     return complete_df
