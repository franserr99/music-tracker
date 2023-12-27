from django.db.models import Prefetch
from ...models import Album, Artist, Genre


def get_genres_for_album_artists(album_uri):
    # Fetch the album with prefetched artists and their genres
    album = Album.objects.prefetch_related(
        Prefetch(
            'artists',
            queryset=Artist.objects.prefetch_related(
                Prefetch(
                    'genres',
                    queryset=Genre.objects.values_list('name', flat=True)
                )
            )
        )
    ).get(uri=album_uri)

    # Extracting genres for each artist
    artist_genres = {}
    for artist in album.artists.all():
        # This will be a list of genre names
        genre_names = list(artist.genres.all())
        artist_genres[artist.name] = genre_names

    return artist_genres

