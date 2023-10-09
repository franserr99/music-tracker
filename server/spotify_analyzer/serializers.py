from rest_framework import serializers
from .models import TrackFeatures, Track, History, User, LikedTrack, Playlist, PlaylistTrack  # Adjust the import based on your project structure

from rest_framework import serializers
from .models import TrackFeatures, Track  # Adjust the import based on your project structure

class TrackFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackFeatures
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    features = TrackFeaturesSerializer(read_only=True, source='features')  # 'features' is the related_name in your model

    class Meta:
        model = Track
        fields = ['uri', 'track_name', 'track_artists', 'features']  # Added 'features'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  

class LikedTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedTrack
        fields = '__all__'  

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'  

class PlaylistTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistTrack
        fields = '__all__'  
