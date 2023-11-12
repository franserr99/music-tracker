import redis
import logging
from typing import List, TypedDict, Set
from .services_util import init_core_services
from ..services.core.track_service import TrackService
from ..services.core.album_service import AlbumService
from ..services.core.playlist_service import PlaylistService
from ..services.core.artist_service import ArtistService


def get_redis_instance() -> redis.Redis:
    try:
        # Create a new Redis client instance
        r = redis.Redis(host='localhost', port=6379, db=0)
        return r
    except Exception:
        print("erre when trying to create the redis instance")
        return None


def from_db_to_redis() -> bool:
    r = get_redis_instance()
    if r is not None:
        app_name = 'spotify_analyzer'
        logger = logging.getLogger(app_name)
        services = init_core_services(logger=logger)
        stored_albums_to_redis(services['album_service'], r)
        stored_artists_to_redis(services['artist_service'], r)
        stored_playlists_to_redis(services['playlist_service'], r)
        stored_tracks_to_redis(services['track_service'], r)
        return True
    else:
        return False


def stored_tracks_to_redis(track_service: TrackService, client: redis.Redis):
    all_track_uris = track_service.get_all_identifiers()
    add_to_redis_in_batches(client, 'existing_track_uris', all_track_uris)


def stored_artists_to_redis(artist_service: ArtistService,
                            client: redis.Redis):
    all_artists_uris = artist_service.get_all_identifiers()
    add_to_redis_in_batches(client, 'existing_artist_uris', all_artists_uris)


def stored_albums_to_redis(album_service: AlbumService, client: redis.Redis):
    all_album_uris = album_service.get_all_identifiers()
    add_to_redis_in_batches(client, 'existing_album_uris', all_album_uris)


def stored_playlists_to_redis(playlist_service: PlaylistService,
                              client: redis.Redis):
    all_playlists_ids = playlist_service.get_all_identifiers()
    add_to_redis_in_batches(client, 'existing_playlist_ids', all_playlists_ids)


def add_to_redis_in_batches(redis_client, key, items, batch_size=8000):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        redis_client.sadd(key, *batch)


def add_tracks_to_redis(track_uris: List[str], r: redis.Redis):
    if r is not None:
        add_to_redis_in_batches(r, 'existing_track_uris', track_uris)


def add_artists_to_redis(artist_uris: List[str], r: redis.Redis):
    if r is not None:
        add_to_redis_in_batches(r, 'existing_artist_uris', artist_uris)


def add_albums_to_redis(album_uris,  r: redis.Redis):
    if r is not None:
        add_to_redis_in_batches(r, 'existing_album_uris', album_uris)


def add_playlists_to_redis(playlist_ids: List[str],  r: redis.Redis):
    if r is not None:
        add_to_redis_in_batches(r, 'existing_playlist_ids', playlist_ids)
    pass


def get_data_from_redis(r: redis.Redis):
    # Retrieve data
    track_uris = r.smembers('existing_track_uris')
    track_uris = {uri.decode('utf-8') for uri in track_uris}

    playlist_ids = r.smembers('existing_playlist_ids')
    playlist_ids = {id.decode('utf-8') for id in playlist_ids}

    album_uris = r.smembers('existing_album_uris')
    album_uris = {uri.decode('utf-8') for uri in album_uris}

    artist_uris = r.smembers('existing_artist_uris')
    artist_uris = {uri.decode('utf-8') for uri in artist_uris}
    return RedisData(
        tracks=track_uris, playlists=playlist_ids,
        albums=album_uris, artists=artist_uris
    )


class RedisData(TypedDict):
    tracks: Set[str]
    playlists: Set[str]
    albums: Set[str]
    artists: Set[str]
