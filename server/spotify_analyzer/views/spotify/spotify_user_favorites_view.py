import traceback
import logging
from typing import TypedDict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ...services.core.user_service import UserService
from ...services.core.track_service import TrackService
from ...services.core.album_service import AlbumService
from ...services.core.artist_service import ArtistService
from ...services.core.playlist_service import PlaylistService
from ...services.core.image_service import ImageService
from ...services.core.genre_service import GenreService


from ...services.core.track_features_service import TrackFeaturesService
from ...services.spotify.spotify_token_handler import SpotifyTokenHandler
from ...models import User, Track, Album, Artist, Playlist, TrackFeatures, \
    Image, Genre
from ...services.spotify.retrieval.spotify_track_service\
    import SpotifyTrackService
from ...services.spotify.spotify_data_persistence_service\
    import SpotifyDataPersistence
from ...services.spotify.data_extractor import \
    SpotifyDataExtractor as extractor

app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


@method_decorator(csrf_exempt, name='dispatch')
class SpotifyFavorites(APIView):
    def post(self, request, id):
        user_id = id
        type = request.data.get('type')
        try:
            # print(authorization_code)
            services = self.init_services(user_id)
            if type == 'tracks':
                # top_tracks = sp_track_service.get_monthly_tracks()
                # records = top_tracks.to_dict(orient='records')
                sp_track_service = services['sp_track_service']
                persistence_service = services['persistence_service']
                parsedInfo = sp_track_service.get_monthly_tracks()
                # tracks = parsedInfo['tracks'].values()
                # artists = parsedInfo['artists'].values()
                # albums = parsedInfo['albums'].values()
                # images = parsedInfo['images']
                genres = list(parsedInfo['genres'].values())
                
                # handle the user here, it gets handled in the token handler
                # for now but also catching it here is worthwhile
                # dont need additional context for this,
                # but for a given track i need the corresponding album_uri
                persistence_service.genre.add_genres_to_library(genres)
                # lets test these one at a time, hopefully we can get genres
                # to work before i go to sleep
                # persistence_service.image.add_images_to_library(images)
                # persistence_service.artist.add_artists_to_library(artists)
                # persistence_service.track.add_tracks_to_library(tracks)
                # persistence_service.album.add_albums_to_library(albums)
                # the next line gets handled when i fix the df part
                # persistence_service.track.\
                #     add_features_to_tracks(tracks_features)
                # persistence_service.album.add_tracks_to_albums(album_tracks)
                return Response(parsedInfo)

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

    def init_services(self, user_id):
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
        playlist_service = PlaylistService(playlist_model=Playlist,
                                           logger=logger,
                                           track_service=track_service,
                                           user_service=user_service)
        feature_service = TrackFeaturesService(
            track_features_model=TrackFeatures,
            track_service=track_service, logger=logger)
        images_service = ImageService(image_model=Image, logger=logger,
                                      album_service=album_service,
                                      artist_service=artist_service)
        genre_service = GenreService(genre_model=Genre, logger=logger)

        persistence_service = SpotifyDataPersistence(
            track_service=track_service, user_service=user_service,
            album_service=album_service, artist_service=artist_service,
            playlist_service=playlist_service,
            feature_service=feature_service,
            image_service=images_service, genre_service=genre_service
        )
        return Services(
            user_service=user_service, token_handler=token_handler,
            sp_track_service=sp_track_service,
            track_service=track_service, album_service=album_service,
            artist_service=artist_service,
            playlist_service=playlist_service,
            feature_service=feature_service, images_service=images_service,
            genre_service=genre_service,
            persistence_service=persistence_service
        )


class Services(TypedDict):
    user_service: UserService
    token_handler: SpotifyTokenHandler
    sp_track_service: SpotifyTrackService
    track_service: TrackService
    album_service: AlbumService
    artist_service: ArtistService
    playlist_service: PlaylistService
    feature_service: TrackFeaturesService
    images_service: ImageService
    genre_service: GenreService

    persistence_service: SpotifyDataPersistence
