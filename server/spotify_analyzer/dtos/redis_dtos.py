from typing import Set, TypedDict


class RedisData(TypedDict):
    tracks: Set[str]
    playlists: Set[str]
    albums: Set[str]
    artists: Set[str]
