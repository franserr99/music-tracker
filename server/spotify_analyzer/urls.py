from django.urls import include, path

from .models import Track,TrackFeatures,User
from .services.track_service import TrackService
from .services.track_features_service import TrackFeaturesService
from .services.user_service import UserService
from .services.liked_track_service import LikedTrackService
from .views.spotify_view import SpotifyAuthCodeView
from .views.track_views import create_track_view
from .views.user_views import create_user_view
from .views.track_features_views import create_track_features_view

import logging


app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)

track_model=Track()
track_features_model=TrackFeatures()
user_model=User()

track_service=TrackService(track_model=track_model,logger=logger)
feature_service=TrackFeaturesService(track_features_model,track_service,logger)
user_service=UserService(user_model=user_model,logger=logger)
liked_track_service=LikedTrackService(track_service,user_service,logger)



urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('spotify/auth-code/', SpotifyAuthCodeView.as_view(), name='spotify-auth-code'),
    path('track/',create_track_view(track_service=track_service,feature_service=feature_service), name="track"),
    path('user/',create_user_view(user_service,liked_track_service),name='user'),
    path('track/feature/',create_track_features_view(feature_service),name='track-features')
]