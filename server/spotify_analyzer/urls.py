from django.urls import include, path

# from .models import Track, TrackFeatures, User
# from .services.track_service import TrackService
# from .services.track_features_service import TrackFeaturesService
# from .services.user_service import UserService
# from .services.liked_track_service import LikedTrackService
from .views.spotify_view import SpotifyAuthCodeView
from .views.user_views import UserListCreate, UserRetrieveUpdateDestroy
from .views.track_views import TrackListCreate, TrackRetrieveUpdateDestroy
from .views.track_features_views import TrackFeatureListCreate
from .views.track_features_views import TrackFeatureRetrieveUpdateDestroy

import logging

app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)

urlpatterns = [
     path('api-auth/', include('rest_framework.urls')),
     path('users/', UserListCreate.as_view(), name='user-list-create'),
     path('users/<str:id>/', UserRetrieveUpdateDestroy.as_view(),
          name='user-retrieve-update-destroy'),
     path('tracks/', TrackListCreate.as_view(), name='track-list-create'),
     path('tracks/features/', TrackFeatureListCreate.as_view(),
          name='track-features-list-create'),
     path('tracks/features/<str:track>/',
          TrackFeatureRetrieveUpdateDestroy.as_view(),
          name='track-features-retrieve-update-destroy'),
     path('tracks/<str:uri>/', TrackRetrieveUpdateDestroy.as_view(),
          name='track-retrieve-update-destroy'),
     path('spotify/auth-code/', SpotifyAuthCodeView.as_view(),
          name='spotify-auth-code'),
]
