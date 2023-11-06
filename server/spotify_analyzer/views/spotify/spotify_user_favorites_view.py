import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import logging
import json
from ...services.core.user_service import UserService
from ...services.core.track_service import TrackService
from ...services.core.album_service import AlbumService
from ...services.core.artist_service import ArtistService
from ...services.core.playlist_service import PlaylistService
from ...services.core.track_features_service import TrackFeaturesService
from ...services.spotify.spotify_token_handler import SpotifyTokenHandler
from ...models import User, Track, Album, Artist, Playlist, TrackFeatures
from ...services.spotify.retrieval.spotify_track_service\
    import SpotifyTrackService
from ...services.spotify.spotify_data_persistence_service\
    import SpotifyDataPersistence
from ...services.spotify.data_extractor import SpotifyDataExtractor as extractor

app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


@method_decorator(csrf_exempt, name='dispatch')
class SpotifyFavorites(APIView):
    def post(self, request, id):
        user_id = id
        type = request.data.get('type')
        try:
            # print(authorization_code)
         
            user_service = UserService(user_model=User, logger=logger)
            token_handler = SpotifyTokenHandler(
                user_service=user_service, user_id=user_id)
            print(token_handler)
            sp_track_service = SpotifyTrackService(client=token_handler.client,
                                                   token_handler=token_handler)
            track_service = TrackService(track_model=Track, logger=logger)
            album_service = AlbumService(album_model=Album, logger=logger,
                                         track_service=track_service)
            artist_service = ArtistService(artist_model=Artist, logger=logger)
            playlist_service = PlaylistService(playlist_model=Playlist, logger=logger,
                                                track_service=track_service,
                                               user_service=user_service)
            feature_service = TrackFeaturesService(track_features_model=TrackFeatures,
                                                   track_service=track_service,logger=logger)

            persistence_service = SpotifyDataPersistence(
                track_service=track_service, user_service=user_service,
                album_service=album_service, artist_service=artist_service,
                playlist_service=playlist_service, feature_service=feature_service
            )
            print(persistence_service)
            if type == 'tracks':
                top_tracks = sp_track_service.get_monthly_tracks()
                records = top_tracks.to_dict(orient='records')
                
                
                # second dict gives me the context i need
                dtos, album_tracks = extractor.parseTopTracksResponse(records)
                # all of these will be track dtos
                tracks = dtos['tracks']
                artists = dtos['artists']
                albums = dtos['albums']
                tracks_features = dtos['tracks_features']
                # handle the user here, it gets handled in the token handler
                # for now but also catching it here is worthwhile
                # dont need additional context for this, 
                # but for a given track i need the corresponding album_uri
                persistence_service.artist.add_artists_to_library(artists)
                persistence_service.track.add_tracks_to_library(tracks)
                persistence_service.album.add_albums_to_library(albums)
                persistence_service.track.\
                    add_features_to_tracks(tracks_features)
                persistence_service.album.add_tracks_to_albums(album_tracks)
                return Response(records)
                
            elif type == 'artists':
                top_artists = sp_track_service.get_monthly_artists()
                extractor.parseTopArtistsResponse(top_artists)
                
                return Response(top_artists)
            else:
                return Response({'error': 'Bad input'},
                                status=status.HTTP_400_BAD_REQUEST)

        except APIException as e:
            print(traceback.format_exc())
            # logger.exception(f"An unexpected error occurred: {str(e)}")
            return Response({'error': e.detail},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)