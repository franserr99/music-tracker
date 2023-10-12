from rest_framework import serializers

from .models import TrackFeatures, Track, History, User, Playlist  # Adjust the import based on your project structure


class TrackFeaturesOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackFeatures
        fields = '__all__'
class TrackOutputSerializer(serializers.ModelSerializer):
    features = TrackFeaturesOutputSerializer(read_only=True, source='features')
    class Meta:
        model = Track
        fields = ['uri', 'track_name', 'track_artists', 'features']
# For input
class TrackInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['uri', 'track_name', 'track_artists']
class HistoryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'  
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  
class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = '__all__'  
# class PlaylistTrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PlaylistTrack
#         fields = '__all__'  
# class LikedTrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LikedTrack
#         fields = '__all__'  
