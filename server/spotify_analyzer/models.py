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
    def to_json(self):
        return {
            'uri':self.pk,
            'danceability':self.danceability, 
            'energy':self.energy ,
            'key': self.key,
            'loudness': self.loudness,
            'mode': self.mode,
            'speechiness':self.speechiness,
            'acousticness':self.acousticness,
            'instrumentalness':self.instrumentalness,
            'liveness':self.liveness,
            'valence':self.valence,
            'tempo':self.tempo,
        }
#spotify track
class Track(models.Model):
    uri = models.CharField(max_length=100, primary_key=True, unique=True)
    track_name = models.CharField(max_length=100)
    track_artists = models.CharField(max_length=100)
    class Meta:
        db_table='Track'
    def to_json(self):
        return {
            'uri':self.uri,
            'track_name':self.track_name,
            'track_artists':self.track_artists
        }
#tracks/records when a user listened to a given song
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
    def to_json(self):
        return { 
            'user_id':self.user_id,
            'date_recorded':self.date_recorded,
            'relative_term':self.relative_term,
            'track_uri':self.track_uri,
        }
#representing the spotify user (using that to create this)
class User(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    class Meta:
        db_table = 'User'
    def to_json(self):
        return {
            'id':self.id
        }
#any liked track
class LikedTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track_uri = models.ForeignKey(Track, on_delete=models.CASCADE)
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['user', 'track_uri'], name='unique_liked_track')
    ]
    def to_json(self):
        return { 
            'user_id':self.user,
            'track_uri':self.track_uri,
        }
#can be created by user or a liked playlist in their library by another user
class Playlist(models.Model):
    playlist_id = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['playlist_id','user_id'],name='playlist_track')]
    def to_json(self):
        return { 
            'user_id':self.user_id,
            'track_uri':self.track_uri,
        }
#given playlist track
class PlaylistTrack(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track_uri = models.ForeignKey(Track, on_delete=models.CASCADE)

    class Meta:
        constraints=[models.UniqueConstraint(fields=['playlist_id','track_uri'],name='playlist_track')]
    def to_json(self):
        return { 
            'playlist_id':self.playlist_id,
            'track_uri':self.track_uri,
        }


    
