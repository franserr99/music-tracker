
from ...models import Playlist
from typing import List, TypedDict, Dict
import math


def playlist_genres(playlist_id: str, genres=None) -> dict:
    try:
        playlist = Playlist.objects.prefetch_related(
            'tracks__track_artists__genres'
        ).get(id=playlist_id)
        if genres is None:
            genres = {}
        for track in playlist.tracks.all():
            for artist in track.track_artists.all():
                for genre in artist.genres.all():
                    genres[genre.name] = genres.get(genre.name, 0) + 1
        return genres

    except Playlist.DoesNotExist:
        print(f"Playlist with ID {playlist_id} does not exist.")
        return {}


def topNGenresInCommon(playlists: List[str], top_n=3):
    playlist_genre_counts = []

    # get the counts of genres over all playlists
    for playlist in playlists:
        playlist_genre_counts.append(playlist_genres(playlist))
    # if not empty
    if playlist_genre_counts:
        # init to first one
        common_genres = set(dict(playlist_genre_counts[0]).keys())
        for genre_counts in playlist_genre_counts:
            common_genres &= set(genre_counts.keys())

        # to keep track of overall frequency
        total_genre_counts = {}
        # genre_counts is the json containg the key value pairs
        for genre_counts in playlist_genre_counts:
            for genre in common_genres:
                if genre not in total_genre_counts:
                    total_genre_counts[genre] = genre_counts[genre]
                else:
                    total_genre_counts[genre] += genre_counts[genre]

        # select top N genres based on aggregated frequencies
        top_genres = sorted(total_genre_counts,
                            key=total_genre_counts.get, reverse=True)[:top_n]
        results = []
        for playlist_id, genre_counts in zip(playlists, playlist_genre_counts):
            result = {}
            result['playlist_id'] = playlist_id
            
            for genre in top_genres:
                if genre in genre_counts:
                    result[genre] = genre_counts[genre]
                else:
                    result[genre] = 0
            results.append(result)
    return results


def all_playlist_genres(playlists: List[str]):
    genres = {}
    for playlist in playlists:
        playlist_genres(playlist, genres)
    return genres


def compare_two_playlists(playlist1: str, playlist2: str):
    a = playlist1
    b = playlist2

    playlist1_genres = playlist_genres(playlist_id=playlist1)
    playlist2_genres = playlist_genres(playlist_id=playlist2)

    unique_a = uniqueGenres(a, b)
    unique_b = uniqueGenres(b, a)

    a_diversity_score = calculate_genre_diversity_score(a)
    b_diversity_score = calculate_genre_diversity_score(b)


#  unique genres in a not found in b
def commonGenres(a: dict, b: dict):
    a_set = set(a.keys())
    b_set = set(b.keys())
    return list(a_set & b_set)


def uniqueGenres(a: dict, b: dict):
    a_set = set(a.keys())
    b_set = set(b.keys())
    return list(a_set-b_set)


def calculate_genre_diversity_score(playlist):
    total_songs = sum(playlist.values())
    entropy = 0

    for genre_count in playlist.values():
        p = genre_count / total_songs
        entropy -= p * math.log(p, 2)  # Using log base 2

    return entropy


def dominantGenre(playlist: dict):
    max_count = 0
    max_genre = None
    for genre, count in playlist.items():
        if count > max_count:
            max_count = count
            max_genre = genre
    return max_genre


def topNGenres(playlist: dict, n: int = 3):
    # sort the playlist items by count in descending order
    sorted_genres = sorted(playlist.items(), key=lambda x: x[1], reverse=True)

    # get the top n genres
    top_n_genres = dict(sorted_genres[:n])

    return top_n_genres


class PlaylistComparison(TypedDict):
    a_genres: Dict[str, int]
    b_genres: Dict[str, int]

    a_unique: List[str]
    b_unique: List[str]
