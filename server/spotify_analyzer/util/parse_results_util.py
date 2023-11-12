
from typing import List, Optional, Tuple, Union
import requests
import spotipy
from ..services.dtos.retrieval_dtos import FavoriteArtistsInfo, \
    FavoriteTracksInfo, PlaylistsInfo, ImageData, FullAlbumData, \
    FullArtistData, FullTrackData, GenreData, UserData, \
    FullPlaylistData
from ..services.spotify.token_handler import SpotifyTokenHandler
from .redis_util import RedisData, get_data_from_redis, get_redis_instance
scope = "user-library-read user-read-playback-position user-top-read \
user-read-recently-played playlist-read-private"
# recall that structure is like this:
# items is a list of track objects
#       where each track has
#           a list of artist objects
#           a list of images
#           an album object
#               has a list of artist objects
#               has a list of images


def get_tracks_info(tracks: dict, choice, info: Union[FavoriteTracksInfo,
                                                      PlaylistsInfo],
                    token_handler: SpotifyTokenHandler):
    missing_artist_info = []

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
        # assert (len(track_artists_uri) != 0)

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
        process_single_artist(artist=artist,
                              info=info,
                              missing=missing,
                              entity_artists_uri=entity_artists_uri)
    return entity_artists_uri, missing


def process_single_artist(artist, info: Union[FavoriteTracksInfo,
                                              PlaylistsInfo,
                                              FavoriteArtistsInfo],
                          missing: List[str],
                          entity_artists_uri: Optional[List[str]] = None):
    artist_uri = artist['uri']
    artist_name = artist['name']

    if (entity_artists_uri is not None):
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
            # that gets passed back up to a higher level
            #  so they can add this logic
            missing.append(artist['id'])
        info['artists'][artist_uri] = FullArtistData(
            artist_uri=artist_uri, genres=genres,
            image_urls=images_urls, name=artist_name)


def get_images_from_arr(images, info: Union[FavoriteTracksInfo,
                                            PlaylistsInfo,
                                            FavoriteArtistsInfo]):
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


def get_missing_artist_info(missing, token_handler: SpotifyTokenHandler,
                            info: Union[FavoriteTracksInfo,
                                        PlaylistsInfo,
                                        FavoriteArtistsInfo]):
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
                                 info: Union[FavoriteTracksInfo,
                                             PlaylistsInfo]):
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
                   response: dict) -> Tuple[FavoriteArtistsInfo, List[str]]:
    assert token_handler.accessToken is not None
    info = FavoriteArtistsInfo(artists={}, images={}, genres={})
    missing = []
    for artist in response['items']:
        process_single_artist(artist, info, missing)
    get_missing_artist_info(missing, token_handler, info)
    return info


def get_owner_dtos(owners: dict) -> List[UserData]:
    unique_owner_ids = list(set(owners.values()))
    owner_dtos = [UserData(id=id) for id in unique_owner_ids]
    return owner_dtos


def get_tracks(client: spotipy.Spotify,
               token_handler: SpotifyTokenHandler,
               source=None, with_audio=True,
               playlist_owners=None) -> Union[FavoriteTracksInfo,
                                              PlaylistsInfo]:
    assert token_handler.accessToken is not None

    info, missing = process_source(
        client, token_handler, source, playlist_owners)
    get_missing_artist_info(missing, token_handler, info)
    return info


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
                   token_handler: SpotifyTokenHandler,
                   source, playlist_owners) -> \
        Union[FavoriteTracksInfo, PlaylistsInfo]:
    choice = source[0]
    playlists = source[1]
    print(playlists)
    if (choice == "p"):
        info = PlaylistsInfo(tracks={}, albums={},
                             artists={}, playlists={},
                             images={}, users={}, genres={})
        for playlist_id in playlists:
            tracks = client.playlist_tracks(playlist_id=playlist_id)
            missing, track_uris = get_tracks_info(
                tracks, "p", info, token_handler)
            if tracks['next']:
                more_missing, more_track_uris = paginate_results(
                    tracks, info,
                    token_handler=token_handler,
                    choice="p")
                missing.extend(more_missing)
                track_uris.extend(more_track_uris)
            # add the playlists
            print("id of playlist we might add: ", playlist_id)
            print("current state of the dict: \n", info['playlists'])
            if playlist_id not in info['playlists'].keys():
                info['playlists'][playlist_id] = FullPlaylistData(
                    playlist_id=playlist_id,
                    created_by=playlist_owners[playlist_id],
                    tracks=track_uris
                )
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
