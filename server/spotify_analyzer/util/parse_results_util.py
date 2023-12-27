
from typing import List, Optional, Tuple, Union
import requests
import spotipy
from ..dtos.retrieval_dtos import FavoriteArtistsInfo, \
    FavoriteTracksInfo, PlaylistsInfo, ImageData, FullAlbumData, \
    FullArtistData, FullTrackData, GenreData, UserData, \
    FullPlaylistData
from ..services.spotify.token_handler import SpotifyTokenHandler
from ..dtos.redis_dtos import RedisData
scope = "user-library-read user-read-playback-position user-top-read \
user-read-recently-played playlist-read-private"


def get_tracks(client: spotipy.Spotify,
               token_handler: SpotifyTokenHandler, redis_data: RedisData,
               source=None, with_audio=True,
               playlist_owners=None,
               names=None, descriptions=None) -> Union[FavoriteTracksInfo,
                                                       PlaylistsInfo]:
    assert token_handler.accessToken is not None
    results = process_source(
        client, token_handler, source, playlist_owners,
        redis_data, names, descriptions)
    if (results is None):
        print("nothing more to add")
        return None
    info = results[0]
    missing = results[1]
    get_missing_artist_info(missing, token_handler, info)
    return info


def process_source(client: spotipy.Spotify,
                   token_handler: SpotifyTokenHandler,
                   source, playlist_owners,
                   redis_data: RedisData,
                   names=None, descriptions=None) -> \
        Tuple[Union[FavoriteTracksInfo, PlaylistsInfo], List[str]]:
    choice = source[0]

    if (len(source[1]) == 0):
        return None
    # print(playlists)
    if (choice == "p"):
        playlists = source[1]
        info = PlaylistsInfo(tracks={}, albums={},
                             artists={}, playlists={},
                             images={}, users={}, genres={})
        missing = []
        for playlist_id in playlists:
            tracks = client.playlist_tracks(playlist_id=playlist_id)
            missing1, track_uris = get_tracks_info(
                tracks, choice, info, token_handler, redis_data)
            # paginate if needed
            # print("missing after going through processing", missing)
            missing.extend(missing1)
            if tracks['next']:
                more_missing, more_track_uris = paginate_results(
                    tracks, info,
                    token_handler=token_handler,
                    choice=choice, redis_data=redis_data)
                missing.extend(more_missing)
                track_uris.extend(more_track_uris)
            # add playlist to info we got

            if playlist_id not in info['playlists'].keys():
                info['playlists'][playlist_id] = FullPlaylistData(
                    playlist_id=playlist_id,
                    created_by=playlist_owners[playlist_id],
                    tracks=track_uris, name=names[playlist_id],
                    description=descriptions[playlist_id]
                )
    elif (choice == "t"):
        info = FavoriteTracksInfo(tracks={}, albums={}, artists={},
                                  images={}, genres={})
        missing = get_tracks_info(source[1], choice, info, token_handler,
                                  redis_data=redis_data)
        if (source[1]['next']):
            missing.extend(paginate_results(source[1],
                                            info,
                                            token_handler=token_handler,
                                            choice="t",
                                            redis_data=redis_data))
    return info, missing


