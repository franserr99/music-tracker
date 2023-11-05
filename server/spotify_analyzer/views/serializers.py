"""_summary_
"""
from rest_framework import serializers

from ..models import TrackFeatures, Track, History, User, Playlist


class TrackFeaturesSerializer(serializers.ModelSerializer):
    """
    Serializer for the TrackFeatures model.

    Example input and output:
    {
        "track": "related_track_uri",
        "danceability": 0.8,
        "energy": 0.6,
        "key": 1.0,
        "loudness": -5.5,
        "mode": 1.0,
        "speechiness": 0.1,
        "acousticness": 0.2,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": 0.4,
        "tempo": 120.0
    }
    """
    # TODO: when this serializer is nested i want to pop the track field off 
    # it, it would create
    #       a bunch of duplicate data
    # def __init__(self, *args, **kwargs):
    #     super(TrackFeaturesSerializer, self).__init__(*args, **kwargs)
    #     self.is_nested = 'parent' in self.context
    # def to_representation(self, instance):
    #     rep = super(TrackSerializer, self).to_representation(instance)
    #     features = instance.features

    #     # Use a separate serializer instance for the nested data
    #     features_serializer = TrackFeaturesSerializer(features,
    #       context={'parent': self})

    #     # Replace the 'features' field with the serialized data
    #     rep['features'] = features_serializer.data

    #     # Optionally remove any unwanted keys
    #     if 'some_condition':  # Replace this with your actual condition
    #         rep['features'].pop('track', None)

    #     return rep

    class Meta:
        model = TrackFeatures
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    """
    Serializer for the Track model.

    Example input and output:
    {
        "uri": "track_uri_1",
        "track_name": "Track Name 1",
        "track_artists": "Artist 1"
    }
    """
    class Meta:
        model = Track
        fields = '__all__'


class TrackWithFeaturesSerializer(serializers.ModelSerializer):

    """
    Serializer for combining the Track and TrackFeatures models.

    When you get a Track object and pass it to the serializer, it will use the 
    nested serializer (TrackFeaturesSerializer) to serialize 
    the associted TrackFeatures object 
    (defined by the one to one in the models)

    It will look for the features attribute in the Track object, 
    it comes from the related_name
    in the one to one relationship in the model.

    Example output:
    {
        "uri": "track_uri_1",
        "track_name": "Track Name 1",
        "track_artists": "Artist 1",
        "features": {
            "danceability": 0.8,
            "energy": 0.6,
            "key": 1.0,
            "loudness": -5.5,
            "mode": 1.0,
            "speechiness": 0.1,
            "acousticness": 0.2,
            "instrumentalness": 0.0,
            "liveness": 0.1,
            "valence": 0.4,
            "tempo": 120.0
        }
    }
    """
    features = TrackFeaturesSerializer(source='features', read_only=True)

    class Meta:
        model = Track
        fields = ['uri', 'track_name', 'track_artists', 'features']


class LikedTrackSerializer(serializers.Serializer):
    user = serializers.CharField()
    track = serializers.CharField()


class HistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the History model.

    Example input and output:
    {
        "user": "user_id_1",
        "date_recorded": "2023-10-13T12:34:56Z",
        ...
        "track": "track_uri_1"
    }
    """
    class Meta:
        model = History
        fields = '__all__'


class UserWithTracksSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model that also includes the user's liked tracks.

    Example output:
    {
        "id": "user_id_1",
        "liked_tracks": [
            {
            "uri": "track_uri_1",
            "track_name": "Track Name 1",
            "track_artists": "Artist 1"
            },
            {
            "uri": "track_uri_2",
            "track_name": "Track Name 2",
            "track_artists": "Artist 2"
            },
            ...
        ]
    }
    """
    liked_tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'liked_tracks']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the basic fields of the User model.

    Example input and output:
    {
        "id": "user_id_1"
    }
    """
    class Meta:
        model = User
        fields = ['id']


class PlaylistWithUsersAndTracksSerializer(serializers.ModelSerializer):
    """
    Serializer for outputting detailed information about a Playlist, 
    including the tracks in it and the users who have liked it.

    Example output:
    {
        "playlist_id": "some_unique_id",
        "created_by": "user_id_of_creator",
        "tracks": [
            {
            "uri": "track_uri_1",
            "track_name": "Track Name 1",
            "track_artists": "Artist 1"
            },
            {
            "uri": "track_uri_2",
            "track_name": "Track Name 2",
            "track_artists": "Artist 2"
            },
            ...
        ],
        "liked_by": [
            {
            "id": "user_id_1",
            "history": ["track_uri_a", "track_uri_b", ...],
            "liked_tracks": ["track_uri_1", "track_uri_2", ...]
            },
            {
            "id": "user_id_2",
            "history": ["track_uri_c", "track_uri_d", ...],
            "liked_tracks": ["track_uri_3", "track_uri_4", ...]
            },
            ...
        ]
    }
    """
    tracks = TrackSerializer(many=True, read_only=True)
    liked_by = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'
# for when you only want to output the data for the tracks in the playlist


class PlaylistWithTracksSerializer(serializers.ModelSerializer):
    """
    Serializer for outputting information about a 
    Playlist including the tracks in it.

    Example output:
    {
        "playlist_id": "some_unique_id",
        "created_by": "user_id_of_creator",
        "tracks": [
            {
            "uri": "track_uri_1",
            "track_name": "Track Name 1",
            "track_artists": "Artist 1"
            },
            {
            "uri": "track_uri_2",
            "track_name": "Track Name 2",
            "track_artists": "Artist 2"
            },
            ...
        ]
    }
    """
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'

# you might get or recieve data in that form using this serializer


class PlaylistSerializer(serializers.ModelSerializer):
    """
    Serializer for handling input and basic output for the Playlist model.

    Example input and output:
    {
        "playlist_id": "some_unique_id",
        "created_by": "user_id_of_creator",
        "tracks": ["track_uri_1", "track_uri_2", ...]
    }
    """
    # pylint: disable=no-member
    tracks = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Track.objects.all())

    class Meta:
        model = Playlist
        fields = '__all__'
