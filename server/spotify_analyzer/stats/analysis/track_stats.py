from ...dtos.retrieval_dtos import TrackFeaturesData
from ...models import Track, Artist
from django.db.models import Prefetch


def map_acousticness(value):
    if 0.0 <= value < 0.3:
        return "Not Acoustic"
    elif 0.3 <= value < 0.6:
        return "Moderately Acoustic"
    else:
        return "Highly Acoustic"


def map_danceability(value):
    if 0.0 <= value < 0.3:
        return "Low Danceability"
    elif 0.3 <= value < 0.6:
        return "Moderately Danceable"
    else:
        return "Highly Danceable"


def map_energy(value):
    if 0.0 <= value < 0.3:
        return "Low Energy"
    elif 0.3 <= value < 0.6:
        return "Moderate Energy"
    else:
        return "High Energy"


def map_instrumentalness(value):
    if 0.0 <= value < 0.5:
        return "Likely Vocal"
    else:
        return "Likely Instrumental"


def map_valence(value):
    if 0.0 <= value < 0.3:
        return "Low Positivity" or "More Melancholic"
    elif 0.3 <= value < 0.6:
        return "Neutral"
    else:
        return "High Positivity" or "Cheerful"


def map_tempo(bpm):
    if bpm < 60:
        return "Very Slow"
    elif 60 <= bpm < 90:
        return "Slow"
    elif 90 <= bpm < 120:
        return "Moderate"
    elif 120 <= bpm < 150:
        return "Fast"
    else:
        return "Very Fast"


def map_speechiness(value):
    if value < 0.33:
        return "Music or Non-Speech"
    elif 0.33 <= value < 0.66:
        return "Mixed Music and Speech"
    else:
        return "Spoken Words"


def interpret_loudness(db):
    if db < -30:
        return "Very Quiet"
    elif -30 <= db < -15:
        return "Quiet"
    elif -15 <= db < -5:
        return "Moderate"
    elif -5 <= db < 0:
        return "Loud"
    else:
        return "Very Loud"


def get_features_descriptions(features: TrackFeaturesData):
    track_descriptions = {
        'acousticness': map_acousticness(features['acousticness']),
        'danceability': map_danceability(features['danceability']),
        'energy': map_energy(features['energy']),
        'instrumentalness': map_instrumentalness(features['instrumentalness']),
        'valence': map_valence(features['valence']),
        'tempo': map_tempo(features['tempo']),
        'speechiness': map_speechiness(features['speechiness']),
        'loudness': interpret_loudness(features['loudness'])
    }
    return track_descriptions


def get_genres_for_track(track_id):
    # Fetch the track with prefetched artists and their genres
    track = Track.objects.prefetch_related(
        Prefetch(
            'track_artists',
            queryset=Artist.objects.prefetch_related('genres')
        )
    ).get(uri=track_id)

    # Extracting genres for each artist
    artist_genres = {}
    for artist in track.track_artists.all():
        genres = [genre.name for genre in artist.genres.all()]
        artist_genres[artist.name] = genres

    return artist_genres
