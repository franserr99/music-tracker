from django.db import models
from typing import TypedDict
from datetime import datetime
#spotify track feature
#get description of features here: https://developer.spotify.com/documentation/web-api/reference/get-audio-features
class TrackFeatures(models.Model):
    track = models.OneToOneField(
        'Track', 
        on_delete=models.CASCADE, 
        related_name='features'
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
        db_table='TrackFeatures'
#spotify track
class Track(models.Model):
    uri = models.CharField(max_length=100, primary_key=True, unique=True)
    track_name = models.CharField(max_length=100)
    track_artists = models.CharField(max_length=100)
    class Meta:
        db_table='Track'
#tracks/records when a user listened to a given song
#use: collecting alot of listening data
class History(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)  # Assuming 'User' is another model
    date_recorded = models.DateTimeField()
    relative_term = models.CharField(max_length=30)
    track_uri = models.ForeignKey('Track', on_delete=models.CASCADE)  # Assuming 'Track' is another model
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'relative_term', 'track_uri', 'date_recorded'], name='unique_history')
        ]
        db_table = 'History'
#representing the spotify user
class User(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    liked_tracks=models.ManyToManyField('Track',related_name='liked_by_users')
    class Meta:
        db_table = 'User'
#single user creates a playlist, multiple users can like it, contains multiple tracks
class Playlist(models.Model):
    playlist_id = models.CharField(max_length=50, unique=True,primary_key=True)  
    created_by=models.ForeignKey('User', related_name='playlists_created')
    liked_by = models.ManyToManyField('User', related_name='playlists_added')  
    tracks = models.ManyToManyField('Track', related_name='included_in_playlists') 