def get_tracks_info(tracks: dict, choice: str, info: Union[FavoriteTracksInfo,
                                                           PlaylistsInfo],
                    token_handler: SpotifyTokenHandler, redis_data: RedisData):
    missing_artist_info = []

    if (choice == "p"):
        track_uris = []
    for item in tracks['items']:
        if (choice == "p"):
            track = item['track']
        elif (choice == "t"):
            track = item

        track_uri = track['uri']
        # get track info
        if track_uri is not None and track_uri not in redis_data['tracks']:
            track_name = track['name']
            # handle all info in album obj

            album = track['album']
            album_uri = album['uri']
            if album_uri is not None:

                if (choice == "p"):
                    track_uris.append(track['uri'])

                album_type = album['album_type']
                # print(album)
                album_total_tracks = album['total_tracks']
                album_name = album['name']
                album_url = album['external_urls']['spotify']
                album_artists_uri, missing2 = get_entity_artists_info(
                    album, info, token_handler, redis_data)
                assert (len(album_artists_uri) > 0), \
                    "an album needs to have an artist on it"
                missing_artist_info.extend(missing2)
                album_image_urls = get_images_from_arr(album['images'], info)
                if album_uri not in redis_data['albums'] and \
                        album_uri not in info['albums']:
                    info['albums'][album_uri] = FullAlbumData(
                        album_uri=album_uri, album_type=album_type,
                        total_tracks=album_total_tracks,
                        album_name=album_name, url=album_url,
                        artists_uri=album_artists_uri,
                        image_urls=album_image_urls)

                track_artists_uri, missing1 = get_entity_artists_info(
                    track, info, token_handler, redis_data)
                missing_artist_info.extend(missing1)

                if (track_uri not in info['tracks']):
                    info['tracks'][track_uri] = FullTrackData(
                        track_uri=track_uri,
                        track_name=track_name,
                        artist_uri=track_artists_uri,
                        album_uri=album_uri)

    if choice == "p":
        # print(missing_artist_info)
        return missing_artist_info, track_uris
    else:
        return missing_artist_info


def paginate_results(tracks: dict, info: Union[FavoriteTracksInfo,
                                               PlaylistsInfo],
                     token_handler: SpotifyTokenHandler,
                     choice, redis_data: RedisData):

    access_token = token_handler.accessToken
    assert access_token is not None

    while (tracks['next']):
        tracks = requests.get(tracks['next'], headers={
                              'Authorization': "Bearer"+" "+access_token}
                              ).json()
        if (choice == "t"):
            return get_tracks_info(tracks, "t", info,
                                   token_handler, redis_data)
        elif (choice == "p"):
            return get_tracks_info(tracks, "p", info,
                                   token_handler, redis_data)


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
                            token_handler: SpotifyTokenHandler,
                            redis_data: RedisData):
    entity_artists_uri = []
    missing = []
    for artist in entity['artists']:
        if artist['uri'] not in info['artists']:
            # print(artist['name'],
            #       " not in our info object, going to process it ")
            process_single_artist(artist=artist, redis_data=redis_data,
                                  info=info,
                                  missing=missing,
                                  entity_artists_uri=entity_artists_uri)
        else:
            entity_artists_uri.append(artist['uri'])
    return entity_artists_uri, missing


def process_single_artist(artist, redis_data: RedisData,
                          info: Union[FavoriteTracksInfo,
                                      PlaylistsInfo,
                                      FavoriteArtistsInfo],
                          missing: List[str],
                          entity_artists_uri: Optional[List[str]] = None):
    artist_uri = artist['uri']
    artist_name = artist['name']

    if (entity_artists_uri is not None):
        entity_artists_uri.append(artist_uri)
    # some of this info is costly to get, only get it if we dont have it
    # duplicated check but done for other callers
    if artist_uri not in info['artists'] and \
            artist['uri'] not in redis_data['artists']:
        # print("not in cache and checked again it was not in info dict")
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
            print("getting added to missin, ", artist['id'])
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
                   response: dict, redis_data: RedisData) \
        -> Tuple[FavoriteArtistsInfo, List[str]]:
    assert token_handler.accessToken is not None
    info = FavoriteArtistsInfo(artists={}, images={}, genres={})
    missing = []
    for artist in response['items']:
        if artist['uri'] not in redis_data['artists']:
            process_single_artist(artist, info, missing)
    get_missing_artist_info(missing, token_handler, info)
    return info


def get_owner_dtos(owners: dict) -> List[UserData]:
    unique_owner_ids = list(set(owners.values()))
    owner_dtos = [UserData(id=id) for id in unique_owner_ids]
    return owner_dtos
