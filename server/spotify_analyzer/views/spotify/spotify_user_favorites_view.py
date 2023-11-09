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
from ...services.spotify.token_handler import SpotifyTokenHandler
from ...models import User, Track, Album, Artist, Playlist, TrackFeatures, \
    Image, Genre
from ...services.spotify.retrieval.spotify_favorite_service\
    import SpotifyTrackService
from ...services.spotify.persistence_service\
    import SpotifyDataPersistence
app_name = 'spotify_analyzer'
logger = logging.getLogger(app_name)


@method_decorator(csrf_exempt, name='dispatch')
class SpotifyFavorites(APIView):
    def post(self, request, id):
        user_id = id
        type = request.data.get('type')
        try:
            services = self.init_services(user_id)
            sp_track_service = services['sp_track_service']
            persistence = services['persistence_service']
            if type == 'tracks':
                parsedInfo = sp_track_service.get_monthly_tracks()
                # break this code up into a function at some point
                tracks = list(parsedInfo['tracks'].values())
                artists = list(parsedInfo['artists'].values())
                albums = list(parsedInfo['albums'].values())
                images = list(parsedInfo['images'].values())
                genres = list(parsedInfo['genres'].values())
                # handle adding base records without fk relationships
                persistence.genre.add_genres_to_library(genres)
                persistence.track.add_tracks_to_library(tracks)
                persistence.image.add_images_to_library(images)
                persistence.artist.add_artists_to_library(artists)
                persistence.album.add_albums_to_library(albums)
                # handle foreign key relationships
                persistence.image.link_images_to_albums(albums)
                persistence.image.link_images_to_artists(artists)
                persistence.album.add_tracks_to_albums(tracks)
                persistence.artist.add_genres_to_artists(artists)
                persistence.album.add_artists_to_albums(albums)
                persistence.track.add_artists_to_tracks(tracks)
                # connect this to my old method, it will do the heavy
                # lifting for getting the audio features
                return Response(parsedInfo)

            elif type == 'artists':
                parsedInfo = sp_track_service.get_monthly_artists()
                images = list(parsedInfo['images'].values())
                genres = list(parsedInfo['genres'].values())
                artists = list(parsedInfo['artists'].values())
                # handle adding base records without fk relationships
                persistence.genre.add_genres_to_library(genres)
                persistence.image.add_images_to_library(images)
                persistence.artist.add_artists_to_library(artists)
                # handle foreign key relationships
                persistence.image.link_images_to_artists(artists)
                persistence.artist.add_genres_to_artists(artists)

                return Response(parsedInfo)
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

        genre_service = GenreService(genre_model=Genre, logger=logger)
        artist_service = ArtistService(
            artist_model=Artist, logger=logger, genre_service=genre_service)
        track_service = TrackService(
            track_model=Track, logger=logger, artist_service=artist_service)
        album_service = AlbumService(album_model=Album, logger=logger,
                                     track_service=track_service,
                                     artist_service=artist_service)

        playlist_service = PlaylistService(playlist_model=Playlist,
                                           logger=logger,
                                           track_service=track_service,
                                           user_service=user_service)
        feature_service = TrackFeaturesService(
            features_model=TrackFeatures,
            track_service=track_service, logger=logger)
        images_service = ImageService(image_model=Image, logger=logger,
                                      album_service=album_service,
                                      artist_service=artist_service)

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
