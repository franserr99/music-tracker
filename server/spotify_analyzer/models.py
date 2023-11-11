"""
models.py
=========

This Django module contains the models used in a Spotify-like application.
It includes representations for tracks, track features, user history,
users, and playlists.

Classes:
    - TrackFeatures: Holds feature information for a specific track.
    - Track: Represents a Spotify track.
    - History: Records when a user listens to a given song.
    - User: Represents a Spotify user.
    - Playlist: Represents a Spotify playlist.
"""
from django.db import models
from django.core.exceptions import ValidationError
# spotify track feature
# get description of features here:
# https://developer.spotify.com/documentation/web-api/reference/get-audio-features


class TrackFeatures(models.Model):
    """
    This class represents various features of a track in Spotify.

    Attributes:
        - track: Foreign key linking to the corresponding Track model.
        - danceability: Indicates how suitable a track is for dancing.
        - energy: Measures a track's energy.
        ...
    """
    track = models.OneToOneField(
        'Track',
        on_delete=models.CASCADE,
        related_name='features',
        primary_key=True
    )
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.FloatField()
    loudness = models.FloatField()
    mode = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()

    class Meta:
        """
        Meta class for TrackFeatures.

        Attributes:
            db_table: Specifies the name of the database table.
        """
        db_table = 'TrackFeatures'


class Album(models.Model):
    uri = models.CharField(max_length=150, primary_key=True)
    name = models.TextField(null=True)
    artists = models.ManyToManyField('Artist', related_name='album_catalogue')
    tracks = models.ManyToManyField('Track', related_name='appears_in')
    album_type = models.CharField(max_length=150, null=True)
    total_tracks = models.IntegerField(null=True)
    url = models.TextField(null=True)


class Artist (models.Model):
    uri = models.CharField(max_length=150, primary_key=True)
    name = models.CharField(max_length=70)
    genres = models.ManyToManyField('Genre', related_name='member_artists')


class Genre(models.Model):
    name = models.CharField(max_length=120, primary_key=True)


class Image(models.Model):
    url = models.TextField(primary_key=True)
    height = models.IntegerField()
    width = models.IntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE,
                               related_name='artist_images',
                               null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE,
                              related_name='album_images',
                              null=True, blank=True)

    # def clean(self):
    #     # Check that the Image instance is linked to
    #     #  either an artist or an album, not both.
    #     if self.artist_id and self.album_id:
    #         raise ValidationError(
    #             'Image cannot be linked to an artist && album.'
    #         )
    #     # if not self.artist_id and not self.album_id:
    #     #     raise ValidationError(
    #     #         'An image must be linked to an artist or an album.'
    #     #     )

    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args, **kwargs)


# the artist image alone is not enough,
#  i need the album image for context as well
class Track(models.Model):
    """
    This class represents a Track in the Spotify application.

    Attributes:
        - uri: The unique identifier for the track.
        - track_name: The name of the track.
        - track_artists: The artist(s) who performed the track.
    """
    uri = models.CharField(max_length=100, primary_key=True, unique=True)
    track_name = models.CharField(max_length=100)
    track_artists = models.ManyToManyField('Artist',
                                           related_name='track_catalogue')

    class Meta:
        """
        Meta class for Track.

        Attributes:
            db_table: Specifies the name of the database table.
        """
        db_table = 'Track'

# tracks/records when a user listened to a given song
# use: collecting alot of listening data


class History(models.Model):
    """
    This class is used for collecting a lot of listening data from users.

    Attributes:
        - user_id: The ID of the user who has the history.
        - date_recorded: The date and time the history was recorded.
        - relative_term: Some sort of term to relate to.
        - track_uri: The URI of the track in the history.
    """
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='listening_history')
    date_recorded = models.DateTimeField()
    relative_term = models.CharField(max_length=30)
    track = models.ForeignKey(
        'Track', on_delete=models.CASCADE, related_name='user_history')

    class Meta:
        """
        Meta class for History.

        Attributes:
            db_table: Specifies the name of the database table.
            constraints: Specifies database constraints.
        """
        constraints = [
            models.UniqueConstraint(fields=['user', 'relative_term',
                                            'track', 'date_recorded'],
                                    name='unique_history')
        ]
        db_table = 'History'
# representing the spotify user


class User(models.Model):
    """
    This class represents a Spotify user.

    Attributes:
        - id: The unique identifier for the user.
        - liked_tracks: The tracks that the user has liked.
    """
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    user_name = models.CharField(max_length=100, null=True)
    expires_at = models.IntegerField(null=True)
    refresh_token = models.CharField(max_length=250, null=True)
    access_token = models.CharField(max_length=250, null=True)
    liked_tracks = models.ManyToManyField(
        'Track', related_name='users_liked')

    class Meta:
        """
        Meta class for User.

        Attributes:
            db_table: Specifies the name of the database table.
        """
        db_table = 'User'
# single user creates a playlist,
#  multiple users can like it,
# contains multiple tracks


class Playlist(models.Model):
    """
    This class represents a playlist in the Spotify application.

    Attributes:
        - playlist_id: The unique identifier for the playlist.
        - created_by: The user who created the playlist.
        - liked_by: The users who have liked the playlist.
        - tracks: The tracks included in the playlist.
    """
    id = models.CharField(
        max_length=100, unique=True, primary_key=True)
    created_by = models.ForeignKey(
        'User', related_name='my_playlists', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField('User', related_name='liked_playlists')
    tracks = models.ManyToManyField(
        'Track', related_name='playlist_appearances')

    class Meta:
        """
        Meta class for Playlist.

        Attributes:
            db_table: Specifies the name of the database table.
        """
        db_table = 'Playlist'
